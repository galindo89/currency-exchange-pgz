document.addEventListener("DOMContentLoaded", function () {
    const deleteModal = document.getElementById("deleteConfirmationModal");
    const deleteForm = document.getElementById("deleteOfferForm");

    deleteModal.addEventListener("show.bs.modal", function (event) {
        
        const button = event.relatedTarget;
        
        const action = button.getAttribute("data-action");
        
        deleteForm.setAttribute("action", action);
    });
});