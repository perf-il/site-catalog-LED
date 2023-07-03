from django import forms

from catalog.models import Product, ProductVersion


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    forbidden_list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = '__all__'

    def clean_description(self, forbidden_lists=forbidden_list):

        cleaned_data = self.cleaned_data['description']
        for word in forbidden_lists:
            if word in cleaned_data:
                raise forms.ValidationError('Недопустимое описание')
        return cleaned_data

    def clean_name(self, forbidden_lists=forbidden_list):

        cleaned_data = self.cleaned_data['name']
        for word in forbidden_lists:
            if word in cleaned_data:
                raise forms.ValidationError('Недопустимое название')
        return cleaned_data


class ProductVersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = ProductVersion
        fields = '__all__'
