/**
 * Conversion-Optimized Micro-Interactions for Agentic Engineering Coaching
 * Performance Target: 60fps, <100ms response time
 * Accessibility: WCAG 2.1 AA compliant
 */

class MicroInteractionManager {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.initializeAnimations();
        this.setupAccessibility();
        this.startPerformanceMonitoring();
    }

    init() {
        // Performance optimization
        this.raf = null;
        this.scrollTicking = false;
        this.resizeTicking = false;
        
        // Form state
        this.formProgress = 0;
        this.formValid = false;
        
        // Carousel state
        this.currentTestimonial = 0;
        this.testimonialCount = document.querySelectorAll('.testimonial-card').length;
        this.autoPlayInterval = null;
        
        // Performance metrics
        this.metrics = {
            interactions: 0,
            loadTime: performance.now(),
            firstInteraction: null,
            conversionFunnel: {
                pageView: true,
                ctaHover: false,
                ctaClick: false,
                formStart: false,
                formComplete: false
            }
        };
    }

    setupEventListeners() {
        // Primary CTA interactions
        this.setupCTAInteractions();
        
        // Form interactions
        this.setupFormInteractions();
        
        // Scroll-based interactions
        this.setupScrollInteractions();
        
        // Testimonial carousel
        this.setupTestimonialCarousel();
        
        // Mobile optimizations
        this.setupMobileInteractions();
        
        // Accessibility
        this.setupKeyboardNavigation();
    }

    setupCTAInteractions() {
        const primaryCTA = document.getElementById('primary-cta');
        const floatingCTA = document.getElementById('floating-cta');
        
        if (primaryCTA) {
            // Hover effects with performance optimization
            primaryCTA.addEventListener('mouseenter', (e) => {
                this.trackEvent('cta_hover', 'primary');
                this.metrics.conversionFunnel.ctaHover = true;
                this.addHoverEffect(e.target);
            });
            
            primaryCTA.addEventListener('mouseleave', (e) => {
                this.removeHoverEffect(e.target);
            });
            
            // Click with ripple effect
            primaryCTA.addEventListener('click', (e) => {
                this.trackEvent('cta_click', 'primary');
                this.metrics.conversionFunnel.ctaClick = true;
                this.createRippleEffect(e);
                this.scrollToForm();
                
                // Success state after scroll
                setTimeout(() => {
                    this.showCTASuccess(primaryCTA);
                }, 1000);
            });
            
            // Touch interactions for mobile
            primaryCTA.addEventListener('touchstart', (e) => {
                this.addTouchFeedback(e.target);
            });
            
            primaryCTA.addEventListener('touchend', (e) => {
                this.removeTouchFeedback(e.target);
            });
        }
        
        // Floating CTA
        if (floatingCTA) {
            const floatingBtn = floatingCTA.querySelector('.floating-cta-btn');
            floatingBtn.addEventListener('click', () => {
                this.trackEvent('cta_click', 'floating');
                this.scrollToForm();
                this.addHapticFeedback();
            });
        }
    }

    setupFormInteractions() {
        const form = document.getElementById('lead-form');
        const inputs = form.querySelectorAll('input, select');
        const submitBtn = document.getElementById('form-submit');
        
        // Real-time validation
        inputs.forEach((input, index) => {
            // Focus animations
            input.addEventListener('focus', (e) => {
                this.animateFieldFocus(e.target);
                this.trackEvent('form_field_focus', input.name);
                
                if (!this.metrics.conversionFunnel.formStart) {
                    this.metrics.conversionFunnel.formStart = true;
                    this.trackEvent('form_start');
                }
            });
            
            input.addEventListener('blur', (e) => {
                this.animateFieldBlur(e.target);
                this.validateField(e.target);
            });
            
            // Real-time validation during typing
            input.addEventListener('input', (e) => {
                this.debounce(() => {
                    this.validateFieldRealTime(e.target);
                    this.updateFormProgress();
                    
                    // Email suggestions
                    if (input.type === 'email') {
                        this.showEmailSuggestions(e.target);
                    }
                }, 300)();
            });
        });
        
        // Form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmission(form, submitBtn);
        });
        
        // Progressive form enhancement
        this.enhanceFormUX(form);
    }

    setupScrollInteractions() {
        window.addEventListener('scroll', () => {
            if (!this.scrollTicking) {
                requestAnimationFrame(() => {
                    this.handleScroll();
                    this.scrollTicking = false;
                });
                this.scrollTicking = true;
            }
        });
        
        // Intersection Observer for animations
        this.setupIntersectionObserver();
    }

    setupTestimonialCarousel() {
        const carousel = document.getElementById('testimonial-carousel');
        const prevBtn = carousel.querySelector('.prev');
        const nextBtn = carousel.querySelector('.next');
        const dotsContainer = carousel.querySelector('.carousel-dots');
        
        // Create dots
        for (let i = 0; i < this.testimonialCount; i++) {
            const dot = document.createElement('div');
            dot.className = `dot ${i === 0 ? 'active' : ''}`;
            dot.addEventListener('click', () => this.goToTestimonial(i));
            dotsContainer.appendChild(dot);
        }
        
        // Button controls
        prevBtn.addEventListener('click', () => this.previousTestimonial());
        nextBtn.addEventListener('click', () => this.nextTestimonial());
        
        // Auto-play with pause on hover
        this.startAutoPlay();
        carousel.addEventListener('mouseenter', () => this.pauseAutoPlay());
        carousel.addEventListener('mouseleave', () => this.startAutoPlay());
        
        // Touch/swipe support for mobile
        this.setupCarouselSwipe(carousel);
        
        // Keyboard navigation
        carousel.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.previousTestimonial();
            if (e.key === 'ArrowRight') this.nextTestimonial();
        });
    }

    setupMobileInteractions() {
        // Touch feedback
        const touchElements = document.querySelectorAll('button, .trust-item, .testimonial-card');
        
        touchElements.forEach(element => {
            element.addEventListener('touchstart', (e) => {
                this.addTouchFeedback(element);
                this.addHapticFeedback('light');
            });
            
            element.addEventListener('touchend', () => {
                setTimeout(() => this.removeTouchFeedback(element), 150);
            });
            
            element.addEventListener('touchcancel', () => {
                this.removeTouchFeedback(element);
            });
        });
        
        // Pull to refresh (if supported)
        this.setupPullToRefresh();
        
        // Floating CTA visibility based on scroll
        this.setupFloatingCTAVisibility();
    }

    setupAccessibility() {
        // Respect prefers-reduced-motion
        this.reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        // Focus management
        this.setupFocusManagement();
        
        // Screen reader announcements
        this.setupScreenReaderSupport();
        
        // High contrast support
        this.setupHighContrastSupport();
        
        // Keyboard shortcuts
        this.setupKeyboardShortcuts();
    }

    // Animation Methods
    animateFieldFocus(field) {
        const label = field.previousElementSibling;
        const feedback = field.nextElementSibling;
        
        if (!this.reducedMotion) {
            field.style.transform = 'translateY(-1px)';
            if (label) {
                label.style.color = 'var(--border-focus)';
                label.style.transform = 'translateY(-2px)';
            }
        }
        
        // Add focus ring with animation
        field.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
    }

    animateFieldBlur(field) {
        const label = field.previousElementSibling;
        
        if (!this.reducedMotion) {
            field.style.transform = 'translateY(0)';
            if (label) {
                label.style.color = 'var(--text-primary)';
                label.style.transform = 'translateY(0)';
            }
        }
    }

    createRippleEffect(event) {
        const button = event.currentTarget;
        const ripple = button.querySelector('.cta-ripple');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.style.transform = 'scale(0)';
        
        // Trigger animation
        requestAnimationFrame(() => {
            ripple.style.transform = 'scale(4)';
            ripple.style.opacity = '0';
        });
        
        setTimeout(() => {
            ripple.style.transform = 'scale(0)';
            ripple.style.opacity = '0.3';
        }, 600);
    }

    showCTASuccess(button) {
        button.classList.add('success');
        const successState = button.querySelector('.cta-success-state');
        successState.style.display = 'flex';
        
        setTimeout(() => {
            button.classList.remove('success');
            successState.style.display = 'none';
        }, 2000);
    }

    // Form Validation
    validateField(field) {
        const feedback = field.nextElementSibling;
        const isValid = field.checkValidity() && field.value.trim() !== '';
        
        if (feedback) {
            feedback.className = `input-feedback ${isValid ? 'valid' : 'invalid'}`;
        }
        
        // Custom validation rules
        if (field.type === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const isValidEmail = emailRegex.test(field.value);
            if (feedback) {
                feedback.className = `input-feedback ${isValidEmail ? 'valid' : 'invalid'}`;
            }
        }
        
        return isValid;
    }

    validateFieldRealTime(field) {
        const isValid = this.validateField(field);
        
        // Animate validation state change
        if (!this.reducedMotion) {
            field.style.transition = 'border-color 0.3s ease';
            field.style.borderColor = isValid ? 'var(--success-color)' : 'var(--error-color)';
        }
        
        return isValid;
    }

    updateFormProgress() {
        const form = document.getElementById('lead-form');
        const inputs = form.querySelectorAll('input[required], select[required]');
        const progressFill = document.querySelector('.progress-fill');
        const progressText = document.querySelector('.progress-text');
        
        let filledInputs = 0;
        inputs.forEach(input => {
            if (input.value.trim() !== '' && input.checkValidity()) {
                filledInputs++;
            }
        });
        
        const progress = (filledInputs / inputs.length) * 100;
        this.formProgress = progress;
        
        if (progressFill && !this.reducedMotion) {
            progressFill.style.width = `${progress}%`;
        }
        
        if (progressText) {
            if (progress === 100) {
                progressText.textContent = 'Ready to submit!';
                progressText.style.color = 'var(--success-color)';
            } else {
                progressText.textContent = `${Math.round(progress)}% complete`;
                progressText.style.color = 'var(--text-secondary)';
            }
        }
        
        // Enable/disable submit button
        const submitBtn = document.getElementById('form-submit');
        submitBtn.disabled = progress < 100;
    }

    showEmailSuggestions(emailInput) {
        const value = emailInput.value;
        const suggestion = emailInput.parentElement.querySelector('.input-suggestion');
        
        if (!suggestion) return;
        
        const domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'company.com'];
        const atIndex = value.indexOf('@');
        
        if (atIndex > 0 && atIndex === value.length - 1) {
            // Show domain suggestions
            suggestion.textContent = `Try: ${value}${domains[0]}`;
            suggestion.style.display = 'block';
            suggestion.onclick = () => {
                emailInput.value = `${value}${domains[0]}`;
                suggestion.style.display = 'none';
                emailInput.focus();
                this.validateFieldRealTime(emailInput);
            };
        } else if (atIndex > 0) {
            const domain = value.substring(atIndex + 1);
            const matchedDomain = domains.find(d => d.startsWith(domain) && d !== domain);
            
            if (matchedDomain) {
                const suggested = value.substring(0, atIndex + 1) + matchedDomain;
                suggestion.textContent = `Did you mean: ${suggested}?`;
                suggestion.style.display = 'block';
                suggestion.onclick = () => {
                    emailInput.value = suggested;
                    suggestion.style.display = 'none';
                    this.validateFieldRealTime(emailInput);
                };
            } else {
                suggestion.style.display = 'none';
            }
        } else {
            suggestion.style.display = 'none';
        }
    }

    handleFormSubmission(form, submitBtn) {
        this.trackEvent('form_submit_attempt');
        
        // Show loading state
        this.showLoadingState(submitBtn);
        
        // Simulate form processing
        setTimeout(() => {
            this.metrics.conversionFunnel.formComplete = true;
            this.trackEvent('form_submit_success');
            
            // Hide loading state
            this.hideLoadingState(submitBtn);
            
            // Show success modal
            this.showSuccessModal();
            
            // Track conversion
            this.trackConversion();
        }, 2000);
    }

    showLoadingState(button) {
        const defaultText = button.querySelector('.submit-default');
        const loadingText = button.querySelector('.submit-loading');
        
        defaultText.style.display = 'none';
        loadingText.style.display = 'flex';
        button.disabled = true;
        
        if (!this.reducedMotion) {
            button.style.transform = 'scale(0.98)';
        }
    }

    hideLoadingState(button) {
        const defaultText = button.querySelector('.submit-default');
        const loadingText = button.querySelector('.submit-loading');
        const successText = button.querySelector('.submit-success');
        
        loadingText.style.display = 'none';
        successText.style.display = 'block';
        
        setTimeout(() => {
            successText.style.display = 'none';
            defaultText.style.display = 'block';
            button.disabled = false;
            
            if (!this.reducedMotion) {
                button.style.transform = 'scale(1)';
            }
        }, 3000);
    }

    showSuccessModal() {
        const modal = document.getElementById('success-modal');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        // Focus management
        const closeBtn = document.getElementById('modal-close');
        closeBtn.focus();
        
        closeBtn.addEventListener('click', () => {
            this.hideSuccessModal();
        });
        
        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideSuccessModal();
            }
        });
        
        // Close on overlay click
        modal.querySelector('.modal-overlay').addEventListener('click', () => {
            this.hideSuccessModal();
        });
    }

    hideSuccessModal() {
        const modal = document.getElementById('success-modal');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Testimonial Carousel Methods
    goToTestimonial(index) {
        const track = document.querySelector('.testimonial-track');
        const cards = document.querySelectorAll('.testimonial-card');
        const dots = document.querySelectorAll('.dot');
        
        // Update active states
        cards.forEach((card, i) => {
            card.classList.toggle('active', i === index);
        });
        
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
        
        // Animate transition
        if (!this.reducedMotion) {
            track.style.transform = `translateX(-${index * 100}%)`;
        }
        
        this.currentTestimonial = index;
        this.trackEvent('testimonial_view', index);
    }

    nextTestimonial() {
        const next = (this.currentTestimonial + 1) % this.testimonialCount;
        this.goToTestimonial(next);
    }

    previousTestimonial() {
        const prev = this.currentTestimonial === 0 
            ? this.testimonialCount - 1 
            : this.currentTestimonial - 1;
        this.goToTestimonial(prev);
    }

    startAutoPlay() {
        this.autoPlayInterval = setInterval(() => {
            this.nextTestimonial();
        }, 5000);
    }

    pauseAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }

    setupCarouselSwipe(carousel) {
        let startX = 0;
        let startY = 0;
        let distX = 0;
        let distY = 0;
        let threshold = 50;
        let restraint = 100;
        
        carousel.addEventListener('touchstart', (e) => {
            const touch = e.touches[0];
            startX = touch.pageX;
            startY = touch.pageY;
        });
        
        carousel.addEventListener('touchend', (e) => {
            const touch = e.changedTouches[0];
            distX = touch.pageX - startX;
            distY = touch.pageY - startY;
            
            if (Math.abs(distX) >= threshold && Math.abs(distY) <= restraint) {
                if (distX > 0) {
                    this.previousTestimonial();
                } else {
                    this.nextTestimonial();
                }
                this.addHapticFeedback('medium');
            }
        });
    }

    // Scroll Interactions
    handleScroll() {
        const scrollY = window.scrollY;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        
        // Update scroll depth
        const scrollDepth = Math.round((scrollY / (documentHeight - windowHeight)) * 100);
        this.metrics.scrollDepth = Math.max(this.metrics.scrollDepth, scrollDepth);
        
        // Floating CTA visibility
        this.updateFloatingCTAVisibility(scrollY);
        
        // Parallax effects (if not reduced motion)
        if (!this.reducedMotion) {
            this.updateParallaxEffects(scrollY);
        }
    }

    setupIntersectionObserver() {
        const animateElements = document.querySelectorAll('.animate-in');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        animateElements.forEach(element => {
            element.style.animationPlayState = 'paused';
            observer.observe(element);
        });
    }

    updateFloatingCTAVisibility(scrollY) {
        const floatingCTA = document.getElementById('floating-cta');
        const formSection = document.getElementById('signup-form');
        const formRect = formSection.getBoundingClientRect();
        
        // Show floating CTA when form is out of view
        const shouldShow = formRect.top > window.innerHeight || formRect.bottom < 0;
        
        if (shouldShow && !floatingCTA.classList.contains('show')) {
            floatingCTA.classList.add('show');
        } else if (!shouldShow && floatingCTA.classList.contains('show')) {
            floatingCTA.classList.remove('show');
        }
    }

    // Mobile Optimizations
    setupPullToRefresh() {
        let startY = 0;
        let pulling = false;
        
        document.addEventListener('touchstart', (e) => {
            startY = e.touches[0].pageY;
            pulling = window.scrollY === 0;
        });
        
        document.addEventListener('touchmove', (e) => {
            if (!pulling) return;
            
            const currentY = e.touches[0].pageY;
            const pullDistance = currentY - startY;
            
            if (pullDistance > 50) {
                // Add visual feedback for pull to refresh
                document.body.style.transform = `translateY(${Math.min(pullDistance * 0.5, 50)}px)`;
            }
        });
        
        document.addEventListener('touchend', () => {
            if (pulling) {
                document.body.style.transform = 'translateY(0)';
                // Could trigger a refresh here
            }
            pulling = false;
        });
    }

    addTouchFeedback(element) {
        if (!this.reducedMotion) {
            element.style.transform = 'scale(0.95)';
            element.style.transition = 'transform 0.1s ease-out';
        }
        element.classList.add('touch-active');
    }

    removeTouchFeedback(element) {
        if (!this.reducedMotion) {
            element.style.transform = 'scale(1)';
        }
        element.classList.remove('touch-active');
    }

    addHapticFeedback(type = 'light') {
        if ('vibrate' in navigator) {
            const patterns = {
                light: [10],
                medium: [20],
                heavy: [30]
            };
            navigator.vibrate(patterns[type]);
        }
    }

    // Accessibility Methods
    setupFocusManagement() {
        let focusedElement = null;
        
        document.addEventListener('focusin', (e) => {
            focusedElement = e.target;
        });
        
        document.addEventListener('focusout', (e) => {
            // Add subtle focus indicators
            if (focusedElement) {
                focusedElement.setAttribute('data-was-focused', 'true');
            }
        });
    }

    setupScreenReaderSupport() {
        // Create live region for announcements
        const liveRegion = document.createElement('div');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.style.position = 'absolute';
        liveRegion.style.left = '-10000px';
        liveRegion.style.width = '1px';
        liveRegion.style.height = '1px';
        liveRegion.style.overflow = 'hidden';
        document.body.appendChild(liveRegion);
        
        this.announceToScreenReader = (message) => {
            liveRegion.textContent = message;
        };
    }

    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Tab trap in modal
            if (document.getElementById('success-modal').style.display === 'flex') {
                if (e.key === 'Tab') {
                    // Keep focus within modal
                    const modal = document.getElementById('success-modal');
                    const focusableElements = modal.querySelectorAll('button, [tabindex]:not([tabindex="-1"])');
                    const firstElement = focusableElements[0];
                    const lastElement = focusableElements[focusableElements.length - 1];
                    
                    if (e.shiftKey && document.activeElement === firstElement) {
                        e.preventDefault();
                        lastElement.focus();
                    } else if (!e.shiftKey && document.activeElement === lastElement) {
                        e.preventDefault();
                        firstElement.focus();
                    }
                }
            }
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Alt + C to focus primary CTA
            if (e.altKey && e.key === 'c') {
                e.preventDefault();
                document.getElementById('primary-cta').focus();
            }
            
            // Alt + F to focus form
            if (e.altKey && e.key === 'f') {
                e.preventDefault();
                document.getElementById('firstName').focus();
                this.scrollToForm();
            }
        });
    }

    // Utility Methods
    scrollToForm() {
        const formSection = document.getElementById('signup-form');
        const offset = 80; // Account for any fixed headers
        
        if (!this.reducedMotion) {
            window.scrollTo({
                top: formSection.offsetTop - offset,
                behavior: 'smooth'
            });
        } else {
            window.scrollTo(0, formSection.offsetTop - offset);
        }
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Analytics and Tracking
    trackEvent(eventName, data = null) {
        this.metrics.interactions++;
        
        if (!this.metrics.firstInteraction) {
            this.metrics.firstInteraction = performance.now();
        }
        
        // Track to analytics service
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, {
                custom_parameter: data,
                value: this.metrics.interactions
            });
        }
        
        // Console log for development
        console.log(`Event: ${eventName}`, data, this.metrics);
    }

    trackConversion() {
        const conversionData = {
            timeToConversion: performance.now() - this.metrics.loadTime,
            scrollDepth: this.metrics.scrollDepth,
            interactions: this.metrics.interactions,
            funnel: this.metrics.conversionFunnel
        };
        
        this.trackEvent('conversion', conversionData);
        
        // Send to conversion tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'conversion', {
                send_to: 'AW-XXXXXXXXX/XXXXXXX', // Replace with actual conversion ID
                value: 1.0,
                currency: 'USD'
            });
        }
    }

    startPerformanceMonitoring() {
        // Monitor frame rate
        let frames = 0;
        let lastTime = performance.now();
        
        const countFrames = (currentTime) => {
            frames++;
            if (currentTime >= lastTime + 1000) {
                const fps = Math.round((frames * 1000) / (currentTime - lastTime));
                this.metrics.fps = fps;
                
                if (fps < 30) {
                    console.warn(`Low FPS detected: ${fps}`);
                    // Reduce animation complexity
                    this.reducedMotion = true;
                }
                
                frames = 0;
                lastTime = currentTime;
            }
            requestAnimationFrame(countFrames);
        };
        
        requestAnimationFrame(countFrames);
        
        // Monitor memory usage
        if (performance.memory) {
            setInterval(() => {
                const memoryUsage = performance.memory.usedJSHeapSize / 1048576; // MB
                if (memoryUsage > 50) {
                    console.warn(`High memory usage: ${memoryUsage.toFixed(2)} MB`);
                }
            }, 30000);
        }
    }

    // Public API for external control
    getMetrics() {
        return this.metrics;
    }

    setReducedMotion(reduced) {
        this.reducedMotion = reduced;
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.microInteractions = new MicroInteractionManager();
    });
} else {
    window.microInteractions = new MicroInteractionManager();
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MicroInteractionManager;
}