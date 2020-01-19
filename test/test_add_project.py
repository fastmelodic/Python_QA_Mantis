
def test_add_project(app, json_projects):
    project = json_projects
    app.project.add_new_porject(project)
    assert app.project.find_name(project)

    #assert len(old_val)+1 == len(new_val)

    #изменить ассерт, т.к. имена уникальные, реализовать проверку по поиску имени на странице