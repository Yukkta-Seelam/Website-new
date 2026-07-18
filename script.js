// Navigation scroll effect
const navbar = document.getElementById('navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

// Mobile menu toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
        }
    });
}, observerOptions);

// Observe skill category cards
document.querySelectorAll('.skill-category-card').forEach((card, index) => {
    observer.observe(card);
    card.style.transitionDelay = `${index * 0.1}s`;
});

// Observe project cards
document.querySelectorAll('.project-card').forEach((card, index) => {
    observer.observe(card);
    card.style.transitionDelay = `${index * 0.1}s`;
});

// Observe education cards
document.querySelectorAll('.education-card').forEach((card, index) => {
    observer.observe(card);
    card.style.transitionDelay = `${index * 0.1}s`;
});

// Observe experience cards
document.querySelectorAll('.experience-card').forEach((card, index) => {
    observer.observe(card);
    card.style.transitionDelay = `${index * 0.1}s`;
});

// Observe publication items
document.querySelectorAll('.publication-item').forEach((item, index) => {
    observer.observe(item);
    item.style.transitionDelay = `${index * 0.1}s`;
});

// Form submission with EmailJS
const contactForm = document.getElementById('contact-form');

if (contactForm) {
    const submitButton = contactForm.querySelector('button[type="submit"]');
    
    // Initialize EmailJS when page loads
    window.addEventListener('DOMContentLoaded', () => {
        if (typeof emailjs !== 'undefined') {
            // Initialize EmailJS with your Public Key
            emailjs.init("TinKeQCquuA1UqkJr");
        }
    });
    
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Check if EmailJS is loaded
        if (typeof emailjs === 'undefined') {
            showMessage('Email service is not configured. Please contact me directly at yukktaseelam54@gmail.com', 'error');
            return;
        }
        
        // Get form values
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        // Simple validation
        if (!name || !email || !message) {
            showMessage('Please fill in all fields.', 'error');
            return;
        }
        
        // Show loading state
        const originalButtonText = submitButton.textContent;
        submitButton.textContent = 'Sending...';
        submitButton.disabled = true;
        
        try {
            // Send email using EmailJS
            await emailjs.send(
                'service_oti2ryt',    // Your EmailJS Service ID
                'template_bepqykj',   // Your EmailJS Template ID
                {
                    from_name: name,
                    from_email: email,
                    message: message,
                    to_email: 'yukktaseelam54@gmail.com' // Your email address
                }
            );
            
            // Success
            showMessage('Thank you for your message! I will get back to you soon.', 'success');
            contactForm.reset();
        } catch (error) {
            // Error
            console.error('EmailJS Error:', error);
            showMessage('Sorry, there was an error sending your message. Please try again or email me directly at yukktaseelam54@gmail.com', 'error');
        } finally {
            // Reset button state
            submitButton.textContent = originalButtonText;
            submitButton.disabled = false;
        }
    });
}

// Function to show success/error messages
function showMessage(text, type) {
    // Remove any existing message
    const existingMessage = document.querySelector('.form-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `form-message ${type}`;
    messageDiv.textContent = text;
    messageDiv.style.cssText = `
        padding: 1rem;
        margin-top: 1rem;
        border-radius: 8px;
        font-weight: 500;
        ${type === 'success' 
            ? 'background: #d4edda; color: #155724; border: 1px solid #c3e6cb;' 
            : 'background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;'
        }
    `;
    
    // Insert after the form
    contactForm.parentNode.insertBefore(messageDiv, contactForm.nextSibling);
    
    // Remove message after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Add parallax effect to hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        hero.style.opacity = 1 - scrolled / 600;
    }
});

// Add typing effect to hero title (optional enhancement)
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}


// Add active state to navigation links based on scroll position
const sections = document.querySelectorAll('section[id]');

function activateNavLink() {
    const scrollY = window.pageYOffset;
    
    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);
        
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLinks.forEach(link => link.classList.remove('active'));
            if (navLink) {
                navLink.classList.add('active');
            }
        }
    });
}

window.addEventListener('scroll', activateNavLink);

// Add CSS for active nav link
const style = document.createElement('style');
style.textContent = `
    .nav-link.active {
        color: var(--blue-primary);
    }
    .nav-link.active::after {
        width: 100%;
    }
`;
document.head.appendChild(style);

// Image error handling - try to convert HEIC or show placeholder
const profileImage = document.getElementById('profile-image');
if (profileImage) {
    profileImage.addEventListener('error', function() {
        // If HEIC fails to load, show placeholder
        const placeholder = this.nextElementSibling;
        if (placeholder) {
            this.style.display = 'none';
            placeholder.style.display = 'flex';
        }
    });
}

// Add subtle animations on page load
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
});


