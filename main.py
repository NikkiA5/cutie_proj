import types
# from types import NoneType
import sys  
from PyQt5 import QtWidgets

import loginWindow
import signupWindow
import forgetWindow
import mariadb

class LogInApp(QtWidgets.QMainWindow, loginWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  

        self.LogInButton.clicked.connect(self.login_button)
        self.RegistrationButton.clicked.connect(self.reg_button)
        self.ForgotPasswordButton.clicked.connect(self.forgot_password)

    def login_button(self):
        check = False
        username = str(self.NameBracket.text())
        password = str(self.PasswordBracket.text())

        if (not username) or (not password):
            self.showMessageBox('Attention!', 'You haven\'t fill every bracket')

        conn = mariadb.connect(
            user = "admin",
            password = "password",
            host = "localhost",
            port = 3306,
            database = "appdb",
        )
        cur = conn.cursor()
        cur.execute("select * from userlist where username = ? and password = ?", (username, password))

        result = cur.fetchall()
        if len(result) == 0:
            self.showMessageBox('mlem','Check ur username or password again')
        else:
            self.showMessageBox('Welcome','Henlooo!')
            check = True
            conn.close()

        if check:
            return([username, password])
        else:
            return None
        
    def reg_button(self):
        widget = signupWin()
        widget.exec_()

        
    def show_password():
            pass
    def remember_me():
            pass


    def forgot_password(self):
        widget = forgetWin()
        widget.exec_()

    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()



class signupWin(QtWidgets.QDialog, signupWindow.Ui_Form):
    def __init__(self, parent=None):
        super(signupWin, self).__init__(parent)
        self.setupUi(self)

        self.submitButton.clicked.connect(self.registration)

    
    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def registration(self):
        email = self.emailBracket.text()
        password = self.passwordBracket.text()
        username = self.usernameBracket.text()

        if (not email) or (not password) or (not username):
            self.showMessageBox('Attention!', 'You haven\'t fill all brackets')

        conn = mariadb.connect(
            user = "admin",
            password = "password",
            host = "localhost",
            port = 3306,
            database = "appdb",
        )
        cur = conn.cursor()
        
        try:
            cur.execute("insert into userlist(email, password, username) values(?,?,?)", (email, password, username))
            conn.commit()
            conn.close()
            self.showMessageBox('Success!', 'Gratz!')
        except mariadb.Error as e:
            self.showMessageBox('Error!', str(e))
            


class forgetWin(QtWidgets.QDialog, forgetWindow.Ui_Form):
    def __init__(self, parent=None):
        super(forgetWin, self).__init__(parent)
        self.setupUi(self)

        self.submitButton.clicked.connect(self.remember)

    
    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def remember(self):
        email = self.emailBracket.text()

        if (not email):
            self.showMessageBox('Attention!', 'You haven\'t fill all brackets')

        conn = mariadb.connect(
            user = "admin",
            password = "password",
            host = "localhost",
            port = 3306,
            database = "appdb",
        )
        cur = conn.cursor()
        
        cur.execute("select password from userlist where email = ?", (email,))
        result = str(cur.fetchone()[0])

        if len(result) == 0:   
            self.showMessageBox('Error!', 'No users with this email')
        else:
            self.showMessageBox('Success!', result)
            conn.close()


def main():
    app = QtWidgets.QApplication(sys.argv) 
    window = LogInApp()  
    window.show()  
    app.exec_() 

if __name__ == '__main__':  
    main()  