from django import forms

class NewTransactionForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'span6', 'rows': 5}), required=False)

class NewOfferForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'span6', 'rows': 5}), required=False)
