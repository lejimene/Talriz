document.addEventListener("DOMContentLoaded", () => {
  // Like button logic
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

  // Image navigation logic
  const imageContainers = document.querySelectorAll(".Images_section");

  imageContainers.forEach((container) => {
    const prevButton = container.querySelector(".prev-button");
    const nextButton = container.querySelector(".next-button");
    const imageElement = container.querySelector("img");

    if (!imageElement || !prevButton || !nextButton) return; // Ensure all elements exist

    // Extract counter and corresponding image URLs
    const counter = prevButton.id.split("-")[1]; // Safe assumption based on ID format
    const imageUrlsElement = document.getElementById(`image-urls-${counter}`);

    if (!imageUrlsElement) return; // Skip if no URLs element
    const imageUrls = imageUrlsElement.textContent.trim().split(",").map((url) => url.trim());

    if (imageUrls.length === 0) return; // Skip if no URLs available

    // Initialize index and update function
    let currentIndex = 0;

    function updateImage(index) {
      if (index >= 0 && index < imageUrls.length) {
        imageElement.src = imageUrls[index];
      }
    }

    // Add click handlers for navigation
    prevButton.addEventListener("click", () => {
      currentIndex = currentIndex === 0 ? imageUrls.length - 1 : currentIndex - 1;
      updateImage(currentIndex);
    });

    nextButton.addEventListener("click", () => {
      currentIndex = currentIndex === imageUrls.length - 1 ? 0 : currentIndex + 1;
      updateImage(currentIndex);
    });
  });

  // Auction overlay logic
  const contactButtons = document.querySelectorAll("#contactButton");
  const auctionOverlay = document.getElementById("auctionOverlay");
  const closeButton = document.getElementById("closeButton");
  const joinAuctionButton = document.getElementById("joinAuctionButton");

  // Function to open overlay
  function openOverlay() {
    auctionOverlay.classList.remove("hidden");
    loadAuctionDetails();
  }

  // Function to close overlay
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
  contactButtons.forEach((button) => button.addEventListener("click", openOverlay));
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

  // Buy button logic
  document.querySelectorAll(".buy_button").forEach((button) => {
    button.addEventListener("click", function () {
      const itemId = this.dataset.itemId; // Get item ID directly from the button
  
      fetch(`/buy/${itemId}/`, { // Fix the URL path to match the Django route
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
            alert("Item purchased successfully!");
            // Update the item status visually
            this.disabled = true;
            this.textContent = "Purchased";
          } else {
            alert(data.error || "Failed to purchase the item.");
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });
});
