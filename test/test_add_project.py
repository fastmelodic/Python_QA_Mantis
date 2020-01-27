from model.project import Project


def test_add_project(app, json_projects, db):
    project = json_projects
    old_list = app.soap.get_project_list()
    app.project.add_new_porject(project)
    new_list = app.soap.get_project_list()
    old_list.append(project)
    assert sorted(old_list, key=Project.id_or_max) == sorted(new_list, key=Project.id_or_max)
    #assert app.project.find_name(project) #ui check

    
    #assert len(old_val)+1 == len(new_val)
    #изменить ассерт, т.к. имена уникальные, реализовать проверку по поиску имени на странице