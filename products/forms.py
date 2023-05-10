from django import forms
from .models import Product, Review, Review_image

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'hits', 'photo', 'is_new', 'content')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields ='__all__'


class Review_imageForm(forms.ModelForm):
    class Meta:
        model = Review_image
        fields='__all__'

# class Review_imageForm(forms.ModelForm):
#     class Meta:
#         model = Review_image
#         fields = ('image',)
#         widgets = {
#             'image': forms.ClearableFileInput(attrs={'multiple': True}),
#         }
#         labels = {
#             'image': 'Upload Images',
#         }
#         help_texts = {
#             'image': 'Upload review images (Optional)',
#         }
#         enctype = 'multipart/form-data'


class Review_imageForm(forms.ModelForm):
    image = forms.ImageField(label='옵션1 이미지', label_suffix='', required=False, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control-file'}))
    class Meta:
        model = Review_image
        fields = ('image',)


