from django import forms
from django.forms import ModelForm
from .models import Listing
from djmoney.forms.fields import MoneyField

class AddListing(forms.Form):
    title = forms.CharField(label='Title', max_length=20, required= True,widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    text = forms.CharField(label = 'Description', max_length= 100, required=True, widget=forms.Textarea(attrs={'rows':4,'class':'form-control form-control-sm','placeholder':'Describe within 100 alphabets'}))
    category = forms.CharField(label = 'Category', max_length=20, required=True, widget=forms.TextInput(attrs={'class': "form-control form-control-sm",'placeholder':'Type to search'}))
    bs_bid = MoneyField(label= 'Base Bid', max_digits=19, decimal_places=2, default_currency='BDT', required=True)
    img = forms.ImageField(label='Add Image', required=False)

class BidForm(forms.Form):
    amount = MoneyField(label='Bid Amount', max_digits=19, decimal_places=2, default_currency='BDT',required=False,min_value=1)
    watchlist = forms.BooleanField(label='Add to watchlist',required=False)
    remove_watchlist = forms.BooleanField(label='Remove from watchlist', required=False)
class UpdateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['active']