from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name','image', 'description',  'price', 'buy_out_price', 'auction_end_date']
