// Advanced client-side validation that can't be easily bypassed via HTML
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const powerLevelInput = document.getElementById('power_level');
    const integrityHashInput = document.getElementById('integrity_hash');
    const validationTokenInput = document.getElementById('validation_token');
    const nameInput = document.getElementById('name');

    // Real-time power level display
    powerLevelInput.addEventListener('input', function(e) {
        const value = parseInt(e.target.value) || 0;
        if (value > 9000) {
            e.target.style.borderColor = '#4CAF50';
            e.target.style.backgroundColor = '#e8f5e8';
        } else {
            e.target.style.borderColor = '#f44336';
            e.target.style.backgroundColor = '#ffe8e8';
        }
    });

    // Calculate integrity hash before form submission
    function calculateIntegrityHash() {
        const name = nameInput.value;
        const powerLevel = powerLevelInput.value;
        const token = validationTokenInput.value;
        
        // Simple SHA256 hash of the concatenated values
        const data = name + powerLevel + token;
        return sha256(data).substring(0, 16);
    }

    // Enhanced form submission handler
    form.addEventListener('submit', function(e) {
        // Calculate and set the integrity hash
        integrityHashInput.value = calculateIntegrityHash();
        
        // Client-side validation (can be bypassed via Burp, but not HTML)
        const powerLevel = parseInt(powerLevelInput.value);
        if (powerLevel > 9000) {
            if (!confirm('Warning: Power level exceeds scouter limits! Continue?')) {
                e.preventDefault();
                return;
            }
        } else if (powerLevel <= 9000) {
            alert('Power level too low! The scouter requires OVER 9000!');
            e.preventDefault();
            return;
        }
        
        // Final hash calculation right before submission
        setTimeout(() => {
            integrityHashInput.value = calculateIntegrityHash();
        }, 10);
    });

    // Simple SHA256 implementation (for demo purposes)
    function sha256(str) {
        // This is a simplified version - in real implementation, use a proper library
        // For this challenge, it's okay to be simple since the point is Burp interception
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16);
    }

    // Prevent HTML attribute modification detection
    const originalSetAttribute = powerLevelInput.setAttribute;
    powerLevelInput.setAttribute = function(name, value) {
        if (name === 'max' || name === 'min' || name === 'value') {
            console.warn('HTML attribute modification detected! This method is blocked.');
            return;
        }
        originalSetAttribute.call(this, name, value);
    };
});