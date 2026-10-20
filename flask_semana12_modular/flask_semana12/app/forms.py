from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    name = StringField(
        "Nome de usuário",
        validators=[
            DataRequired(message="Informe um nome de usuário."),
            Length(min=2, max=120, message="Use entre 2 e 120 caracteres."),
        ],
    )
    submit = SubmitField("Cadastrar")
