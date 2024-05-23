import requests
from robot.api.deco import keyword, library
from robot.api import logger, FatalError, Failure

@library
class CkanLibrary:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self, host='localhost', port=80):
        logger.debug("Using CkanLibrary")
        self.host = host
        self.port = port

    def call_action(self, action, **params):
        return requests.get(f"http://{self.host}:{self.port}/api/action/{action}", params=params).json()

    def open_page(self, path=""):
        return requests.get(f"http://{self.host}:{self.port}{path}")

    @keyword
    def ckan_version_should_be(self, version):
        running_version = self.call_action("status_show")["result"]["ckan_version"]
        if running_version != version:
            raise Failure(f"CKAN version should be {version} but is {running_version}")

