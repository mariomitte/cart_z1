from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(required=False, initial=1)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity is None:
            return self.fields['quantity'].initial
        return quantity
