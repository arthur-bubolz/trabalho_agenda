from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Configurações do banco de dados PostgreSQL
db_host = 'localhost'
db_port = '5432'
db_name = 'teste'
db_user = 'postgres'
db_password = '123'

@app.route('/')
def index():
    # Conecta ao banco de dados
    conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()

    # Recupera os contatos adicionados do banco de dados
    cur.execute("SELECT nome,sobrenome,telefone,email from contato")
    contatos = cur.fetchall()

    # Renderiza o template do Flask com a lista de contatos
    return render_template('index.html', contatos=contatos)

@app.route('/add_contato', methods=['POST'])
def add_contato():
    # Obtém os detalhes do contato do formulário
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    email = request.form['email']
    telefone = request.form['telefone']

    # Conecta ao banco de dados
    conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()

    # Insere o novo contato no banco de dados
    cur.execute("INSERT INTO contato (nome,sobrenome,telefone,email) VALUES (%s, %s, %s, %s)", (nome, sobrenome, telefone, email))
    conn.commit()

    # Redireciona para a página inicial após a adição do contato
    return redirect('/')

if __name__ == '__main__':
    app.run()

