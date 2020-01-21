from model.project import Project
import pymysql

class Dbfixture():
    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host = host, database = name, user = user, password = password, autocommit = True)

    def get_project_list(self):
        cursor = self.connection.cursor()
        list=[]
        try:
            cursor.execute("select id, name, status, view_state, description from mantis_project_table")
            for row in cursor:
                (id, name, status, view_status, desc) = row
                status = self.transfordm_status(status)
                view_status = self.transform_view_state(view_status)
                list.append(Project(id = str(id), name=name, status = status, view_status = view_status, desc =desc))
        finally:
            cursor.close()
        return list

    def destroy(self):
        self.connection.close()

    def transfordm_status(self, status):
        if status == 10:
            return 'development'
        elif status == 20:
            return 'release'
        elif status == 70:
            return 'obsolete'

    def transform_view_state(self, view_state):
        if view_state == 10:
            return 'public'
        elif view_state == 50:
            return 'private'