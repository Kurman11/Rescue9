from django import forms
from .models import Product, Comment, ConvenienceStore
from taggit.forms import TagField, TagWidget
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, MaxValueValidator


category_choices = (
    ('간편식사', '간편 식사'),
    ('과자류', '과자류'),
    ('냉동식품', '냉동 식품'),
    ('식재료', '식재료'),
    ('빵', '빵'),
    ('아이스크림', '아이스크림'),
    ('음료', '음료'),
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','price','convenience_stores' ,'category', 'photo', 'is_new', 'content','tags',)
        widgets = {
            'tags':TagWidget(
                attrs={
                    'class': 'form-control', 
                    'placeholder': '콤마로 구분하여 입력해주세요',
                }
            ),        
        }
        help_texts = {
            'tags': '콤마로 구분하여 입력해주세요',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].label = '태그'

    name = forms.CharField(
        label='제품 이름',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id' : '제품 이름',
                'placeholder' : '상품명을 입력해주세요',
            }
        )
    )

    category = forms.ChoiceField(
        label='카테고리',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id' : 'category',
                'placeholder' : '분류',
            }
        ),
        choices=category_choices,
    )

    convenience_stores = forms.ModelMultipleChoiceField(
        label='편의점 선택',
        widget=forms.CheckboxSelectMultiple(attrs={'placeholder': '분류'}),
        queryset=ConvenienceStore.objects.all(),
    )


    price = forms.IntegerField(
        label='제품 가격',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'id' : 'price',
                'step': '50',
            }
        )
    )

    photo = forms.ImageField(
        label='제품 사진 첨부',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'id' : 'photo',
            }
        )
    )
    is_new = forms.BooleanField(
        label='신제품 여부',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id' : 'is_new',
            }
        )
        ,required=False,
    )
    content = forms.CharField(
        label='제품 설명',
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
                'placeholder' : '댓글을 입력해주세요!'
            }
        )
    )


