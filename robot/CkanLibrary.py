from requests import get, post
from robot.api.deco import keyword, library
from robot.api import logger, Failure

@library
class CkanLibrary:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self, host='localhost', port=80, admin_username='admin', admin_password='administrator'):
        logger.debug("Using CkanLibrary")
        self.host = host
        self.port = port
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.admin_token = None

    def action(self, name):
        return f"http://{self.host}:{self.port}/api/action/{name}"

    def page(self, path=""):
        return f"http://{self.host}:{self.port}{path}"

    @keyword
    def ckan_version_should_be(self, version):
        running_version = get(self.action("status_show")).json()["result"]["ckan_version"]
        if running_version != version:
            raise Failure(f"CKAN version should be {version} but is {running_version}")

    @keyword
    def reset_ckan(self):
        result = post(self.action("reset"), data={'admin_username': self.admin_username,
                                                  'admin_password': self.admin_password})
        self.admin_token = result.json()['result']['token']

    @keyword
    def create_ckan_user(self, name, email, password):
        data = {'name': name, 'email': email, 'password': password}
        headers = {'Authorization': self.admin_token}
        post(self.action('user_create'), data=data, headers=headers)

    @keyword
    def create_organization(self, title_fi, title_sv, name):
        data = {'title_translated': {'fi': title_fi, 'sv': title_sv}, 'name': name, "image_url": ""}
        headers = {'Authorization': self.admin_token}
        post(self.action('organization_create'), json=data, headers=headers)
