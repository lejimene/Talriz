from django import forms
from .models import Item, ItemImage


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description',  'price', 'buy_out_price', 'auction_end_date']


class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']