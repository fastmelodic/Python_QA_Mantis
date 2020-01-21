from selenium.webdriver.support.ui import Select
from model.project import Project

class ProjectHelper():

    def __init__(self, app):
        self.app = app

    def open_manage_projects(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php") and len(wd.find_elements_by_xpath("//input[@value='Add Project']")) > 0):
            wd.find_element_by_xpath("//a[contains(text(),'Manage')]").click()
            wd.find_element_by_xpath("//p/span[2]").click()


    def add_new_porject(self, Project):
        wd = self.app.wd
        self.open_manage_projects()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_form(Project.name, Project.desc, Project.status, Project.view_status)
        self.submit()

    def fill_form(self, name, desc, status, view_status):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@name='name']").click()
        wd.find_element_by_xpath("//input[@name='name']").send_keys(name)
        wd.find_element_by_xpath("//textarea[@name='description']").click()
        wd.find_element_by_xpath("//textarea[@name='description']").send_keys(desc)
        wd.find_element_by_xpath("//select[@name='status']").click()
        Select(wd.find_element_by_name("status")).select_by_visible_text(status)
        wd.find_element_by_xpath("//select[@name='view_state']").click()
        Select(wd.find_element_by_name("view_state")).select_by_visible_text(view_status)


    def submit(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Add Project']").click()

    def elements_by_text(self, text):
        self.open_manage_projects()
        wd = self.app.wd
        el = wd.find_elements_by_link_text(text)
        return list(el)

    def find_name(self, Project):
        wd = self.app.wd
        self.open_manage_projects()
        return len(wd.find_elements_by_link_text(Project.name)) > 0

    def delete_project_by_name(self, name):
        wd = self.app.wd
        self.open_manage_projects()
        wd.find_element_by_xpath(f"//a[contains(text(),'{name}')]").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()