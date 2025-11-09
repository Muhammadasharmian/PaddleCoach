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
    
    // Ball Tracking button handler
    const ballTrackingBtn = document.getElementById('startBallTracking');
    if (ballTrackingBtn) {
        ballTrackingBtn.addEventListener('click', () => {
            window.location.href = 'ball_tracking.html';
        });
    }
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
        
        // Close dropdown
        if (userDropdown) {
            userDropdown.classList.remove('active');
        }
        
        alert('You have been logged out successfully!');
    });
}

// Handle Upload Match Video button
const uploadMatchVideoBtn = document.getElementById('uploadMatchVideoBtn');
const matchVideoInput = document.getElementById('matchVideoInput');
const matchVideoModal = document.getElementById('matchVideoModal');
const closeMatchVideoModal = document.getElementById('closeMatchVideoModal');
const matchVideoFileInput = document.getElementById('matchVideoFileInput');
const selectVideoBtn = document.getElementById('selectVideoBtn');
const uploadArea = document.getElementById('uploadArea');
const uploadSection = document.getElementById('uploadSection');
const previewSection = document.getElementById('previewSection');
const processingSection = document.getElementById('processingSection');
const resultsSection = document.getElementById('resultsSection');
const selectedFileInfo = document.getElementById('selectedFileInfo');
const analyzeAnotherBtn = document.getElementById('analyzeAnotherBtn');
const startAnalysisBtn = document.getElementById('startAnalysisBtn');
const previewVideo = document.getElementById('previewVideo');
const leftPlayerSelect = document.getElementById('leftPlayerSelect');
const rightPlayerSelect = document.getElementById('rightPlayerSelect');

let selectedFile = null;

if (uploadMatchVideoBtn) {
    uploadMatchVideoBtn.addEventListener('click', () => {
        // Open the modal
        if (matchVideoModal) {
            matchVideoModal.classList.add('active');
            document.body.style.overflow = 'hidden';
            // Reset modal to upload section
            resetMatchVideoModal();
        }
    });
}

// Close modal
if (closeMatchVideoModal) {
    closeMatchVideoModal.addEventListener('click', () => {
        matchVideoModal.classList.remove('active');
        document.body.style.overflow = '';
        resetMatchVideoModal();
    });
}

// Close modal when clicking outside
if (matchVideoModal) {
    matchVideoModal.addEventListener('click', (e) => {
        if (e.target === matchVideoModal) {
            matchVideoModal.classList.remove('active');
            document.body.style.overflow = '';
            resetMatchVideoModal();
        }
    });
}

// Select video button
if (selectVideoBtn) {
    selectVideoBtn.addEventListener('click', () => {
        matchVideoFileInput.click();
    });
}

// File input change
if (matchVideoFileInput) {
    matchVideoFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            selectedFile = file;
            showFileInfo(file);
        }
    });
}

// Drag and drop functionality
if (uploadArea) {
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#7c3aed';
        uploadArea.style.background = 'rgba(124, 58, 237, 0.05)';
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#e5e7eb';
        uploadArea.style.background = 'transparent';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#e5e7eb';
        uploadArea.style.background = 'transparent';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('video/')) {
                selectedFile = file;
                matchVideoFileInput.files = files;
                showFileInfo(file);
            } else {
                alert('Please upload a video file.');
            }
        }
    });
}

function showFileInfo(file) {
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    
    if (fileName && fileSize && selectedFileInfo) {
        fileName.textContent = file.name;
        fileSize.textContent = `(${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
        selectedFileInfo.style.display = 'flex';
        
        // Show preview section instead of auto-uploading
        setTimeout(() => {
            showPreview(file);
        }, 500);
    }
}

function showPreview(file) {
    // Hide upload section, show preview section
    uploadSection.style.display = 'none';
    previewSection.style.display = 'block';
    processingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    
    // Load video preview
    if (previewVideo) {
        const videoUrl = URL.createObjectURL(file);
        previewVideo.src = videoUrl;
        previewVideo.load();
    }
}

// Start Analysis button handler
if (startAnalysisBtn) {
    startAnalysisBtn.addEventListener('click', () => {
        const leftPlayer = leftPlayerSelect.value;
        const rightPlayer = rightPlayerSelect.value;
        
        console.log('Starting analysis with:', { leftPlayer, rightPlayer });
        
        if (selectedFile) {
            uploadMatchVideo(selectedFile, leftPlayer, rightPlayer);
        }
    });
}

async function uploadMatchVideo(file, leftPlayer = 'myself', rightPlayer = 'rank1') {
    // Show processing section
    previewSection.style.display = 'none';
    uploadSection.style.display = 'none';
    processingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    
    const formData = new FormData();
    formData.append('video', file);
    
    try {
        // Simulate progress
        simulateProgress();
        
        const response = await fetch('http://localhost:5000/api/upload-match-video', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Show results after processing
            setTimeout(() => {
                showProcessedVideo(data.processed_video_url);
            }, 2000);
        } else {
            alert('Error: ' + data.message);
            resetMatchVideoModal();
        }
    } catch (error) {
        console.error('Upload error:', error);
        alert('Error uploading video. Please try again.');
        resetMatchVideoModal();
    }
}

function simulateProgress() {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    let progress = 0;
    
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 95) {
            progress = 95;
            clearInterval(interval);
        }
        
        if (progressFill && progressText) {
            progressFill.style.width = progress + '%';
            progressText.textContent = Math.round(progress) + '%';
        }
    }, 300);
}

function showProcessedVideo(videoUrl) {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    // Complete progress
    if (progressFill && progressText) {
        progressFill.style.width = '100%';
        progressText.textContent = '100%';
    }
    
    setTimeout(() => {
        processingSection.style.display = 'none';
        resultsSection.style.display = 'block';
        
        // Set video source directly on the video element
        const processedVideo = document.getElementById('processedVideo');
        
        if (processedVideo) {
            console.log('Setting video source to:', videoUrl);
            
            // Add full URL with cache buster
            const fullUrl = `http://localhost:5000${videoUrl}?t=${Date.now()}`;
            console.log('Full video URL:', fullUrl);
            
            // Set src directly on video element for better compatibility
            processedVideo.src = fullUrl;
            processedVideo.type = 'video/mp4';
            
            // Add event listeners for debugging
            processedVideo.addEventListener('loadstart', () => {
                console.log('Video loading started...');
            });
            
            processedVideo.addEventListener('loadedmetadata', () => {
                console.log('Video metadata loaded');
                console.log('Video duration:', processedVideo.duration);
                console.log('Video dimensions:', processedVideo.videoWidth, 'x', processedVideo.videoHeight);
            });
            
            processedVideo.addEventListener('loadeddata', () => {
                console.log('Video data loaded successfully');
            });
            
            processedVideo.addEventListener('canplay', () => {
                console.log('Video can play now');
                // Try to play the video
                processedVideo.play().catch(e => console.log('Autoplay prevented:', e));
            });
            
            processedVideo.addEventListener('error', (e) => {
                console.error('Video error event:', e);
                if (processedVideo.error) {
                    console.error('Error code:', processedVideo.error.code);
                    console.error('Error message:', processedVideo.error.message);
                    
                    // Error codes: 1=ABORTED, 2=NETWORK, 3=DECODE, 4=SRC_NOT_SUPPORTED
                    const errorMessages = {
                        1: 'Video loading aborted',
                        2: 'Network error while loading video',
                        3: 'Video decoding failed (codec issue)',
                        4: 'Video format not supported by browser'
                    };
                    console.error('Error description:', errorMessages[processedVideo.error.code] || 'Unknown error');
                }
            });
            
            // Try to load the video
            processedVideo.load();
        } else {
            console.error('Video element not found');
        }
    }, 500);
}

function resetMatchVideoModal() {
    selectedFile = null;
    uploadSection.style.display = 'block';
    previewSection.style.display = 'none';
    processingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    
    if (selectedFileInfo) {
        selectedFileInfo.style.display = 'none';
    }
    
    if (matchVideoFileInput) {
        matchVideoFileInput.value = '';
    }
    
    if (previewVideo) {
        previewVideo.src = '';
    }
    
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    if (progressFill && progressText) {
        progressFill.style.width = '0%';
        progressText.textContent = '0%';
    }
}

// Analyze another video button
if (analyzeAnotherBtn) {
    analyzeAnotherBtn.addEventListener('click', () => {
        resetMatchVideoModal();
    });
}

// Keep the old matchVideoInput for backward compatibility
if (matchVideoInput) {
    matchVideoInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            console.log('Selected file:', file.name);
            console.log('File size:', (file.size / (1024 * 1024)).toFixed(2), 'MB');
            console.log('File type:', file.type);
            
            // Show confirmation to user
            alert(`Video selected: ${file.name}\nSize: ${(file.size / (1024 * 1024)).toFixed(2)} MB\n\nVideo upload functionality will be implemented when backend is ready.`);
            
            // TODO: Implement actual upload to backend when available
            // Example: uploadVideoToBackend(file);
        }
    });
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
                }
                // If logged in, let the file input handler take over
                return;
            }
            
            if (!isUserLoggedIn()) {
                e.preventDefault();
                e.stopPropagation();
                promptLogin();
            } else {
                // User is logged in
                // Check if this is the ball tracking button - it has its own handler
                if (button.id === 'startBallTracking') {
                    // Let the dedicated ball tracking handler take over
                    return;
                }
                // For other buttons, show feature coming soon message
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
