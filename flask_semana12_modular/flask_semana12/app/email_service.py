import os

import requests

from app import db
from app.models import Email

PROFESSOR_EMAIL = "flaskaulasweb@zohomail.com"


def send_registration_email(user, recipient):
    """Envia uma notificação individual e registra o envio bem-sucedido."""
    api_url = os.getenv("MAILGUN_API_URL")
    api_key = os.getenv("MAILGUN_API_KEY")
    sender = os.getenv("MAILGUN_FROM")
    student_name = os.getenv("ALUNO_NOME")
    student_record = os.getenv("ALUNO_PRONTUARIO")

    missing = [
        key for key, value in {
            "MAILGUN_API_URL": api_url,
            "MAILGUN_API_KEY": api_key,
            "MAILGUN_FROM": sender,
            "ALUNO_NOME": student_name,
            "ALUNO_PRONTUARIO": student_record,
        }.items() if not value
    ]
    if missing:
        raise RuntimeError(
            "Variáveis ausentes no .env: " + ", ".join(missing)
        )

    subject = "[Flasky] Novo usuário cadastrado"
    body = (
        "Novo usuário cadastrado na aplicação Flasky.\n\n"
        f"Prontuário: {student_record}\n"
        f"Nome do aluno: {student_name}\n"
        f"Usuário cadastrado: {user.username}\n"
    )

    response = requests.post(
        api_url,
        auth=("api", api_key),
        data={
            "from": sender,
            "to": recipient,
            "subject": subject,
            "text": body,
        },
        timeout=20,
    )
    response.raise_for_status()

    db.session.add(
        Email(
            sender=sender,
            recipient=recipient,
            subject=subject,
            text=body,
        )
    )
    db.session.commit()
    return response.json()


def send_all_registration_emails(user):
    """Envia para o e-mail do professor e para o e-mail institucional do aluno."""
    student_email = os.getenv("ALUNO_EMAIL")
    if not student_email:
        raise RuntimeError("A variável ALUNO_EMAIL não está configurada no .env.")

    # Envia separadamente para que cada destinatário tenha seu próprio registro.
    results = []
    for recipient in (PROFESSOR_EMAIL, student_email):
        results.append({
            "recipient": recipient,
            "result": send_registration_email(user, recipient),
        })
    return results
