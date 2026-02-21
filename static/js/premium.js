// Premium subscription management

// Initialize Stripe
const stripe = Stripe(STRIPE_PUBLISHABLE_KEY);

// Premium status
let isPremium = IS_PREMIUM || false;

// DOM Elements
const btnPremium = document.getElementById('btnPremium');
const premiumModal = document.getElementById('premiumModal');
const successModal = document.getElementById('successModal');
const modalClose = document.getElementById('modalClose');
const selectPlanButtons = document.querySelectorAll('.btn-select-plan');
const btnCloseSuccess = document.getElementById('btnCloseSuccess');
const btnCopyToken = document.getElementById('btnCopyToken');
const premiumTokenDisplay = document.getElementById('premiumTokenDisplay');

// Ad elements
const adTop = document.getElementById('adTop');
const adBottom = document.getElementById('adBottom');

// Check premium status on load
function checkPremiumStatus() {
    const token = localStorage.getItem('premium_token');

    if (token) {
        // Verify token with backend
        fetch('/check-premium', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ token })
        })
            .then(res => res.json())
            .then(data => {
                if (data.is_premium) {
                    isPremium = true;
                    hideAds();
                } else {
                    showAds();
                    showPremiumButton();
                }
            })
            .catch(() => {
                showAds();
                showPremiumButton();
            });
    } else {
        showAds();
        showPremiumButton();
    }
}

function showAds() {
    if (adTop) adTop.style.display = 'block';
    if (adBottom) adBottom.style.display = 'block';
}

function hideAds() {
    if (adTop) adTop.style.display = 'none';
    if (adBottom) adBottom.style.display = 'none';
}

function showPremiumButton() {
    if (btnPremium) btnPremium.style.display = 'flex';
}

// Open premium modal
function openPremiumModal() {
    if (premiumModal) {
        premiumModal.style.display = 'flex';
    }
}

// Close premium modal
function closePremiumModal() {
    if (premiumModal) {
        premiumModal.style.display = 'none';
    }
}

// Handle plan selection
async function selectPlan(plan) {
    try {
        // Get the appropriate price ID based on plan
        const response = await fetch('/create-checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ plan })
        });

        const data = await response.json();

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        // Redirect to Stripe Checkout
        const result = await stripe.redirectToCheckout({
            sessionId: data.session_id
        });

        if (result.error) {
            alert(result.error.message);
        }
    } catch (error) {
        console.error('Payment error:', error);
        alert('An error occurred. Please try again.');
    }
}

// Handle successful payment (from URL parameter)
function checkPaymentSuccess() {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id');

    if (sessionId) {
        // Get premium token from backend
        fetch('/payment-success?session_id=' + sessionId)
            .then(res => res.json())
            .then(data => {
                if (data.token) {
                    // Store token
                    localStorage.setItem('premium_token', data.token);

                    // Show success modal
                    if (premiumTokenDisplay) {
                        premiumTokenDisplay.value = data.token;
                    }

                    if (successModal) {
                        successModal.style.display = 'flex';
                    }

                    // Hide ads
                    isPremium = true;
                    hideAds();

                    // Hide premium button
                    if (btnPremium) {
                        btnPremium.style.display = 'none';
                    }

                    // Clear URL parameters
                    window.history.replaceState({}, document.title, window.location.pathname);
                }
            })
            .catch(error => {
                console.error('Error fetching payment data:', error);
            });
    }
}

// Copy token to clipboard
function copyToken() {
    if (premiumTokenDisplay) {
        premiumTokenDisplay.select();
        document.execCommand('copy');

        // Change button text temporarily
        if (btnCopyToken) {
            const originalText = btnCopyToken.textContent;
            btnCopyToken.textContent = 'Copied!';
            setTimeout(() => {
                btnCopyToken.textContent = originalText;
            }, 2000);
        }
    }
}

// Initialize event listeners
function initPremium() {
    // Premium button click
    if (btnPremium) {
        btnPremium.addEventListener('click', openPremiumModal);
    }

    // Modal close button
    if (modalClose) {
        modalClose.addEventListener('click', closePremiumModal);
    }

    // Close modal when clicking outside
    if (premiumModal) {
        premiumModal.addEventListener('click', (e) => {
            if (e.target === premiumModal) {
                closePremiumModal();
            }
        });
    }

    // Plan selection buttons
    selectPlanButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const plan = btn.getAttribute('data-plan');
            selectPlan(plan);
        });
    });

    // Success modal close
    if (btnCloseSuccess) {
        btnCloseSuccess.addEventListener('click', () => {
            if (successModal) {
                successModal.style.display = 'none';
            }
        });
    }

    // Copy token button
    if (btnCopyToken) {
        btnCopyToken.addEventListener('click', copyToken);
    }

    // Check for payment success
    checkPaymentSuccess();

    // Check premium status
    checkPremiumStatus();
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPremium);
} else {
    initPremium();
}

// Expose for debugging
window.premiumDebug = {
    checkStatus: checkPremiumStatus,
    showAds,
    hideAds,
    isPremium: () => isPremium
};
