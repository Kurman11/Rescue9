from django import forms
from .models import Recipe, Comment


class RecipeForm(forms.ModelForm):
    category = forms.ChoiceField(
        label='카테고리',
        widget=forms.Select(
            attrs={
                'placeholder': '카테고리 선택',
                'class': 'form-select',
            }
        ),
        choices = (
            ('', ''), ('', ''), 
            ('', ''), ('', ''), 
            ('', ''), ('', ''),
        ),
        required=True,
    )

    class Meta:
        model = Recipe
        exclude = ('like_users', 'hits')

        labels = {
            'title': '레시피 명',
        }
        widget = {
            'title': forms.TextInput(attrs={'class': 'form-control w-75'}),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='댓글 입력',
        widget=forms.TextInput(
            attrs={
                'placeholder': '댓글 입력칸',
                'class': 'form-control'
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ('content',)


class CommentImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='레시피 이미지 업로드',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'multiple': True,
            },
        ),
        required=False,
    )
    class Meta:
        model = CommentImage
        fields = ('image',)