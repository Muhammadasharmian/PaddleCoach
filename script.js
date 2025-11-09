// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background change on scroll
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.08)';
    } else {
        navbar.style.background = 'white';
        navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.05)';
    }
    
    lastScroll = currentScroll;
});

// Intersection Observer for animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards and sections
const animateElements = document.querySelectorAll('.step-card, .feature-card, .tech-card, .module-card');
animateElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'all 0.6s ease-out';
    observer.observe(el);
});

// Button click animations
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', function(e) {
        // Create ripple effect
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
});

// Add ripple effect CSS dynamically
const style = document.createElement('style');
style.textContent = `
    button {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    
    // Only apply parallax effect when user is NOT logged in
    if (hero && !isUserLoggedIn()) {
        // Only apply parallax when scrolled is low to avoid making it invisible
        hero.style.transform = `translateY(${scrolled * 0.3}px)`;
        // Keep minimum opacity at 0.3 to ensure it's always visible
        const newOpacity = Math.max(0.3, 1 - scrolled / 700);
        hero.style.opacity = newOpacity;
    } else if (hero && isUserLoggedIn()) {
        // When logged in, apply fade in/out effect based on visibility
        const heroRect = hero.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        
        // Calculate how much of the hero is visible
        const heroTop = heroRect.top;
        const heroBottom = heroRect.bottom;
        const heroHeight = heroRect.height;
        
        let opacity = 0;
        
        // Fade in as hero comes into view from bottom
        if (heroTop < windowHeight && heroTop > windowHeight - heroHeight) {
            // Element is entering from bottom
            const visibleAmount = windowHeight - heroTop;
            opacity = Math.min(1, visibleAmount / (heroHeight * 0.5));
        }
        // Full opacity when hero is in the middle of viewport
        else if (heroTop <= windowHeight - heroHeight && heroBottom >= heroHeight) {
            opacity = 1;
        }
        // Fade out as hero exits from top
        else if (heroBottom > 0 && heroBottom < heroHeight) {
            // Element is exiting from top
            opacity = Math.max(0, heroBottom / (heroHeight * 0.5));
        }
        // Fully visible when completely in viewport
        else if (heroTop >= 0 && heroBottom <= windowHeight) {
            opacity = 1;
        }
        
        hero.style.transform = 'translateY(0)';
        hero.style.opacity = opacity;
        hero.style.transition = 'opacity 0.3s ease';
    }
});

// Counter animation for statistics
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

// Dynamic text highlighting
const highlights = document.querySelectorAll('.highlight');
highlights.forEach(highlight => {
    highlight.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.05)';
        this.style.display = 'inline-block';
    });
    
    highlight.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});

// Progress bar animation for stat bars
const statBars = document.querySelectorAll('.stat-bar');
const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'grow 1.5s ease-out forwards';
        }
    });
}, { threshold: 0.5 });

statBars.forEach(bar => statObserver.observe(bar));

// Mobile menu toggle (for future implementation)
const createMobileMenu = () => {
    const navContent = document.querySelector('.nav-content');
    const menuButton = document.createElement('button');
    menuButton.className = 'mobile-menu-button';
    menuButton.innerHTML = '<i class="fas fa-bars"></i>';
    menuButton.style.display = 'none';
    
    const checkWidth = () => {
        if (window.innerWidth <= 768) {
            menuButton.style.display = 'block';
        } else {
            menuButton.style.display = 'none';
        }
    };
    
    window.addEventListener('resize', checkWidth);
    checkWidth();
    
    navContent.appendChild(menuButton);
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('PaddleCoach website loaded successfully!');
    createMobileMenu();
});

// Add loading animation
window.addEventListener('load', () => {
    // Only apply fade-in if not already visible
    if (document.body.style.opacity === '' || document.body.style.opacity === '1') {
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.5s ease-in';
        setTimeout(() => {
            document.body.style.opacity = '1';
        }, 100);
    }
});

// Tech card hover effects
document.querySelectorAll('.tech-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        const icon = this.querySelector('.tech-icon i');
        if (icon) {
            icon.style.transform = 'rotate(360deg) scale(1.2)';
            icon.style.transition = 'transform 0.5s ease';
        }
    });
    
    card.addEventListener('mouseleave', function() {
        const icon = this.querySelector('.tech-icon i');
        if (icon) {
            icon.style.transform = 'rotate(0deg) scale(1)';
        }
    });
});

// Module card interactions
document.querySelectorAll('.module-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.borderColor = 'var(--secondary-purple)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.borderColor = 'rgba(124, 58, 237, 0.2)';
    });
});

// ==================== //
// Authentication Modals //
// ==================== //

// Function to update chatbot greeting based on login state
function updateChatbotGreeting() {
    const greetingElement = document.getElementById('chatbotGreeting');
    if (greetingElement) {
        if (isUserLoggedIn()) {
            greetingElement.textContent = "Hi! I'm your Match Analysis AI. I can help you understand your table tennis match statistics. Ask me anything about your performance!";
        } else {
            greetingElement.textContent = "Hi! I'm PaddleCoach AI. I can help you learn about our platform and features. Sign up or log in to get personalized match analysis!";
        }
    }
}

// Function to clear chatbot conversation
function clearChatbotConversation() {
    // Clear conversation history
    conversationHistory = [];
    
    // Clear all messages except the greeting
    const chatbotMessages = document.getElementById('chatbotMessages');
    if (chatbotMessages) {
        // Remove all messages
        chatbotMessages.innerHTML = '';
        
        // Add back the greeting message
        const greetingDiv = document.createElement('div');
        greetingDiv.className = 'chatbot-message bot-message';
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.id = 'chatbotGreeting';
        greetingDiv.appendChild(contentDiv);
        chatbotMessages.appendChild(greetingDiv);
        
        // Update greeting based on login state
        updateChatbotGreeting();
    }
    
    // Clear input field
    const chatbotInput = document.getElementById('chatbotInput');
    if (chatbotInput) {
        chatbotInput.value = '';
    }
    
    // Stop any ongoing speech
    if (typeof stopSpeaking === 'function') {
        stopSpeaking();
    }
    
    // Turn off microphone if it's on
    if (isListening && recognition) {
        try {
            recognition.stop();
        } catch (e) {
            console.warn('Could not stop recognition:', e);
        }
        isListening = false;
        if (typeof updateMicButton === 'function') {
            updateMicButton();
        }
    }
}

// Function to hide authentication buttons
function hideAuthButtons() {
    const navButtons = document.querySelector('.nav-buttons');
    const userMenu = document.querySelector('.user-menu');
    const heroSection = document.querySelector('.hero');
    
    if (navButtons) {
        navButtons.style.display = 'none';
    }
    if (userMenu) {
        userMenu.style.display = 'flex';
        // Update user name if available
        const userName = localStorage.getItem('userName');
        const userNameSpan = document.querySelector('.user-name');
        if (userName && userNameSpan) {
            userNameSpan.textContent = userName;
        }
    }
    
    // Move hero section (landing image) between core-features and steps when logged in
    if (heroSection && !sectionsReordered) {
        const coreFeatures = document.getElementById('core-features');
        const stepsSection = document.querySelector('.steps');
        
        if (coreFeatures && stepsSection) {
            // Show hero section
            heroSection.style.display = 'flex';
            
            // Insert hero section after core-features (before steps)
            stepsSection.parentNode.insertBefore(heroSection, stepsSection);
        }
    }
    
    // Hide CTA banner when logged in
    const ctaBanner = document.getElementById('ctaBanner');
    if (ctaBanner) {
        ctaBanner.style.display = 'none';
    }
    
    // Move Core Features section above where Hero was
    moveCoreFeaturesToTop();
}

// Function to show authentication buttons
function showAuthButtons() {
    const navButtons = document.querySelector('.nav-buttons');
    const userMenu = document.querySelector('.user-menu');
    const heroSection = document.querySelector('.hero');
    
    if (navButtons) {
        navButtons.style.display = 'flex';
    }
    if (userMenu) {
        userMenu.style.display = 'none';
    }
    
    // Move hero section back to its original position (before steps) when logged out
    if (heroSection) {
        const stepsSection = document.querySelector('.steps');
        
        if (stepsSection) {
            // Show hero section
            heroSection.style.display = 'flex';
            
            // Insert hero section before steps (original position)
            stepsSection.parentNode.insertBefore(heroSection, stepsSection);
        }
    }
    
    // Show CTA banner when logged out
    const ctaBanner = document.getElementById('ctaBanner');
    if (ctaBanner) {
        ctaBanner.style.display = 'block';
    }
    
    // Move Core Features back to original position
    moveCoreFeaturesToOriginal();
}

// Flag to track if sections have been moved
let sectionsReordered = false;

// Function to move Core Features section to top (after nav, before hero)
function moveCoreFeaturesToTop() {
    if (sectionsReordered) {
        console.log('Sections already reordered, skipping');
        return;
    }
    
    const coreFeatures = document.getElementById('core-features');
    const heroSection = document.querySelector('.hero');
    
    if (!coreFeatures) {
        console.error('Core Features section not found');
        return;
    }
    if (!heroSection) {
        console.error('Hero section not found');
        return;
    }
    
    // Check if core features is already before hero
    const heroParent = heroSection.parentElement;
    const coreParent = coreFeatures.parentElement;
    
    if (heroParent === coreParent) {
        const allSections = Array.from(heroParent.children);
        const heroIndex = allSections.indexOf(heroSection);
        const coreIndex = allSections.indexOf(coreFeatures);
        
        // If core features is already before hero, don't move
        if (coreIndex < heroIndex) {
            console.log('Core Features already before Hero');
            sectionsReordered = true;
            // Ensure hero is visible
            heroSection.style.opacity = '1';
            heroSection.style.transform = 'translateY(0)';
            return;
        }
    }
    
    // Move core features before hero
    console.log('Moving Core Features before Hero');
    heroSection.parentNode.insertBefore(coreFeatures, heroSection);
    sectionsReordered = true;
    
    // Ensure hero section is visible after moving
    heroSection.style.opacity = '1';
    heroSection.style.transform = 'translateY(0)';
}

// Function to move Core Features section back to original position (after Coming Soon)
function moveCoreFeaturesToOriginal() {
    sectionsReordered = false;
    
    const coreFeatures = document.getElementById('core-features');
    const comingSoon = document.querySelector('.coming-soon');
    const features = document.getElementById('features');
    
    if (!coreFeatures || !features) {
        console.error('Required sections not found for moving back');
        return;
    }
    
    console.log('Moving Core Features back to original position');
    // Move it before Features section (which puts it after Coming Soon)
    features.parentNode.insertBefore(coreFeatures, features);
}

// Check login state on page load
function checkLoginState() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (isLoggedIn === 'true') {
        hideAuthButtons();
    } else {
        showAuthButtons();
    }
    // Update chatbot greeting based on login state
    updateChatbotGreeting();
}

// Ensure DOM is fully loaded before checking login state
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkLoginState);
} else {
    // DOM is already loaded
    checkLoginState();
}

// Get modal elements
const signupModal = document.getElementById('signupModal');
const loginModal = document.getElementById('loginModal');
const verificationModal = document.getElementById('verificationModal');

// Get button elements
const signupButtons = document.querySelectorAll('.btn-signup');
const loginButtons = document.querySelectorAll('.btn-login');

// Get close buttons
const closeButtons = document.querySelectorAll('.close');

// Get switch links
const switchLinks = document.querySelectorAll('.switch-link');

// Store user data temporarily
let tempUserData = {};
let generatedVerificationCode = '';

// Password toggle functionality
document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const passwordInput = document.getElementById(targetId);
        const icon = this.querySelector('i');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    });
});

// Password validation for signup
const signupPasswordInput = document.getElementById('signupPassword');
const requirements = {
    length: document.getElementById('req-length'),
    uppercase: document.getElementById('req-uppercase'),
    lowercase: document.getElementById('req-lowercase'),
    number: document.getElementById('req-number')
};

signupPasswordInput.addEventListener('input', function() {
    const password = this.value;
    
    // Check length (at least 8 characters)
    if (password.length >= 8) {
        requirements.length.classList.add('valid');
    } else {
        requirements.length.classList.remove('valid');
    }
    
    // Check for uppercase letter
    if (/[A-Z]/.test(password)) {
        requirements.uppercase.classList.add('valid');
    } else {
        requirements.uppercase.classList.remove('valid');
    }
    
    // Check for lowercase letter
    if (/[a-z]/.test(password)) {
        requirements.lowercase.classList.add('valid');
    } else {
        requirements.lowercase.classList.remove('valid');
    }
    
    // Check for number
    if (/[0-9]/.test(password)) {
        requirements.number.classList.add('valid');
    } else {
        requirements.number.classList.remove('valid');
    }
});

// Validate password strength
function validatePassword(password) {
    const hasLength = password.length >= 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    
    return hasLength && hasUppercase && hasLowercase && hasNumber;
}

// Open Sign Up Modal
signupButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        signupModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
});

// Open Login Modal
loginButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        loginModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
});

// Close modals
closeButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modalId = button.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    });
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === signupModal) {
        signupModal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
    if (e.target === loginModal) {
        loginModal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
    if (e.target === verificationModal) {
        verificationModal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
});

// Switch between modals
switchLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetModal = link.getAttribute('data-switch');
        
        // Close all modals
        signupModal.classList.remove('active');
        loginModal.classList.remove('active');
        
        // Open target modal
        document.getElementById(targetModal).classList.add('active');
    });
});

// Handle Sign Up Form Submission
document.getElementById('signupForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;
    
    // Validate password strength
    if (!validatePassword(password)) {
        alert('Password does not meet all requirements! Please ensure it has:\n- At least 8 characters\n- One uppercase letter\n- One lowercase letter\n- One number');
        return;
    }
    
    // Check password match
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }
    
    // Store user data temporarily
    tempUserData = { name, email, password };
    
    // Generate 6-digit verification code
    generatedVerificationCode = Math.floor(100000 + Math.random() * 900000).toString();
    
    // Simulate sending email (in production, this would be a backend API call)
    console.log('Sending verification code to:', email);
    console.log('Verification Code:', generatedVerificationCode);
    
    // Show success message
    alert(`Verification code sent to ${email}\n\nFor demo purposes, your code is: ${generatedVerificationCode}`);
    
    // Close signup modal and open verification modal
    signupModal.classList.remove('active');
    verificationModal.classList.add('active');
    
    // Display email in verification modal
    document.querySelector('.verification-email').textContent = email;
    
    // Reset signup form but keep validation indicators
    e.target.reset();
    Object.values(requirements).forEach(req => req.classList.remove('valid'));
});

// Handle Login Form Submission
document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    
    // Here you would typically send data to your backend
    console.log('Login Data:', { email, password, rememberMe });
    alert('Login successful! Welcome back!');
    
    // Set logged in state
    localStorage.setItem('isLoggedIn', 'true');
    localStorage.setItem('userEmail', email);
    
    // Hide login/signup buttons
    hideAuthButtons();
    
    // Clear chatbot conversation and update greeting
    clearChatbotConversation();
    
    // Close modal and reset form
    loginModal.classList.remove('active');
    document.body.style.overflow = 'auto';
    e.target.reset();
});

// Social login buttons (placeholder functionality)
document.querySelectorAll('.google-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        alert('Google Sign-In would be implemented here using OAuth');
        // In production, you would integrate with Google OAuth API
    });
});

document.querySelectorAll('.facebook-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        alert('Facebook Sign-In would be implemented here using OAuth');
        // In production, you would integrate with Facebook OAuth API
    });
});

// ==================== //
// Email Verification //
// ==================== //

// Auto-focus and auto-advance for verification code inputs
const codeDigits = document.querySelectorAll('.code-digit');

codeDigits.forEach((digit, index) => {
    // Move to next input on input
    digit.addEventListener('input', (e) => {
        const value = e.target.value;
        
        // Only allow numbers
        if (!/^\d$/.test(value)) {
            e.target.value = '';
            return;
        }
        
        // Move to next input if available
        if (value && index < codeDigits.length - 1) {
            codeDigits[index + 1].focus();
        }
    });
    
    // Handle backspace
    digit.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && !e.target.value && index > 0) {
            codeDigits[index - 1].focus();
        }
    });
    
    // Handle paste
    digit.addEventListener('paste', (e) => {
        e.preventDefault();
        const pastedData = e.clipboardData.getData('text').slice(0, 6);
        
        if (/^\d+$/.test(pastedData)) {
            pastedData.split('').forEach((char, i) => {
                if (codeDigits[i]) {
                    codeDigits[i].value = char;
                }
            });
            
            // Focus last filled digit
            const lastIndex = Math.min(pastedData.length - 1, 5);
            codeDigits[lastIndex].focus();
        }
    });
});

// Handle verification form submission
document.getElementById('verificationForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Get entered code
    const enteredCode = Array.from(codeDigits).map(digit => digit.value).join('');
    
    // Validate code
    if (enteredCode.length !== 6) {
        alert('Please enter the complete 6-digit code');
        return;
    }
    
    if (enteredCode === generatedVerificationCode) {
        // Verification successful
        console.log('User verified:', tempUserData);
        alert('Email verified successfully! Welcome to PaddleCoach!');
        
        // Set logged in state
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('userEmail', tempUserData.email);
        localStorage.setItem('userName', tempUserData.name);
        
        // Hide login/signup buttons
        hideAuthButtons();
        
        // Clear chatbot conversation and update greeting
        clearChatbotConversation();
        
        // Close verification modal
        verificationModal.classList.remove('active');
        document.body.style.overflow = 'auto';
        
        // Clear verification inputs
        codeDigits.forEach(digit => digit.value = '');
        
        // Clear temp data
        tempUserData = {};
        generatedVerificationCode = '';
        
        // In production, you would:
        // 1. Send verified user data to backend
        // 2. Create user account
        // 3. Log user in
        // 4. Redirect to dashboard
    } else {
        // Verification failed
        alert('Invalid verification code. Please try again.');
        codeDigits.forEach(digit => {
            digit.value = '';
            digit.style.borderColor = '#EF4444';
        });
        codeDigits[0].focus();
        
        // Reset border color after 1 second
        setTimeout(() => {
            codeDigits.forEach(digit => digit.style.borderColor = '#E2E8F0');
        }, 1000);
    }
});

// Resend verification code
let resendTimer = null;
document.getElementById('resendCode').addEventListener('click', function() {
    // Disable button temporarily
    this.disabled = true;
    this.textContent = 'Code Sent!';
    
    // Generate new code
    generatedVerificationCode = Math.floor(100000 + Math.random() * 900000).toString();
    
    // Simulate sending email
    console.log('Resending verification code to:', tempUserData.email);
    console.log('New Verification Code:', generatedVerificationCode);
    
    alert(`New verification code sent!\n\nFor demo purposes, your code is: ${generatedVerificationCode}`);
    
    // Re-enable after 30 seconds
    let countdown = 30;
    this.textContent = `Resend in ${countdown}s`;
    
    resendTimer = setInterval(() => {
        countdown--;
        if (countdown > 0) {
            this.textContent = `Resend in ${countdown}s`;
        } else {
            clearInterval(resendTimer);
            this.disabled = false;
            this.textContent = 'Resend Code';
        }
    }, 1000);
});

// ==================== //
// User Menu & Logout //
// ==================== //

// Toggle user dropdown
const userMenuButton = document.querySelector('.btn-user-menu');
const userDropdown = document.querySelector('.user-dropdown');

if (userMenuButton && userDropdown) {
    userMenuButton.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('active');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.user-menu')) {
            userDropdown.classList.remove('active');
        }
    });
}

// Handle logout
const logoutButton = document.querySelector('.btn-logout');
if (logoutButton) {
    logoutButton.addEventListener('click', () => {
        // Clear login state
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userName');
        
        // Show auth buttons again
        showAuthButtons();
        
        // Clear chatbot conversation and update greeting
        clearChatbotConversation();
        
        // Close dropdown
        if (userDropdown) {
            userDropdown.classList.remove('active');
        }
        
        alert('You have been logged out successfully!');
    });
}

// Handle Upload Match Video button - Open Modal
const uploadMatchVideoBtn = document.getElementById('uploadMatchVideoBtn');
const uploadVideoModal = document.getElementById('uploadVideoModal');
const closeUploadModal = document.getElementById('closeUploadModal');
const uploadMatchVideo = document.getElementById('uploadMatchVideo');
const matchVideoInput = document.getElementById('matchVideoInput');

// Store selected video file temporarily
let selectedMatchVideo = null;

if (uploadMatchVideoBtn && uploadVideoModal) {
    // Open modal when clicking Upload Match Video button
    uploadMatchVideoBtn.addEventListener('click', () => {
        uploadVideoModal.classList.add('active');
    });
    
    // Close modal
    if (closeUploadModal) {
        closeUploadModal.addEventListener('click', () => {
            uploadVideoModal.classList.remove('active');
        });
    }
    
    // Close modal when clicking outside
    uploadVideoModal.addEventListener('click', (e) => {
        if (e.target === uploadVideoModal) {
            uploadVideoModal.classList.remove('active');
        }
    });
    
    // Handle Match Video Upload
    if (uploadMatchVideo && matchVideoInput) {
        uploadMatchVideo.addEventListener('click', () => {
            matchVideoInput.click();
        });
        
        matchVideoInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                console.log('Match video selected:', file.name);
                selectedMatchVideo = file;
                
                // Show upload progress
                showUploadProgress(file);
                
                // Process video after upload
                processVideo();
            }
        });
    }
}

// Show upload progress for selected video
function showUploadProgress(file) {
    const card = uploadMatchVideo;
    const fileName = file.name;
    const fileSize = (file.size / (1024 * 1024)).toFixed(2);
    
    // Add uploaded class to card
    card.classList.add('uploaded');
    
    // Update card content to show upload status
    card.innerHTML = `
        <div class="upload-option-icon" style="background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);">
            <i class="fas fa-check"></i>
        </div>
        <h3>Match Video Uploaded</h3>
        <p><strong>${fileName}</strong></p>
        <p style="font-size: 0.85rem; color: #64748B;">${fileSize} MB</p>
        <div class="upload-progress-bar">
            <div class="upload-progress-fill"></div>
        </div>
    `;
    
    // Simulate upload progress animation
    const progressFill = card.querySelector('.upload-progress-fill');
    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        if (progressFill) {
            progressFill.style.width = progress + '%';
        }
        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 50);
}

// IndexedDB helper functions for storing video files
function saveVideoToIndexedDB(name, file) {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('VideoDatabase', 1);
        
        request.onerror = () => reject(request.error);
        
        request.onsuccess = () => {
            const db = request.result;
            const transaction = db.transaction(['videos'], 'readwrite');
            const store = transaction.objectStore('videos');
            const putRequest = store.put({ name: name, file: file });
            
            putRequest.onsuccess = () => {
                console.log(`✓ ${name} saved to IndexedDB`);
                resolve();
            };
            putRequest.onerror = () => reject(putRequest.error);
        };
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('videos')) {
                db.createObjectStore('videos', { keyPath: 'name' });
            }
        };
    });
}

// Process uploaded video and redirect to comparison page
function processVideo() {
    if (selectedMatchVideo) {
        // Wait for upload animations to complete
        setTimeout(async () => {
            // Show loading message
            const loadingMsg = document.createElement('div');
            loadingMsg.id = 'videoLoadingMsg';
            loadingMsg.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); z-index: 10002; text-align: center;';
            loadingMsg.innerHTML = '<div style="font-size: 1.5rem; font-weight: 700; color: #7C3AED; margin-bottom: 1rem;">Preparing Videos...</div><div style="color: #64748B;">Processing your match video...</div>';
            document.body.appendChild(loadingMsg);
            
            // Close modal
            uploadVideoModal.classList.remove('active');
            
            console.log('Preparing video for comparison...');
            console.log('Match video size:', (selectedMatchVideo.size / (1024 * 1024)).toFixed(2), 'MB');
            
            try {
                // Store video file metadata
                sessionStorage.setItem('professionalVideoName', selectedMatchVideo.name);
                sessionStorage.setItem('yourVideoName', 'analyzed_video.mp4');
                sessionStorage.setItem('professionalVideoType', selectedMatchVideo.type);
                sessionStorage.setItem('yourVideoType', 'video/mp4');
                sessionStorage.setItem('videosReady', 'true');
                sessionStorage.setItem('useLocalAnalyzedVideo', 'true');
                
                // Save uploaded file to IndexedDB
                await saveVideoToIndexedDB('professional', selectedMatchVideo);
                
                console.log('✓ Video saved, redirecting...');
                
                // Redirect to comparison page
                setTimeout(() => {
                    window.location.href = 'video-comparison.html';
                }, 500);
                
            } catch (error) {
                console.error('Error saving video:', error);
                alert('Error preparing video for analysis. Please try again.');
                const msg = document.getElementById('videoLoadingMsg');
                if (msg) document.body.removeChild(msg);
            }
        }, 600); // Wait for progress bar animation
    }
}

// Function to check if user is logged in
function isUserLoggedIn() {
    return localStorage.getItem('isLoggedIn') === 'true';
}

// Function to show login prompt
function promptLogin() {
    const userChoice = confirm('You need to be logged in to access this feature.\n\nClick OK to Log In or Cancel to Sign Up.');
    if (userChoice) {
        // Open login modal
        const loginModal = document.getElementById('loginModal');
        if (loginModal) {
            loginModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    } else {
        // Open signup modal
        const signupModal = document.getElementById('signupModal');
        if (signupModal) {
            signupModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }
}

// Add click handlers to all feature buttons
document.addEventListener('DOMContentLoaded', () => {
    const featureButtons = document.querySelectorAll('.btn-showcase');
    const uploadMatchVideoBtn = document.getElementById('uploadMatchVideoBtn');
    
    featureButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            // Skip the upload button as it has its own handler
            if (button.id === 'uploadMatchVideoBtn') {
                if (!isUserLoggedIn()) {
                    e.preventDefault();
                    e.stopPropagation();
                    promptLogin();
                    return;
                }
                // If logged in, the modal handler above will take over
                return;
            }
            
            // Skip the Talk to Coach button as it has its own handler
            if (button.id === 'talkToCoachBtn') {
                return;
            }
            
            if (!isUserLoggedIn()) {
                e.preventDefault();
                e.stopPropagation();
                promptLogin();
            } else {
                // User is logged in, show feature coming soon message
                const buttonText = button.textContent.trim();
                alert(`${buttonText} feature will be available soon!\n\nThis feature is currently in development and will be implemented when the backend is ready.`);
            }
        });
    });
});

// Handle Start Training button - scroll to features section or prompt login
const startTrainingBtn = document.getElementById('startTrainingBtn');
if (startTrainingBtn) {
    startTrainingBtn.addEventListener('click', () => {
        if (isUserLoggedIn()) {
            const featuresSection = document.getElementById('core-features');
            if (featuresSection) {
                featuresSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        } else {
            promptLogin();
        }
    });
}

// Handle Watch Demo button
const watchDemoBtn = document.getElementById('watchDemoBtn');
if (watchDemoBtn) {
    watchDemoBtn.addEventListener('click', () => {
        if (isUserLoggedIn()) {
            const featuresSection = document.getElementById('core-features');
            if (featuresSection) {
                featuresSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        } else {
            promptLogin();
        }
    });
}

// Handle Start Now button
const startNowBtn = document.getElementById('startNowBtn');
if (startNowBtn) {
    startNowBtn.addEventListener('click', () => {
        if (isUserLoggedIn()) {
            const featuresSection = document.getElementById('core-features');
            if (featuresSection) {
                featuresSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        } else {
            promptLogin();
        }
    });
}

// Handle Train Now button
const trainNowBtn = document.getElementById('trainNowBtn');
if (trainNowBtn) {
    trainNowBtn.addEventListener('click', () => {
        if (isUserLoggedIn()) {
            const featuresSection = document.getElementById('core-features');
            if (featuresSection) {
                featuresSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        } else {
            promptLogin();
        }
    });
}

// Handle Get Started Now button
const getStartedNowBtn = document.getElementById('getStartedNowBtn');
if (getStartedNowBtn) {
    getStartedNowBtn.addEventListener('click', () => {
        if (isUserLoggedIn()) {
            // When logged in, scroll to features section
            const featuresSection = document.getElementById('core-features');
            if (featuresSection) {
                featuresSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        } else {
            // When not logged in, prompt to login or sign up
            promptLogin();
        }
    });
}

// ==================== //
// Chatbot Functionality //
// ==================== //

const GEMINI_API_KEY = 'AIzaSyBWi0BYuO1CB-J8lvcTmRX4b1JVZ2w-Pvs';
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent';

// Match analysis data (embedded from the text file)
const matchAnalysisData = `
PADDLECOACH - TABLE TENNIS BIOMECHANICAL ANALYSIS

Video: output_pose/dataDetection_annotated.mp4
Analysis Date: 2025-11-08 18:54:34
Processing FPS: 30
Total Frames Analyzed: 2431
Total Detections: 4769

Detected Players: Player_1, Player_2

SHOT DETECTION:S

Player_1: 157 total shots (104 Forehand, 53 Backhand)
Player_2: 151 total shots (94 Forehand, 57 Backhand)

BIOMECHANICAL METRICS:

Player_1:
- Avg Max Racket Velocity: 1706.90 px/s
- Avg Min Hip/Knee Angle: 151.07°
- Avg Min Elbow Angle: 112.88°
- Avg Center of Gravity Movement: 18.58 px

Player_2:
- Avg Max Racket Velocity: 1870.90 px/s
- Avg Min Hip/Knee Angle: 165.28°
- Avg Min Elbow Angle: 88.94°
- Avg Center of Gravity Movement: 18.63 px

PERFORMANCE COMPARISON:
Player_2 has 9.6% faster average racket speed.
`;

const chatbot = document.getElementById('chatbot');
const chatbotToggle = document.getElementById('chatbotToggle');
const chatbotClose = document.getElementById('chatbotClose');
const chatbotMessages = document.getElementById('chatbotMessages');
const chatbotInput = document.getElementById('chatbotInput');
const chatbotSend = document.getElementById('chatbotSend');

let conversationHistory = [];
let recognition = null;
let isListening = false;
let isSpeaking = false;
let autoSendTimeout = null;
let isVoiceInput = false; // Track if input was from voice
let shouldIgnoreRecognition = false; // Flag to ignore recognition while bot is speaking
let currentAudio = null; // Store reference to current playing audio
let manuallyStoppedAudio = false; // Flag to prevent fallback after manual stop

// Initialize Speech Recognition
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true; // Keep listening continuously
    recognition.interimResults = true; // Show interim results
    recognition.lang = 'en-US';
    
    recognition.onresult = (event) => {
        // Ignore results if bot is currently speaking
        if (shouldIgnoreRecognition || isSpeaking) {
            // Check if user said "stop" to interrupt the bot
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript.toLowerCase();
            }
            
            // Only stop if user explicitly says "stop" (not just any speech)
            if (event.results[event.results.length - 1].isFinal && transcript.trim().includes('stop')) {
                stopSpeaking();
            }
            // Don't update the input field or process the speech
            return;
        }
        
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        chatbotInput.value = transcript;
        
        // Mark as voice input
        isVoiceInput = true;
        
        // Clear existing timeout
        if (autoSendTimeout) {
            clearTimeout(autoSendTimeout);
        }
        
        // Auto-send after 2 seconds of silence (only for final results)
        if (event.results[event.results.length - 1].isFinal) {
            autoSendTimeout = setTimeout(() => {
                if (chatbotInput.value.trim() && !shouldIgnoreRecognition && !isSpeaking) {
                    sendMessage();
                }
            }, 2000); // 2 second pause
        }
    };
    
    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        // Don't stop listening on minor errors
        if (event.error !== 'no-speech' && event.error !== 'aborted' && event.error !== 'audio-capture') {
            console.warn('Speech recognition error that might require restart:', event.error);
        }
    };
    
    recognition.onend = () => {
        // Auto-restart recognition if still in listening mode
        if (isListening) {
            setTimeout(() => {
                if (isListening) {
                    try {
                        recognition.start();
                    } catch (e) {
                        console.warn('Could not restart recognition:', e);
                    }
                }
            }, 100);
        }
    };
}

// ElevenLabs Configuration
const ELEVENLABS_API_KEY = 'sk_58b691e7138d0e942b1e096150cc237631742c85f467b86f';
const ELEVENLABS_VOICE_ID = 'bPMKpgEe88vKSwusXTMU'; // Selected voice from library

// Initialize Speech Synthesis (fallback)
const synth = window.speechSynthesis;

// Function to stop speaking immediately
function stopSpeaking() {
    console.log('Stopping speech...');
    
    // Set flag to prevent fallback
    manuallyStoppedAudio = true;
    
    // Stop the stored audio reference
    if (currentAudio) {
        try {
            currentAudio.pause();
            currentAudio.currentTime = 0;
            currentAudio.src = '';
            currentAudio.remove();
            currentAudio = null;
        } catch (e) {
            console.warn('Error stopping current audio:', e);
        }
    }
    
    // Stop ElevenLabs audio by ID
    const existingAudio = document.getElementById('tts-audio');
    if (existingAudio) {
        try {
            existingAudio.pause();
            existingAudio.currentTime = 0;
            existingAudio.src = '';
            existingAudio.remove();
        } catch (e) {
            console.warn('Error stopping audio by ID:', e);
        }
    }
    
    // Also try to find any audio elements without the ID
    const allAudioElements = document.querySelectorAll('audio');
    allAudioElements.forEach(audio => {
        try {
            audio.pause();
            audio.currentTime = 0;
            audio.src = '';
            audio.remove();
        } catch (e) {
            console.warn('Error stopping audio element:', e);
        }
    });
    
    // Stop browser TTS
    if (synth.speaking) {
        synth.cancel();
    }
    
    // Reset flags
    isSpeaking = false;
    shouldIgnoreRecognition = false;
    
    // Update button
    updateMicButton();
    
    // Clear input
    if (chatbotInput) {
        chatbotInput.value = '';
    }
    
    console.log('Speech stopped, flags reset');
}

// Function to speak text using ElevenLabs
async function speakText(text) {
    // Reset the manual stop flag when starting new speech
    manuallyStoppedAudio = false;
    
    if (isSpeaking) {
        // Stop any currently playing audio
        const existingAudio = document.getElementById('tts-audio');
        if (existingAudio) {
            existingAudio.pause();
            existingAudio.remove();
        }
    }
    
    // Set flag to ignore speech recognition while bot is speaking
    // Don't stop the recognition, just ignore its results
    shouldIgnoreRecognition = true;
    isSpeaking = true;
    
    // Update mic button to show stop icon
    updateMicButton();
    
    // Clear the input field to prevent it from showing bot's speech
    if (isListening) {
        chatbotInput.value = '';
    }
    
    try {
        // Call ElevenLabs API
        const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${ELEVENLABS_VOICE_ID}`, {
            method: 'POST',
            headers: {
                'Accept': 'audio/mpeg',
                'Content-Type': 'application/json',
                'xi-api-key': ELEVENLABS_API_KEY
            },
            body: JSON.stringify({
                text: text,
                model_id: 'eleven_multilingual_v2',
                voice_settings: {
                    stability: 0.5,
                    similarity_boost: 0.75,
                    style: 0.0,
                    use_speaker_boost: true
                }
            })
        });
        
        if (!response.ok) {
            throw new Error('ElevenLabs API request failed');
        }
        
        // Convert response to blob and play
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        
        // Create and play audio element
        const audio = new Audio(audioUrl);
        audio.id = 'tts-audio';
        
        // Store reference globally so we can stop it
        currentAudio = audio;
        
        audio.onended = () => {
            isSpeaking = false;
            currentAudio = null;
            URL.revokeObjectURL(audioUrl);
            audio.remove();
            
            // Wait a bit before re-enabling recognition to avoid tail end
            setTimeout(() => {
                shouldIgnoreRecognition = false;
                chatbotInput.value = ''; // Clear any captured bot speech
                updateMicButton();
            }, 1000);
        };
        
        audio.onerror = () => {
            isSpeaking = false;
            currentAudio = null;
            console.error('Audio playback error');
            
            setTimeout(() => {
                shouldIgnoreRecognition = false;
                chatbotInput.value = '';
                updateMicButton();
            }, 1000);
            
            // Only fallback if not manually stopped
            if (!manuallyStoppedAudio) {
                console.log('Audio error - falling back to browser TTS');
                speakTextFallback(text);
            } else {
                console.log('Audio manually stopped - not falling back');
            }
        };
        
        await audio.play();
        
    } catch (error) {
        console.error('ElevenLabs TTS error:', error);
        isSpeaking = false;
        currentAudio = null;
        
        setTimeout(() => {
            shouldIgnoreRecognition = false;
            chatbotInput.value = '';
            updateMicButton();
        }, 1000);
        
        // Only fallback if not manually stopped
        if (!manuallyStoppedAudio) {
            console.log('ElevenLabs error - falling back to browser TTS');
            speakTextFallback(text);
        } else {
            console.log('Audio manually stopped - not falling back');
        }
    }
}

// Fallback to browser speech synthesis
function speakTextFallback(text) {
    // Set flag to ignore speech recognition while bot is speaking
    shouldIgnoreRecognition = true;
    isSpeaking = true;
    
    // Update mic button to show stop icon
    updateMicButton();
    
    // Clear the input field to prevent it from showing bot's speech
    if (isListening) {
        chatbotInput.value = '';
    }
    
    if (synth.speaking) {
        synth.cancel();
    }
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    
    // Try to use a natural voice
    const voices = synth.getVoices();
    const preferredVoice = voices.find(voice => 
        voice.name.includes('Natural') || 
        voice.name.includes('Premium') ||
        voice.lang.startsWith('en')
    );
    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }
    
    utterance.onstart = () => {
        isSpeaking = true;
        shouldIgnoreRecognition = true;
        updateMicButton();
    };
    
    utterance.onend = () => {
        isSpeaking = false;
        
        // Wait a bit before re-enabling recognition
        setTimeout(() => {
            shouldIgnoreRecognition = false;
            chatbotInput.value = ''; // Clear any captured bot speech
            updateMicButton();
        }, 1000);
    };
    
    synth.speak(utterance);
}

// Function to toggle voice input
function toggleVoiceInput() {
    if (!recognition) {
        alert('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
        return;
    }
    
    // If bot is speaking, stop it
    if (isSpeaking) {
        stopSpeaking();
        return;
    }
    
    // Otherwise toggle listening
    if (isListening) {
        recognition.stop();
        isListening = false;
    } else {
        recognition.start();
        isListening = true;
    }
    updateMicButton();
}

// Update microphone button appearance
function updateMicButton() {
    const micButton = document.getElementById('micButton');
    if (micButton) {
        if (isSpeaking) {
            // Show stop/circle icon when bot is speaking
            micButton.classList.add('speaking');
            micButton.classList.remove('listening');
            micButton.innerHTML = '<i class="fas fa-stop-circle"></i>';
        } else if (isListening) {
            micButton.classList.add('listening');
            micButton.classList.remove('speaking');
            micButton.innerHTML = '<i class="fas fa-microphone-slash"></i>';
        } else {
            micButton.classList.remove('listening', 'speaking');
            micButton.innerHTML = '<i class="fas fa-microphone"></i>';
        }
    }
}

// Toggle chatbot
if (chatbotToggle) {
    chatbotToggle.addEventListener('click', () => {
        chatbot.classList.toggle('active');
        if (chatbot.classList.contains('active')) {
            // Update greeting based on login state when opening
            updateChatbotGreeting();
            chatbotInput.focus();
        }
    });
}

// Handle "Talk to Coach" button click
const talkToCoachBtn = document.getElementById('talkToCoachBtn');
if (talkToCoachBtn) {
    talkToCoachBtn.addEventListener('click', () => {
        // Open the chatbot
        if (chatbot) {
            chatbot.classList.add('active');
            // Update greeting based on login state when opening
            updateChatbotGreeting();
            if (chatbotInput) {
                chatbotInput.focus();
            }
        }
    });
}

// Close chatbot
if (chatbotClose) {
    chatbotClose.addEventListener('click', () => {
        // Close the chatbot
        chatbot.classList.remove('active');
        
        // Stop any ongoing speech immediately
        stopSpeaking();
        
        // Turn off microphone if it's on
        if (isListening && recognition) {
            try {
                recognition.stop();
            } catch (e) {
                console.warn('Could not stop recognition:', e);
            }
            isListening = false;
        }
        
        // Clear any auto-send timeout
        if (autoSendTimeout) {
            clearTimeout(autoSendTimeout);
            autoSendTimeout = null;
        }
        
        // Clear input field
        chatbotInput.value = '';
        
        // Reset voice input flag
        isVoiceInput = false;
        
        // Update mic button to default state
        updateMicButton();
    });
}

// Send message function
async function sendMessage() {
    const message = chatbotInput.value.trim();
    if (!message) return;

    // Check if this was voice input
    const shouldSpeak = isVoiceInput;
    
    // Reset voice input flag
    isVoiceInput = false;

    // Clear auto-send timeout if exists
    if (autoSendTimeout) {
        clearTimeout(autoSendTimeout);
        autoSendTimeout = null;
    }

    // Add user message to chat
    addMessageToChat(message, 'user');
    chatbotInput.value = '';
    chatbotSend.disabled = true;

    // Show typing indicator
    const typingIndicator = showTypingIndicator();

    try {
        // Get AI response
        const response = await getGeminiResponse(message);
        
        // Remove typing indicator
        typingIndicator.remove();
        
        // Add bot response to chat
        addMessageToChat(response, 'bot');
        
        // Speak the response only if input was from voice
        if (shouldSpeak) {
            speakText(response);
        }
    } catch (error) {
        console.error('Error getting AI response:', error);
        typingIndicator.remove();
        // Show the actual error message for debugging
        const errorMessage = error.message || 'Sorry, I encountered an error. Please try again.';
        addMessageToChat(`Error: ${errorMessage}`, 'bot');
    }

    chatbotSend.disabled = false;
}

// Add message to chat
function addMessageToChat(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chatbot-message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    
    messageDiv.appendChild(contentDiv);
    chatbotMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    
    // Add to conversation history
    conversationHistory.push({
        role: sender === 'user' ? 'user' : 'model',
        parts: [{ text: message }]
    });
}

// Show typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chatbot-message bot-message';
    typingDiv.id = 'typing-indicator';
    
    const typingContent = document.createElement('div');
    typingContent.className = 'typing-indicator';
    typingContent.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    
    typingDiv.appendChild(typingContent);
    chatbotMessages.appendChild(typingDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    
    return typingDiv;
}

// Get Gemini AI response
async function getGeminiResponse(userMessage) {
    // Add current user message to conversation history
    conversationHistory.push({
        role: 'user',
        parts: [{ text: userMessage }]
    });

    // Check if user is logged in
    const userLoggedIn = isUserLoggedIn();
    
    // Create different system instructions based on login state
    let systemInstructionText;
    
    if (userLoggedIn) {
        // Logged in - provide personalized coaching with match data
        systemInstructionText = `You are a table tennis coach AI analyzing a specific match. Here is the match data you have access to:

${matchAnalysisData}

CRITICAL INSTRUCTIONS:
- When the user mentions "the match", "my match", or asks about match statistics, they are ALWAYS referring to the table tennis match data above
- This is a table tennis match between Marcus Chen (the user, referred to as "you") and Daniel Rodriguez (the opponent)
- When discussing Player 1 or Marcus Chen, use "you" or "your" (e.g., "your average racket velocity", "you executed 157 shots")
- When discussing Player 2, always use the name "Daniel Rodriguez" (e.g., "Daniel Rodriguez had 9.6% faster racket speed", "Daniel executed 151 shots")
- Never say "Player 1" or "Player 2" - always use "you/your" for Marcus Chen and "Daniel Rodriguez" for the opponent
- Provide specific stats from this data when asked about the match
- Be conversational and helpful like a real coach
- Give concise answers (2-3 sentences) unless asked for more detail
- Focus on actionable insights and training recommendations
- When giving advice, speak directly to the user as their coach (e.g., "You should focus on...", "I recommend you work on...")`;
    } else {
        // Not logged in - focus on getting user to sign up/login
        systemInstructionText = `You are PaddleCoach AI, a friendly assistant for a table tennis coaching platform.

CRITICAL INSTRUCTIONS:
- The user is NOT logged in, so you do NOT have access to their match data or statistics
- DO NOT provide any personalized analysis, player names, or specific match statistics
- DO NOT mention Marcus Chen, Daniel Rodriguez, or any player-specific information
- Your main goal is to help users understand the platform and encourage them to sign up or log in
- Be friendly, helpful, and enthusiastic about the platform's features
- When asked about matches, stats, or personal performance, politely explain they need to log in first
- Highlight benefits of signing up: AI-powered match analysis, personalized coaching, shot detection, biomechanical analysis
- Keep responses concise (2-3 sentences) and welcoming
- Example responses:
  * "I'd love to help you analyze your game! To access personalized match analysis and statistics, please sign up or log in first."
  * "PaddleCoach uses AI to track your shots, analyze your technique, and provide coaching insights. Create an account to get started!"
  * "Once you're logged in, I can provide detailed analysis of your matches, including shot counts, racket speed, and personalized training recommendations."`;
    }

    const requestBody = {
        systemInstruction: {
            parts: [{
                text: systemInstructionText
            }]
        },
        contents: conversationHistory,
        generationConfig: {
            temperature: 0.8,
            maxOutputTokens: 2000,
            topK: 40,
            topP: 0.95,
        }
    };

    try {
        console.log('Making API request to Gemini...');
        const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('API Error Response:', errorText);
            
            try {
                const errorData = JSON.parse(errorText);
                console.error('Parsed API Error:', errorData);
                
                if (errorData.error && errorData.error.message) {
                    throw new Error(errorData.error.message);
                }
            } catch (parseError) {
                console.error('Could not parse error response');
            }
            
            throw new Error(`API request failed with status: ${response.status}`);
        }

        const data = await response.json();
        console.log('API Response:', JSON.stringify(data, null, 2));
        
        if (data.candidates && data.candidates.length > 0) {
            const candidate = data.candidates[0];
            
            // Check if response was cut off
            if (candidate.finishReason === 'MAX_TOKENS') {
                console.warn('Response was cut off due to MAX_TOKENS');
                // Still try to get the partial response if available
            }
            
            if (candidate.content && candidate.content.parts && candidate.content.parts.length > 0) {
                const part = candidate.content.parts[0];
                console.log('Part:', part);
                
                let aiResponse = part.text || '';
                
                if (aiResponse) {
                    // Remove markdown formatting (asterisks for bold/italic)
                    aiResponse = aiResponse
                        .replace(/\*\*\*/g, '')  // Remove triple asterisks
                        .replace(/\*\*/g, '')    // Remove double asterisks (bold)
                        .replace(/\*/g, '');     // Remove single asterisks (italic)
                    
                    // Add only the model's response (user message was already added at function start)
                    conversationHistory.push({
                        role: 'model',
                        parts: [{ text: aiResponse }]
                    });
                    
                    return aiResponse;
                }
            }
            
            // Handle case where there's no parts (like MAX_TOKENS with no output)
            if (candidate.finishReason === 'MAX_TOKENS') {
                throw new Error('Response was cut off. Try asking a shorter question or be more specific.');
            }
        }
        
        console.error('Invalid response structure:', JSON.stringify(data, null, 2));
        throw new Error('Invalid response format from API');
    } catch (error) {
        console.error('Gemini API Error Details:', error);
        throw error;
    }
}

// Send message on button click
if (chatbotSend) {
    chatbotSend.addEventListener('click', sendMessage);
}

// Send message on Enter key
if (chatbotInput) {
    chatbotInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}
