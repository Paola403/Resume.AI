from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):
    # Sobrescrevendo o username para remover validações restritivas
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nome de Usuário"
    )

    nome_completo = models.CharField(max_length=150, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    nome_exibicao = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.nome_exibicao or self.username

    



class PDFHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historicos')
    arquivo = models.FileField(upload_to='pdfs/')
    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.arquivo.name




