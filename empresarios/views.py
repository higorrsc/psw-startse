from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import redirect, render

from .models import Empresas, Documento, Metricas


# Create your views here.
@login_required(login_url="/usuarios/login/")
def cadastrar_empresa(request):
    if request.method == "GET":
        return render(
            request,
            "cadastrar_empresa.html",
            {
                "tempo_existencia": Empresas.tempo_existencia_choices,
                "areas": Empresas.area_choices,
            },
        )
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("/usuarios/login")

        nome = request.POST.get("nome")
        cnpj = request.POST.get("cnpj")
        site = request.POST.get("site")
        tempo_existencia = request.POST.get("tempo_existencia")
        descricao = request.POST.get("descricao")
        data_final = request.POST.get("data_final")
        percentual_equity = request.POST.get("percentual_equity")
        estagio = request.POST.get("estagio")
        area = request.POST.get("area")
        publico_alvo = request.POST.get("publico_alvo")
        valor = request.POST.get("valor")
        pitch = request.FILES.get("pitch")
        logo = request.FILES.get("logo")

        try:
            empresa = Empresas(
                user=request.user,
                nome=nome,
                cnpj=cnpj,
                site=site,
                tempo_existencia=tempo_existencia,
                descricao=descricao,
                data_final_captacao=data_final,
                percentual_equity=percentual_equity,
                estagio=estagio,
                area=area,
                publico_alvo=publico_alvo,
                valor=valor,
                pitch=pitch,
                logo=logo,
            )
            empresa.save()
        except Exception as e:
            messages.add_message(
                request,
                constants.ERROR,
                f"Erro interno do sistema - {e}",
            )
            return redirect("/empresarios/cadastrar_empresa")

        messages.add_message(
            request,
            constants.SUCCESS,
            "Empresa criada com sucesso",
        )
        return redirect("/empresarios/cadastrar_empresa")


@login_required(login_url="/usuarios/login/")
def listar_empresas(request):
    if request.method == "GET":
        empresas = Empresas.objects.filter(user=request.user)
        if request.GET.get("empresa"):
            empresas = empresas.filter(nome__contains=request.GET.get("empresa"))
        return render(
            request,
            "listar_empresas.html",
            {"empresas": empresas},
        )


def empresa(request, id):
    empresa = Empresas.objects.get(id=id)

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, "Acesso negado")
        return redirect("/empresarios/listar_empresas")

    if request.method == "GET":
        documentos = Documento.objects.filter(empresa=empresa)
        return render(
            request,
            "empresa.html",
            {
                "empresa": empresa,
                "documentos": documentos,
            },
        )


def add_doc(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get("titulo")
    arquivo = request.FILES.get("arquivo")

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, "Acesso negado")
        return redirect("/empresarios/listar_empresas")

    if not arquivo:
        messages.add_message(request, constants.ERROR, "Envie um arquivo")
        return redirect(f"/empresarios/empresa/{id}")

    extensao = arquivo.name.split(".")
    if extensao[1] != "pdf":
        messages.add_message(request, constants.ERROR, "Envie apenas PDF's")
        return redirect(f"/empresarios/empresa/{id}")

    documento = Documento(empresa=empresa, titulo=titulo, arquivo=arquivo)
    documento.save()
    messages.add_message(request, constants.SUCCESS, "Arquivo cadastrado com sucesso")
    return redirect(f"/empresarios/empresa/{id}")


def excluir_dc(request, id):
    documento = Documento.objects.get(id=id)
    if documento.empresa.user != request.user:
        messages.add_message(request, constants.ERROR, "Esse documento não é seu")
        return redirect(f"/empresarios/empresa/{empresa.id}")

    documento.delete()
    messages.add_message(request, constants.SUCCESS, "Documento excluído com sucesso")
    return redirect(f"/empresarios/empresa/{documento.empresa.id}")


def add_metrica(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get("titulo")
    valor = request.POST.get("valor")

    metrica = Metricas(
        empresa=empresa,
        titulo=titulo,
        valor=valor,
    )
    metrica.save()

    messages.add_message(request, constants.SUCCESS, "Métrica cadastrada com sucesso")
    return redirect(f"/empresarios/empresa/{empresa.id}")
