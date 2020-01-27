from suds.client import Client
from suds import WebFault
from model.project import Project

class SoapHelper():

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        soap_config = self.app.config["soap"]
        client = Client(soap_config["wsdl"])
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self):
        project_list=[]
        soap_config = self.app.config["soap"]
        client = Client(soap_config["wsdl"])
        projects = client.service.mc_projects_get_user_accessible(self.app.config["web_admin"]['username'],
                                                                  self.app.config["web_admin"]['password'])
        for obj in projects:
            project_list.append(Project(id = obj.id, name = obj.name, desc = obj.description, status = obj.status,
                                        view_status= obj.view_state))
        return project_list