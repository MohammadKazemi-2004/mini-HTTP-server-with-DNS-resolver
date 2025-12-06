function sayHello() {
    const greetings = [
        "kaaaaaa kaaaaaa"
        // "Hello from the Python server! 🐍",
        // "Welcome! Your form will be processed by Python",
        // "Server is running smoothly! ⚡",
        // "Thanks for visiting our custom server! ✨",
        // "Powered by Python socket programming! 🔌"
    ];
    
    const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];
    showToast(randomGreeting);
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        font-weight: 500;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Form validation and feedback
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const nameInput = document.getElementById('name');
    const ageInput = document.getElementById('age');
    const submitBtn = document.querySelector('.submit-btn');
    
    if (!form) return;
    
    // Real-time validation
    nameInput.addEventListener('input', function() {
        const name = this.value.trim();
        if (name.length >= 2) {
            this.style.borderColor = '#48bb78';
            showValidationMessage('name', '✅ Valid name', '#48bb78');
        } else {
            this.style.borderColor = '#e53e3e';
            showValidationMessage('name', 'Name must be at least 2 characters', '#e53e3e');
        }
    });
    
    ageInput.addEventListener('input', function() {
        const age = parseInt(this.value) || 0;
        if (age >= 1 && age <= 120) {
            this.style.borderColor = '#48bb78';
            showValidationMessage('age', '✅ Valid age', '#48bb78');
        } else {
            this.style.borderColor = '#e53e3e';
            showValidationMessage('age', 'Age must be between 1 and 120', '#e53e3e');
        }
    });
    
    function showValidationMessage(fieldId, message, color) {
        let msgElement = document.getElementById(`${fieldId}-validation`);
        if (!msgElement) {
            msgElement = document.createElement('small');
            msgElement.id = `${fieldId}-validation`;
            const input = document.getElementById(fieldId);
            input.parentElement.appendChild(msgElement);
        }
        msgElement.textContent = message;
        msgElement.style.color = color;
        msgElement.style.fontWeight = 'bold';
    }
    
    // Form submission feedback
    form.addEventListener('submit', function(e) {
        const name = nameInput.value.trim();
        const age = parseInt(ageInput.value) || 0;
        
        // Client-side validation
        if (name.length < 2) {
            e.preventDefault();
            showToast('Please enter a valid name (at least 2 characters)');
            nameInput.focus();
            return;
        }
        
        if (age < 1 || age > 120) {
            e.preventDefault();
            showToast('Please enter a valid age (1-120)');
            ageInput.focus();
            return;
        }
        
        // Show loading state
        submitBtn.innerHTML = '⏳ Processing on server...';
        submitBtn.disabled = true;
        
        // Add loading animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
        
        // Remove animation after form submits
        setTimeout(() => {
            submitBtn.innerHTML = 'Submit to Server';
            submitBtn.disabled = false;
            document.head.removeChild(style);
        }, 3000);
    });
});