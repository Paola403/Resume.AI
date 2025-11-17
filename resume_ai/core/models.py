from django.db import models

class resume_ai(models.Model):
    nome_completo = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nome_completo} - {self.email}"
