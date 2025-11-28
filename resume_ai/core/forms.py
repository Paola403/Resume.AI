from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CadastroForm(UserCreationForm):
    
    nome_completo = forms.CharField(max_length=150, required=True)
    telefone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "nome_completo",
            "telefone",
            "password1",
            "password2",
        ]

    # Validação de email único
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    # Salvando todos os campos
    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.nome_completo = self.cleaned_data["nome_completo"]
        user.telefone = self.cleaned_data["telefone"]

        if commit:
            user.save()

        return user
    
# ------------------------------------------------------------------------------------------------------------

# Atualização de dados do usuário
class UpdateUserForm(forms.ModelForm):
        # Sobrescreve o campo para remover validação nativa
    username = forms.CharField(
        required=True,
        label="Nome de Usuário",
        max_length=150,
        strip=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    
    class Meta:
        model = User
        fields = ['username', 'nome_completo', 'telefone', 'email']

       # Remove help_text e limitações automáticas do Django
        help_texts = {
            'username': '',
            'email': '',
        }
    def clean_email(self):
        email = self.cleaned_data['email']
        user_id = self.instance.id  # Usuário atual

        if not email or email.strip() == "":
            raise forms.ValidationError("Campo obrigatório vazio.")

        # Verifica se existe outro usuário com este email
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError("Este e-mail já está em uso por outro usuário.")

        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username or username.strip() == "":
            raise forms.ValidationError("Campo obrigatório vazio.")

        return username

