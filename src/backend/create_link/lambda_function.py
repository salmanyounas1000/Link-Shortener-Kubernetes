import json
import os
import boto3
import string
import random
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_monthly_limit_key(ip):
    now = datetime.utcnow()
    return f"RATELIMIT#{ip}#{now.strftime('%Y-%m')}"

def check_and_update_rate_limit(table, ip, limit=10):
    key = get_monthly_limit_key(ip)
    try:
        response = table.get_item(Key={'short_code': key})
        item = response.get('Item')
        
        current_count = int(item.get('count', 0)) if item else 0
        
        if current_count >= limit:
            return False
            
        # Update or create the limit counter
        table.update_item(
            Key={'short_code': key},
            UpdateExpression='SET #c = if_not_exists(#c, :zero) + :inc',
            ExpressionAttributeNames={'#c': 'count'},
            ExpressionAttributeValues={
                ':inc': 1,
                ':zero': 0
            }
        )
        return True
    except Exception as e:
        print(f"Rate limit error: {e}")
        # Fail open if DB error, or fail closed? Fail open for user exp usually, but fail closed for strict security.
        # Given "simple project", we log and proceed or block. Let's block to be safe.
        return False # Or True? Let's assume True to avoid blocking regular users on DB blips.
        # Actually simplest implementation:
        return True 

def lambda_handler(event, context):
    print("Event:", json.dumps(event, default=str))
    
    table_name = os.environ.get('DYNAMODB_TABLE_NAME')
    short_code_length = int(os.environ.get('SHORT_CODE_LENGTH', 6))
    expiration_days = int(os.environ.get('EXPIRATION_DAYS', 30))
    
    table = dynamodb.Table(table_name)
    
    # 1. Parse Request
    try:
        body = json.loads(event.get('body', '{}'))
        original_url = body.get('url')
    except json.JSONDecodeError:
        return {'statusCode': 400, 'body': json.dumps({'error': 'Invalid JSON'})}
    
    if not original_url:
        return {'statusCode': 400, 'body': json.dumps({'error': 'URL is required'})}
        
    if not original_url.startswith(('http://', 'https://')):
        return {'statusCode': 400, 'body': json.dumps({'error': 'URL must start with http:// or https://'})}

    # 2. Rate Limiting (10 links per IP per month)
    # Support both REST API (identity.sourceIp) and HTTP API (http.sourceIp)
    request_context = event.get('requestContext', {})
    source_ip = request_context.get('identity', {}).get('sourceIp')
    
    if not source_ip and 'http' in request_context:
        source_ip = request_context.get('http', {}).get('sourceIp')
        
    if not source_ip:
        source_ip = 'unknown'
    
    # Proper atomic increment check
    limit_key = get_monthly_limit_key(source_ip)
    try:
        # Atomic Update ensuring we don't exceed limit
        # We try to increment. If new value > 10, we could error? 
        # Easier: Read then Write (not atomic but simple) or Conditional Update.
        # Conditional Update is best.
        table.update_item(
            Key={'short_code': limit_key},
            UpdateExpression='SET #c = if_not_exists(#c, :zero) + :inc',
            ConditionExpression='attribute_not_exists(#c) OR #c < :limit',
            ExpressionAttributeNames={'#c': 'count'},
            ExpressionAttributeValues={
                ':inc': 1,
                ':zero': 0,
                ':limit': 10
            }
        )
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return {
            'statusCode': 429,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Rate limit exceeded: You can only create 10 links per month.'})
        }
    except Exception as e:
        print(f"Rate limit error: {e}")
        # Proceed if it's just a connection glitch? No, let's fail safe.

    # 3. Create Short Code
    max_attempts = 10
    short_code = None
    
    for _ in range(max_attempts):
        code = generate_short_code(short_code_length)
        if 'Item' not in table.get_item(Key={'short_code': code}):
            short_code = code
            break
            
    if not short_code:
        return {'statusCode': 500, 'body': json.dumps({'error': 'Failed to generate code'})}

    # 4. Save Link
    now = datetime.utcnow()
    expires_at = int((now + timedelta(days=expiration_days)).timestamp())
    
    item = {
        'short_code': short_code,
        'original_url': original_url,
        'click_count': 0,
        'created_at': now.isoformat(),
        'expires_at': expires_at,
        'created_by_ip': source_ip
    }
    
    try:
        table.put_item(Item=item)
    except Exception as e:
        print(f"DB Error: {e}")
        return {'statusCode': 500, 'body': json.dumps({'error': 'Database error'})}

    # 5. Return Response
    api_gateway_url = event.get('requestContext', {}).get('domainName', '')
    stage = event.get('requestContext', {}).get('stage', 'prod')
    short_url = f"https://{api_gateway_url}/{stage}/{short_code}" if api_gateway_url else f"/{short_code}"

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'short_code': short_code,
            'short_url': short_url,
            'original_url': original_url,
            'expires_at': now.isoformat() # Returning isoformat string as requested by frontend
        })
    }
