from django import forms


class createListingForm(forms.Form):
    title = forms.CharField(label = "Title",max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label = "Description", widget=forms.TextInput(attrs={'cols':40,'rows':20,'class':'form-control'}))
    category = forms.CharField(label="Category", max_length=64,required=False ,widget=forms.TextInput(attrs={'class': 'form-control'}))
    bid = forms.FloatField(label = "Bid",widget=forms.NumberInput(attrs={'class': 'form-control'}))
    url = forms.URLField(label = "Image URL" , required = False,widget=forms.URLInput(attrs={'class': 'form-control'}))
