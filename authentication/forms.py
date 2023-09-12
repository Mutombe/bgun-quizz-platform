from django import forms
from .models import UserProfile, Category

class UserProfileForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['interests'].initial = self.instance.interests.all()

    class Meta:
        model = UserProfile
        fields = ['location', 'email', 'interests']