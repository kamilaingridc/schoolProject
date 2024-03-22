from django.http import HttpResponse
from django.db import connection, transaction
from django.contrib import messages
from django.shortcuts import render
from hashlib import sha256
from .models import Professor, Turma, Atividade


def initial_population():
    print("Vou popular.")

    cursor = connection.cursor()

    # popular tabela professor
    senha = '123456' # senha inicial de todos usuários
    senha_armazenar = sha256(senha.encode()).hexdigest()
    # instrução SQL
    insert_sql_professor = "INSERT INTO App_School_professor (nome, email, senha) VALUES"
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "'), "
    insert_sql_professor = insert_sql_professor + "('Profa. Angela Merkel', 'angela.merkel@gmail.com', '" + senha_armazenar + "'), "
    insert_sql_professor = insert_sql_professor + "('Prof. Xi Jinping', 'xi.jinping@gmail.com', '" + senha_armazenar + "'),"

    cursor.execute(insert_sql_professor)
    transaction.atomic()  # necessário commit para insert e update
    # fim da população da tabela professor

    # popular tabela turma
    # instrução SQL
    insert_sql_turma = "INSERT INTO App_School_turma (nome_turma, id_professor_id) VALUES"
    insert_sql_turma = insert_sql_turma + "('1º semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2º semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3º semestre - Desenvolvimento de Sistemas', 3),"

    cursor.execute(insert_sql_turma)
    transaction.atomic()  # necessário commit para insert e update
    # fim da população da tabela turma

    # popular tabela atividade
    # instrução SQL
    insert_sql_atividade = "INSERT INTO App_School_atividade (nome_atividade, id_turma_id) VALUES"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos de Programação', 1"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Framework Django', 2"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar conceitos de gerenciamento de projetos', 3"

    cursor.execute(insert_sql_atividade)
    transaction.atomic()  # necessário commit para insert e update
    # fim da população da tabela atividade

    print("Populei.")




def abre_index(request):
    # return render(request, 'Index.html')
    # mensagem = "Olá turma, muito bom dia!"
    # return HttpResponse(mensagem)

    # query set Tipos de Look Up
    # nome__exact='SS' - tem que ser exatamente igual
    # nome__contains='H' - contém o H maiúsculo 
    # nome__icontains = 'H' - ignora se maiúsculo ou minúsculo
    # nome__startswith = 'M' - traz o que começa com a letra M ou sequência de letras
    # nome__istartswith = 'M' - traz o que começa com a letra M ignorando se maiúsculo ou minúsculo / sequência de letras
    # nome__endswith = 'a' - traz o que termina com a letra a minúsculo ou sequência de letras
    # nome__iendswith = 'a' - traz o que termina com a letra a ignorando maiúsculo ou minúsculo
    # nome__in=['Michael', ['Obama']) traz somente  os nomes que estão n alista
    # pode ser feito uma composição 'and' utilizando , (vírgula entre os campos) ou 'or' utilizando | (pipe entre os campos)

    dado_pesqusia = 'Obama'

    verifica_populado = Professor.objects.filter(nome__icontains=dado_pesqusia)
    # verifica_populado = Professor.objects.filter(nome='Prof. Barak Obama')

    if len(verifica_populado) == 0:
        print("Não está populado.")
        initial_population()
    else:
        print("Achei Obama", verifica_populado)

    return render(request, 'login.html')


def enviar_login(request):
    if (request.method == 'POST'):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email=email).values("nome", "senha", "id")
        print("Dados do professor: ", dados_professor)

        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']
            if senha == senha_criptografada:
                messages.info(request, 'Bem-Vindo.')

                mensagem = "Olá professor, " + email + ". Seja bem-vindo!"
                return HttpResponse(mensagem)
            else:
                messages.info(request, 'Usuário ou senha incorretos. Tente novamente.')
                return render(request, 'login.html')
        messages.info(request,
                      'Olá' + email + ', seja bem-vindo! Percebemos que você é novo por aqui. Complete o seu cadastro.')
        return render(request, 'cadastro.html', {'login': email})


def confirmar_cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('login')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()

        grava_professor = Professor(
            nome=nome,
            email=email,
            senha=senha_criptografada
        )

        grava_professor.save()

        mensagem = 'Olá professor(a)' + nome + ', seja bem-vindo(a)!'
        return HttpResponse(mensagem)

    # substituir por html
    # return render(request, 'lalala.html')
