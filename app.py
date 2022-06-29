import streamlit as st
import streamlit.components.v1 as components

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

dialogo_sucesso ='''
    <script language="javascript">
    alert("Bem-vindo(a) ao Alexandria!");
    </script>
'''
components.html(dialogo_sucesso, height=0)

options = st.sidebar.radio("SELECIONE UMA OPÇÃO: ",("Alexandria - Início",
                                                    "Novo Empréstimo",
                                                    "Finalizar Empréstimo",
                                                    "Cadastrar Livro",
                                                    "Cadastrar Aluno",
                                                    "Tabelas do Sistema"),index=0)
if options == "Alexandria - Início":
    st.title("SISTEMA DE GESTÃO DE SALA DE LEITURA ESCOLAR")
    st.success("INSTRUÇÔES:")
    st.subheader("As seguintes opções estão disponíveis no menu lateral à esquerda:")
    st.write("*Novo Empréstimo")
    st.write("*Finalizar Empréstimo")
    st.write("*Cadastrar Livro")
    st.write("*Cadastrar Aluno")
    st.write("*Tabelas do Sistema")

if options == "Novo Empréstimo":
    tela_novo_emprestimo()

if options == "Finalizar Empréstimo":
    tela_finalizar_emprestimo()

if options == "Cadastrar Livro":
    tela_cadastro_livro()

if options == "Cadastrar Aluno":
    tela_cadastro_aluno()

if options == "Tabelas do Sistema":
    tela_consulta_tabelas()
