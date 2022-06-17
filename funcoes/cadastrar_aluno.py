import streamlit as st
import psycopg2

# Conexão do Banco de dados
mydb = psycopg2.connect(
    database="deg4do58nvsta5",
    user="nvhkstpynbzgqi",
    password="b4288fbb1fbc757e60e9aba5e362828464e2a36db1a54d2f9cb3903f2b0b6dc5",
    host="ec2-52-204-195-41.compute-1.amazonaws.com",
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
