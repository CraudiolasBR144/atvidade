from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError

from app import db
from app.email_service import send_all_registration_emails
from app.forms import NameForm
from app.models import Email, Role, User

main = Blueprint("main", __name__)


def get_user_role():
    role = Role.query.filter_by(name="User").first()
    if role is None:
        role = Role(name="User")
        db.session.add(role)
        db.session.commit()
    return role


@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()

    if form.validate_on_submit():
        username = form.name.data.strip()
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            session["name"] = existing_user.username
            session["known"] = True
            flash("Esse usuário já está cadastrado.", "info")
            return redirect(url_for("main.index"))

        user = User(username=username, role=get_user_role())
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Não foi possível cadastrar esse usuário. Tente novamente.", "danger")
            return redirect(url_for("main.index"))

        session["name"] = username
        session["known"] = False

        try:
            send_all_registration_emails(user)
            flash("Usuário cadastrado e e-mails enviados aos dois destinatários.", "success")
        except Exception as error:
            # O usuário continua cadastrado mesmo se o serviço de e-mail falhar.
            db.session.rollback()
            current_app_logger = __import__("logging").getLogger(__name__)
            current_app_logger.exception("Falha no envio de e-mail: %s", error)
            flash(
                "Usuário cadastrado, mas houve uma falha no envio de e-mail. "
                "Confira as configurações do Mailgun e os logs do servidor.",
                "warning",
            )

        return redirect(url_for("main.index"))

    users = User.query.order_by(User.id).all()
    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        known=session.get("known", False),
        users=users,
        users_count=User.query.count(),
        roles_count=Role.query.count(),
    )


@main.route("/emails-enviados")
def emails_enviados():
    emails = Email.query.order_by(Email.timestamp.desc()).all()
    return render_template("emailsEnviados.html", emails=emails)


@main.route("/health")
def health():
    return {"status": "ok"}
