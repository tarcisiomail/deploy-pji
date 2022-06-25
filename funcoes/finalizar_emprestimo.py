import pandas as pd
import streamlit as st
import psycopg2
from datetime import date

# Conexão do Banco de dados
mydb = psycopg2.connect(
    database="deg4do58nvsta5",
    user="nvhkstpynbzgqi",
    password="b4288fbb1fbc757e60e9aba5e362828464e2a36db1a54d2f9cb3903f2b0b6dc5",
    host="ec2-52-204-195-41.compute-1.amazonaws.com",
    port="5432")


def alterar_banco(sql, val):
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()

def tela_finalizar_emprestimo():
    st.subheader("Finalizar empréstimo")
    st.write("Pesquise os empréstimos vigentes por nome ou ra do aluno, ou título ou tombo do livro:")
    mycursor = mydb.cursor()
    mycursor.execute('''
        SELECT public."EMPRESTIMO".livrotombo, public."EMPRESTIMO".livronlivro, 
        public."LIVRO".titulo,public."ALUNO".nome,public."ALUNO".ra,public."ALUNO".ano,
        public."ALUNO".turma,public."EMPRESTIMO".datainicio,public."EMPRESTIMO".dataentrega
        FROM public."ALUNO"
        INNER JOIN public."EMPRESTIMO" ON public."ALUNO".ra=public."EMPRESTIMO".alunora
        INNER JOIN public."LIVRO" ON  
        (public."EMPRESTIMO".livrotombo=public."LIVRO".tombo 
        AND public."EMPRESTIMO".livronlivro = public."LIVRO".nlivro)
                     ''')
    tabela_emprestimo = mycursor.fetchall()
    df_emprestimo = pd.DataFrame(tabela_emprestimo)
    df_emprestimo = df_emprestimo.rename(columns={
        0: 'Número do Tombo',
        1: 'Número do Livro',
        2: 'Título do Livro',
        3: 'Nome do(a) Aluno(a)',
        4: 'RA do(a) Aluno(a)',
        5: 'Ano do(a) Aluno(a)',
        6: 'Turma do(a) Aluno(a)',
        7: 'Início do Empréstimo',
        8: 'Fim do Empréstimo'
    })
    emprestimos = ['...']
    for i in range(len(df_emprestimo)):
        emprestimos.append(df_emprestimo['Número do Tombo'][i] + '-' + df_emprestimo['Número do Livro'][i]
                           + ' - ' + df_emprestimo['Nome do(a) Aluno(a)'][i] + ' - '
                           + df_emprestimo['Título do Livro'][i])
    select_borrow = st.selectbox('', emprestimos)
    if select_borrow != '...':
        st.write(select_borrow)

    with st.form(key='finalizar_emprestimo'):
        col1, col2 = st.columns(2)
        with col1:
            st.empty
        with col2:
            extraviado = st.selectbox("Estado de conservação do livro?", ('Bom', 'Regular', 'Ruim', 'Extraviado'))
            finish_button = st.form_submit_button("FINALIZAR EMPRÉSTIMO")
            if finish_button:
                try:
                    mylist = [str(tabela_emprestimo[0][0]), str(tabela_emprestimo[0][1]), str(tabela_emprestimo[0][2]),
                              str(tabela_emprestimo[0][3]), str(tabela_emprestimo[0][4]), str(tabela_emprestimo[0][5]),
                              str(tabela_emprestimo[0][6]), str(tabela_emprestimo[0][7]), str(date.today()), extraviado]

                    with mydb.cursor() as mycursor:
                        try:
                            mycursor.execute(f'''
                                            INSERT INTO public."HISTORICO_EMPRESTIMO" 
                                            (hlivrotombo, hlivronlivro, hlivrotitulo, halunonome, halunora, halunoano, 
                                            halunoturma, hdatainicio, hdataentrega, hextraviado)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                                ''', mylist)
                            mydb.commit()
                        except:
                            st.write("ERROR")
                            mydb.rollback()
                    with mydb.cursor() as mycursor:
                        try:
                            n_tombo = str(select_borrow.split(sep='-')[0].rstrip())
                            n_livro = str(select_borrow.split(sep='-')[1]).strip()
                            mycursor.execute(f'''
                            DELETE FROM public."EMPRESTIMO" WHERE (livrotombo = '{n_tombo}' AND 
                            livronlivro = '{n_livro}')
                            ''')
                            mydb.commit()
                        except:
                            st.write("ERROR2")
                            mydb.rollback()
                        st.success("Empréstimo finalizado!")
                except:
                    st.error("Nenhum empréstimo selecionado.")
