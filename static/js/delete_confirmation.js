document.addEventListener("DOMContentLoaded", function () {
    const deleteForms = document.querySelectorAll(".delete-form");

    deleteForms.forEach(form => {
        form.addEventListener("submit", function (event) {
            const confirmMessage = this.querySelector("button[data-confirm]").getAttribute("data-confirm");
            if (!confirm(confirmMessage)) {
                event.preventDefault(); // Prevent form submission if the user cancels
            }
        });
    });
});