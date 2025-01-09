document.addEventListener("DOMContentLoaded", function () {
    const deleteModal = document.getElementById("deleteConfirmationModal");
    const deleteForm = document.getElementById("deleteForm");

    deleteModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget; 
        const actionUrl = button.getAttribute("data-action"); 
        deleteForm.setAttribute("action", actionUrl); 
    });
});