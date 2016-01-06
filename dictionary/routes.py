# -*- coding: utf-8 -*-

"""All app routes."""


from flask import Blueprint, request
from .forms import SlashCommandForm
from .client import get_definition
from .helpers import make_json_response

app_bp = Blueprint('app', __name__)


@app_bp.route('/', methods=['POST'])
def define_a_word():
    data = request.get_json(force=True, silent=True) or {}
    form = SlashCommandForm.from_json(data)
    form.validate()

    text = form.text.data
    definition = get_definition(text)

    resp = dict(response_type='in_channel',
                text='Urban Dictionary Definition',
                attachments=[dict(text=definition['definition'],
                                  author_name=definition['author'],
                                  title=definition['word'],
                                  title_link=definition['permalink'])])
    return make_json_response(**resp)
