import sys,sqlite3,time,re
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QComboBox,QVBoxLayout,QGridLayout,QDialog,QWidget, QPushButton, QApplication, QMainWindow,QAction,QMessageBox,QLabel,QTextEdit,QProgressBar,QLineEdit
from PyQt5.QtCore import QCoreApplication,QRegExp
import student
import librarian

class DBRegister():
    def __init__(self):
        self.conn=sqlite3.connect("bms.db")
        self.c=self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS registrations(regno INTEGER PRIMARY KEY, username TEXT,password TEXT,name TEXT,address TEXT,mobile INTEGER,year INTEGER,gender INTEGER)")

    def addRegistration(self,regno,username,password,name,address,mobile,year,gender):
        try:
            self.c.execute("INSERT INTO registrations(regno,username,password,name,address,mobile,year,gender) VALUES (?,?,?,?,?,?,?,?)",(regno,username,password,name,address,mobile,year,gender))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Registration is successful.')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not Register you.')
                           
class AddUser(QDialog):
    def __init__(self):
        super().__init__()

        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnAdd=QPushButton("Add",self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.yearCombo=QComboBox(self)
        self.yearCombo.addItem("1st")
        self.yearCombo.addItem("2nd")
        self.yearCombo.addItem("3rd")
        self.yearCombo.addItem("4th")

        self.genderCombo = QComboBox(self)
        self.genderCombo.addItem("Male")
        self.genderCombo.addItem("Female")

        self.regLabel = QLabel("Registration No.")
        self.userLabel = QLabel("Username")
        self.passLabel=QLabel("Password")
        self.nameLabel=QLabel("Name")
        self.addressLabel = QLabel("Address")
        self.mobLabel = QLabel("Mobile")
        self.yearLabel = QLabel("Current Year")
        self.genderLabel=QLabel("Gender")

        self.regText = QLineEdit(self)
        self.userText = QLineEdit(self)
        self.passText= QLineEdit(self)
        self.passText.setEchoMode(QLineEdit.Password)
        self.nameText=QLineEdit(self)
        self.addressText = QLineEdit(self)
        self.mobText = QLineEdit(self)

        self.grid=QGridLayout(self)
        self.grid.addWidget(self.regLabel, 1, 1)
        self.grid.addWidget(self.userLabel, 2, 1)
        self.grid.addWidget(self.passLabel,3,1)
        self.grid.addWidget(self.nameLabel,4,1)
        self.grid.addWidget(self.genderLabel, 5, 1)
        self.grid.addWidget(self.addressLabel, 6, 1)
        self.grid.addWidget(self.mobLabel, 7, 1)
        self.grid.addWidget(self.yearLabel,8,1)

        self.grid.addWidget(self.regText, 1, 2)
        self.grid.addWidget(self.userText, 2, 2)
        self.grid.addWidget(self.passText,3,2)
        self.grid.addWidget(self.nameText,4,2)
        self.grid.addWidget(self.genderCombo, 5, 2)
        self.grid.addWidget(self.addressText, 6, 2)
        self.grid.addWidget(self.mobText, 7, 2)
        self.grid.addWidget(self.yearCombo,8,2)

        self.grid.addWidget(self.btnReset,10,1)
        self.grid.addWidget(self.btnCancel,10,3)
        self.grid.addWidget(self.btnAdd,10,2)

        self.btnAdd.clicked.connect(self.addRegistration)
        self.btnCancel.clicked.connect(self.close)
        self.btnReset.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Registration Form")
        self.resize(500,300)
        self.show()
        #sys.exit(self.exec())
        self.exec()

    def reset(self):
        self.regText.setText("")
        self.userText.setText("")
        self.passText.setText("")
        self.nameText.setText("")
        self.addressText.setText("")
        self.mobText.setText("")
        
    def addRegistration(self):
        self.gender=self.genderCombo.currentIndex()
        self.year=self.yearCombo.currentIndex()
        self.regno=self.regText.text()
        self.username=self.userText.text()
        self.password=self.passText.text()
        self.name=self.nameText.text()
        self.address=self.addressText.text()
        self.mobile=int(self.mobText.text())

        #sp=['!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','}']

        if re.search('[0-9]',self.password) is None:
            QMessageBox.warning(QMessageBox(), 'Error', 'Password must have a digit')
            return None
        elif re.search('[A-Z]',self.password) is None:
            QMessageBox.warning(QMessageBox(), 'Error', 'Password must have a Capital letter')
            return None
        #elif re.search(sp,self.password) is None:
            #QMessageBox.warning(QMessageBox(), 'Error', 'Password must have a Special character')
            #return None
        else:
            self.dbregister=DBRegister()
            self.dbregister.addRegistration(self.regno,self.username,self.password,self.name,self.address,self.mobile,self.year,self.gender)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.btnStudentLogin=QPushButton("Student Login",self)
        self.btnLibrarian=QPushButton("Librarian Login",self)
        self.btnNewUser=QPushButton("New User",self)

        #picture
        self.picLabel=QLabel(self)
        self.picLabel.resize(150,150)
        self.picLabel.move(120,20)
        self.picLabel.setScaledContents(True)
        self.picLabel.setPixmap(QtGui.QPixmap("user.jpg"))

        self.btnStudentLogin.move(15,185)
        self.btnStudentLogin.resize(180,40)
        self.btnStudentLoginFont=self.btnStudentLogin.font()
        self.btnStudentLoginFont.setPointSize(13)
        self.btnStudentLogin.setFont(self.btnStudentLoginFont)
        self.btnStudentLogin.clicked.connect(self.studentlogin)

        self.btnLibrarian.move(205,185)
        self.btnLibrarian.resize(180, 40)
        self.btnLibrarianFont = self.btnStudentLogin.font()
        self.btnLibrarianFont.setPointSize(13)
        self.btnLibrarian.setFont(self.btnLibrarianFont)
        self.btnLibrarian.clicked.connect(self.librarianlogin)

        self.btnNewUser.move(110, 230)
        self.btnNewUser.resize(180, 40)
        self.btnNewUserFont = self.btnStudentLogin.font()
        self.btnNewUserFont.setPointSize(13)
        self.btnNewUser.setFont(self.btnNewUserFont)
        self.btnNewUser.clicked.connect(self.newuser)

        self.resize(400,280)
        self.setWindowTitle("Books Management System")

    def studentlogin(self):
        #student #password
        student.login = student.Login()
        if student.login.exec_() == QDialog.Accepted:
            student.window = student.Window()
            student.window.show()
    def librarianlogin(self):
        #admin #pass
        librarian.login = librarian.Login()
        if librarian.login.exec_() == QDialog.Accepted:
            librarian.window = librarian.Window()
            librarian.window.show()
    def newuser(self):
        newUser = AddUser()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
