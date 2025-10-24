from flask import render_template, request, url_for, redirect, flash, session
from models.database import db, Game, Console, Usuario
import urllib # Permitir ler URL das APIS
import json # Conversão de dados
from werkzeug.security import generate_password_hash, check_password_hash # Importando a biblioteca de segurança

# Lista de jogadores
jogadores = ['Miguel José', 'Miguel Isack', 'Leaf',
             'Quemario', 'Trop', 'Aspax', 'maxxdiego']
# Lista de jogos
gamelist = [{'Título': 'CS-GO', 'Ano': 2012, 'Categoria': 'FPS Online'}]


def init_app(app):
    # Realizando a configuração para TRANCAR as rotas não permitidas sem o LOGIN
    @app.before_request
    def check_auth():
        # Rotas que não precisam de autenticação
        routes = ['home', 'login', 'caduser']

        # Se a rota não requer autentificação, permite o acesso
        if request.endpoint in routes or request.path.startswith('/static'):
            return None
        # Se o usuário não estiver autentificado, redireciona para a página de Login:
        if 'user_id' not in session:
            return redirect(url_for('login'))

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        game = gamelist[0]

        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
                return redirect(url_for('games'))
        return render_template('games.html',
                               game=game,
                               jogadores=jogadores)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            if request.form.get('titulo') and request.form.get('ano') and request.form.get('categoria'):
                gamelist.append({'Título': request.form.get('titulo'), 'Ano': request.form.get(
                    'ano'), 'Categoria': request.form.get('categoria')})
                return redirect(url_for('cadgames'))

        return render_template('cadgames.html',
                               gamelist=gamelist)

    # CRUD GAMES - LISTAGEM, CADASTRO E EXCLUSÃO
    @app.route('/games/estoque', methods=['GET', 'POST'])
    @app.route('/games/estoque/delete/<int:id>')
    def gamesEstoque(id=None):
        if id:
            game = Game.query.get(id)
            # Deleta o jogo cadastro pela ID
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('gamesEstoque'))
        # Cadastra um novo jogo
        if request.method == 'POST':
            newgame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'],
                           request.form['preco'], request.form['quantidade'], request.form['console'])
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('gamesEstoque'))
        else:
            # Captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 3)
            per_page = 3
            # Faz um SELECT no banco a partir da pagina informada (page)
            # Filtrando os registro de 3 em 3 (per_page)
            games_page = Game.query.paginate(page=page, per_page=per_page)
            
            consoles = Console.query.all()
                       
            return render_template('gamesestoque.html', gamesestoque=games_page, consoles=consoles)

    # CRUD GAMES - EDIÇÃO
    @app.route('/games/edit/<int:id>', methods=['GET', 'POST'])
    def gameEdit(id):
        g = Game.query.get(id)
        # Edita o jogo com as informações do formulário
        if request.method == 'POST':
            g.titulo = request.form['titulo']
            g.ano = request.form['ano']
            g.categoria = request.form['categoria']
            
            g.console_id = request.form['console']
            
            g.preco = request.form['preco']
            g.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('gamesEstoque'))
        
        consoles = Console.query.all()
        return render_template('editgame.html', g=g, consoles=consoles)

    # CRUD CONSOLES - LISTAGEM, CADASTRO E EXCLUSÃO
    @app.route('/consoles/estoque', methods=['GET', 'POST'])
    @app.route('/consoles/estoque/delete/<int:id>')
    def consolesEstoque(id=None):
        if id:
            console = Console.query.get(id)
            # Deleta o console cadastro pela ID
            db.session.delete(console)
            db.session.commit()
            return redirect(url_for('consolesEstoque'))
        # Cadastra um novo console
        if request.method == 'POST':
            newconsole = Console(request.form['nome'], request.form['fabricante'], request.form['ano_lancamento'])
            db.session.add(newconsole)
            db.session.commit()
            return redirect(url_for('consolesEstoque'))
        else:
            # Captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 3)
            per_page = 3
            # Faz um SELECT no banco a partir da pagina informada (page)
            # Filtrando os registro de 3 em 3 (per_page)
            consoles_page = Console.query.paginate(page=page, per_page=per_page)
            return render_template('consolesestoque.html', consolesestoque=consoles_page)

    # CRUD CONSOLES - EDIÇÃO
    @app.route('/consoles/edit/<int:id>', methods=['GET', 'POST'])
    def consoleEdit(id):
        console = Console.query.get(id)
        # Edita o console com as informações do formulário
        if request.method == 'POST':
            console.nome = request.form['nome']
            console.fabricante = request.form['fabricante']
            console.ano_lancamento = request.form['ano_lancamento']
            db.session.commit()
            return redirect(url_for('consolesEstoque'))
        return render_template('editconsole.html', console=console)
    
    # ROTA de Catálogo de Jogos (Consumo da API)
    @app.route('/apigames', methods=['GET', 'POST'])
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        urlApi = 'https://www.freetogame.com/api/games'
        response = urllib.request.urlopen(urlApi)
        apiData = response.read()
        listaJogos = json.loads(apiData)
        # Buscando o jogo individual na lista de jogos
        if id:
            gameInfo = []
            for jogo in listaJogos:
                if jogo['id'] == id:
                    gameInfo = jogo
                    break
            if gameInfo:
                return render_template('gameinfo.html', gameInfo=gameInfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'        
        return render_template('apigames.html', listaJogos=listaJogos)

    # ROTA de LOGIN
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            # Verificando se o usuário existe
            user = Usuario.query.filter_by(email=email).first()
            # Verificando se o email e senha estão corretors
            if user and check_password_hash(user.senha, senha):
                # Aqui será criado a sessão para o usuário
                session['user_id'] = user.id
                session['user_email'] = user.email
                flash("Login realizado com sucesso! Bem vindo {user.nome}!", "success")
                return redirect(url_for("home"))
            # Dados invalidos
            else:
                flash("Falha no login. Verifique seu e-mail e sua senha e tente novamente.", 'danger')
                redirect(url_for('login'))
        return render_template('login.html')
    
    # ROTA de LOGOUT
    @app.route('/logout')
    def logout():
        session.clear()
        flash("Você foi desconectado!", "warning")
        return redirect(url_for('home'))
    
    # ROTA de CADASTRO
    @app.route('/caduser', methods=['GET', 'POST'])
    def caduser():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            nome = request.form['nome']
            # Verificando se o usuário já existe
            # Se o usuário existir
            user = Usuario.query.filter_by(email=email).first()
            if user:
                flash("Usuário já cadastrado. Faça o login!", "danger")
                return redirect(url_for('caduser'))
            # Se o usuário não existir
            else:
                hash = generate_password_hash(senha, method='scrypt')
                newUser = Usuario(nome=nome, email=email, senha=hash)
                db.session.add(newUser)
                db.session.commit()
                flash("Usuário cadastrado com sucesso! Você já pode fazer o login!" , "success")
                return redirect(url_for('login'))
            
        return render_template('caduser.html')