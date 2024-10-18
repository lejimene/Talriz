function toggleAuctionFields() {
    const auctionFields = document.getElementById("auction_fields");
    const priceLabel = document.getElementById("price_label");
    const itemPriceInput = document.getElementById("item_price");
    const isAuction = document.getElementById("is_auction").checked;

    auctionFields.style.display = isAuction ? "block" : "none"; // Show/hide auction fields
    itemPriceInput.style.display = isAuction ? "none" : "block"; // Hide price input if auction
    priceLabel.style.display = isAuction ? "none" : "block"; // Hide price label if auction
}

function validateForm(event) {
    const priceInput = document.getElementById("item_price");
    const startingBidInput = document.getElementById("starting_bid");
    const buyOutInput = document.getElementById("buy_out");
    const isAuction = document.getElementById("is_auction").checked;

    // Check if price inputs are valid numbers (skip if auction)
    if (!isAuction && priceInput.value < 0) {
        alert("Price must be a positive number.");
        event.preventDefault();
        return false;
    }

    if (startingBidInput.value < 0 && isAuction) {
        alert("Starting bid must be a positive number.");
        event.preventDefault();
        return false;
    }

    // Validate Buy Out Price if provided
    if (buyOutInput.value && (buyOutInput.value < 0 || !Number.isInteger(Number(buyOutInput.value)))) {
        alert("Buy Out Price must be a positive integer.");
        event.preventDefault();
        return false;
    }

    // Check if auction end date is selected
    const auctionEndDateInput = document.getElementById("auction_end_date");
    if (isAuction && !auctionEndDateInput.value) {
        alert("Please select an auction end date.");
        event.preventDefault();
        return false;
    }

    return true; // If all validations pass
}

// Attach the validateForm function to the form's submit event
document.querySelector('form').addEventListener('submit', validateForm);
