from telnetlib import Telnet

class JamesHelper():
    def __init__(self, app):
        self.app = app

    # def t(self, username, password):
    #     session = JamesHelper.Session("localhost", 4555, "root", "root")
    #     session.create_user(username, password)

    def ensure_user_exists(self, username, password):
        james_config = self.app.config["james"]
        session = JamesHelper.Session(james_config["host"],james_config["port"], james_config["username"], james_config["password"])
        if session.is_users_registred(username):
            session.reset_password(username, password)
        else:
            session.create_user(username,password)
        session.quit()

    class Session():
        def __init__(self, host, port, username, password):
            self.telnet = Telnet(host, port, 5)
            self.read_until("Login id:")
            self.write(username + "\n")
            self.read_until("Password:")
            self.write(password + "\n")
            self.read_until('Welcome root. HELP for a list of commands')

        def read_until(self, text):
            self.telnet.read_until(text.encode('ascii'), 5)

        def write(self, text):
            self.telnet.write(text.encode('ascii'))

        def is_users_registred(self, username):
            self.write("verify %s \n" % username)
            res = self.telnet.expect([b"does not exist", b"exist"])
            return res[0] == 1

        def create_user(self, username, password):
            self.write(f"adduser {username} {password} \n")
            self.read_until(f"User {username} added")

        def reset_password(self, username, password):
            self.write(f"setpassword {username} {password} \n")
            self.read_until(f"Password for {username} reset")

        def quit(self):
            self.write("quit\n")
