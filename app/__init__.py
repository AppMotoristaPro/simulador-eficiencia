import os
from flask import Flask
from app.extensions import db
from app.rotas.simulador_bp import simulador_bp

def create_app():
    app = Flask(__name__)
    
    # Configurações de segurança e banco de dados
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave-super-secreta-simulador')
    
    # Puxa a URL do banco Neon configurada no Render. Se não achar, cria um SQLite local.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local_dev.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa as extensões com o app
    db.init_app(app)

    # AQUI FOI A MUDANÇA: O simulador agora abre direto na URL principal
    app.register_blueprint(simulador_bp, url_prefix='/')

    # Cria as tabelas no banco de dados se elas não existirem
    with app.app_context():
        db.create_all()

    return app

