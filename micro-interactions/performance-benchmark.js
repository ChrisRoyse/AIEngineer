/**
 * Performance Benchmarking Suite for Micro-Interactions
 * Tests and validates 60fps target and conversion optimization
 */

class PerformanceBenchmark {
    constructor() {
        this.benchmarks = {
            frameRate: { target: 60, current: 0, samples: [] },
            interactionResponse: { target: 100, current: 0, samples: [] },
            memoryUsage: { target: 50, current: 0, baseline: 0 },
            loadTime: { target: 2500, current: 0 },
            coreWebVitals: {
                lcp: { target: 2500, current: 0 },
                fid: { target: 100, current: 0 },
                cls: { target: 0.1, current: 0 }
            }
        };
        
        this.testResults = [];
        this.running = false;
        this.startTime = performance.now();
        
        this.init();
    }

    init() {
        this.createBenchmarkUI();
        this.setupPerformanceObservers();
        this.startContinuousMonitoring();
    }

    createBenchmarkUI() {
        // Create floating benchmark panel
        const panel = document.createElement('div');
        panel.id = 'performance-benchmark';
        panel.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            width: 300px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            z-index: 10000;
            display: none;
            max-height: 400px;
            overflow-y: auto;
        `;
        
        panel.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h3 style="margin: 0; font-size: 14px;">Performance Monitor</h3>
                <button id="toggle-benchmark" style="background: #333; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Hide</button>
            </div>
            <div id="benchmark-content">
                <div id="fps-display">FPS: <span style="color: #10b981;">--</span></div>
                <div id="response-display">Response: <span style="color: #10b981;">--ms</span></div>
                <div id="memory-display">Memory: <span style="color: #10b981;">--MB</span></div>
                <div id="lcp-display">LCP: <span style="color: #10b981;">--ms</span></div>
                <div id="fid-display">FID: <span style="color: #10b981;">--ms</span></div>
                <div id="cls-display">CLS: <span style="color: #10b981;">--</span></div>
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #333;">
                    <button id="run-benchmark" style="background: #3b82f6; color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; width: 100%; margin-bottom: 5px;">Run Full Benchmark</button>
                    <button id="export-results" style="background: #6b7280; color: white; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; width: 100%;">Export Results</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(panel);
        
        // Setup panel controls
        this.setupBenchmarkControls(panel);
        
        // Show panel if in development mode
        if (window.location.hostname === 'localhost' || window.location.search.includes('benchmark')) {
            panel.style.display = 'block';
        }
    }

    setupBenchmarkControls(panel) {
        const toggleBtn = panel.querySelector('#toggle-benchmark');
        const content = panel.querySelector('#benchmark-content');
        const runBtn = panel.querySelector('#run-benchmark');
        const exportBtn = panel.querySelector('#export-results');
        
        toggleBtn.addEventListener('click', () => {
            const isVisible = content.style.display !== 'none';
            content.style.display = isVisible ? 'none' : 'block';
            toggleBtn.textContent = isVisible ? 'Show' : 'Hide';
        });
        
        runBtn.addEventListener('click', () => {
            this.runFullBenchmark();
        });
        
        exportBtn.addEventListener('click', () => {
            this.exportResults();
        });
        
        // Keyboard shortcut to toggle benchmark (Ctrl+Shift+P)
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'P') {
                panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
            }
        });
    }

    setupPerformanceObservers() {
        // Largest Contentful Paint
        if ('PerformanceObserver' in window) {
            new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                this.benchmarks.coreWebVitals.lcp.current = Math.round(lastEntry.startTime);
                this.updateDisplay('lcp', this.benchmarks.coreWebVitals.lcp.current);
            }).observe({ entryTypes: ['largest-contentful-paint'] });

            // First Input Delay
            new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    const fid = entry.processingStart - entry.startTime;
                    this.benchmarks.coreWebVitals.fid.current = Math.round(fid);
                    this.updateDisplay('fid', this.benchmarks.coreWebVitals.fid.current);
                });
            }).observe({ entryTypes: ['first-input'] });

            // Cumulative Layout Shift
            let clsValue = 0;
            new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                    }
                });
                this.benchmarks.coreWebVitals.cls.current = Math.round(clsValue * 1000) / 1000;
                this.updateDisplay('cls', this.benchmarks.coreWebVitals.cls.current);
            }).observe({ entryTypes: ['layout-shift'] });
        }
    }

    startContinuousMonitoring() {
        this.monitorFrameRate();
        this.monitorMemoryUsage();
        this.monitorInteractionResponse();
        
        // Update displays every second
        setInterval(() => {
            this.updateAllDisplays();
        }, 1000);
    }

    monitorFrameRate() {
        let frames = 0;
        let lastTime = performance.now();
        
        const countFrames = (currentTime) => {
            frames++;
            
            if (currentTime >= lastTime + 1000) {
                const fps = Math.round((frames * 1000) / (currentTime - lastTime));
                this.benchmarks.frameRate.current = fps;
                this.benchmarks.frameRate.samples.push(fps);
                
                // Keep only last 60 samples (1 minute of data)
                if (this.benchmarks.frameRate.samples.length > 60) {
                    this.benchmarks.frameRate.samples.shift();
                }
                
                frames = 0;
                lastTime = currentTime;
            }
            
            requestAnimationFrame(countFrames);
        };
        
        requestAnimationFrame(countFrames);
    }

    monitorMemoryUsage() {
        if (performance.memory) {
            const checkMemory = () => {
                const memoryMB = Math.round(performance.memory.usedJSHeapSize / 1048576);
                
                if (this.benchmarks.memoryUsage.baseline === 0) {
                    this.benchmarks.memoryUsage.baseline = memoryMB;
                }
                
                this.benchmarks.memoryUsage.current = memoryMB - this.benchmarks.memoryUsage.baseline;
                
                setTimeout(checkMemory, 5000); // Check every 5 seconds
            };
            
            checkMemory();
        }
    }

    monitorInteractionResponse() {
        const interactionElements = document.querySelectorAll('button, input, .trust-item, .testimonial-card');
        
        interactionElements.forEach(element => {
            element.addEventListener('click', (e) => {
                const startTime = performance.now();
                
                // Measure time to visual feedback
                requestAnimationFrame(() => {
                    const responseTime = performance.now() - startTime;
                    this.benchmarks.interactionResponse.current = Math.round(responseTime);
                    this.benchmarks.interactionResponse.samples.push(responseTime);
                    
                    // Keep only last 20 samples
                    if (this.benchmarks.interactionResponse.samples.length > 20) {
                        this.benchmarks.interactionResponse.samples.shift();
                    }
                });
            });
        });
    }

    async runFullBenchmark() {
        console.log('Starting comprehensive performance benchmark...');
        this.running = true;
        
        const runBtn = document.querySelector('#run-benchmark');
        runBtn.textContent = 'Running...';
        runBtn.disabled = true;
        
        const results = {
            timestamp: new Date().toISOString(),
            testDuration: 0,
            tests: []
        };
        
        try {
            // Test 1: Animation Performance
            console.log('Testing animation performance...');
            const animationResult = await this.testAnimationPerformance();
            results.tests.push(animationResult);
            
            // Test 2: Form Interaction Performance
            console.log('Testing form interaction performance...');
            const formResult = await this.testFormPerformance();
            results.tests.push(formResult);
            
            // Test 3: CTA Button Performance
            console.log('Testing CTA button performance...');
            const ctaResult = await this.testCTAPerformance();
            results.tests.push(ctaResult);
            
            // Test 4: Carousel Performance
            console.log('Testing carousel performance...');
            const carouselResult = await this.testCarouselPerformance();
            results.tests.push(carouselResult);
            
            // Test 5: Memory Leak Detection
            console.log('Testing for memory leaks...');
            const memoryResult = await this.testMemoryLeaks();
            results.tests.push(memoryResult);
            
            // Test 6: Accessibility Performance
            console.log('Testing accessibility features...');
            const accessibilityResult = await this.testAccessibilityPerformance();
            results.tests.push(accessibilityResult);
            
            results.testDuration = performance.now() - this.startTime;
            this.testResults.push(results);
            
            console.log('Benchmark completed:', results);
            this.displayBenchmarkResults(results);
            
        } catch (error) {
            console.error('Benchmark failed:', error);
        } finally {
            runBtn.textContent = 'Run Full Benchmark';
            runBtn.disabled = false;
            this.running = false;
        }
    }

    async testAnimationPerformance() {
        return new Promise((resolve) => {
            const testElement = document.createElement('div');
            testElement.style.cssText = `
                position: absolute;
                width: 100px;
                height: 100px;
                background: red;
                top: -200px;
                left: 50%;
                transition: transform 1s ease;
            `;
            document.body.appendChild(testElement);
            
            const frameRates = [];
            let animationStart = performance.now();
            let frameCount = 0;
            
            const measureFrames = () => {
                frameCount++;
                const elapsed = performance.now() - animationStart;
                
                if (elapsed < 1000) {
                    requestAnimationFrame(measureFrames);
                } else {
                    const avgFPS = Math.round((frameCount * 1000) / elapsed);
                    document.body.removeChild(testElement);
                    
                    resolve({
                        test: 'Animation Performance',
                        fps: avgFPS,
                        target: 60,
                        passed: avgFPS >= 55,
                        details: `Animation maintained ${avgFPS} FPS over 1 second`
                    });
                }
            };
            
            // Start animation and measurement
            requestAnimationFrame(() => {
                testElement.style.transform = 'translateY(400px) rotate(360deg) scale(1.2)';
                requestAnimationFrame(measureFrames);
            });
        });
    }

    async testFormPerformance() {
        return new Promise((resolve) => {
            const form = document.getElementById('lead-form');
            const emailInput = document.getElementById('email');
            
            if (!emailInput) {
                resolve({
                    test: 'Form Performance',
                    result: 'SKIPPED',
                    reason: 'Email input not found'
                });
                return;
            }
            
            const responseTimes = [];
            const testValues = ['test@', 'test@gmail', 'test@gmail.com'];
            let testIndex = 0;
            
            const testInput = () => {
                if (testIndex >= testValues.length) {
                    const avgResponse = responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length;
                    
                    resolve({
                        test: 'Form Performance',
                        averageResponseTime: Math.round(avgResponse),
                        target: 100,
                        passed: avgResponse <= 100,
                        details: `Real-time validation averaged ${Math.round(avgResponse)}ms response`
                    });
                    return;
                }
                
                const startTime = performance.now();
                emailInput.value = testValues[testIndex];
                emailInput.dispatchEvent(new Event('input', { bubbles: true }));
                
                // Measure time to validation feedback
                requestAnimationFrame(() => {
                    const responseTime = performance.now() - startTime;
                    responseTimes.push(responseTime);
                    testIndex++;
                    
                    setTimeout(testInput, 100);
                });
            };
            
            testInput();
        });
    }

    async testCTAPerformance() {
        return new Promise((resolve) => {
            const ctaButton = document.getElementById('primary-cta');
            
            if (!ctaButton) {
                resolve({
                    test: 'CTA Performance',
                    result: 'SKIPPED',
                    reason: 'Primary CTA not found'
                });
                return;
            }
            
            const responseTimes = [];
            let testCount = 0;
            const maxTests = 10;
            
            const testCTAResponse = () => {
                if (testCount >= maxTests) {
                    const avgResponse = responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length;
                    
                    resolve({
                        test: 'CTA Performance',
                        averageResponseTime: Math.round(avgResponse),
                        target: 100,
                        passed: avgResponse <= 100,
                        details: `CTA hover effects averaged ${Math.round(avgResponse)}ms response`
                    });
                    return;
                }
                
                const startTime = performance.now();
                
                // Trigger hover effect
                ctaButton.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
                
                requestAnimationFrame(() => {
                    const responseTime = performance.now() - startTime;
                    responseTimes.push(responseTime);
                    
                    // Reset hover state
                    ctaButton.dispatchEvent(new MouseEvent('mouseleave', { bubbles: true }));
                    
                    testCount++;
                    setTimeout(testCTAResponse, 50);
                });
            };
            
            testCTAResponse();
        });
    }

    async testCarouselPerformance() {
        return new Promise((resolve) => {
            const carousel = document.getElementById('testimonial-carousel');
            const nextBtn = carousel?.querySelector('.next');
            
            if (!nextBtn) {
                resolve({
                    test: 'Carousel Performance',
                    result: 'SKIPPED',
                    reason: 'Carousel not found'
                });
                return;
            }
            
            const transitionTimes = [];
            let testCount = 0;
            const maxTests = 5;
            
            const testTransition = () => {
                if (testCount >= maxTests) {
                    const avgTransition = transitionTimes.reduce((a, b) => a + b, 0) / transitionTimes.length;
                    
                    resolve({
                        test: 'Carousel Performance',
                        averageTransitionTime: Math.round(avgTransition),
                        target: 400,
                        passed: avgTransition <= 400,
                        details: `Carousel transitions averaged ${Math.round(avgTransition)}ms`
                    });
                    return;
                }
                
                const startTime = performance.now();
                nextBtn.click();
                
                // Measure transition completion time
                setTimeout(() => {
                    const transitionTime = performance.now() - startTime;
                    transitionTimes.push(transitionTime);
                    testCount++;
                    
                    setTimeout(testTransition, 200);
                }, 400); // Wait for transition to complete
            };
            
            testTransition();
        });
    }

    async testMemoryLeaks() {
        return new Promise((resolve) => {
            if (!performance.memory) {
                resolve({
                    test: 'Memory Leak Detection',
                    result: 'SKIPPED',
                    reason: 'Memory API not available'
                });
                return;
            }
            
            const initialMemory = performance.memory.usedJSHeapSize;
            
            // Simulate heavy interaction
            const triggerInteractions = () => {
                for (let i = 0; i < 100; i++) {
                    const event = new MouseEvent('click', { bubbles: true });
                    document.dispatchEvent(event);
                }
            };
            
            // Run interactions multiple times
            for (let i = 0; i < 10; i++) {
                setTimeout(triggerInteractions, i * 100);
            }
            
            // Check memory after interactions
            setTimeout(() => {
                const finalMemory = performance.memory.usedJSHeapSize;
                const memoryIncrease = (finalMemory - initialMemory) / 1048576; // MB
                
                resolve({
                    test: 'Memory Leak Detection',
                    memoryIncrease: Math.round(memoryIncrease * 100) / 100,
                    target: 5,
                    passed: memoryIncrease <= 5,
                    details: `Memory usage increased by ${Math.round(memoryIncrease * 100) / 100}MB during stress test`
                });
            }, 2000);
        });
    }

    async testAccessibilityPerformance() {
        return new Promise((resolve) => {
            const issues = [];
            
            // Test focus indicators
            const focusableElements = document.querySelectorAll('button, input, select, a, [tabindex]');
            const focusIndicators = Array.from(focusableElements).filter(el => {
                const styles = getComputedStyle(el);
                return styles.outline !== 'none' && styles.outline !== '0px';
            });
            
            if (focusIndicators.length === 0) {
                issues.push('No focus indicators found');
            }
            
            // Test ARIA labels
            const interactiveElements = document.querySelectorAll('button[aria-label], input[aria-label]');
            if (interactiveElements.length < 3) {
                issues.push('Insufficient ARIA labels');
            }
            
            // Test reduced motion support
            const reducedMotionSupported = CSS.supports('(prefers-reduced-motion: reduce)');
            if (!reducedMotionSupported) {
                issues.push('Reduced motion not supported');
            }
            
            resolve({
                test: 'Accessibility Performance',
                issues: issues,
                passed: issues.length === 0,
                details: issues.length === 0 ? 'All accessibility checks passed' : `Found ${issues.length} issues: ${issues.join(', ')}`
            });
        });
    }

    displayBenchmarkResults(results) {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 20000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        `;
        
        const content = document.createElement('div');
        content.style.cssText = `
            background: white;
            padding: 30px;
            border-radius: 12px;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        `;
        
        let html = `
            <h2 style="margin-top: 0;">Performance Benchmark Results</h2>
            <p><strong>Test Duration:</strong> ${Math.round(results.testDuration)}ms</p>
            <p><strong>Timestamp:</strong> ${results.timestamp}</p>
            
            <div style="margin: 20px 0;">
                <h3>Test Results:</h3>
        `;
        
        results.tests.forEach(test => {
            const status = test.passed ? '✅ PASS' : '❌ FAIL';
            const color = test.passed ? '#10b981' : '#ef4444';
            
            html += `
                <div style="margin: 10px 0; padding: 15px; border-left: 4px solid ${color}; background: #f9fafb;">
                    <div style="font-weight: bold;">${test.test} ${status}</div>
                    <div style="margin-top: 5px; color: #6b7280;">${test.details}</div>
                </div>
            `;
        });
        
        html += `
            </div>
            <button id="close-results" style="background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">Close</button>
            <button id="copy-results" style="background: #6b7280; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; margin-left: 10px;">Copy Results</button>
        `;
        
        content.innerHTML = html;
        modal.appendChild(content);
        document.body.appendChild(modal);
        
        // Event listeners
        modal.querySelector('#close-results').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        modal.querySelector('#copy-results').addEventListener('click', () => {
            navigator.clipboard.writeText(JSON.stringify(results, null, 2));
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
    }

    updateDisplay(metric, value) {
        const display = document.getElementById(`${metric}-display`);
        if (!display) return;
        
        const span = display.querySelector('span');
        if (!span) return;
        
        const benchmark = metric === 'lcp' || metric === 'fid' 
            ? this.benchmarks.coreWebVitals[metric] 
            : this.benchmarks[metric];
        
        let color = '#10b981'; // Green
        let text = '';
        
        switch (metric) {
            case 'fps':
                text = `${value}fps`;
                color = value >= 55 ? '#10b981' : value >= 30 ? '#f59e0b' : '#ef4444';
                break;
            case 'response':
                text = `${value}ms`;
                color = value <= 100 ? '#10b981' : value <= 200 ? '#f59e0b' : '#ef4444';
                break;
            case 'memory':
                text = `${value}MB`;
                color = value <= 30 ? '#10b981' : value <= 50 ? '#f59e0b' : '#ef4444';
                break;
            case 'lcp':
                text = `${value}ms`;
                color = value <= 2500 ? '#10b981' : value <= 4000 ? '#f59e0b' : '#ef4444';
                break;
            case 'fid':
                text = `${value}ms`;
                color = value <= 100 ? '#10b981' : value <= 300 ? '#f59e0b' : '#ef4444';
                break;
            case 'cls':
                text = value.toFixed(3);
                color = value <= 0.1 ? '#10b981' : value <= 0.25 ? '#f59e0b' : '#ef4444';
                break;
        }
        
        span.textContent = text;
        span.style.color = color;
    }

    updateAllDisplays() {
        this.updateDisplay('fps', this.benchmarks.frameRate.current);
        this.updateDisplay('response', this.benchmarks.interactionResponse.current);
        this.updateDisplay('memory', this.benchmarks.memoryUsage.current);
        this.updateDisplay('lcp', this.benchmarks.coreWebVitals.lcp.current);
        this.updateDisplay('fid', this.benchmarks.coreWebVitals.fid.current);
        this.updateDisplay('cls', this.benchmarks.coreWebVitals.cls.current);
    }

    exportResults() {
        const exportData = {
            timestamp: new Date().toISOString(),
            benchmarks: this.benchmarks,
            testResults: this.testResults,
            userAgent: navigator.userAgent,
            viewport: `${window.innerWidth}x${window.innerHeight}`,
            deviceMemory: navigator.deviceMemory || 'unknown',
            hardwareConcurrency: navigator.hardwareConcurrency || 'unknown'
        };
        
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `performance-benchmark-${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        URL.revokeObjectURL(url);
    }

    // Public API
    getBenchmarks() {
        return this.benchmarks;
    }

    getTestResults() {
        return this.testResults;
    }

    isRunning() {
        return this.running;
    }
}

// Initialize performance benchmark
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.performanceBenchmark = new PerformanceBenchmark();
    });
} else {
    window.performanceBenchmark = new PerformanceBenchmark();
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceBenchmark;
}