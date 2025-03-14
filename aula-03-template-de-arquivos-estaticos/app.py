# Comentário em Python
# Importando o pacote do Flask
from flask import Flask
from controllers import routes


# Carregando o Flask na variável app
# O valor da variável "name" sempre é o nome do arquivo. Template folder mostra que todas as páginas estão dentro da View
app = Flask(__name__, template_folder='views')

# Enviando o flask (app) para a função init_app do rotes
routes.init_app(app)

# Ao inciar o arquivo, o nome dele muda para main, por isso conferir para o arquivo só ser executado se o nome do arquivo for igual a main
if __name__ == '__main__':
    # Rodando o servidor no localhost e na porta 5000
    # debugar o código siginifica que a checagem do código será verdadeira, ou seja, caso haja algum erro no código, ele avisa
    app.run(host='localhost', port=5000, debug=True)
