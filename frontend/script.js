const API_BASE_URL = 'http://localhost:8001'; // Make sure this matches backend port

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('shorten-form');
    const urlInput = document.getElementById('url-input');
    const generateBtn = document.getElementById('generate-btn');
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.getElementById('btn-loader');
    const errorMessage = document.getElementById('error-message');
    const resultSection = document.getElementById('result-section');
    const shortUrlEl = document.getElementById('short-url');
    const copyBtn = document.getElementById('copy-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const originalUrl = urlInput.value.trim();
        if (!originalUrl) return;

        // Reset UI
        errorMessage.classList.add('hidden');
        resultSection.classList.add('hidden');
        
        // Show loading state
        generateBtn.disabled = true;
        btnText.classList.add('hidden');
        btnLoader.style.display = 'block';

        try {
            const response = await fetch(`${API_BASE_URL}/api/shorten`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: originalUrl })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate short URL');
            }

            const data = await response.json();
            
            // Show result
            shortUrlEl.href = data.short_url;
            shortUrlEl.textContent = data.short_url;
            resultSection.classList.remove('hidden');
            
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove('hidden');
        } finally {
            // Revert loading state
            generateBtn.disabled = false;
            btnText.classList.remove('hidden');
            btnLoader.style.display = 'none';
        }
    });

    copyBtn.addEventListener('click', () => {
        const urlToCopy = shortUrlEl.textContent;
        navigator.clipboard.writeText(urlToCopy).then(() => {
            // Brief visual feedback
            const originalIcon = copyBtn.innerHTML;
            copyBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
            setTimeout(() => {
                copyBtn.innerHTML = originalIcon;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy: ', err);
        });
    });
});
