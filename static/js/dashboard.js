/**
 * Retrieves the CSRF token from the meta tag in the document.
 *
 * @returns {string} The CSRF token.
 */
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

/**
 * Toggles the visibility of contact details for a specific bid.
 * If the contact details are not currently visible, it fetches the contact details from the server
 * and displays them. If they are already visible, it hides them.
 *
 * @param {number} bidId - The ID of the bid for which to show or hide contact details.
 */
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
