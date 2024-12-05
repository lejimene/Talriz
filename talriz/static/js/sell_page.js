function toggleAuctionFields() {
    const auctionFields = document.getElementById("auction_fields");
    const priceInput = document.getElementById("item_price");
    const bidAmountInput = document.getElementById("id_bid_amount");
    const auctionEndDateInput = document.getElementById("auction_end_date");
    const auctionEndTimeInput = document.getElementById("auction_end_time");
    const isAuction = document.getElementById("is_auction").checked;

    // Toggle auction fields visibility
    auctionFields.style.display = isAuction ? "block" : "none";


    if (isAuction) {
        // Auction mode: Require auction fields, clear price field
        priceInput.removeAttribute("required");
        priceInput.value = ''; // Clear the price input
        bidAmountInput.setAttribute("required", "required");
        auctionEndDateInput.setAttribute("required", "required");
    } else {
        // Price mode: Require price, clear auction fields
        priceInput.setAttribute("required", "required");
        bidAmountInput.removeAttribute("required");
        auctionEndDateInput.removeAttribute("required");
        auctionEndTimeInput.value = ''; // Clear optional fields
        bidAmountInput.value = '';
    }
}

function validateForm(event) {
    const priceInput = document.getElementById("item_price");
    const bidAmountInput = document.getElementById("id_bid_amount");
    const auctionEndDateInput = document.getElementById("auction_end_date");
    const isAuction = document.getElementById("is_auction").checked;

    // Validate price input
    if (!isAuction && (!priceInput.value || parseFloat(priceInput.value) <= 0)) {
        alert("Please enter a valid price.");
        event.preventDefault();
        return false;
    }

    // Validate auction fields if auction is selected
    if (isAuction) {
        if (!bidAmountInput.value || parseFloat(bidAmountInput.value) <= 0) {
            alert("Please enter a valid starting bid.");
            event.preventDefault();
            return false;
        }

        if (!auctionEndDateInput.value) {
            alert("Please select an auction end date.");
            event.preventDefault();
            return false;
        }
    }

    return true; // Allow form submission
}

function combineAuctionDateTime() {
    var auctionDate = document.getElementById("auction_end_date").value;
    var auctionTime = document.getElementById("auction_end_time").value;

    // Combine date and time into ISO format for backend processing
    if (auctionDate && auctionTime) {
      var auctionDateTime = new Date(auctionDate + "T" + auctionTime); // Combine date and time

      // Set the combined datetime value to the hidden input field
      document.getElementById("auction_end_datetime").value = auctionDateTime.toISOString();
    }
}

// Trigger the combine function when the form is submitted
document.querySelector("form").addEventListener("submit", combineAuctionDateTime);

// Attach event listeners for auction fields visibility and form validation
document.getElementById("is_auction").addEventListener("change", toggleAuctionFields);
document.querySelector("form").addEventListener("submit", validateForm);

document.addEventListener("DOMContentLoaded", () => {
    const darkModeState = localStorage.getItem("darkmode");
    if (darkModeState === "disabled") {
        document.body.classList.add("dark-mode"); // Apply dark mode class
    }
    else{
        document.body.classList.remove("dark-mode"); // Apply dark mode class
    }

    // Listen for changes to the dark mode state
    window.addEventListener("storage", (event) => {
        if (event.key === "darkmode_updated") {
            const updatedDarkModeState = localStorage.getItem("darkmode");
            if (updatedDarkModeState === "enabled") {
                document.body.classList.add("dark-mode");
            } else {
                document.body.classList.remove("dark-mode");
            }
        }
    });

});

