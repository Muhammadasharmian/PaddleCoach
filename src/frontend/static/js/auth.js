/**
 * PaddleCoach - Authentication JavaScript
 * Handles login, signup, and session management
 */

// Toggle authentication dropdown
function toggleAuthDropdown() {
    const dropdown = document.getElementById('dropdownMenu');
    dropdown.classList.toggle('show');
}

// Show login modal
function showLoginModal() {
    document.getElementById('loginModal').style.display = 'block';
    const dropdown = document.getElementById('dropdownMenu');
    if (dropdown) dropdown.classList.remove('show');
}

// Show signup modal
function showSignupModal() {
    document.getElementById('signupModal').style.display = 'block';
    const dropdown = document.getElementById('dropdownMenu');
    if (dropdown) dropdown.classList.remove('show');
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    // Clear error messages
    const errorElements = document.querySelectorAll('.error-message');
    errorElements.forEach(el => {
        el.classList.remove('show');
        el.textContent = '';
    });
}

// Close dropdown when clicking outside
window.onclick = function(event) {
    const dropdown = document.getElementById('dropdownMenu');
    if (dropdown && !event.target.matches('.auth-btn') && !event.target.closest('.auth-dropdown')) {
        dropdown.classList.remove('show');
    }
    
    // Close modals when clicking outside
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Handle login form submission
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const errorDiv = document.getElementById('loginError');
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store token in localStorage
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('userName', data.user.name);
            localStorage.setItem('userEmail', data.user.email);
            localStorage.setItem('userId', data.user.id);
            
            // Update UI
            updateAuthUI(data.user.name);
            
            // Close modal
            closeModal('loginModal');
            
            // Show success message
            showNotification('Welcome back, ' + data.user.name + '!', 'success');
        } else {
            errorDiv.textContent = data.message;
            errorDiv.classList.add('show');
        }
    } catch (error) {
        errorDiv.textContent = 'Login failed. Please try again.';
        errorDiv.classList.add('show');
        console.error('Login error:', error);
    }
}

// Handle signup form submission
async function handleSignup(event) {
    event.preventDefault();
    
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const errorDiv = document.getElementById('signupError');
    
    // Validate password length
    if (password.length < 6) {
        errorDiv.textContent = 'Password must be at least 6 characters long';
        errorDiv.classList.add('show');
        return;
    }
    
    try {
        const response = await fetch('/api/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Close signup modal
            closeModal('signupModal');
            
            // Show success message
            showNotification('Account created successfully! Please log in.', 'success');
            
            // Open login modal
            setTimeout(() => {
                showLoginModal();
                // Pre-fill email
                document.getElementById('loginEmail').value = email;
            }, 1000);
        } else {
            errorDiv.textContent = data.message;
            errorDiv.classList.add('show');
        }
    } catch (error) {
        errorDiv.textContent = 'Signup failed. Please try again.';
        errorDiv.classList.add('show');
        console.error('Signup error:', error);
    }
}

// Update authentication UI
function updateAuthUI(userName) {
    const authBtn = document.querySelector('.auth-btn');
    const authBtnText = document.getElementById('authBtnText');
    const dropdownMenu = document.getElementById('dropdownMenu');
    
    if (userName) {
        // User is logged in
        if (authBtnText) {
            authBtnText.textContent = userName;
        }
        
        // Update dropdown menu
        dropdownMenu.innerHTML = `
            <div class="dropdown-item" onclick="viewProfile()">
                👤 Profile
            </div>
            <div class="dropdown-item" onclick="handleLogout()">
                🚪 Log Out
            </div>
        `;
    } else {
        // User is logged out
        if (authBtnText) {
            authBtnText.textContent = 'Account';
        }
        
        // Reset dropdown menu
        dropdownMenu.innerHTML = `
            <div class="dropdown-item" onclick="showLoginModal()">
                🔐 Log In
            </div>
            <div class="dropdown-item" onclick="showSignupModal()">
                ✨ Sign Up
            </div>
        `;
    }
}

// Handle logout
async function handleLogout() {
    const token = localStorage.getItem('authToken');
    
    try {
        await fetch('/api/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ token })
        });
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    // Clear local storage
    localStorage.removeItem('authToken');
    localStorage.removeItem('userName');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userId');
    
    // Update UI
    updateAuthUI(null);
    
    // Show notification
    showNotification('You have been logged out', 'info');
    
    // Close dropdown
    document.getElementById('dropdownMenu').classList.remove('show');
}

// View profile (placeholder)
function viewProfile() {
    const userName = localStorage.getItem('userName');
    const userEmail = localStorage.getItem('userEmail');
    
    showNotification(`Profile: ${userName} (${userEmail})`, 'info');
    document.getElementById('dropdownMenu').classList.remove('show');
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#667eea'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        font-weight: 500;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add notification animations to page
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);

// Check authentication status on page load
document.addEventListener('DOMContentLoaded', function() {
    const userName = localStorage.getItem('userName');
    if (userName) {
        updateAuthUI(userName);
    }
});

// Verify token with server (optional, for added security)
async function verifyToken() {
    const token = localStorage.getItem('authToken');
    
    if (!token) return false;
    
    try {
        const response = await fetch('/api/auth/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ token })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.user;
        } else {
            // Token is invalid, clear storage
            localStorage.removeItem('authToken');
            localStorage.removeItem('userName');
            localStorage.removeItem('userEmail');
            localStorage.removeItem('userId');
            updateAuthUI(null);
            return false;
        }
    } catch (error) {
        console.error('Token verification error:', error);
        return false;
    }
}
