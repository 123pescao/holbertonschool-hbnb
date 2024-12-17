/* scripts.js */

/* Wait for DOM to fully load */
document.addEventListener('DOMContentLoaded', () => {
    setupLoginForm();
    loadPlaces();
    setupReviewForm();
});

/* Helper function to get a cookie value */
function getCookieValue(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}

/* ------------------- LOGIN FUNCTIONALITY ------------------- */
function setupLoginForm() {
    const loginForm = document.getElementById('signin-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('user-email').value;
        const password = document.getElementById('user-password').value;

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                document.cookie = `token=${data.access_token}; path=/;`;
                window.location.href = 'index.html';
            } else {
                showError('Invalid email or password.');
            }
        } catch (error) {
            console.error('Error logging in:', error);
            showError('Something went wrong. Please try again.');
        }
    });
}

/* Display error messages */
function showError(message) {
    const errorMsg = document.getElementById('error-msg');
    if (errorMsg) {
        errorMsg.textContent = message;
        errorMsg.style.display = 'block';
    }
}

/* ------------------- LOAD PLACES FUNCTIONALITY ------------------- */
async function loadPlaces() {
    const placesContainer = document.getElementById('listing-places');
    const priceFilter = document.getElementById('cost-filter');
    const authLink = document.getElementById('auth-link');

    if (!placesContainer || !priceFilter || !authLink) return;

    const token = getCookieValue('token');

    // Update the Login/Logout link
    if (!token) {
        authLink.textContent = 'Login';
        authLink.href = 'login.html';
    } else {
        authLink.textContent = 'Logout';
        authLink.href = '#';
        authLink.addEventListener('click', () => {
            document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            window.location.href = 'login.html';
        });
    }

    // Fetch and display places
    let places = await fetchPlaces(token);
    renderPlaces(places);

    // Apply price filter
    priceFilter.addEventListener('change', () => {
        const maxPrice = priceFilter.value;
        const filtered = filterPlacesByPrice(places, maxPrice);
        renderPlaces(filtered);
    });
}

/* Fetch places from API */
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
            headers: token ? { Authorization: `Bearer ${token}` } : {}
        });
        if (!response.ok) throw new Error('Failed to fetch places');
        return await response.json();
    } catch (error) {
        console.error('Error fetching places:', error);
        return [];
    }
}

/* Render places dynamically */
function renderPlaces(places) {
    const container = document.getElementById('listing-places');
    container.innerHTML = '';

    if (places.length === 0) {
        container.innerHTML = '<p>No places found.</p>';
        return;
    }

    places.forEach((place) => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
            <img src="${place.image_url || 'assets/default-image.png'}" alt="${place.title}">
            <div class="place-info">
                <h2>${place.title}</h2>
                <p>${place.description || 'No description available.'}</p>
                <p class="place-price">$${place.price || 'N/A'}</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            </div>
        `;
        container.appendChild(card);
    });
}

/* Filter places by max price */
function filterPlacesByPrice(places, maxPrice) {
    if (maxPrice === 'all') return places;
    return places.filter((place) => place.price <= Number(maxPrice));
}

/* ------------------- ADD REVIEW FUNCTIONALITY ------------------- */
function setupReviewForm() {
    const reviewForm = document.getElementById('feedback-form');
    const placeNameElement = document.getElementById('place-name');
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get('id');
    const token = getCookieValue('token');

    if (!reviewForm || !token || !placeId) {
        window.location.href = 'index.html';
        return;
    }

    if (placeNameElement) placeNameElement.textContent = `Place #${placeId}`;

    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const feedback = document.getElementById('feedback-text').value;
        const rating = document.getElementById('star-rating').value;

        try {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({ text: feedback, rating })
            });

            if (response.ok) {
                alert('Review submitted successfully!');
                reviewForm.reset();
                window.location.reload(); // Reload to show the new review
            } else {
                alert('Failed to submit review. Please try again.');
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('An error occurred while submitting your review.');
        }
    });
}
