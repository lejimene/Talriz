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
  // const contactButtons = document.querySelectorAll("#contactButton");
  // const auctionOverlay = document.getElementById("auctionOverlay");
  // const closeButton = document.getElementById("closeButton");
  // const joinAuctionButton = document.getElementById("joinAuctionButton");

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
  // Function to toggle dark mode
  function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle('dark-mode');  // Toggle the dark mode class

    // Save the user's theme preference in localStorage
    if (body.classList.contains('dark-mode')) {
      localStorage.setItem('theme', 'dark');
    } else {
      localStorage.setItem('theme', 'light');
    }
  }

  // Check if the user has a saved theme preference in localStorage
  window.onload = function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      document.body.classList.add('dark-mode');
    }
  };

  // Add the event listener to the button
  document.getElementById('theme-toggle-button').addEventListener('click', () => {
    console.log('Button clicked');
    toggleDarkMode();
  });

  // Auction Bid Functionality
  document.querySelectorAll(".bid_button").forEach((button) => {
    button.addEventListener("click", function () {
        const itemId = this.dataset.itemId; // Get item ID directly from the button

        // Replace the button with an input field and a submit button
        const input = document.createElement("input");
        input.type = "number";
        input.min = "0";
        input.placeholder = "Enter bid";
        input.classList.add("bid_input");

        const submitButton = document.createElement("button");
        submitButton.textContent = "Submit";
        submitButton.classList.add("submit_button");

        // Replace the current button with the input and submit button
        this.replaceWith(input, submitButton);

        // Add functionality to the submit button
        submitButton.addEventListener("click", function () {
            const bidValue = parseFloat(input.value);
            if (isNaN(bidValue) || bidValue <= 0) {
                alert("Please enter a valid bid amount.");
                return;
            }

            fetch(`/submit-bid/${itemId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ bid: bidValue }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (!data.error) {
                        alert("Bid successfully submitted!");
                        // Update the UI or reload the page as needed
                        const header = document.querySelector(`#header-${itemId}`);
                        header.textContent = `Current Bid: $${bidValue}`
                        input.replaceWith(document.createTextNode(`Bid Placed: $${bidValue}`));
                        submitButton.remove();
                    } else {
                        alert(data.error || "Failed to submit the bid.");
                    }
                })
                .catch((error) => console.error("Error:", error));
            });
        });
    });



  // // Event listeners for buttons
  // contactButtons.forEach((button) => button.addEventListener("click", openOverlay));
  // closeButton.addEventListener("click", closeOverlay);
  // joinAuctionButton.addEventListener("click", () => {
  //   alert("You have joined the auction!");
  //   closeOverlay();
  // });

  // // Close overlay when clicking outside the modal content
  // auctionOverlay.addEventListener("click", (event) => {
  //   if (event.target === auctionOverlay) {
  //     closeOverlay();
  //   }
  // });

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
