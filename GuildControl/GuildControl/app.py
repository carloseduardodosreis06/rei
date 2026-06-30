import os, qrcode, io, base64
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
from database.models import db, Usuario, Guilda, Membro, Pagamento

# Importação dos Blueprints
from routes.auth import auth
from routes.guildas import guildas
from routes.membros import membros
from routes.planos import planos
from routes.pontuacoes import pontuacoes

app = Flask(__name__)

# Configurações do Banco de Dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///guildcontrol.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "guildcontrol2026")

# Inicializa o banco de dados
db.init_app(app)

# Cria as tabelas do banco de dados automaticamente
with app.app_context():
    db.create_all()

# Registro dos Blueprints
app.register_blueprint(auth)
app.register_blueprint(guildas)
app.register_blueprint(membros)
app.register_blueprint(planos)
app.register_blueprint(pontuacoes)

# Dados de teste para compatibilidade
USUARIO_LOGADO = {
    "username": "GuildMaster_Pro",
    "plano_ativo": "Gratuito",
    "expiracao_plano": None
}

@app.context_processor
def inject_user():
    return dict(usuario=USUARIO_LOGADO)

@app.route("/")
def index():
    return redirect(url_for("auth.login"))

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

@app.route("/verificar-pagamento", methods=["POST"])
def verificar_pagamento():
    dados = request.get_json()
    if not dados:
        return jsonify({"sucesso": False, "mensagem": "Dados inválidos."}), 400
        
    valor_texto = dados.get('valor')
    
    if valor_texto == "15,00":
        dias_acesso = 7
        nome_plano = "Premium Semanal (7 Dias)"
        valor_float = 15.00
    elif valor_texto == "30,00":
        dias_acesso = 20
        nome_plano = "Premium Bronze (20 Dias)"
        valor_float = 30.00
    elif valor_texto == "60,00":
        dias_acesso = 30
        nome_plano = "Premium Ouro (30 Dias)"
        valor_float = 60.00
    else:
        return jsonify({"sucesso": False, "mensagem": "Plano inválido."}), 400

    data_expiracao = datetime.now() + timedelta(days=dias_acesso)
    expiracao_formatada = data_expiracao.strftime("%d/%m/%Y às %H:%M")
    
    USUARIO_LOGADO["plano_ativo"] = nome_plano
    USUARIO_LOGADO["expiracao_plano"] = expiracao_formatada

    try:
        novo_pagamento = Pagamento(
            usuario=USUARIO_LOGADO["username"],
            valor=valor_float,
            status="Pago"
        )
        db.session.add(novo_pagamento)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar pagamento: {e}")

    return jsonify({
        "sucesso": True, 
        "mensagem": "Pagamento validado com sucesso!",
        "plano": USUARIO_LOGADO["plano_ativo"],
        "expira": USUARIO_LOGADO["expiracao_plano"]
    })

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
