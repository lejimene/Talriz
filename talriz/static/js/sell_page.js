function toggleAuctionFields() {
    const auctionFields = document.getElementById("auction_fields");
    const priceInput = document.getElementById("item_price");
    const startingBidInput = document.getElementById("starting_bid");
    const auctionEndDateInput = document.getElementById("auction_end_date");
    const isAuction = document.getElementById("is_auction").checked;

    // Toggle auction fields visibility
    auctionFields.style.display = isAuction ? "block" : "none";

    if (isAuction) {
        // Auction mode: Remove "required" from price and add "required" to auction fields
        priceInput.removeAttribute("required");
        startingBidInput.setAttribute("required", "required");
        auctionEndDateInput.setAttribute("required", "required");

        // Clear the price input value to avoid accidental submission
        priceInput.value = '';
    } else {
        // Price mode: Add "required" to price and remove "required" from auction fields
        priceInput.setAttribute("required", "required");
        startingBidInput.removeAttribute("required");
        auctionEndDateInput.removeAttribute("required");

        // Clear auction-specific input values to avoid accidental submission
        startingBidInput.value = '';
        auctionEndDateInput.value = '';
        document.getElementById("buy_out").value = '';
        document.getElementById("auction_end_time").value = '';
    }
}

function validateForm(event) {
    const priceInput = document.getElementById("item_price");
    const startingBidInput = document.getElementById("starting_bid");
    const buyOutInput = document.getElementById("buy_out");
    const auctionEndDateInput = document.getElementById("auction_end_date");
    const isAuction = document.getElementById("is_auction").checked;

    // Price validation if auction is not selected
    if (!isAuction && (!priceInput.value || priceInput.value <= 0)) {
        alert("Please enter a valid price.");
        event.preventDefault();
        return false;
    }

    // Auction validation
    if (isAuction) {
        if (!startingBidInput.value || startingBidInput.value <= 0) {
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

    return true; // Allow form submission if all validations pass
}

// Attach event listeners
document.getElementById("is_auction").addEventListener("change", toggleAuctionFields);
document.querySelector("form").addEventListener("submit", validateForm);
