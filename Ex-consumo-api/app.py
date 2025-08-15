# Importando o Flask
from flask import Flask
# Importando as rotas que estão nos controllers
from controllers import routes

# Carregando o Flask na variável app
app = Flask(__name__, template_folder='views')

# Chamando as rotas
routes.init_app(app)

# Inicializando a aplicação Flask
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
