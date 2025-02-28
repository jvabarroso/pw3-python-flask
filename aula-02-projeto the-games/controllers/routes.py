from flask import render_template, request
# Render template é o pacote responsável por carregar as páginas

jogadores = ['iruah', 'davi_lambari', 'edsongf',
             'kioto', 'black.butterfly', 'jujudopix']


def init_app(app):
    # Criando a rota principal do site:

    @app.route('/')
    # Criando função no Python. Equivalente ao "function" em javascript
    # View function - função de visualização. Irá te enviar para a página
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    # View function - função de visualização. Irá te enviar para a página
    def games():

        # Dicionário no Python (Objeto)
        game = {'Título': 'CS-GO',
                'Ano': 2012,
                'Categoria': 'FPS Online'}

        listaGames = ['Minecraft', 'GTA V', 'Red Dead Redemption 2', 'God of War Ragnarok',
                      'Roblox', 'Subnautica Below Zero', 'Ancestors: the humankind odyssey']

        if request.method == 'POST':
            if request.form.get('jogador'):  # Meio que a gnt colocou lá no input
                jogadores.append(request.form.get('jogador'))

        return render_template('games.html', game=game, jogadores=jogadores, listaGames=listaGames)
# A primeira variável é a que será chamada na página, enquanto a segunda é o nome da variável em que estão armazenados os dados
