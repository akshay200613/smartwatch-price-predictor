/* ─── Particle Canvas Init ─────────────────────────────────── */
(function initParticles() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let particles = [];
    const NUM = 55;

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    for (let i = 0; i < NUM; i++) {
        particles.push({
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            r: Math.random() * 1.5 + 0.3,
            dx: (Math.random() - 0.5) * 0.4,
            dy: (Math.random() - 0.5) * 0.4,
            alpha: Math.random() * 0.5 + 0.1,
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(147,197,253,${p.alpha})`;
            ctx.fill();
            p.x += p.dx;
            p.y += p.dy;
            if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
        });
        requestAnimationFrame(draw);
    }
    draw();
})();

/* ─── State ──────────────────────────────────────────────────── */
let selectedBrand = 'noise';

/* ─── Brand Card Selection ───────────────────────────────────── */
function selectBrand(el) {
    document.querySelectorAll('.brand-card').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    selectedBrand = el.dataset.brand;
    document.getElementById('sw-brand').value = selectedBrand;
    updateLivePreview();
}

/* ─── Slider Sync ────────────────────────────────────────────── */
function syncSlider(type) {
    const slider = document.getElementById('price-slider');
    const input = document.getElementById('sw-original');
    if (type === 'price') {
        input.value = slider.value;
        updateSliderTrack(slider, 100, 200000);
    }
    updateLivePreview();
}

function updateRating(val) {
    const slider = document.getElementById('sw-rating');
    document.getElementById('rating-display').textContent = `${parseFloat(val).toFixed(1)} ⭐`;
    updateSliderTrack(slider, 1, 5);
}

function updateSliderTrack(slider, min, max) {
    const pct = ((slider.value - min) / (max - min)) * 100;
    slider.style.setProperty('--pct', pct + '%');
}

/* ─── Sync price input → slider ─────────────────────────────── */
document.getElementById('sw-original').addEventListener('input', function () {
    const slider = document.getElementById('price-slider');
    slider.value = Math.min(Math.max(this.value, 100), 200000);
    updateSliderTrack(slider, 100, 200000);
    updateLivePreview();
});

/* ─── Init slider tracks on load ────────────────────────────── */
window.addEventListener('DOMContentLoaded', () => {
    updateSliderTrack(document.getElementById('price-slider'), 100, 200000);
    updateSliderTrack(document.getElementById('sw-rating'), 1, 5);
    updateRating(4.2);
});

/* ─── Live hero preview ──────────────────────────────────────── */
function updateLivePreview() {
    const orig = parseFloat(document.getElementById('sw-original').value) || 0;
    if (orig > 0) {
        const rough = Math.round(orig * 0.68);
        document.getElementById('hero-price').textContent = `~₹${rough.toLocaleString('en-IN')}`;
    }
}

/* ─── Main Predict Function ──────────────────────────────────── */
async function predictSmartwatch() {
    const brand = selectedBrand;
    const originalPrice = parseFloat(document.getElementById('sw-original').value);
    const rating = parseFloat(document.getElementById('sw-rating').value);
    const numRatings = parseInt(document.getElementById('sw-numratings').value) || 500;

    const resultEl = document.getElementById('sw-result');
    const subtitleEl = document.getElementById('sw-subtitle');
    const btn = document.getElementById('predict-btn');

    if (isNaN(originalPrice) || originalPrice <= 0) {
        subtitleEl.textContent = '⚠️ Please enter a valid original price.';
        return;
    }

    // Loading state
    btn.disabled = true;
    btn.querySelector('.btn-text').textContent = 'Predicting...';
    resultEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
    resultEl.style.cssText = 'color: #9095b8; -webkit-text-fill-color: #9095b8;';
    resultEl.classList.remove('animating');
    subtitleEl.textContent = 'Analyzing market data...';
    document.getElementById('hero-price').textContent = '...';

    await new Promise(r => setTimeout(r, 700));

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ brand, original_price: originalPrice, rating, num_ratings: numRatings })
        });

        if (response.ok) {
            const data = await response.json();
            displayPrice(data.predicted_price, true);
            resetBtn(btn);
            return;
        }
    } catch (e) {
        console.warn('Backend not available. Using client-side model.');
    }

    // Fallback client-side estimation
    let predicted = originalPrice * 0.6;
    if (brand === 'apple') predicted = originalPrice * 0.95;
    else if (brand === 'samsung' || brand === 'garmin') predicted = originalPrice * 0.82;
    else if (brand === 'fire-boltt' || brand === 'noise') predicted = originalPrice * 0.46;
    else if (brand === 'boat') predicted = originalPrice * 0.52;

    if (rating >= 4.5) predicted *= 1.1;
    else if (rating < 3.5) predicted *= 0.82;

    displayPrice(Math.round(predicted), false);
    resetBtn(btn);
}

function displayPrice(price, fromModel) {
    const resultEl = document.getElementById('sw-result');
    const subtitleEl = document.getElementById('sw-subtitle');
    const heroPrice = document.getElementById('hero-price');
    const formatted = `₹ ${price.toLocaleString('en-IN')}`;

    resultEl.textContent = formatted;
    resultEl.style.cssText = '';
    resultEl.classList.add('animating');
    heroPrice.textContent = formatted;

    subtitleEl.textContent = fromModel
        ? 'Estimated market value · ML model prediction'
        : 'Estimated market value · Client-side model';
}

function resetBtn(btn) {
    btn.disabled = false;
    btn.querySelector('.btn-text').textContent = 'Predict Market Value';
}
