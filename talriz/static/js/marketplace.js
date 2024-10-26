document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".like_button").forEach(button => {
    button.addEventListener("click", function() {
      const itemId = this.dataset.itemId;
      fetch(`/like-item/${itemId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({})
      })
        .then(response => response.json())
        .then(data => {
          if (!data.error) {
            this.textContent = data.liked ? "Unlike" : "Like";
            document.getElementById(`like-count-${itemId}`).textContent = `Likes: ${data.likes_count}`;
          }
        })
        .catch(error => console.error("Error:", error));
    });
  });
});
