from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CadastroForm(UserCreationForm):
    nome_completo = forms.CharField(max_length=150, required=True)
    telefone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ["username", 
                  "email", 
                  "nome_completo", 
                  "telefone", 
                  "password1", 
                  "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        
        if commit:
            user.save()
        return user
