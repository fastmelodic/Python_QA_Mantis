from sys import maxsize


class Project():
    def __init__(self, name, status = None, view_status = None, desc = None, id = None):
        self.name = name
        self.desc = desc
        self.id = id
        self.status = status
        self.view_status = view_status

    def __repr__(self):
        return f"id = {self.id}, name = {self.name}, status = {self.status}, view_status{self.view_status} discritotion = {self.desc} "

    def __eq__(self, other):
        return self.name == other.name and (self.id is None or other.id is None or self.id == other.id)

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
