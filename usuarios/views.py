from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants


# Create your views here.
def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if not password == confirm_password:
            messages.add_message(
                request,
                constants.ERROR,
                "As senhas precisam ser iguais",
            )
            return redirect("/usuarios/cadastro")
        if len(password) < 6:
            messages.add_message(
                request,
                constants.ERROR,
                "A senha deve possuir pelo menos 6 caracteres",
            )
            return redirect("/usuarios/cadastro")

        users = User.objects.filter(username=username)
        if users.exists():
            messages.add_message(
                request,
                constants.ERROR,
                "Já existe um usuário com esse nome",
            )
            return redirect("/usuarios/cadastro")

        user = User.objects.create_user(username=username, password=password)
        return redirect("/usuarios/logar")
