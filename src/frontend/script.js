const API_BASE_URL = 'https://p82qoazful.execute-api.us-east-1.amazonaws.com/dev';

function showError(message) {
    const errorElement = document.getElementById('errorMessage');
    errorElement.textContent = message;
    errorElement.style.display = 'block';

    setTimeout(() => {
        errorElement.style.display = 'none';
        errorElement.textContent = '';
    }, 5000);
}

function hideError() {
    const errorElement = document.getElementById('errorMessage');
    errorElement.style.display = 'none';
    errorElement.textContent = '';
}

function showLoading() {
    document.getElementById('loadingIndicator').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingIndicator').style.display = 'none';
}

async function createShortLink(event) {
    event.preventDefault();
    hideError();
    showLoading();

    const urlInput = document.getElementById('originalUrl');
    const originalUrl = urlInput.value.trim();

    if (!originalUrl) {
        hideLoading();
        showError('Please enter a URL');
        return;
    }

    if (!API_BASE_URL) {
        hideLoading();
        showError('API configuration missing');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: originalUrl })
        });

        const data = await response.json();

        if (response.ok) {
            displayShortLink(data);
        } else {
            showError(data.error || 'Failed to create short link');
        }

    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please try again.');
    } finally {
        hideLoading();
    }
}

function displayShortLink(data) {
    const resultSection = document.getElementById('resultSection');
    const shortUrlDisplay = document.getElementById('shortUrlDisplay');
    const linkInfo = document.getElementById('linkInfo');

    shortUrlDisplay.value = data.short_url;

    linkInfo.innerHTML = `
        <p><strong>Original URL:</strong> ${data.original_url}</p>
        <p><strong>Short Code:</strong> ${data.short_code}</p>
        <p><strong>Expires:</strong> ${new Date(data.expires_at).toLocaleDateString()}</p>
    `;

    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

async function copyToClipboard() {
    const shortUrlInput = document.getElementById('shortUrlDisplay');
    const shortUrl = shortUrlInput.value;
    const copyButton = document.querySelector('.btn-copy'); // updated selector

    if (!shortUrl) return;

    try {
        await navigator.clipboard.writeText(shortUrl);

        const originalText = copyButton.textContent;
        copyButton.textContent = 'Copied!';
        setTimeout(() => copyButton.textContent = originalText, 2000);

    } catch (error) {
        // Fallback
        shortUrlInput.select();
        document.execCommand('copy');

        const originalText = copyButton.textContent;
        copyButton.textContent = 'Copied!';
        setTimeout(() => copyButton.textContent = originalText, 2000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('App initialized');
});
