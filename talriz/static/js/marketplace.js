    const socket = new WebSocket('ws://' + window.location.host + '/ws/chat/');
    socket.onmessage = function (ws_message) {
          const message = JSON.parse(ws_message.data);
          let Likes = message["Likes"]
          let item_id = message["item_id"]
          document.getElementById(
            `like-count-${item_id}`
          ).innerText = `Likes: ${Likes}`
          request = new XMLHttpRequest();
          request.open("POST", "/submit-likes/");

          csrf_token = "";
          for (let cookie of document.cookie.split("; ")) {
          let [key, value] = cookie.split("=");
              if (key === "csrftoken") {
                  csrf_token = value;
              }
          }
          request.setRequestHeader("X-CSRFToken", csrf_token);
          request.send(JSON.stringify(message));
        }

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
            socket.send(JSON.stringify({"Likes": data.likes_count, "item_id": itemId }));
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
      // Check the current dark mode state
    const currentMode = localStorage.getItem("darkmode");

    // Toggle dark mode state based on current value
    if (currentMode === "enabled") {
        document.body.classList.remove("dark-mode"); // Remove dark mode
        localStorage.setItem("darkmode", "disabled"); // Save state
    } else {
        document.body.classList.add("dark-mode"); // Enable dark mode
        localStorage.setItem("darkmode", "enabled"); // Save state
    }

    // Communicate the change to other pages
    window.localStorage.setItem("darkmode_updated", Date.now());
    console.log('Button clicked');
    toggleDarkMode();
  });

  let top_bidder = "Nobody";
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
                        const header = document.querySelector(`#header-${itemId}`);

                        // Update the UI or reload the page as needed
                        alert("Bid successfully submitted!");
                         const buyout = document.querySelector(`#buyout-${itemId}`);
                         const buyoutText = buyout.textContent || buyout.innerText;
                         const dollarIdx = buyoutText.indexOf('$');
                         const buyoutAmountString = buyoutText.substring(dollarIdx + 1)
                         const buyoutAmount = parseInt(buyoutAmountString, 10);
                        if(bidValue >= buyoutAmount){
                            header.textContent = `Winner: ${data['winner']}`
                            input.replaceWith(document.createTextNode(`Final Winning Bid: $${bidValue}`));
                            submitButton.remove();
                            const buyButton = document.querySelector(`#buyButton-${itemId}`);
                            buyButton.style.display = "none";

                        }
                        else{
                            header.textContent = `Current Bid: $${bidValue}`
                            input.replaceWith(document.createTextNode(`Bid Placed: $${bidValue}`));
                            submitButton.remove();
                        }
                        top_bidder = data['winner'];
                    } else {
                        alert(data.error || "Failed to submit the bid.");
                    }
                })
                .catch((error) => console.error("Error:", error));
            });
        });
    });

   // Auction time calculation
  function updateCountdown() {
      const auctionTimers = document.querySelectorAll(".auction-timer");
      auctionTimers.forEach((timer) => {
          const itemId = timer.dataset.itemId;
          const endTime = new Date(timer.dataset.endTime);
          const now = new Date();
          const timeLeft = endTime - now;

          if (timeLeft > 0) {
              const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
              const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
              const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
              const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

              timer.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;

              // Debugging log
              console.log(`Timer updated: ${timer.innerHTML}`);
          } else {
              fetch(`/end-auction/${itemId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                        "Content-Type": "application/json",
                    },
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (!data.error) {
                            timer.innerHTML = `Auction ended.`;
                            const header = document.querySelector(`#header-${itemId}`);
                            const bidButton = document.querySelector(`#bidButton-${itemId}`);
                            const buyButton = document.querySelector(`#buyButton-${itemId}`);
                             const bidText = header.textContent || header.innerText;
                             const dollarIdx = bidText.indexOf('$');
                             const bidAmountString = bidText.substring(dollarIdx + 1)
                             const bidValue = parseInt(bidAmountString, 10);
                            bidButton.replaceWith(document.createTextNode(`Final Winning Bid: $${bidValue}`))
                            header.textContent = ` Winner: ${data['winner']}`;
                            buyButton.style.display = "none";


                        }
                    })
                    .catch((error) => console.error("Error ending auction:", error));

          }
      });
  }
  setInterval(updateCountdown, 1000);



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
            this.textContent = `Purchased by ${data['winner']}`;
          } else {
            alert(data.error || "Failed to purchase the item.");
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });
});
