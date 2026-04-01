// Client-side JavaScript

document.addEventListener('DOMContentLoaded', function () {
    const payNowBtn = document.getElementById('pay-now-btn');
    const billerInput = document.getElementById('biller-input');
    const amountInput = document.getElementById('amount-input');
    const errorMsg = document.getElementById('error-msg');
    const successMsg = document.getElementById('success-msg');

    console.log('Dummy bank application loaded');

    payNowBtn.addEventListener('click', handlePayment);

    function handlePayment() {
        console.log('Payment initiated');

        const billerName = billerInput.value.trim();
        const amount = parseFloat(amountInput.value);

        console.log('Biller:', billerName);
        console.log('Amount:', amount);

        // Hide previous messages
        hideMessages();

        // Validate biller name
        if (!billerName) {
            console.log('Validation failed: Biller name is required');
            showError('Biller name is required');
            return;
        }

        // Validate amount
        if (!amount || amount <= 0) {
            console.log('Validation failed: Invalid amount');
            showError('Amount must be greater than 0');
            return;
        }

        console.log('Validation passed. Processing payment...');

        // Disable button during processing
        payNowBtn.disabled = true;
        payNowBtn.textContent = 'Processing...';

        // Simulate payment processing delay
        setTimeout(function () {
            console.log('Payment successful');
            showSuccess('Payment successful');

            // Clear form
            billerInput.value = '';
            amountInput.value = '';

            // Re-enable button
            payNowBtn.disabled = false;
            payNowBtn.textContent = 'Pay Now';
        }, 2000);
    }

    function showError(message) {
        errorMsg.textContent = message;
        errorMsg.style.display = 'block';
    }

    function showSuccess(message) {
        successMsg.textContent = message;
        successMsg.style.display = 'block';
    }

    function hideMessages() {
        errorMsg.style.display = 'none';
        successMsg.style.display = 'none';
    }
});
