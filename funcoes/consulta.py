import pandas as pd
import streamlit as st
import psycopg2

# Conexão do Banco de dados
mydb = psycopg2.connect(
    database="deg4do58nvsta5",
    user="nvhkstpynbzgqi",
    password="b4288fbb1fbc757e60e9aba5e362828464e2a36db1a54d2f9cb3903f2b0b6dc5",
    host="ec2-52-204-195-41.compute-1.amazonaws.com",
    port="5432")


#Função para parar de exibir 'telas'/formulários, limpando a tela
def nada():
    return None

#Função para selecionar as tabelas de uma lista e visualizá-las, elaborada pelo Daniel
def tela_consulta_tabelas():
    mycursor = mydb.cursor()

    sql = '''
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE schemaname != 'pg_catalog' AND 
            schemaname != 'information_schema';
        '''

    mycursor.execute(sql)

    tab = mycursor.fetchall()
    mycursor.close()
    tabelas = []
    for i in range(len(tab)):
        tabelas.append(tab[i][0])

    # aa = st.slider(label:'tabelas',value:myresult)
    st.subheader("Selecione a tabela desejada:")
    tabela_escolhida = st.selectbox("",tabelas,key='new')

    mycursor.close()
    mycursor = mydb.cursor()

    sql = f'''
    SELECT * FROM public."{tabela_escolhida}"
    '''
    mycursor.execute(sql)

    TABELA_T = mycursor.fetchall()

    DATAFRAME = pd.DataFrame(TABELA_T)
    try:
        # Colocar nome nas colunas:
        if tabela_escolhida == 'ALUNO':
            st.subheader("Relação de Alunos(as)")
            DATAFRAME = DATAFRAME.rename(columns={
                0:'ID',
                1:'Nome',
                2:'Ano',
                3:'Turma'
            })
            st.dataframe(DATAFRAME)

        elif tabela_escolhida == 'LIVRO':
            st.subheader("Livros do Acervo")
            DATAFRAME = DATAFRAME.rename(columns={
                0:'Número do Tombo',
                1:'Título',
                2:'Autor',
                3:'Editora',
                4:'Edição',
                5:'Gênero',
                6:'Prateleira',
                7:'Extraviado'
            })
            st.dataframe(DATAFRAME)

        elif tabela_escolhida == 'EMPRESTIMO':
            st.subheader("Empréstimos em Andamento")
            DATAFRAME = DATAFRAME.rename(columns={
                0:'Número do Tombo',
                1:'Nùmero do Livro',
                2:'Nome do(a) Aluno(a)',
                3:'ID do(a) Aluno(a)',
                4:'Ano do(a) Aluno(a)',
                5:'Turma do(a) Aluno(a)',
                6:'Início do Empréstimo',
                7:'Extraviado',
                8:'Data de Devolução'
            })
            st.dataframe(DATAFRAME[['Número do Tombo', 'Nùmero do Livro', 'Nome do(a) Aluno(a)', 'ID do(a) Aluno(a)',
                         'Ano do(a) Aluno(a)', 'Turma do(a) Aluno(a)', 'Início do Empréstimo', 'Data de Devolução']])

        elif tabela_escolhida == 'HISTORICO_EMPRESTIMO':
            st.subheader("HISTÓRICO DE EMPRÉSTIMOS")
            DATAFRAME = DATAFRAME.rename(columns={

                0:'Nùmero do Empréstimo',
                1:'Número do Tombo',
                2:'Nùmero do Livro',
                3:'Nome do(a) Aluno(a)',
                4:'ID do(a) Aluno(a)',
                5:'Ano do(a) Aluno(a)',
                6:'Início do Empréstimo',
                7:'Livro Extraviado?',
                8:'Data da Devolução',
                9:'Turma do(a) Aluno(a)',
                10:'Título do Livro'

            })
            st.dataframe(DATAFRAME[['Número do Tombo','Nùmero do Livro','Título do Livro','Nome do(a) Aluno(a)',
                                    'Ano do(a) Aluno(a)', 'Turma do(a) Aluno(a)', 'Início do Empréstimo',
                                    'Livro Extraviado?', 'Data da Devolução']])
    except:
        st.warning("Não há dados para exibir.")

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
    '''
    Criar um função que Retorna os livros, pesquisando por:
        - Titulo do Livro
        - Autor
        - Numero do Tombo
    Tentar fazer uma barra que tenha as opções 
    '''
    nada()

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
            FROM public."ALUNO"
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