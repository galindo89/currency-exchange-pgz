document.addEventListener('DOMContentLoaded', () => {
    const deleteConfirmationModal = document.getElementById('deleteConfirmationModal');
    const deleteForm = document.getElementById('deleteForm');
    const deleteItemType = document.getElementById('deleteItemType');

    deleteConfirmationModal.addEventListener('show.bs.modal', (event) => {
        const button = event.relatedTarget; 
        const actionUrl = button.getAttribute('data-action'); 
        const itemType = button.getAttribute('data-item'); 
       
        deleteForm.setAttribute('action', actionUrl);

       
        deleteItemType.textContent = itemType || 'item'; 
    });
});
