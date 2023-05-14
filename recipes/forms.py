from django import forms
from .models import Recipe, Review
from django_ckeditor_5.widgets import CKEditor5Widget
from products.models import Product




class RecipeForm(forms.ModelForm):
    used_products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}),
        label='사용된 제품',
        required=False
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["content"].required = False
        self.fields['used_products'].label_from_instance = lambda obj: obj.name

    category = forms.ChoiceField(
        label='카테고리',
        widget=forms.Select(
            attrs={
                'placeholder': '카테고리 선택',
                'class': 'form-select',
            }
        ),
        choices = (
            ('라면', '라면'), ('', ''), 
            ('', ''), ('', ''), 
            ('', ''), ('', ''),
        ),
        required=True,
    )

    class Meta:
        model = Recipe
        exclude = ('user', 'like_users', 'hits',)
        labels = {
            'title': '레시피 명',
        }
        widget = {
            'title': forms.TextInput(attrs={'class': 'form-control w-75'}),
        }

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if commit:
            recipe.save()
            self.save_m2m()  # recipe 저장 후에 save_m2m() 메소드 호출
        return recipe



class ReviewForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '댓글 입력칸',
                'class': 'recipe__comment__input-area--form'
            }
        ),
    )

# 아래 CommentImageForm 내용을 옮겼습니다. 수정/삭제 하셔도 상관 없습니다.
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'd-none',
                'id': 'input-commentimage'
            },
        ),
        required=False,
    )

# 일단 products에서 사용하던거 그대로 넣었습니다 안쓰신다면 그냥 지우셔도 상관 없습니다.
    rating = forms.IntegerField(
        label='rating',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'style' : 
                    'width: 90%; outline: 1px solid #e0e0e0; border:1px solid #ffffff; border-radius:5px; padding:0.5rem; min-width: 100px;', 
                'id' : 'rating',
                'min': 1,
                'max': 5,
                'value':1,
            }
        )
    )

    class Meta:
        model = Review
        fields = ('content','image',)



# class CommentImageForm(forms.ModelForm):
#     image = forms.ImageField(
#         widget=forms.ClearableFileInput(
#             attrs={
#                 'class': 'd-none',
#                 'id': 'input-commentimage'
#             },
#         ),
#         required=False,
#     )

#     class Meta:
#         model = CommentImage
#         fields = ('image',)
