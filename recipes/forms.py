from django import forms
from .models import Recipe, Comment, CommentImage
from django_ckeditor_5.widgets import CKEditor5Widget





class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["content"].required = False

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
            },
        ),
        required=False,
    )

    class Meta:
        model = CommentImage
        fields = ('image',)
