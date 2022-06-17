import streamlit as st
from funcoes.novo_emprestimo import tela_novo_emprestimo
from funcoes.cadastrar_livro import tela_cadastro_livro
from funcoes.cadastrar_aluno import tela_cadastro_aluno
from funcoes.consulta import tela_consulta_tabelas
from funcoes.finalizar_emprestimo import tela_finalizar_emprestimo

st.set_page_config(page_title='Alexandria',
                   page_icon='📚',
                   layout='centered',
                   initial_sidebar_state='expanded',
                   menu_items=None)

def alexandria():
    st.title("SISTEMA DE GESTÃO DE SALA DE LEITURA ESCOLAR")
    st.success("INSTRUÇÔES:")
    st.write("As seguintes opções estão disponíveis no menu à esquerda:")
    st.write("*Novo Empréstimo")
    st.write("*Finalizar Empréstimo")
    st.write("*Cadastrar Livro")
    st.write("*Cadastrar Aluno")
    st.write("*Tabelas do Sistema")


def novo_emprestimo():
    st.markdown("Novo Empréstimo")
    tela_novo_emprestimo()

def livro():
    st.markdown("Cadastrar Livro")
    tela_cadastro_livro()

def aluno():
    st.markdown("Cadastrar Aluno")
    tela_cadastro_aluno()

def tabelas():
    tela_consulta_tabelas()

def finalizar_emprestimo():
    st.markdown("Finalizar Empréstimo")
    tela_finalizar_emprestimo()


page_names_to_funcs = {
    "Alexandria - Início": alexandria,
    "Novo Empréstimo": novo_emprestimo,
    "Finalizar Emprestimo": finalizar_emprestimo,
    "Cadastrar Livro": livro,
    "Cadastrar Aluno": aluno,
    "Tabelas do Sistema": tabelas,

}

page = st.sidebar.selectbox("Selecione uma opção", page_names_to_funcs.keys())
page_names_to_funcs[page]()
