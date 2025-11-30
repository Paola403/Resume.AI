from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import PasswordResetCode, PDFHistory

User = get_user_model()


class UserFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="paola",
            email="paola@example.com",
            password="senha123"
        )

    # -------------------------------
    # TESTE DE CADASTRO
    # -------------------------------
    def test_register_user(self):
        response = self.client.post(reverse("register"), {
            "username": "novo_user",
            "email": "novo@example.com",
            "password1": "SenhaForte123",
            "password2": "SenhaForte123",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="novo_user").exists())

    # -------------------------------
    # TESTE DE LOGIN
    # -------------------------------
    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "username": "paola",
            "password": "senha123"
        })

        self.assertEqual(response.status_code, 302)

    # -------------------------------
    # TESTE DE LOGIN FALHO
    # -------------------------------
    def test_login_fail(self):
        response = self.client.post(reverse("login"), {
            "username": "paola",
            "password": "senha_errada"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credenciais inválidas")

    # -------------------------------
    # TESTE DE LOGOUT
    # -------------------------------
    def test_logout(self):
        self.client.login(username="paola", password="senha123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    # -------------------------------
    # TESTE ALTERAÇÃO DE DADOS
    # -------------------------------
    def test_update_profile(self):
        self.client.login(username="paola", password="senha123")

        response = self.client.post(reverse("alterar_dados"), {
            "username": "paola_new",
            "email": "novoemail@example.com",
        })

        self.assertEqual(response.status_code, 302)

        updated = User.objects.get(id=self.user.id)
        self.assertEqual(updated.username, "paola_new")
        self.assertEqual(updated.email, "novoemail@example.com")

    # -------------------------------
    # TESTE ALTERAR SENHA LOGADA
    # -------------------------------
    def test_change_password(self):
        self.client.login(username="paola", password="senha123")

        response = self.client.post(reverse("alterar_senha"), {
            "senha_atual": "senha123",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "NovaSenha123"
        })

        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NovaSenha123"))

    # -------------------------------
    # TESTE FLUXO ESQUECI MINHA SENHA — GERAR CÓDIGO
    # -------------------------------
    def test_esqueci_minha_senha(self):
        self.client.login(username="paola", password="senha123")

        response = self.client.get(reverse("alterar_senha") + "?esqueci")
        self.assertEqual(response.status_code, 200)

        reset = PasswordResetCode.objects.get(user=self.user)
        self.assertTrue(reset.code)
        self.assertTrue(reset.expires_at > timezone.now())

    # -------------------------------
    # TESTE DE VALIDAR CÓDIGO E TROCAR A SENHA
    # -------------------------------
    def test_reset_password_with_code(self):
        code_obj = PasswordResetCode.objects.create(
            user=self.user,
            code="123456",
            expires_at=timezone.now() + timezone.timedelta(minutes=10)
        )

        response = self.client.post(reverse("alterar_senha") + "?esqueci", {
            "codigo": "123456",
            "nova_senha": "SenhaNova999",
            "confirmar_senha": "SenhaNova999"
        })

        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("SenhaNova999"))

