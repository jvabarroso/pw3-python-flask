# Comentário em Python
# Importando o pacote do Flask
from flask import Flask

# Carregando o Flask na variável app
app = Flask(__name__) # O valor da variável "name" sempre é o nome do arquivo

# Criando a rota principal do site:
@app.route('/')




# Criando função no Python. Equivalente ao "function" em javascript
def home():
    return '<h1>O primeiro de muitos sites Flask. Bem vindo!<h1>'

@app.route('/games')
def games():
    return '<h1>Seja bem vindo a página de games<h1>'

# Ao inciar o arquivo, o nome dele muda para main, por isso conferir para o arquivo só ser executado se o nome do arquivo for igual a main
if __name__ == '__main__':
    # Rodando o servidor no localhost e na porta 5000
     app.run(host='localhost', port=5000, debug=True) # debugar o código siginifica que a checagem do código será verdadeira, ou seja, caso haja algum erro no código, ele avisa
