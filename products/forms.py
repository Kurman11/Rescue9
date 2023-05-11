from django import forms
from .models import Product, Review, Review_image


category_choices = (
    ('음료', '음료'),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
)
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'hits', 'photo', 'is_new', 'content')
    name = forms.CharField(
        label='name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id' : 'name',
                'placeholder' : '상품명을 입력해주세요.',
            }
        )
    )

    category = forms.ChoiceField(
        label='category',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id' : 'category',
                'placeholder' : '분류',
            }
        ),
        choices=category_choices,
    )

    hits = forms.IntegerField(
        label='hits',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'id' : 'hits',
            }
        )
    )
    photo = forms.ImageField(
        label='photo',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'id' : 'photo',
            }
        )
    )
    is_new = forms.BooleanField(
        label='is_new',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id' : 'is_new',
            }
        )
    )
    content = forms.CharField(
        label='content',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id' : 'content',
            }
        )
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields =('content', 'rating',)

    content = forms.CharField(
        widget = forms.TextInput(
            attrs= {
                'class' : 'form-control',
                'style' : 
                    'width: 100%; outline: 1px solid #e0e0e0; border:1px solid #ffffff; border-radius:5px; padding:1rem;', 
                'placeholder' : '댓글을 입력해주세요!'
            }
        )
    )
    
    rating = forms.IntegerField(
        label='rating',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'style' : 
                    'width: 90%; outline: 1px solid #e0e0e0; border:1px solid #ffffff; border-radius:5px; padding:0.5rem; min-width: 100px;', 
                'id' : 'rating',
            }
        )
    )


class Review_imageForm(forms.ModelForm):
    class Meta:
        model = Review_image
        fields='__all__'
    image = forms.ImageField(
        label='image',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'id' : 'image',
            }
        )
    )

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
        attrs={'class': 'form-control'}))
    
    class Meta:
        model = Review_image
        fields = ('image',)


