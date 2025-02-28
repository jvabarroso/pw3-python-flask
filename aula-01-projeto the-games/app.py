# Comentário em Python
# Importando o pacote do Flask
from flask import Flask, render_template
# Render template é o pacote responsável por carregar as páginas

# Carregando o Flask na variável app
# O valor da variável "name" sempre é o nome do arquivo. Template folder mostra que todas as páginas estão dentro da View
app = Flask(__name__, template_folder='views')

# Criando a rota principal do site:


@app.route('/')
# Criando função no Python. Equivalente ao "function" em javascript
# View function - função de visualização. Irá te enviar para a página
def home():
    return render_template('index.html')


@app.route('/games')
# View function - função de visualização. Irá te enviar para a página
def games():

    # Dicionário no Python (Objeto)
    game = {'Título': 'CS-GO',
            'Ano': 2012,
            'Categoria': 'FPS Online'}

    listaGames = ['Minecraft', 'GTA V', 'Red Dead Redemption 2', 'God of War Ragnarok',
                  'Roblox', 'Subnautica Below Zero', 'Ancestors: the humankind odyssey']

    jogadores = ['iruah', 'davi_lambari', 'edsongf',
                 'kioto', 'black.butterfly', 'jujudopix']
    return render_template('games.html', game=game, jogadores=jogadores, listaGames=listaGames)
# A primeira variável é a que será chamada na página, enquanto a segunda é o nome da variável em que estão armazenados os dados


# Ao inciar o arquivo, o nome dele muda para main, por isso conferir para o arquivo só ser executado se o nome do arquivo for igual a main
if __name__ == '__main__':
    # Rodando o servidor no localhost e na porta 5000
    # debugar o código siginifica que a checagem do código será verdadeira, ou seja, caso haja algum erro no código, ele avisa
    app.run(host='localhost', port=5000, debug=True)
