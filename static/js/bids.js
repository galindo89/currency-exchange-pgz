document.addEventListener("input", function (event) {
    if (event.target && event.target.id.startsWith("amount-")) {
        const modalId = event.target.id.split("-")[1];
        const bidAmount = parseFloat(event.target.value) || 0;
        const exchangeRate = parseFloat(document.getElementById(`exchangeRate-${modalId}`).textContent) || 0;
        const conversionPreview = document.getElementById(`conversionPreview-${modalId}`);
        const currencyType = document.getElementById(`currencyType-${modalId}`).textContent.trim();

        let convertedAmount;

        if (currencyType === "EUR") {
           
            convertedAmount = bidAmount * exchangeRate;
        } else if (currencyType === "USD") {
            
            convertedAmount = bidAmount / exchangeRate;
        }

       
        if (convertedAmount !== undefined) {
            conversionPreview.textContent = convertedAmount.toFixed(2);
        }
    }
});
