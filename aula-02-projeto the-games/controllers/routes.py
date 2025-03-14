from flask import render_template, request
# Render template é o pacote responsável por carregar as páginas
# request é um pacote responsável pelo envio de dados para as páginas. As requisições

jogadores = ['iruah', 'davi_lambari', 'edsongf',
             'kioto', 'black.butterfly', 'jujudopix']

gamelist = [{'Título': 'CS-GO',
             'Ano': 2012,
             'Categoria': 'FPS Online'}
            ]

consolelist = [{'Nome' : '',
                'Preço':'',
                'País': ''}]

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
        # Acessando o primeiro jogo da lista de jogos. Indice 0
        game = gamelist[0]
        listaGames = ['Minecraft', 'GTA V', 'Red Dead Redemption 2', 'God of War Ragnarok',
                      'Roblox', 'Subnautica Below Zero', 'Ancestors: the humankind odyssey']

        if request.method == 'POST':
            if request.form.get('jogador'):  # O Meio que a gnt colocou lá no input
                jogadores.append(request.form.get('jogador'))

        return render_template('games.html', game=game, jogadores=jogadores, listaGames=listaGames)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():

        if request.method == 'POST':
            if request.form.get('titulo') and request.form.get('ano') and request.form.get('categoria'):
                gamelist.append({'Título': request.form.get('titulo'),
                                 'Ano': request.form.get('ano'),
                                 'Categoria': request.form.get('categoria')})
        # append serve para adicionar os dados na lista
        return render_template('cadgames.html', gamelist=gamelist)
# A primeira variável é a que será chamada na página, enquanto a segunda é o nome da variável em que estão armazenados os dados
    @app.route('/consoles', methods=['GET', 'POST'])
    def consoles():
        console = consolelist[0]
        if request.method == 'POST':
            if request.form.get('nomeConsole') and request.form.get('precoConsole') and request.form.get('paisConsole'):
                consolelist.append({'Nome': request.form.get('nomeConsole'),
                                    'Preço': request.form.get('precoConsole'),
                                    'País': request.form.get('paisConsole')})
        return render_template('consoles.html', consolelist=consolelist, console=console)