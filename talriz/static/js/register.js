document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const registerContainer = document.querySelector(".Register_box");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent form from submitting traditionally

        const formData = new FormData(form);

        const response = await fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
            },
            body: formData,
        });

        const result = await response.json();

        // Remove any existing error messages
        const errorBox = document.getElementById("error-box");
        //if (errorBox) errorBox.remove();

        if (!response.ok) {
            //const errorMessage = document.createElement("p");
            //errorMessage.id = "error-box";
            errorBox.textContent = result.error;
            errorBox.style.color = "red";
            errorBox.style.textAlign = "center";
            errorBox.style.display = "block";
            //registerContainer.insertBefore(errorBox, form); // Insert above the form
        } else {
            const redirectUrl = form.getAttribute("data-redirect-url");
            window.location.href = redirectUrl; // Redirect on success
        }
    });
});
