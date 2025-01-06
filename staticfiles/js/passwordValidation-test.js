document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.querySelector("#id_password1"); 
    const lengthRequirement = document.querySelector("#length");
    const numericRequirement = document.querySelector("#numeric");
    const specialRequirement = document.querySelector("#special");

    passwordInput.addEventListener("input", function () {
        const value = passwordInput.value;

        // Validate length
        if (value.length >= 8) {
            lengthRequirement.classList.add("valid");
            lengthRequirement.classList.remove("invalid");
        } else {
            lengthRequirement.classList.add("invalid");
            lengthRequirement.classList.remove("valid");
        }

        // Validate non-numeric
        if (!/^\d+$/.test(value)) {
            numericRequirement.classList.add("valid");
            numericRequirement.classList.remove("invalid");
        } else {
            numericRequirement.classList.add("invalid");
            numericRequirement.classList.remove("valid");
        }

        // Validate special character
        if (/[!@#$%^&*(),.?":{}|<>]/.test(value)) {
            specialRequirement.classList.add("valid");
            specialRequirement.classList.remove("invalid");
        } else {
            specialRequirement.classList.add("invalid");
            specialRequirement.classList.remove("valid");
        }
    });
});
