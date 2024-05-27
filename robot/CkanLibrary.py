from requests import get, post
from robot.api.deco import keyword, library
from robot.api import logger, Failure

@library
class CkanLibrary:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self, host='localhost', port=80):
        logger.debug("Using CkanLibrary")
        self.host = host
        self.port = port

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
        post(self.action("reset"))
