// Main JavaScript for Lung Cancer Classifier

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add fade-in animation to cards with staggered timing
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 150);
    });

    // Create floating particles background
    createFloatingParticles();

    // Add medical decoration to specific elements
    addMedicalDecorations();

    // Smooth scrolling for anchor links
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

    // Auto-hide alerts after 5 seconds with fade out
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                const closeBtn = alert.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.click();
                }
            }, 500);
        }, 5000);
    });

    // Add hover effects to navigation items
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// Create floating particles for background animation
function createFloatingParticles() {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'floating-particles';
    document.body.appendChild(particleContainer);

    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random size between 2-6px
        const size = Math.random() * 4 + 2;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        
        // Random position
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        
        // Random animation delay
        particle.style.animationDelay = Math.random() * 6 + 's';
        particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
        
        particleContainer.appendChild(particle);
    }
}

// Add medical decorations to specific elements
function addMedicalDecorations() {
    const decorationTargets = document.querySelectorAll('.card-header, .jumbotron h1');
    decorationTargets.forEach((element, index) => {
        if (index % 2 === 0) { // Add decoration to every other element
            element.classList.add('medical-decoration');
        }
    });
}

// Utility Functions
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px; animation: slideInRight 0.5s ease;';
    alertDiv.innerHTML = `
        <i class="fas fa-${getIconForType(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds with animation
    setTimeout(() => {
        alertDiv.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 500);
    }, 5000);
}

function getIconForType(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function formatPercentage(value) {
    return (value * 100).toFixed(1) + '%';
}

function formatConfidence(value) {
    return (value * 100).toFixed(1) + '%';
}

// Print functionality with enhanced styling
function printReport() {
    const reportContent = document.getElementById('medicalReport').innerHTML;
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Medical Report - Lung Cancer Analysis</title>
            <style>
                body { 
                    font-family: 'Times New Roman', serif; 
                    margin: 20px; 
                    line-height: 1.6;
                    color: #333;
                }
                .report-content { 
                    white-space: pre-wrap; 
                    line-height: 1.8;
                    background: #f9f9f9;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #0f4c75;
                }
                h1 {
                    color: #0f4c75;
                    border-bottom: 2px solid #3282b8;
                    padding-bottom: 10px;
                }
                @media print { 
                    body { margin: 0; }
                    .report-content { background: white; }
                }
            </style>
        </head>
        <body>
            <h1>🏥 Lung Cancer CT Scan Analysis Report</h1>
            <div class="report-content">${reportContent}</div>
            <footer style="margin-top: 30px; text-align: center; color: #666; font-size: 12px;">
                Generated by Enhanced Clinical-Grade Lung Cancer Classifier
            </footer>
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

// Download functionality with enhanced formatting
function downloadReport() {
    const reportContent = document.getElementById('medicalReport').textContent;
    const enhancedContent = `
🏥 LUNG CANCER CT SCAN ANALYSIS REPORT
${'='.repeat(50)}

${reportContent}

${'='.repeat(50)}
Generated by: Enhanced Clinical-Grade Lung Cancer Classifier
Date: ${new Date().toLocaleString()}
System: EfficientNet-B4 + GPT-3.5 Hybrid AI
    `;
    
    const blob = new Blob([enhancedContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `lung_cancer_report_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    showNotification('Report downloaded successfully!', 'success');
}

// Loading state management with enhanced animations
function showLoading(element) {
    element.innerHTML = `
        <div class="d-flex justify-content-center align-items-center">
            <div class="spinner-border text-primary me-3" role="status" style="animation: spin 1s linear infinite;">
                <span class="visually-hidden">Loading...</span>
            </div>
            <span class="fw-bold">Processing medical data...</span>
        </div>
    `;
}

function hideLoading(element, originalContent) {
    element.style.transition = 'opacity 0.3s ease';
    element.style.opacity = '0';
    setTimeout(() => {
        element.innerHTML = originalContent;
        element.style.opacity = '1';
    }, 300);
}

// Form validation with enhanced feedback
function validateImageFile(file) {
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (!allowedTypes.includes(file.type)) {
        return { valid: false, message: '⚠️ Please select a PNG, JPG, or JPEG file.' };
    }
    
    if (file.size > maxSize) {
        return { valid: false, message: '⚠️ File size must be less than 16MB.' };
    }
    
    return { valid: true, message: '✅ File validation successful!' };
}

// Error handling with enhanced notifications
function handleError(error, context = 'Operation') {
    console.error(`${context} error:`, error);
    showNotification(`❌ ${context} failed. Please try again.`, 'danger');
}

// Success handling with enhanced notifications
function handleSuccess(message) {
    showNotification(`✅ ${message}`, 'success');
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);