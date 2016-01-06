# -*- coding: utf-8 -*-

"""Forms module"""

import wtforms_json

from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import InputRequired

from .errors import APIError

wtforms_json.init()

class SlashCommandForm(Form):
    token = StringField(validators=[InputRequired()])
    team_id = StringField(validators=[InputRequired()])
    channel_id = StringField(validators=[InputRequired()])
    channel_name = StringField(validators=[InputRequired()])
    user_id = StringField(validators=[InputRequired()])
    user_name = StringField(validators=[InputRequired()])
    command = StringField(validators=[InputRequired()])
    text = StringField(validators=[InputRequired()])
    response_url = StringField(validators=[InputRequired()])

    def validate(self):
        if super(SlashCommandForm, self).validate():
            return True
        else:
            raise APIError('Received invalid data')


