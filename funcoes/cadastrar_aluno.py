import streamlit as st
import psycopg2

# Conexão do Banco de dados
mydb = psycopg2.connect(
    database="dcj8rehkg575jt",
    user="mukyulukhffrky",
    password="1537728423988d4a4010276828a4e0f56798a783e3e044598e12ce421bd23fe4",
    host="ec2-3-214-136-47.compute-1.amazonaws.com",
    port="5432")


def tela_cadastro_aluno():
    with st.form(key='form_aluno'):
        st.subheader('CADASTRAR ALUNO(A)')

        # Nome
        nome = st.text_input(label='Nome do(a) Aluno(a):', max_chars=200)
        col1, col2 = st.columns(2)
        with col1:
            # Série (O preenchimento deste campo está gerando erros)
            serie = st.text_input('Série:', max_chars=1)
        with col2:
            # Turma (O preenchimento deste campo está gerando erros)
            turma = st.text_input('Turma', max_chars=1)

        button_new_aluno = st.form_submit_button(label='CADASTRAR ALUNO(A)')

        if button_new_aluno:
            mycursor = mydb.cursor()
            sql = """
            INSERT INTO "ALUNO" (nome, ano, turma) 
            VALUES (%s, %s, %s)
            """
            val = (nome, serie, turma)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Aluno(a) cadastrado com sucesso!")

tela_cadastro_aluno()