import qrcode, io, base64
from flask import Blueprint, render_template, request, redirect, url_for

planos = Blueprint("planos", __name__)

CHAVE_PIX = "ce023233@gmail.com"

@planos.route("/pagamentos")
def pagamentos():
    # Gera um QR Code básico para a chave Pix
    img = qrcode.make(CHAVE_PIX)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return render_template("pagamentos.html", chave_pix=CHAVE_PIX, qrcode_image=qr_base64)

@planos.route("/plano/escolher", methods=["POST"])
def escolher_plano():
    return redirect(url_for("planos.pagamentos"))
