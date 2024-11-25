from django import forms
from .models import Item, ItemImage
from datetime import datetime


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'is_auction', 'bid_amount', 'buy_out_price']

    # Add status as a hidden field ??  Might be able to remove since its already there in the html
    status = forms.CharField(widget=forms.HiddenInput(), initial='active')

    def clean(self):
        cleaned_data = super().clean()
        is_auction = cleaned_data.get('is_auction')
        bid_amount = cleaned_data.get('bid_amount')
        price = cleaned_data.get('price')

        if is_auction:
            # Validate bid amount and price for auction items
            if not bid_amount:
                self.add_error('bid_amount', "Starting bid amount is required for auction items.")
            elif bid_amount <= 0:
                self.add_error('bid_amount', "Bid amount must be greater than zero.")
        else:
            # Validate price for non-auction items
            if price is None or price <= 0:
                self.add_error('price', "Price must be greater than zero for non-auction items.")

        return cleaned_data
    
class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']