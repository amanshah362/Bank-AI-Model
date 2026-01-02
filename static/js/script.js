// Counter animation for stats
$(document).ready(function() {
    $('.counter').each(function() {
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text().replace('%', '')
        }, {
            duration: 2000,
            easing: 'swing',
            step: function(now) {
                $(this).text(Math.ceil(now) + ($(this).text().includes('%') ? '%' : ''));
            }
        });
    });

    // Form validation
    $('#predictionForm').submit(function(e) {
        e.preventDefault();
        
        // Show loading animation
        const submitBtn = $(this).find('button[type="submit"]');
        const originalText = submitBtn.html();
        submitBtn.html('<i class="fas fa-spinner fa-spin"></i> Processing...');
        submitBtn.prop('disabled', true);
        
        // Submit form after animation
        setTimeout(() => {
            this.submit();
        }, 1000);
    });

    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
});

// API integration example
async function makeAPIPrediction(data) {
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

// Local storage for recent predictions
function saveRecentPrediction(predictionData) {
    let recent = JSON.parse(localStorage.getItem('recentPredictions') || '[]');
    recent.unshift({
        ...predictionData,
        timestamp: new Date().toISOString()
    });
    
    // Keep only last 10 predictions
    recent = recent.slice(0, 10);
    localStorage.setItem('recentPredictions', JSON.stringify(recent));
}

// Export functionality
function exportPredictionReport() {
    const report = {
        prediction: sessionStorage.getItem('lastPrediction'),
        data: sessionStorage.getItem('lastInputData'),
        timestamp: new Date().toISOString()
    };
    
    const dataStr = JSON.stringify(report, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `prediction_report_${Date.now()}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
}