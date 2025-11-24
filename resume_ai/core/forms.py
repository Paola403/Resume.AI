
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CadastroForm(UserCreationForm):
    # Campos adicionais não presentes no UserCreationForm nativo
    nome_completo = forms.CharField(label='Nome Completo', max_length=100)
    telefone = forms.CharField(label='Telefone', max_length=15, required=False) # Opcional

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'nome_completo', 'telefone')

    def save(self, commit=True):
        user = super().save(commit=False)
        
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        
        if commit:
            user.save()
        return user