import streamlit as st

# Funções feitas
from funcoes.cadastro import tela_cadastro_livro
from funcoes.cadastro import tela_cadastro_aluno
from funcoes.cadastro import tela_cadastro_emprestimo
from funcoes.cadastro import nada
from funcoes.cadastro import tela_novo_emprestimo
from funcoes.cadastro import tela_finalizar_emprestimo

from funcoes.consulta import tela_consulta_tabelas
from funcoes.consulta import tela_consulta_emprestimo
from funcoes.consulta import tela_consulta_atrasado
from funcoes.consulta import tela_consulta_livros
from funcoes.consulta import tela_consulta_aluno

from funcoes.update import upload_alunos
from funcoes.update import tela_cadastro_update_aluno
from funcoes.update import tela_cadastro_update_livro

def sala_de_leitura():

    # Parte que chama as Funções do Codigo
    st.sidebar.subheader('CADASTRO')
    tela_cadastro = st.sidebar.radio("Opções de cadastro e empréstimo", ("Empréstimo",
                                                                         "Novo Empréstimo",
                                                                         "Finalizar Empréstimo",
                                                                         "Livro",
                                                                         "Aluno",
                                                                         "Nenhuma ação"), index=5)

    st.sidebar.subheader('CONSULTA')
    tela_consulta = st.sidebar.radio("Opções de consultas", ("Empréstimos",
                                                             "Livros atrasados",
                                                             "Livros do acervo",
                                                             "Alunos",
                                                             "Tabelas",
                                                             "Nenhuma ação"), index=5)

    st.sidebar.subheader('ATUALIZAÇÃO E MANUTENÇÃO')
    tela_update = st.sidebar.radio("Opções de consultas", ("Alterar alunos",
                                                           "Alterar livros",
                                                           "Upload de lista de alunos",
                                                           "Upload de lista de livros",
                                                           "Nenhuma ação",), index=4)

    # Condições para selecionar as telas de cadastro
    if tela_cadastro == "Livro":
        tela_cadastro_livro()
    if tela_cadastro == "Aluno":
        tela_cadastro_aluno()
    if tela_cadastro == "Empréstimo":
        tela_cadastro_emprestimo()
    if tela_cadastro == "Novo Empréstimo":
        tela_novo_emprestimo()
    if tela_cadastro == "Finalizar Empréstimo":
        tela_finalizar_emprestimo()


    if tela_cadastro == "Nenhuma ação":
        nada()

    # Condições para selecionar as telas de consulta
    if tela_consulta == "Tabelas":
        tela_consulta_tabelas()
    if tela_consulta == "Empréstimos":
        tela_consulta_emprestimo()
    if tela_consulta == "Livros atrasados":
        tela_consulta_atrasado()
    if tela_consulta == "Livros do acervo":
        tela_consulta_livros()
    if tela_consulta == "Alunos":
        tela_consulta_aluno()
    if tela_consulta == "Nenhuma ação":
        nada()

    # Condições para selecionar as telas de atualização
    if tela_update == "Nenhuma ação":
        nada()
    if tela_update == "Upload de lista de alunos":
        upload_alunos()
    if tela_update == "Alterar alunos":
        tela_cadastro_update_aluno()
    if tela_update == "Alterar livros":
        tela_cadastro_update_livro()

if st.session_state == {}:
    st.session_state['user'] = 'none'
if st.session_state.user == 'none':
    with st.form(key='login'):
        user = st.text_input("Digite seu usuário")
        password = st.text_input("Digite sua senha:")
        login_button = st.form_submit_button("Enviar")
        if login_button:

            if password == 'nova_senha' and user == 'user':
                st.session_state['user'] = 1
            elif password == '':
                None
if st.session_state.user == 1:
    sala_de_leitura()
