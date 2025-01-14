function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function showContactDetails(bidId) {
    const contactDetailsDiv = document.getElementById(`contact-details-${bidId}`);
    const isVisible = contactDetailsDiv.style.display === 'block';

    if (isVisible) {
       
        contactDetailsDiv.style.display = 'none';
    } else {
       
        fetch(`/bids/${bidId}/view-contact/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(), 
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`contact-name-${bidId}`).textContent =
                        data.contact_details.name || 'Not Provided';
                    document.getElementById(`contact-email-${bidId}`).textContent =
                        data.contact_details.email || 'Not Provided';
                    contactDetailsDiv.style.display = 'block';
                } else {
                    alert(data.message || 'Unable to fetch contact details.');
                }
            })
            .catch(error => console.error('Error:', error));
    }
}
