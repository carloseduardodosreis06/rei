from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.models import db, Membro

membros = Blueprint("membros", __name__)

@membros.route("/membros")
def listar_membros():
    todos_membros = Membro.query.all()
    return render_template("ranking.html", membros=todos_membros)

@membros.route("/membros/adicionar", methods=["POST"])
def adicionar_membro():
    nick = request.form.get("nick")
    line = request.form.get("line")

    if nick and line:
        novo_membro = Membro(nick=nick, line=line)
        db.session.add(novo_membro)
        db.session.commit()
        return redirect(url_for("membros.listar_membros"))

    return redirect(url_for("membros.listar_membros"))

@membros.route("/membros/remover/<int:id>")
def remover_membro(id):
    membro = Membro.query.get(id)
    if membro:
        db.session.delete(membro)
        db.session.commit()
    return redirect(url_for("membros.listar_membros"))
