/**
 * PaddleCoach - Main JavaScript Application
 * Author: Rakshit
 * Description: Core frontend functionality and utilities
 */

// Global application state
const PaddleCoach = {
    currentUser: null,
    currentMatch: null,
    socket: null,
    
    // Initialize the application
    init() {
        console.log('🏓 PaddleCoach initialized');
        this.setupEventListeners();
        this.checkAuthStatus();
    },
    
    // Setup global event listeners
    setupEventListeners() {
        // Handle navigation active states
        this.updateActiveNav();
        
        // Handle responsive menu (if needed)
        this.setupMobileMenu();
    },
    
    // Update active navigation link
    updateActiveNav() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-links a');
        
        navLinks.forEach(link => {
            const linkPath = new URL(link.href).pathname;
            if (linkPath === currentPath) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    },
    
    // Setup mobile menu toggle
    setupMobileMenu() {
        // Placeholder for mobile menu functionality
        // Will be implemented when needed
    },
    
    // Check authentication status
    checkAuthStatus() {
        // Placeholder for auth check
        // Will integrate with backend auth system
    },
    
    // Utility: Show notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type} fade-in`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'success' ? 'var(--secondary-color)' : type === 'error' ? 'var(--danger-color)' : 'var(--primary-color)'};
            color: white;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            z-index: 10000;
            max-width: 300px;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },
    
    // Utility: Format timestamp
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    },
    
    // Utility: Format date
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    },
    
    // API call wrapper
    async apiCall(endpoint, options = {}) {
        try {
            const response = await fetch(endpoint, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'API call failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            this.showNotification(error.message, 'error');
            throw error;
        }
    },
    
    // Load match data
    async loadMatchData(matchId) {
        try {
            const data = await this.apiCall(`/api/match/${matchId}`);
            this.currentMatch = data.data;
            return data.data;
        } catch (error) {
            console.error('Failed to load match data:', error);
            return null;
        }
    },
    
    // Load player stats
    async loadPlayerStats(playerId) {
        try {
            const data = await this.apiCall(`/api/player/${playerId}/stats`);
            return data.data;
        } catch (error) {
            console.error('Failed to load player stats:', error);
            return null;
        }
    },
    
    // Load coaching insights
    async loadCoachingInsights(playerId) {
        try {
            const data = await this.apiCall(`/api/coaching/insights/${playerId}`);
            return data.data;
        } catch (error) {
            console.error('Failed to load coaching insights:', error);
            return null;
        }
    }
};

// Animation utilities
const AnimationUtils = {
    // Fade in elements on scroll
    fadeInOnScroll() {
        const elements = document.querySelectorAll('.fade-in-scroll');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        elements.forEach(el => observer.observe(el));
    },
    
    // Count up animation for numbers
    countUp(element, end, duration = 1000) {
        const start = 0;
        const increment = end / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                element.textContent = Math.round(end);
                clearInterval(timer);
            } else {
                element.textContent = Math.round(current);
            }
        }, 16);
    },
    
    // Pulse animation
    pulse(element) {
        element.classList.add('pulse');
        setTimeout(() => element.classList.remove('pulse'), 2000);
    }
};

// Form validation utilities
const FormUtils = {
    // Validate email
    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },
    
    // Validate required fields
    validateRequired(formElement) {
        const requiredFields = formElement.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('error');
                isValid = false;
            } else {
                field.classList.remove('error');
            }
        });
        
        return isValid;
    }
};

// Local storage utilities
const StorageUtils = {
    // Save data
    save(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    },
    
    // Load data
    load(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error('Storage error:', error);
            return null;
        }
    },
    
    // Remove data
    remove(key) {
        localStorage.removeItem(key);
    },
    
    // Clear all data
    clear() {
        localStorage.clear();
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    PaddleCoach.init();
    AnimationUtils.fadeInOnScroll();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PaddleCoach, AnimationUtils, FormUtils, StorageUtils };
}
