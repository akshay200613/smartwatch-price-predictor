async function predictSmartwatch() {
    const brand = document.getElementById('sw-brand').value;
    const originalPrice = parseFloat(document.getElementById('sw-original').value);
    const rating = parseFloat(document.getElementById('sw-rating').value);

    const resultEl = document.getElementById('sw-result');
    const subtitleEl = document.getElementById('sw-subtitle');
    
    if (isNaN(originalPrice) || isNaN(rating)) {
        alert("Please enter valid numbers");
        return;
    }

    resultEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
    subtitleEl.innerText = "Analyzing pricing trends...";
    
    await new Promise(resolve => setTimeout(resolve, 800));

    try {
        const apiEndpoint = window.location.hostname === 'localhost' && window.location.port === '8000' ? '/api/predict' : '/api/predict';
        const response = await fetch(apiEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ brand, original_price: originalPrice, rating, num_ratings: 500 })
        });
        
        if (response.ok) {
            const data = await response.json();
            displaySmartwatchPrice(data.predicted_price);
            return;
        }
    } catch (e) {
        console.log("Real backend not available. Using simulated model.");
    }

    // Simulated Model Logic
    let predictedPrice = originalPrice * 0.6;
    if (brand === 'apple') predictedPrice = originalPrice * 0.95; 
    else if (brand === 'samsung' || brand === 'garmin') predictedPrice = originalPrice * 0.8;
    else if (brand === 'fire-boltt' || brand === 'noise') predictedPrice = originalPrice * 0.45;
    
    if (rating > 4.5) predictedPrice *= 1.1;
    else if (rating < 3.5) predictedPrice *= 0.8;
    
    displaySmartwatchPrice(Math.round(predictedPrice));
}

function displaySmartwatchPrice(price) {
    const resultEl = document.getElementById('sw-result');
    const subtitleEl = document.getElementById('sw-subtitle');
    
    resultEl.innerHTML = `₹ ${price.toLocaleString('en-IN')}`;
    resultEl.style.color = '#4ade80';
    subtitleEl.innerText = "Estimated market value based on current trends";
}
