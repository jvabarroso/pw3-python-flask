# Comentário em Python
# Importando o pacote do Flask
from flask import Flask

# Importando o pyMySql
import pymysql

from controllers import routes

# Importando os Models
from models.database import db


# Carregando o Flask na variável app
# O valor da variável "name" sempre é o nome do arquivo. Template folder mostra que todas as páginas estão dentro da View
app = Flask(__name__, template_folder='views')

# Enviando o flask (app) para a função init_app do rotes
routes.init_app(app)

# Define o nome do banco de dados
DB_NAME = 'games'

# Configura o flask com o bd
app.config['DATABASE_NAME'] = DB_NAME

# Passando o endereço do banco para o flask
# O f ajuda a inserir variáveis numa string
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'

# Ao inciar o arquivo, o nome dele muda para main, por isso conferir para o arquivo só ser executado se o nome do arquivo for igual a main
if __name__ == '__main__':
     # Criando os dados de conexão
    connection = pymysql.connect(host='localhost', user='root', password='',
                                 charset='utf8mb4', cursorclass='pymysql.cursors.DictCursor')
    # Dcti indica que os dados enviados do banco de dados será de dicionario. Dita o tipo de retorno do banco

    # tenta criar o banco, try trata o sucesso
    try:
        # With cria um recurso temporariamente
        with connection.cursor() as cursor: #apelido pro método connection.cursor
            # Cria o banco de dados caso ele não exista
            cursor.execute(f"CREATE DATABASE OF NOT EXISTS {DB_NAME}")
            print(f"O banco de dados {DB_NAME} está criado")
        # except trata a falha
    except Exception as e:
            print(f"Erro ao criar o banco de dados: {e}")
    finally:
        connection.close()
        
        # Passando o flask para SQLAlchemy
        db.init_app(app=app)
        
        # Criando as tabelas a partir do Model
        with app.test_request_context():
            db.create_all()
    
    # Inicializando a aplicação Flask
    # Rodando o servidor no localhost e na porta 5000
    # debugar o código siginifica que a checagem do código será verdadeira, ou seja, caso haja algum erro no código, ele avisa
    app.run(host='localhost', port=5000, debug=True)
