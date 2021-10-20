import pandas as pd
import streamlit as st
import mysql.connector
from funcoes.cadastro import SENHA
from funcoes.cadastro import selecionar_registro
from funcoes.cadastro import consultar_banco

# Conexão do Banco de dados
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=SENHA, #alterar a constante SENHA apenas no módulo 'cadastro.py'
  database="pji"
)

#Função para parar de exibir 'telas'/formulários, limpando a tela
def nada():
    return None

#Função para selecionar as tabelas de uma lista e visualizá-las, elaborada pelo Daniel
def tela_consulta_tabelas():
    mycursor = mydb.cursor()

    sql = "SHOW TABLES FROM pji"

    mycursor.execute(sql)

    tab = mycursor.fetchall()
    tabelas = []
    for i in range(len(tab)):
        tabelas.append(tab[i][0])

    # aa = st.slider(label:'tabelas',value:myresult)

    tabela_escolhida = st.selectbox("Qual tabela deseja selecionar",tabelas,key='new')

    # aa = st.slider('tabelas',myresult)

    st.subheader('TABELAS')
    # st.select_slider(list(myresult))

    # mycursor.close()

    mycursor = mydb.cursor()

    sql = f"SELECT * FROM pji.{tabela_escolhida}"

    mycursor.execute(sql)

    TABELA_T = mycursor.fetchall()

    DATAFRAME = pd.DataFrame(TABELA_T)

    # Colocar nome nas colunas:
    if tabela_escolhida == 'aluno':
        DATAFRAME = DATAFRAME.rename(columns={
            0:'RA',
            1:'Nome',
            2:'Sexo',
            3:'CPF',
            4:'RG',
            5:'Telefone',
            6:'Responsavel',
            7:'Data de Nascimento',
            8:'Serie',
            9:'Turma'
        })
    elif tabela_escolhida == 'sala':
        DATAFRAME = DATAFRAME.rename(columns={
            0:'Serie',
            1:'Turma',
            2:'Período'
        })
    elif tabela_escolhida == 'livro':
        DATAFRAME = DATAFRAME.rename(columns={
            0:'Número do Tombo',
            1:'Título',
            2:'Autor',
            3:'Editora',
            4:'Edição',
            5:'Ano da Edição',
            6:'ISBN',
            7:'Genero',
            8:'Prateleira'
        })
    elif tabela_escolhida == 'emprestimo':
        DATAFRAME = DATAFRAME.rename(columns={
            0:'Número do Tombo',
            1:'RA do Aluno',
            2:'Serie do Aluno',
            3:'Turma do Aluno',
            4:'Data de emprestimo',
            5:'Extraviado',
            6:'Data de Devolução'
        })

    st.write(f'{tabela_escolhida}'.upper())
    st.dataframe(DATAFRAME)

def tela_consulta_emprestimo():
    '''
    Criar um função que Retorna os emprestimos, pesquisando por:
        - Nome do Aluno
        - RA do Aluno
        - Numero do Tombo
        - Nome do Livro
    Tentar fazer uma barra que tenha as opções 
    '''
    nada()

def tela_consulta_atrasado():
    mycursor = mydb.cursor()
    # Tabela para ver os livros Atrasados
    sql = """
    SELECT 
        a.nome AS aluno,
        CONCAT(a.SALA_serie, " ", a.SALA_turma) AS turma,
        l.titulo AS livro,
        e.data_inicio,
        DATE_ADD(e.data_inicio, INTERVAL 3 DAY)
    FROM pji.emprestimo AS e
    LEFT JOIN pji.aluno AS a
    ON e.ALUNO_ra = a.ra
    LEFT JOIN pji.livro AS l
    ON e.LIVRO_n_tombo = l.n_tombo
    WHERE DATE_ADD(e.data_inicio, INTERVAL 3 DAY) < NOW()
    ORDER BY e.data_inicio
    """

    mycursor.execute(sql)

    TABELA_E = mycursor.fetchall()

    DATAFRAME = pd.DataFrame(TABELA_E).rename(columns={0:'Nome do Aluno',
                                                    1:'Turma',
                                                    2:'Titulo do Livro',
                                                    3:'Data do Emprestimo',
                                                    4:'Data de Devolução' })
    DATAFRAME['Data de Devolução'] = pd.to_datetime(DATAFRAME['Data de Devolução']).dt.strftime('%d-%m-%Y')                                                   
    DATAFRAME['Data do Emprestimo'] = pd.to_datetime(DATAFRAME['Data do Emprestimo']).dt.strftime('%d-%m-%Y')
    st.title('ENTREGAS ATRASADOS')
    st.dataframe(DATAFRAME)

def tela_consulta_livros():
   st.subheader("Consultar livros do acervo.")
   consultar_livro = selecionar_registro('livro','n_tombo','titulo','autor','titulo',878)
   st.dataframe(consultar_livro)
   if consultar_livro is None:
       consultar_banco("SELECT * FROM")

def tela_consulta_aluno():
    '''
    Criar um função que Retorna os aluno, pesquisando por:
        - Nome do Aluno
        - RA do Aluno
    Tentar fazer uma barra que tenha as opções 
    '''
    with st.form(key ='form_pesquisar_aluno'):
        st.subheader('PROCURAR ALUNO(A)')

        col1, col2 = st.columns(2)
        with col1:
            campo = st.selectbox(label='Procurar Aluno por:', options=['RA', 'Nome'])
        with col2:
            if campo == 'RA':
                pesquisa = st.text_input(label='Registro do(a) Aluno(a) (RA):', max_chars=8)
            elif campo == 'Nome':
                pesquisa = st.text_input(label='Nome do(a) Aluno(a):', max_chars=200)
        
        button_search_aluno = st.form_submit_button(label='Pesquisar aluno')
            # adicionar = st.form_submit_button('Adicionar o Emprestimo')

        if button_search_aluno:
            mycursor = mydb.cursor()
            sql = f"""
            SELECT *
            FROM aluno
            WHERE UPPER({campo}) LIKE UPPER('%{pesquisa}%')
            """
            mycursor.execute(sql)

            TABELA_E = mycursor.fetchall()
            DATAFRAME = pd.DataFrame(TABELA_E).rename(columns={
                    0:'RA',
                    1:'Nome',
                    2:'Sexo',
                    3:'CPF',
                    4:'RG',
                    5:'Telefone',
                    6:'Responsavel',
                    7:'Data de Nascimento',
                    8:'Serie',
                    9:'Turma'
                })

            st.title('ALUNOS')
            st.dataframe(DATAFRAME)

