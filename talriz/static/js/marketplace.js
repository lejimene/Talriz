document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".like_button").forEach((button) => {
    button.addEventListener("click", function () {
      const itemId = this.dataset.itemId;
      fetch(`/like-item/${itemId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data.error) {
            this.textContent = data.liked ? "Unlike" : "Like";
            document.getElementById(
              `like-count-${itemId}`
            ).textContent = `Likes: ${data.likes_count}`;
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });


  const imageContainers = document.querySelectorAll(".Images_section");
  imageContainers.forEach((container) => {
    const counter = container.querySelector('.prev-button').getAttribute('id').split('-')[1];
    const imageUrls = document.getElementById(`image-urls-${counter}`).textContent.trim().split(',');
    const imageElement = document.getElementById(`current-image-${counter}`);
    let currentIndex = 0;

    function updateImage(index) {
      imageElement.src = imageUrls[index].trim(); // Use .trim() to remove any extra spaces
    }

    container.querySelector(`.prev-button`).addEventListener('click', function () {
      currentIndex = (currentIndex === 0) ? imageUrls.length - 1 : currentIndex - 1;
      updateImage(currentIndex);
    });

    container.querySelector(`.next-button`).addEventListener('click', function () {
      currentIndex = (currentIndex === imageUrls.length - 1) ? 0 : currentIndex + 1;
      updateImage(currentIndex);
    });
  });
});