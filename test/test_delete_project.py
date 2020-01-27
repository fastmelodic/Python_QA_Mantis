from model.project import Project
import random


def test_delete_project(app,db):
    if len(app.soap.get_project_list()) == 0:
        app.project.add_new_porject(name= "TestTestTest666")
    old_list = app.soap.get_project_list()
    project_to_delete = random.choice(old_list)
    app.project.delete_project_by_name(project_to_delete.name)
    new_list = app.soap.get_project_list()
    old_list.remove(project_to_delete)
    assert sorted(old_list, key=Project.id_or_max) == sorted(new_list, key=Project.id_or_max)