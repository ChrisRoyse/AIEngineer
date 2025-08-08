/**
 * Conversion Analytics & A/B Testing for Micro-Interactions
 * Real-time tracking and optimization system
 */

class ConversionAnalytics {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.userId = this.getUserId();
        this.startTime = Date.now();
        
        this.metrics = {
            pageViews: 0,
            uniqueVisitors: 0,
            conversionRate: 0,
            avgTimeOnPage: 0,
            bounceRate: 0,
            formCompletionRate: 0,
            ctaClickRate: 0,
            scrollDepth: {},
            heatmapData: [],
            userFlow: [],
            performanceMetrics: {
                loadTime: 0,
                firstContentfulPaint: 0,
                largestContentfulPaint: 0,
                cumulativeLayoutShift: 0,
                firstInputDelay: 0
            }
        };
        
        this.abTests = {
            'cta-button-color': {
                variants: ['green', 'blue', 'orange'],
                currentVariant: null,
                conversions: { green: 0, blue: 0, orange: 0 },
                visitors: { green: 0, blue: 0, orange: 0 }
            },
            'form-layout': {
                variants: ['single-column', 'two-column'],
                currentVariant: null,
                conversions: { 'single-column': 0, 'two-column': 0 },
                visitors: { 'single-column': 0, 'two-column': 0 }
            },
            'testimonial-format': {
                variants: ['carousel', 'grid', 'single'],
                currentVariant: null,
                conversions: { carousel: 0, grid: 0, single: 0 },
                visitors: { carousel: 0, grid: 0, single: 0 }
            }
        };
        
        this.init();
    }

    init() {
        this.setupPerformanceTracking();
        this.setupConversionTracking();
        this.setupHeatmapTracking();
        this.setupScrollTracking();
        this.setupFormAnalytics();
        this.setupUserFlowTracking();
        this.initializeABTests();
        this.startRealTimeTracking();
    }

    generateSessionId() {
        return 'sess_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }

    getUserId() {
        let userId = localStorage.getItem('user_id');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('user_id', userId);
        }
        return userId;
    }

    setupPerformanceTracking() {
        // Core Web Vitals tracking
        if ('PerformanceObserver' in window) {
            // Largest Contentful Paint (LCP)
            new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                this.metrics.performanceMetrics.largestContentfulPaint = lastEntry.startTime;
                this.trackMetric('lcp', lastEntry.startTime);
            }).observe({ entryTypes: ['largest-contentful-paint'] });

            // First Input Delay (FID)
            new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    this.metrics.performanceMetrics.firstInputDelay = entry.processingStart - entry.startTime;
                    this.trackMetric('fid', entry.processingStart - entry.startTime);
                });
            }).observe({ entryTypes: ['first-input'] });

            // Cumulative Layout Shift (CLS)
            let clsValue = 0;
            new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                    }
                });
                this.metrics.performanceMetrics.cumulativeLayoutShift = clsValue;
                this.trackMetric('cls', clsValue);
            }).observe({ entryTypes: ['layout-shift'] });
        }

        // First Contentful Paint
        window.addEventListener('load', () => {
            const perfData = performance.getEntriesByType('navigation')[0];
            this.metrics.performanceMetrics.loadTime = perfData.loadEventEnd - perfData.fetchStart;
            this.metrics.performanceMetrics.firstContentfulPaint = perfData.domContentLoadedEventEnd - perfData.fetchStart;
            
            this.trackMetric('page_load_time', this.metrics.performanceMetrics.loadTime);
        });
    }

    setupConversionTracking() {
        // Track page views
        this.trackPageView();
        
        // Track CTA interactions
        this.setupCTATracking();
        
        // Track form interactions
        this.setupFormTracking();
        
        // Track exit intent
        this.setupExitIntentTracking();
        
        // Track scroll-based conversions
        this.setupScrollConversions();
    }

    setupCTATracking() {
        const ctaButtons = document.querySelectorAll('.cta-primary, .floating-cta-btn, .form-submit');
        
        ctaButtons.forEach(button => {
            // Hover tracking
            button.addEventListener('mouseenter', () => {
                this.trackEvent('cta_hover', {
                    buttonType: this.getCTAType(button),
                    timestamp: Date.now(),
                    scrollPosition: window.scrollY
                });
            });
            
            // Click tracking
            button.addEventListener('click', () => {
                this.trackEvent('cta_click', {
                    buttonType: this.getCTAType(button),
                    timestamp: Date.now(),
                    scrollPosition: window.scrollY,
                    timeOnPage: Date.now() - this.startTime
                });
                
                this.trackConversionFunnel('cta_click');
            });
            
            // View tracking (intersection observer)
            this.trackCTAVisibility(button);
        });
    }

    getCTAType(button) {
        if (button.classList.contains('cta-primary')) return 'primary';
        if (button.classList.contains('floating-cta-btn')) return 'floating';
        if (button.classList.contains('form-submit')) return 'form-submit';
        return 'unknown';
    }

    trackCTAVisibility(button) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.trackEvent('cta_view', {
                        buttonType: this.getCTAType(button),
                        visibilityRatio: entry.intersectionRatio,
                        timestamp: Date.now()
                    });
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(button);
    }

    setupFormTracking() {
        const form = document.getElementById('lead-form');
        const inputs = form.querySelectorAll('input, select');
        
        let formStarted = false;
        let fieldInteractions = {};
        
        inputs.forEach((input, index) => {
            const fieldName = input.name || `field_${index}`;
            fieldInteractions[fieldName] = {
                focused: false,
                completed: false,
                timeSpent: 0,
                corrections: 0
            };
            
            // Track field focus
            input.addEventListener('focus', () => {
                if (!formStarted) {
                    this.trackEvent('form_start', {
                        timestamp: Date.now(),
                        timeOnPage: Date.now() - this.startTime
                    });
                    formStarted = true;
                }
                
                fieldInteractions[fieldName].focused = true;
                fieldInteractions[fieldName].focusTime = Date.now();
                
                this.trackEvent('field_focus', {
                    fieldName: fieldName,
                    fieldIndex: index,
                    timestamp: Date.now()
                });
            });
            
            // Track field completion
            input.addEventListener('blur', () => {
                if (fieldInteractions[fieldName].focusTime) {
                    fieldInteractions[fieldName].timeSpent += Date.now() - fieldInteractions[fieldName].focusTime;
                }
                
                if (input.value.trim() !== '') {
                    fieldInteractions[fieldName].completed = true;
                }
                
                this.trackEvent('field_blur', {
                    fieldName: fieldName,
                    completed: fieldInteractions[fieldName].completed,
                    timeSpent: fieldInteractions[fieldName].timeSpent,
                    timestamp: Date.now()
                });
            });
            
            // Track field corrections
            let lastValue = '';
            input.addEventListener('input', () => {
                if (lastValue.length > input.value.length) {
                    fieldInteractions[fieldName].corrections++;
                }
                lastValue = input.value;
            });
        });
        
        // Track form submission
        form.addEventListener('submit', (e) => {
            this.trackEvent('form_submit', {
                fieldInteractions: fieldInteractions,
                totalTimeSpent: Date.now() - this.startTime,
                timestamp: Date.now()
            });
            
            this.trackConversionFunnel('form_submit');
            this.trackConversion();
        });
        
        // Track form abandonment
        this.setupFormAbandonmentTracking(form, fieldInteractions);
    }

    setupFormAbandonmentTracking(form, fieldInteractions) {
        let abandonmentTimeout;
        
        const resetAbandonmentTimer = () => {
            clearTimeout(abandonmentTimeout);
            abandonmentTimeout = setTimeout(() => {
                const completedFields = Object.values(fieldInteractions).filter(field => field.completed).length;
                const totalFields = Object.keys(fieldInteractions).length;
                
                if (completedFields > 0 && completedFields < totalFields) {
                    this.trackEvent('form_abandonment', {
                        completedFields: completedFields,
                        totalFields: totalFields,
                        completionRate: (completedFields / totalFields) * 100,
                        fieldInteractions: fieldInteractions,
                        timestamp: Date.now()
                    });
                }
            }, 60000); // 1 minute of inactivity
        };
        
        form.addEventListener('input', resetAbandonmentTimer);
        form.addEventListener('focus', resetAbandonmentTimer, true);
    }

    setupHeatmapTracking() {
        let clickHeatmapData = [];
        let scrollHeatmapData = [];
        
        // Click heatmap
        document.addEventListener('click', (e) => {
            const clickData = {
                x: e.clientX,
                y: e.clientY,
                pageX: e.pageX,
                pageY: e.pageY,
                timestamp: Date.now(),
                element: e.target.tagName,
                className: e.target.className,
                id: e.target.id
            };
            
            clickHeatmapData.push(clickData);
            this.metrics.heatmapData.push(clickData);
            
            // Send heatmap data in batches
            if (clickHeatmapData.length >= 10) {
                this.sendHeatmapData('click', clickHeatmapData);
                clickHeatmapData = [];
            }
        });
        
        // Mouse movement heatmap
        let mouseMoveBuffer = [];
        document.addEventListener('mousemove', (e) => {
            mouseMoveBuffer.push({
                x: e.clientX,
                y: e.clientY,
                timestamp: Date.now()
            });
            
            // Sample mouse movements (every 10th movement)
            if (mouseMoveBuffer.length >= 10) {
                const sample = mouseMoveBuffer[mouseMoveBuffer.length - 1];
                scrollHeatmapData.push(sample);
                mouseMoveBuffer = [];
            }
        });
        
        // Send remaining heatmap data on page unload
        window.addEventListener('beforeunload', () => {
            if (clickHeatmapData.length > 0) {
                this.sendHeatmapData('click', clickHeatmapData);
            }
            if (scrollHeatmapData.length > 0) {
                this.sendHeatmapData('scroll', scrollHeatmapData);
            }
        });
    }

    setupScrollTracking() {
        let scrollDepth = 0;
        let scrollMilestones = [25, 50, 75, 90, 100];
        let reachedMilestones = {};
        
        const trackScrollDepth = () => {
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            const scrollTop = window.scrollY;
            
            const currentDepth = Math.round(((scrollTop + windowHeight) / documentHeight) * 100);
            scrollDepth = Math.max(scrollDepth, currentDepth);
            
            // Track milestone achievements
            scrollMilestones.forEach(milestone => {
                if (currentDepth >= milestone && !reachedMilestones[milestone]) {
                    reachedMilestones[milestone] = true;
                    this.trackEvent('scroll_milestone', {
                        milestone: milestone,
                        timestamp: Date.now(),
                        timeOnPage: Date.now() - this.startTime
                    });
                    
                    if (milestone >= 75) {
                        this.trackConversionFunnel('scroll_engagement');
                    }
                }
            });
        };
        
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(trackScrollDepth, 100);
        });
        
        // Store final scroll depth on page unload
        window.addEventListener('beforeunload', () => {
            this.metrics.scrollDepth = scrollDepth;
            this.trackMetric('final_scroll_depth', scrollDepth);
        });
    }

    setupUserFlowTracking() {
        const trackUserFlow = (event) => {
            const flowEvent = {
                event: event.type,
                timestamp: Date.now(),
                url: window.location.href,
                element: event.target.tagName,
                className: event.target.className,
                id: event.target.id,
                scrollPosition: window.scrollY
            };
            
            this.metrics.userFlow.push(flowEvent);
            
            // Keep only last 50 events to prevent memory issues
            if (this.metrics.userFlow.length > 50) {
                this.metrics.userFlow = this.metrics.userFlow.slice(-50);
            }
        };
        
        ['click', 'focus', 'scroll', 'resize'].forEach(eventType => {
            document.addEventListener(eventType, trackUserFlow, { passive: true });
        });
    }

    setupExitIntentTracking() {
        let exitIntentShown = false;
        
        document.addEventListener('mouseleave', (e) => {
            if (e.clientY <= 0 && !exitIntentShown) {
                exitIntentShown = true;
                this.trackEvent('exit_intent', {
                    timestamp: Date.now(),
                    timeOnPage: Date.now() - this.startTime,
                    scrollDepth: Math.round((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100)
                });
                
                // Trigger exit intent popup or offer
                this.triggerExitIntentOffer();
            }
        });
    }

    triggerExitIntentOffer() {
        // Implementation for exit intent offer
        // Could show a special discount or lead magnet
        console.log('Exit intent detected - showing offer');
    }

    initializeABTests() {
        // Assign user to test variants
        Object.keys(this.abTests).forEach(testName => {
            const test = this.abTests[testName];
            const savedVariant = localStorage.getItem(`ab_test_${testName}`);
            
            if (savedVariant && test.variants.includes(savedVariant)) {
                test.currentVariant = savedVariant;
            } else {
                // Random assignment
                const randomIndex = Math.floor(Math.random() * test.variants.length);
                test.currentVariant = test.variants[randomIndex];
                localStorage.setItem(`ab_test_${testName}`, test.currentVariant);
            }
            
            // Track visitor assignment
            test.visitors[test.currentVariant]++;
            
            // Apply variant
            this.applyTestVariant(testName, test.currentVariant);
            
            this.trackEvent('ab_test_assignment', {
                testName: testName,
                variant: test.currentVariant,
                timestamp: Date.now()
            });
        });
    }

    applyTestVariant(testName, variant) {
        switch (testName) {
            case 'cta-button-color':
                this.applyCTAColorVariant(variant);
                break;
            case 'form-layout':
                this.applyFormLayoutVariant(variant);
                break;
            case 'testimonial-format':
                this.applyTestimonialFormatVariant(variant);
                break;
        }
    }

    applyCTAColorVariant(variant) {
        const ctaButtons = document.querySelectorAll('.cta-primary');
        const colors = {
            green: '#10b981',
            blue: '#3b82f6',
            orange: '#f59e0b'
        };
        
        ctaButtons.forEach(button => {
            button.style.backgroundColor = colors[variant];
            button.setAttribute('data-ab-variant', variant);
        });
    }

    applyFormLayoutVariant(variant) {
        const formRow = document.querySelector('.form-row');
        if (formRow) {
            if (variant === 'single-column') {
                formRow.style.gridTemplateColumns = '1fr';
            } else {
                formRow.style.gridTemplateColumns = '1fr 1fr';
            }
            formRow.setAttribute('data-ab-variant', variant);
        }
    }

    applyTestimonialFormatVariant(variant) {
        const testimonialSection = document.querySelector('.testimonials');
        if (testimonialSection) {
            testimonialSection.setAttribute('data-ab-variant', variant);
            
            if (variant === 'grid') {
                // Convert carousel to grid layout
                const track = testimonialSection.querySelector('.testimonial-track');
                track.style.display = 'grid';
                track.style.gridTemplateColumns = 'repeat(auto-fit, minmax(300px, 1fr))';
                track.style.gap = '20px';
                track.style.transform = 'none';
                
                // Hide carousel controls
                const controls = testimonialSection.querySelector('.carousel-controls');
                controls.style.display = 'none';
                
                // Show all testimonials
                const cards = testimonialSection.querySelectorAll('.testimonial-card');
                cards.forEach(card => {
                    card.style.opacity = '1';
                    card.style.transform = 'scale(1)';
                });
            } else if (variant === 'single') {
                // Show only first testimonial
                const cards = testimonialSection.querySelectorAll('.testimonial-card');
                cards.forEach((card, index) => {
                    if (index > 0) {
                        card.style.display = 'none';
                    }
                });
                
                // Hide carousel controls
                const controls = testimonialSection.querySelector('.carousel-controls');
                controls.style.display = 'none';
            }
        }
    }

    trackConversion() {
        // Update conversion metrics for A/B tests
        Object.keys(this.abTests).forEach(testName => {
            const test = this.abTests[testName];
            if (test.currentVariant) {
                test.conversions[test.currentVariant]++;
            }
        });
        
        this.trackEvent('conversion', {
            timestamp: Date.now(),
            timeOnPage: Date.now() - this.startTime,
            abTestVariants: this.getCurrentVariants(),
            conversionValue: 1
        });
        
        // Calculate and update conversion rates
        this.updateConversionRates();
    }

    getCurrentVariants() {
        const variants = {};
        Object.keys(this.abTests).forEach(testName => {
            variants[testName] = this.abTests[testName].currentVariant;
        });
        return variants;
    }

    updateConversionRates() {
        Object.keys(this.abTests).forEach(testName => {
            const test = this.abTests[testName];
            test.variants.forEach(variant => {
                const visitors = test.visitors[variant];
                const conversions = test.conversions[variant];
                const rate = visitors > 0 ? (conversions / visitors) * 100 : 0;
                
                this.trackMetric(`${testName}_${variant}_conversion_rate`, rate);
            });
        });
    }

    trackConversionFunnel(step) {
        this.trackEvent('funnel_step', {
            step: step,
            timestamp: Date.now(),
            timeOnPage: Date.now() - this.startTime
        });
    }

    trackPageView() {
        this.metrics.pageViews++;
        
        this.trackEvent('page_view', {
            url: window.location.href,
            referrer: document.referrer,
            timestamp: Date.now(),
            userAgent: navigator.userAgent,
            screenResolution: `${screen.width}x${screen.height}`,
            viewport: `${window.innerWidth}x${window.innerHeight}`
        });
    }

    trackEvent(eventName, data = {}) {
        const eventData = {
            eventName: eventName,
            sessionId: this.sessionId,
            userId: this.userId,
            timestamp: Date.now(),
            url: window.location.href,
            ...data
        };
        
        // Send to analytics service
        this.sendAnalyticsData(eventData);
        
        // Console log for development
        console.log('Analytics Event:', eventData);
    }

    trackMetric(metricName, value) {
        const metricData = {
            metricName: metricName,
            value: value,
            sessionId: this.sessionId,
            userId: this.userId,
            timestamp: Date.now()
        };
        
        this.sendMetricData(metricData);
    }

    sendAnalyticsData(data) {
        // Send to your analytics endpoint
        if (typeof fetch !== 'undefined') {
            fetch('/api/analytics/events', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).catch(error => {
                console.error('Analytics error:', error);
                // Fallback: store in localStorage for later retry
                this.storeOfflineData('events', data);
            });
        }
        
        // Also send to Google Analytics if available
        if (typeof gtag !== 'undefined') {
            gtag('event', data.eventName, {
                event_category: 'Micro Interactions',
                event_label: data.eventName,
                value: 1
            });
        }
    }

    sendMetricData(data) {
        if (typeof fetch !== 'undefined') {
            fetch('/api/analytics/metrics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).catch(error => {
                console.error('Metrics error:', error);
                this.storeOfflineData('metrics', data);
            });
        }
    }

    sendHeatmapData(type, data) {
        if (typeof fetch !== 'undefined') {
            fetch('/api/analytics/heatmap', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    type: type,
                    sessionId: this.sessionId,
                    userId: this.userId,
                    data: data,
                    timestamp: Date.now()
                })
            }).catch(error => {
                console.error('Heatmap error:', error);
                this.storeOfflineData('heatmap', { type, data });
            });
        }
    }

    storeOfflineData(type, data) {
        const offlineKey = `analytics_offline_${type}`;
        const offlineData = JSON.parse(localStorage.getItem(offlineKey) || '[]');
        offlineData.push(data);
        
        // Keep only last 100 entries to prevent localStorage overflow
        if (offlineData.length > 100) {
            offlineData.splice(0, offlineData.length - 100);
        }
        
        localStorage.setItem(offlineKey, JSON.stringify(offlineData));
    }

    retryOfflineData() {
        ['events', 'metrics', 'heatmap'].forEach(type => {
            const offlineKey = `analytics_offline_${type}`;
            const offlineData = JSON.parse(localStorage.getItem(offlineKey) || '[]');
            
            if (offlineData.length > 0) {
                offlineData.forEach(data => {
                    switch (type) {
                        case 'events':
                            this.sendAnalyticsData(data);
                            break;
                        case 'metrics':
                            this.sendMetricData(data);
                            break;
                        case 'heatmap':
                            this.sendHeatmapData(data.type, data.data);
                            break;
                    }
                });
                
                localStorage.removeItem(offlineKey);
            }
        });
    }

    startRealTimeTracking() {
        // Track time on page every 30 seconds
        setInterval(() => {
            this.trackMetric('time_on_page', Date.now() - this.startTime);
        }, 30000);
        
        // Retry offline data every 2 minutes
        setInterval(() => {
            if (navigator.onLine) {
                this.retryOfflineData();
            }
        }, 120000);
        
        // Track page visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                this.trackEvent('page_visible');
            } else {
                this.trackEvent('page_hidden');
            }
        });
        
        // Track session end
        window.addEventListener('beforeunload', () => {
            this.trackEvent('session_end', {
                sessionDuration: Date.now() - this.startTime,
                finalScrollDepth: this.metrics.scrollDepth,
                totalInteractions: this.metrics.userFlow.length
            });
        });
    }

    // Public API for external access
    getABTestVariant(testName) {
        return this.abTests[testName]?.currentVariant || null;
    }

    getMetrics() {
        return this.metrics;
    }

    getConversionRates() {
        const rates = {};
        Object.keys(this.abTests).forEach(testName => {
            const test = this.abTests[testName];
            rates[testName] = {};
            test.variants.forEach(variant => {
                const visitors = test.visitors[variant];
                const conversions = test.conversions[variant];
                rates[testName][variant] = visitors > 0 ? (conversions / visitors) * 100 : 0;
            });
        });
        return rates;
    }

    // Manual conversion tracking for custom events
    trackCustomConversion(conversionType, value = 1) {
        this.trackEvent('custom_conversion', {
            conversionType: conversionType,
            value: value,
            timestamp: Date.now(),
            abTestVariants: this.getCurrentVariants()
        });
    }
}

// Initialize analytics
window.addEventListener('load', () => {
    window.conversionAnalytics = new ConversionAnalytics();
});

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ConversionAnalytics;
}