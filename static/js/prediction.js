// Prediction page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsContainer = document.getElementById('resultsContainer');
    const noResults = document.getElementById('noResults');
    const reportSection = document.getElementById('reportSection');

    // File input change handler
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const validation = validateImageFile(file);
            if (!validation.valid) {
                showNotification(validation.message, 'danger');
                fileInput.value = '';
                hideImagePreview();
                return;
            }
            
            showImagePreview(file);
        } else {
            hideImagePreview();
        }
    });

    // Form submission handler
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            showNotification('Please select an image file first.', 'warning');
            return;
        }

        const validation = validateImageFile(file);
        if (!validation.valid) {
            showNotification(validation.message, 'danger');
            return;
        }

        uploadAndPredict(file);
    });

    function showImagePreview(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            imagePreview.style.display = 'block';
            imagePreview.classList.add('fade-in');
        };
        reader.readAsDataURL(file);
    }

    function hideImagePreview() {
        imagePreview.style.display = 'none';
        previewImg.src = '';
    }

    function uploadAndPredict(file) {
        const formData = new FormData();
        formData.append('file', file);

        // Show loading state
        showLoadingState();

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideLoadingState();
            
            if (data.error) {
                showNotification(data.error, 'danger');
                return;
            }

            displayResults(data);
            showNotification('Analysis completed successfully!', 'success');
        })
        .catch(error => {
            hideLoadingState();
            console.error('Prediction error:', error);
            showNotification('Analysis failed. Please try again.', 'danger');
        });
    }

    function showLoadingState() {
        loadingSpinner.style.display = 'block';
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
        
        // Hide previous results
        resultsContainer.style.display = 'none';
        reportSection.style.display = 'none';
        noResults.style.display = 'none';
    }

    function hideLoadingState() {
        loadingSpinner.style.display = 'none';
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-brain me-2"></i>Analyze Image';
    }

    function displayResults(data) {
        // Update prediction results
        document.getElementById('predictedClass').textContent = data.predicted_class;
        document.getElementById('confidenceScore').textContent = formatConfidence(data.confidence);
        document.getElementById('basicRecommendation').textContent = data.basic_recommendation;

        // Update probability bars
        displayProbabilityBars(data.class_probabilities);

        // Update medical report
        document.getElementById('medicalReport').textContent = data.medical_report;

        // Show results with animation
        noResults.style.display = 'none';
        resultsContainer.style.display = 'block';
        resultsContainer.classList.add('slide-up');
        
        setTimeout(() => {
            reportSection.style.display = 'block';
            reportSection.classList.add('slide-up');
        }, 300);
    }

    function displayProbabilityBars(probabilities) {
        const container = document.getElementById('probabilityBars');
        container.innerHTML = '';

        // Define colors for each class
        const classColors = {
            'Adenocarcinoma': 'bg-danger',
            'Large Cell Carcinoma': 'bg-warning',
            'Squamous Cell Carcinoma': 'bg-info',
            'Normal (Non-cancerous)': 'bg-success'
        };

        Object.entries(probabilities).forEach(([className, probability]) => {
            const percentage = (probability * 100).toFixed(1);
            const colorClass = classColors[className] || 'bg-secondary';
            
            const barHtml = `
                <div class="probability-bar mb-2">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                        <small class="fw-bold">${className}</small>
                        <small class="text-muted">${percentage}%</small>
                    </div>
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar ${colorClass}" role="progressbar" 
                             style="width: ${percentage}%" 
                             aria-valuenow="${percentage}" 
                             aria-valuemin="0" 
                             aria-valuemax="100">
                        </div>
                    </div>
                </div>
            `;
            
            container.innerHTML += barHtml;
        });
    }

    // Drag and drop functionality
    const uploadArea = document.querySelector('.card-body');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        uploadArea.classList.add('border-primary', 'bg-light');
    }

    function unhighlight(e) {
        uploadArea.classList.remove('border-primary', 'bg-light');
    }

    uploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            fileInput.files = files;
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to analyze
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (fileInput.files[0] && !analyzeBtn.disabled) {
                uploadForm.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to clear selection
        if (e.key === 'Escape') {
            fileInput.value = '';
            hideImagePreview();
            resultsContainer.style.display = 'none';
            reportSection.style.display = 'none';
            noResults.style.display = 'block';
        }
    });
});

// Additional utility functions specific to prediction page
function resetPredictionForm() {
    document.getElementById('fileInput').value = '';
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('resultsContainer').style.display = 'none';
    document.getElementById('reportSection').style.display = 'none';
    document.getElementById('noResults').style.display = 'block';
}

function copyReportToClipboard() {
    const reportText = document.getElementById('medicalReport').textContent;
    navigator.clipboard.writeText(reportText).then(() => {
        showNotification('Report copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy report to clipboard.', 'danger');
    });
}