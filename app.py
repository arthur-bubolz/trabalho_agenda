from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Configurações do banco de dados PostgreSQL
db_host = 'localhost'
db_port = '5432'
db_name = 'teste'
db_user = 'postgres'
db_password = '123'

conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
cur = conn.cursor()

@app.route('/')
def index():
    # Recupera os contatos adicionados do banco de dados
    cur.execute("SELECT nome,sobrenome,telefone,email from contato")
    contatos = cur.fetchall()

    # Renderiza o template do Flask com a lista de contatos
    return render_template('index.html', contatos=contatos)

@app.route('/grupos')
def grupos():
    # Recupera os grupos do banco de dados
    cur.execute("SELECT * FROM grupos")
    grupos = cur.fetchall()
    
    # Renderiza o template do Flask com a lista de grupos
    return render_template('grupos.html', grupos=grupos, contatos=[])

@app.route('/add_grupos', methods=['POST'])
def add_grupo():
    #obter nome do grupo
    nome_grupo = request.form['nome_grupo']

    # Insere o novo grupo no banco de dados
    cur.execute("INSERT INTO grupos (nome_grupo) VALUES (%s)", (nome_grupo,))
    conn.commit()
    
    return redirect('/grupos')

@app.route('/add_contato_grupos', methods=['POST'])
def add_contato_grupos():
    telefone = request.form['telefone']
    grupo_id = request.form['grupo']
    
    # Atualiza o grupo_id para o contato com o telefone informado
    cur.execute("UPDATE contato SET grupoid = %s WHERE telefone = %s", (grupo_id, telefone))
    conn.commit()
    
    return redirect('/grupos')

@app.route('/verificar_contatos', methods=['POST'])
def verificar_contatos():
    grupo_id = request.form['grupo_id']

    # Recupera os grupos do banco de dados
    cur.execute("SELECT * FROM grupos")
    grupos = cur.fetchall()

    # Recupera os contatos do grupo informado
    cur.execute("SELECT nome, sobrenome, telefone, email FROM contato WHERE grupoid = %s", (grupo_id,))
    contatos = cur.fetchall()

    # Redireciona para a página de grupos com a lista de contatos do grupo
    return render_template('grupos.html', grupos=grupos, contatos=contatos)

@app.route('/add_contato', methods=['POST'])
def add_contato():
    # Obtém os detalhes do contato do formulário
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    email = request.form['email']
    telefone = request.form['telefone']

    # Insere o novo contato no banco de dados
    cur.execute("INSERT INTO contato (nome,sobrenome,telefone,email) VALUES (%s, %s, %s, %s)", (nome, sobrenome, telefone, email))
    conn.commit()

    # Redireciona para a página inicial após a adição do contato
    return redirect('/')

if __name__ == '__main__':
    app.run()

