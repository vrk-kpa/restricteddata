from ckan.plugins import toolkit
from ckan.views.dataset import GroupView as CkanDatasetGroupView
from flask import Blueprint
import logging

log = logging.getLogger(__name__)

ns = Blueprint("ns", __name__)


def dcat_spec():
    return toolkit.render('dcat-ap/index.html')


ns.add_url_rule("/ns", view_func=dcat_spec)


restricted_data_dataset = Blueprint("restricted_data_dataset", __name__,
                                    url_prefix='/dataset',
                                    url_defaults={'package_type': 'dataset'})

class GroupView(CkanDatasetGroupView):
    def post(self, package_type, id):
        context, pkg_dict = self._prepare(id)

        category_list = toolkit.request.form.getlist('groups')
        groups = [{'name': name } for name in category_list ]
        try:
            toolkit.get_action('package_patch')(context, {"id": id, "groups": groups})
            return toolkit.h.redirect_to('dataset_groups', id=id)
        except (toolkit.ObjectNotFound, toolkit.NotAuthorized):
            return toolkit.abort(404, toolkit._('Dataset not found'))


restricted_data_dataset.add_url_rule(u'/groups/<id>', view_func=GroupView.as_view('groups'))

def get_blueprints():
    return [ns, restricted_data_dataset]
