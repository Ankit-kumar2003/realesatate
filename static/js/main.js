// Form Validation
const validateForm = (form) => {
    const inputs = form.querySelectorAll('input, textarea, select');
    let isValid = true;

    inputs.forEach(input => {
        if (input.hasAttribute('required') && !input.value.trim()) {
            isValid = false;
            showError(input, 'This field is required');
        } else if (input.type === 'email' && input.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                isValid = false;
                showError(input, 'Please enter a valid email address');
            }
        } else if (input.type === 'tel' && input.value) {
            const phoneRegex = /^\+?[\d\s-]{10,}$/;
            if (!phoneRegex.test(input.value)) {
                isValid = false;
                showError(input, 'Please enter a valid phone number');
            }
        } else if (input.type === 'number' && input.value) {
            if (input.min && Number(input.value) < Number(input.min)) {
                isValid = false;
                showError(input, `Value must be at least ${input.min}`);
            }
            if (input.max && Number(input.value) > Number(input.max)) {
                isValid = false;
                showError(input, `Value must be at most ${input.max}`);
            }
        }
    });

    return isValid;
};

const showError = (input, message) => {
    const formGroup = input.closest('.form-group');
    const errorDiv = formGroup.querySelector('.error-message') || document.createElement('div');
    errorDiv.className = 'error-message text-danger mt-1';
    errorDiv.textContent = message;

    if (!formGroup.querySelector('.error-message')) {
        formGroup.appendChild(errorDiv);
    }

    input.classList.add('is-invalid');
};

const clearErrors = (form) => {
    form.querySelectorAll('.is-invalid').forEach(input => {
        input.classList.remove('is-invalid');
    });
    form.querySelectorAll('.error-message').forEach(error => {
        error.remove();
    });
};

// Image Lazy Loading
const lazyLoadImages = () => {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
};

// Smooth Scrolling
const smoothScroll = (target) => {
    const element = document.querySelector(target);
    if (element) {
        window.scrollTo({
            top: element.offsetTop - 80,
            behavior: 'smooth'
        });
    }
};

// Dynamic Content Loading
const loadMoreContent = async (url, container, options = {}) => {
    const { page = 1, limit = 10, append = true } = options;

    try {
        showLoading();
        const response = await fetch(`${url}?page=${page}&limit=${limit}`);
        const data = await response.json();

        if (data.success) {
            if (append) {
                container.innerHTML += data.html;
            } else {
                container.innerHTML = data.html;
            }

            if (data.hasMore) {
                const loadMoreBtn = document.createElement('button');
                loadMoreBtn.className = 'btn btn-primary mt-4';
                loadMoreBtn.textContent = 'Load More';
                loadMoreBtn.onclick = () => loadMoreContent(url, container, { page: page + 1, limit });
                container.appendChild(loadMoreBtn);
            }
        } else {
            throw new Error(data.message || 'Failed to load content');
        }
    } catch (error) {
        console.error('Error loading content:', error);
        showError(container, 'Failed to load content. Please try again.');
    } finally {
        hideLoading();
    }
};

// Property Search
const searchProperties = async (form) => {
    const formData = new FormData(form);
    const params = new URLSearchParams(formData);

    try {
        showLoading();
        const response = await fetch(`/api/properties/search?${params.toString()}`);
        const data = await response.json();

        if (data.success) {
            const container = document.querySelector('#property-results');
            container.innerHTML = data.html;

            if (data.total > 0) {
                updateSearchResults(data.total, data.filters);
            } else {
                showNoResults();
            }
        } else {
            throw new Error(data.message || 'Search failed');
        }
    } catch (error) {
        console.error('Search error:', error);
        showError(document.querySelector('#property-results'), 'Search failed. Please try again.');
    } finally {
        hideLoading();
    }
};

// Property Filtering
const filterProperties = (filters) => {
    const container = document.querySelector('#property-results');
    const cards = container.querySelectorAll('.property-card');

    cards.forEach(card => {
        let show = true;

        Object.entries(filters).forEach(([key, value]) => {
            if (value && card.dataset[key] !== value) {
                show = false;
            }
        });

        card.style.display = show ? 'block' : 'none';
    });

    updateFilterCounts();
};

// Property Favorites
const toggleFavorite = async (propertyId) => {
    try {
        const response = await fetch(`/api/properties/${propertyId}/favorite`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        });

        const data = await response.json();

        if (data.success) {
            const button = document.querySelector(`#favorite-${propertyId}`);
            button.classList.toggle('active');
            button.querySelector('i').classList.toggle('fas');
            button.querySelector('i').classList.toggle('far');

            updateFavoriteCount(data.count);
        } else {
            throw new Error(data.message || 'Failed to update favorite');
        }
    } catch (error) {
        console.error('Favorite error:', error);
        showError(document.querySelector('#property-results'), 'Failed to update favorite. Please try again.');
    }
};

// Contact Form
const handleContactForm = async (form) => {
    if (!validateForm(form)) {
        return;
    }

    const formData = new FormData(form);

    try {
        showLoading();
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(Object.fromEntries(formData))
        });

        const data = await response.json();

        if (data.success) {
            showSuccess('Message sent successfully! We will get back to you soon.');
            form.reset();
        } else {
            throw new Error(data.message || 'Failed to send message');
        }
    } catch (error) {
        console.error('Contact error:', error);
        showError(form, 'Failed to send message. Please try again.');
    } finally {
        hideLoading();
    }
};

// Utility Functions
const showLoading = () => {
    document.getElementById('loadingOverlay').classList.remove('d-none');
};

const hideLoading = () => {
    document.getElementById('loadingOverlay').classList.add('d-none');
};

const showSuccess = (message) => {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('main').insertAdjacentElement('afterbegin', alert);

    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 150);
    }, 5000);
};

const showError = (element, message) => {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    element.insertAdjacentElement('beforebegin', alert);

    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 150);
    }, 5000);
};

const getCsrfToken = () => {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
};

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize lazy loading
    lazyLoadImages();

    // Form validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            e.preventDefault();
            smoothScroll(anchor.getAttribute('href'));
        });
    });

    // Property search form
    const searchForm = document.querySelector('#property-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            searchProperties(searchForm);
        });
    }

    // Contact form
    const contactForm = document.querySelector('#contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleContactForm(contactForm);
        });
    }

    // Favorite buttons
    document.querySelectorAll('.favorite-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const propertyId = button.dataset.propertyId;
            toggleFavorite(propertyId);
        });
    });

    // Filter inputs
    document.querySelectorAll('.filter-input').forEach(input => {
        input.addEventListener('change', () => {
            const filters = {};
            document.querySelectorAll('.filter-input').forEach(input => {
                if (input.value) {
                    filters[input.name] = input.value;
                }
            });
            filterProperties(filters);
        });
    });
}); 