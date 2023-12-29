from ckan.plugins import toolkit
from flask import Blueprint

ns = Blueprint("ns", __name__)


def dcat_spec():
    return toolkit.render('dcat-ap/index.html')


ns.add_url_rule("/ns", view_func=dcat_spec)


def get_blueprints():
    return [ns]
