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


// Below is the Auction details stuff this NEEDS REVISING ONLY FOR TESTING 
// DOES NOT LOAD ANYTHING USEFUL
// This means handlin 

document.addEventListener("DOMContentLoaded", () => {
  const contactButtons = document.querySelectorAll("#contactButton");
  const auctionOverlay = document.getElementById("auctionOverlay");
  const closeButton = document.getElementById("closeButton");
  const joinAuctionButton = document.getElementById("joinAuctionButton");

  // Function to open the overlay
  function openOverlay() {
    auctionOverlay.classList.remove("hidden");
    loadAuctionDetails();
  }

  // Function to close the overlay
  function closeOverlay() {
    auctionOverlay.classList.add("hidden");
  }

  // Load dynamic auction details (placeholder function for now)
  function loadAuctionDetails() {
    const auctionDetails = document.getElementById("auctionDetails");
    // Replace this with actual dynamic data loading in the future
    auctionDetails.innerHTML = `
      <p>Auction for this item will start soon!</p>
      <p>Starting bid: $100</p>
      <p>Number of participants: 5</p>
    `;
  }

  // Event listeners for buttons
  contactButtons.forEach((button) =>
    button.addEventListener("click", openOverlay)
  );
  closeButton.addEventListener("click", closeOverlay);
  joinAuctionButton.addEventListener("click", () => {
    alert("You have joined the auction!");
    closeOverlay();
  });

  // Close overlay when clicking outside the modal content
  auctionOverlay.addEventListener("click", (event) => {
    if (event.target === auctionOverlay) {
      closeOverlay();
    }
  });
});
