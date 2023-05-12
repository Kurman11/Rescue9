from django import forms
from .models import Product, Comment
from taggit.forms import TagField, TagWidget
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, MaxValueValidator


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
        fields = ('name','price', 'category', 'photo', 'is_new', 'content','tags',)
        widgets = {
            'tags':TagWidget(attrs={'class': 'form-control', 'placeholder': "콤마 구분"}),
            
        }
        help_texts = {
            'tags': '콤마로 구분',
        }
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

    # hits = forms.IntegerField(
    #     label='hits',
    #     widget=forms.NumberInput(
    #         attrs={
    #             'class': 'form-control',
    #             'id' : 'hits',
    #         }
    #     )
    # )

    price = forms.IntegerField(
        label='price',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'id' : 'price',
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
        ,required=False,
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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =('content',)

    content = forms.CharField(
        widget = forms.TextInput(
            attrs= {
                'class' : 'form-control',
                'style' : 
                    'width: 100%; outline: 1px solid #e0e0e0; border:1px solid #ffffff; border-radius:5px; padding:1rem;', 
                'placeholder' : '리뷰을 입력해주세요!'
            }
        )
    )


