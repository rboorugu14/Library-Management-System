import sys,sqlite3,time
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QComboBox,QVBoxLayout,QGridLayout,QDialog,QWidget, QPushButton, QApplication, QMainWindow,QAction,QMessageBox,QLabel,QTextEdit,QProgressBar,QLineEdit
from PyQt5.QtCore import QCoreApplication

class DBHelper():
    def __init__(self):
        self.conn=sqlite3.connect("bms.db")
        self.c=self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS payments(reciept_no INTEGER,regno INTEGER PRIMARY KEY,fee INTEGER,semester INTEGER,reciept_date TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS books(idn INTEGER PRIMARY KEY, title TEXT, author TEXT, bookyear TEXT, price INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS registrations(regno INTEGER PRIMARY KEY, username TEXT,password TEXT,name TEXT,address TEXT,mobile INTEGER,year INTEGER,gender INTEGER)")

    def searchStudent(self,regno):
        self.c.execute("SELECT * from registrations WHERE regno="+str(regno))
        self.data=self.c.fetchone()

        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not find any Student with Registration No. '+str(regno))
            return None
        self.list=self.data
       
        self.c.close()
        self.conn.close()
        showStudent(self.list)

    def searchPayment(self,regno):
        self.c.execute("SELECT * from payments WHERE regno="+str(regno)+" ORDER BY reciept_no DESC")
        self.data=self.c.fetchone()
        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not find any Student with Registration No. '+str(regno))
            return None
        self.list=self.data
        self.c.close()
        self.conn.close()
        showPaymentFunction(self.list)
        
    def searchBook(self,idn):
        self.c.execute("SELECT * from books WHERE idn="+str(idn))
        self.data=self.c.fetchone()
        if not self.data:
            QMessageBox.warning(QMessageBox(),'Error', 'Could not find any Book with ID '+str(idn))
            return None
        self.list=self.data
        self.c.close()
        self.conn.close()
        searchBookFunction(self.list)

    def showBooks(self):
        self.c.execute("SELECT * from books")
        self.data=self.c.fetchall()
        self.list=self.data
        self.c.close()
        self.conn.close()
        showBooksFunction(self.list)

    def rentbook(self,username,password,idn):
        self.c.execute("SELECT * from registrations WHERE username=? and password=?",(username, password))
        self.conn.commit()
        if not self.c.fetchone:
            QMessageBox.warning(QMessageBox(),'Error', 'Username and Password mis-match')
            return None
        self.c.execute("SELECT * from books WHERE idn="+str(idn))
        self.conn.commit()
        if not self.c.fetchone:
            QMessageBox.warning(QMessageBox(),'Error', 'Could not find any Book with ID '+str(idn))
            return None
        self.c.execute("DELETE from books WHERE idn="+str(idn))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        QMessageBox.information(QMessageBox(), 'Successful','Book checkout successful. \nBook ID=' + str(idn))

    def salebook(self,regno,idn,title,author,bookyear,price):
        self.c.execute("SELECT * from registrations WHERE regno="+str(regno))
        self.data=self.c.fetchone()
        if not self.data:
            QMessageBox.warning(QMessageBox(),'Error', 'No Student found with Registration No '+str(regno))
            return None
        self.c.execute("SELECT * from books WHERE idn="+str(idn))
        self.data1=self.c.fetchone()
        if self.data1:
            QMessageBox.warning(QMessageBox(),'Error', 'Book ID already in use. \nPlease re-check with Librarian')
            return None
        self.c.execute("INSERT into books (idn,title,author,bookyear,price) VALUES (?,?,?,?,?)",(idn,title,author,bookyear,price))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        QMessageBox.information(QMessageBox(),'Successful','Book transaction is successful. \nBook ID '+str(idn))

# Default username and password are 'student' and 'password' respectively.
class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.userNameLabel=QLabel("Username")
        self.userPassLabel=QLabel("Password")
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QGridLayout(self)
        layout.addWidget(self.userNameLabel, 1, 1)
        layout.addWidget(self.userPassLabel, 2, 1)
        layout.addWidget(self.textName,1,2)
        layout.addWidget(self.textPass,2,2)
        layout.addWidget(self.buttonLogin,3,1,1,2)

        self.setWindowTitle("Student Login")

    def handleLogin(self):
        if (self.textName.text() == 'student' and self.textPass.text() == 'password'):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad Username or Password')

def showStudent(list):

    gender = ""
    year = ""
    regno=-1
    username=""
    password=""
    name = ""
    address = ""
    mobile = -1
        
    regno=list[0]
    username=list[1]
    password=list[2]
    name=list[3]
    address=list[4]
    mobile=list[5]

    if list[6]==0:
        year="1st"
    elif list[6]==1:
        year="2nd"
    elif list[6]==2:
        year="3rd"
    elif list[6]==3:
        year="4th"
    if list[7]==0:
        gender="Male"
    else:
        gender="Female"

    table=QTableWidget()
    tableItem=QTableWidgetItem()
    table.setRowCount(7)
    table.setColumnCount(2)

    table.setItem(0, 0, QTableWidgetItem("Registration No."))
    table.setItem(0, 1, QTableWidgetItem(str(regno)))
    table.setItem(1, 0, QTableWidgetItem("Username"))
    table.setItem(1, 1, QTableWidgetItem(str(username)))
    table.setItem(2, 0, QTableWidgetItem("Password"))
    table.setItem(2, 1, QTableWidgetItem(str(password)))
    table.setItem(3, 0, QTableWidgetItem("Name"))
    table.setItem(3, 1, QTableWidgetItem(str(name)))
    table.setItem(4, 0, QTableWidgetItem("Year"))
    table.setItem(4, 1, QTableWidgetItem(str(year)))
    table.setItem(5, 0, QTableWidgetItem("Address"))
    table.setItem(5, 1, QTableWidgetItem(str(address)))
    table.setItem(6, 0, QTableWidgetItem("Mobile"))
    table.setItem(6, 1, QTableWidgetItem(str(mobile)))
    table.setItem(7, 0, QTableWidgetItem("Gender"))
    table.setItem(7, 1, QTableWidgetItem(str(gender)))

    table.resizeColumnsToContents();    
    table.horizontalHeader().setStretchLastSection(True)
    table.show()
    dialog=QDialog()
    dialog.setWindowTitle("Student Details")
    dialog.resize(500,300)
    dialog.setLayout(QVBoxLayout())
    dialog.layout().addWidget(table)
    dialog.exec()

def showPaymentFunction(list):

    regno = -1
    reciept_no = -1
    fee = -1
    semester = -1
    reciept_date = ""

    reciept_no = list[0]
    regno = list[1]
    fee = list[2]

    if list[3] == 0:
        semester = "Odd Semester"
    elif list[3]==1:
        semester = "Paid for both Odd and Even Semester"
    reciept_date=list[4]


    table = QTableWidget()
    tableItem = QTableWidgetItem()
    table.setRowCount(5)
    table.setColumnCount(2)

    table.setItem(0, 0, QTableWidgetItem("Receipt No"))
    table.setItem(0, 1, QTableWidgetItem(str(reciept_no)))
    table.setItem(1, 0, QTableWidgetItem("Registration No."))
    table.setItem(1, 1, QTableWidgetItem(str(regno)))
    table.setItem(2, 0, QTableWidgetItem("Total Fee"))
    table.setItem(2, 1, QTableWidgetItem(str(fee)))
    table.setItem(3, 0, QTableWidgetItem("Semester"))
    table.setItem(3, 1, QTableWidgetItem(str(semester)))
    table.setItem(4, 0, QTableWidgetItem("Receipt Date"))
    table.setItem(4, 1, QTableWidgetItem(str(reciept_date)))

    table.resizeColumnsToContents();
    table.horizontalHeader().setStretchLastSection(True)
    table.show()
    dialog = QDialog()
    dialog.setWindowTitle("Student Payment Details")
    dialog.resize(500, 300)
    dialog.setLayout(QVBoxLayout())
    dialog.layout().addWidget(table)
    dialog.exec()

def searchBookFunction(list):

    idn = -1
    title = ""
    author = ""
    bookyear = ""
    price = -1

    idn = list[0]
    title = list[1]
    author = list[2]
    bookyear = list[3]
    price = list[4]

    table = QTableWidget()
    tableItem = QTableWidgetItem()
    table.setRowCount(5)
    table.setColumnCount(2)

    table.setItem(0, 0, QTableWidgetItem("Book ID"))
    table.setItem(0, 1, QTableWidgetItem(str(idn)))
    table.setItem(1, 0, QTableWidgetItem("Book Title"))
    table.setItem(1, 1, QTableWidgetItem(str(title)))
    table.setItem(2, 0, QTableWidgetItem("Book Author"))
    table.setItem(2, 1, QTableWidgetItem(str(author)))
    table.setItem(3, 0, QTableWidgetItem("Book Year"))
    table.setItem(3, 1, QTableWidgetItem(str(bookyear)))
    table.setItem(4, 0, QTableWidgetItem("Book Price"))
    table.setItem(4, 1, QTableWidgetItem(str(price)))

    table.resizeColumnsToContents();
    table.horizontalHeader().setStretchLastSection(True)
    table.show()
    dialog = QDialog()
    dialog.setWindowTitle("Book Details")
    dialog.resize(500, 300)
    dialog.setLayout(QVBoxLayout())
    dialog.layout().addWidget(table)
    dialog.exec()

class Rentbook(QDialog):
    def __init__(self):
        super().__init__()

        self.username=""
        self.password=""
        self.idn=-1
        self.price=-1
        
        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnFinish=QPushButton("Check Out",self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnFinish.setFixedHeight(30)

        self.modeCombo = QComboBox(self)
        self.modeCombo.addItem("")
        self.modeCombo.addItem("Rent")
        self.modeCombo.addItem("Buy")

        self.userLabel=QLabel("Username")
        self.passLabel=QLabel("Password")
        self.idnLabel=QLabel("Book ID")
        self.priceLabel=QLabel("Price")
        self.modeLabel = QLabel("Rent / Buy")

        self.userText=QLineEdit(self)
        self.passText=QLineEdit(self)
        self.passText.setEchoMode(QLineEdit.Password)
        self.idnText=QLineEdit(self)
        self.priceText=QLineEdit(self)

        self.grid=QGridLayout(self)
        self.grid.addWidget(self.userLabel,1,1)
        self.grid.addWidget(self.passLabel,2,1)
        self.grid.addWidget(self.idnLabel,3,1)
        self.grid.addWidget(self.priceLabel,4,1)
        self.grid.addWidget(self.modeLabel, 5, 1)

        self.grid.addWidget(self.userText,1,2)
        self.grid.addWidget(self.passText,2,2)
        self.grid.addWidget(self.idnText,3,2)
        self.grid.addWidget(self.priceText,4,2)
        self.grid.addWidget(self.modeCombo, 5, 2)

        self.grid.addWidget(self.btnReset,6,1)
        self.grid.addWidget(self.btnCancel,6,3)
        self.grid.addWidget(self.btnFinish,6,2)

        self.btnFinish.clicked.connect(self.rentbook)
        self.btnCancel.clicked.connect(self.close)
        self.btnReset.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Buy / Rent Book")
        self.resize(500,300)
        self.show()
        #sys.exit(self.exec())
        self.exec()

    def reset(self):
        self.userText.setText("")
        self.passText.setText("")
        self.idnText.setText("")
        self.priceText.setText("")

    def rentbook(self):
        self.mode=self.modeCombo.currentIndex()
        self.username=self.userText.text()
        self.password=self.passText.text()
        self.idn=int(self.idnText.text())
        
        self.dbhelper=DBHelper()
        self.dbhelper.rentbook(self.username, self.password, self.idn)

class SaleBook(QDialog):
    def __init__(self):
        super().__init__()

        self.regno=-1
        self.idn=-1
        self.title=""
        self.author=""
        self.bookyear=""
        self.price=-1
        
        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnFinish=QPushButton("Submit",self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnFinish.setFixedHeight(30)

        self.modeCombo = QComboBox(self)
        self.modeCombo.addItem("")
        self.modeCombo.addItem("Return")
        self.modeCombo.addItem("Sell")

        self.regnoLabel=QLabel("Registration No")
        self.idnLabel=QLabel("Book ID")
        self.titleLabel=QLabel("Book Title")
        self.authorLabel=QLabel("Book Author")
        self.yearLabel=QLabel("Book Year")
        self.priceLabel=QLabel("Book Price")
        self.modeLabel = QLabel("Return / Sell")

        self.regnoText=QLineEdit(self)
        self.idnText=QLineEdit(self)
        self.titleText=QLineEdit(self)
        self.authorText=QLineEdit(self)
        self.yearText=QLineEdit(self)
        self.priceText=QLineEdit(self)

        self.grid=QGridLayout(self)
        self.grid.addWidget(self.regnoLabel,1,1)
        self.grid.addWidget(self.idnLabel,2,1)
        self.grid.addWidget(self.titleLabel,3,1)
        self.grid.addWidget(self.authorLabel,4,1)
        self.grid.addWidget(self.yearLabel,5,1)
        self.grid.addWidget(self.priceLabel,6,1)
        self.grid.addWidget(self.modeLabel, 7, 1)

        self.grid.addWidget(self.regnoText,1,2)
        self.grid.addWidget(self.idnText,2,2)
        self.grid.addWidget(self.titleText,3,2)
        self.grid.addWidget(self.authorText,4,2)
        self.grid.addWidget(self.yearText,5,2)
        self.grid.addWidget(self.priceText,6,2)
        self.grid.addWidget(self.modeCombo, 7, 2)

        self.grid.addWidget(self.btnReset,8,1)
        self.grid.addWidget(self.btnCancel,8,3)
        self.grid.addWidget(self.btnFinish,8,2)

        self.btnFinish.clicked.connect(self.salebook)
        self.btnCancel.clicked.connect(self.close)
        self.btnReset.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Return / Sell Book")
        self.resize(500,300)
        self.show()
        self.exec()
        
    def reset(self):
        self.regnoText.setText("")
        self.idnText.setText("")
        self.titleText.setText("")
        self.authorText.setText("")
        self.yearText.setText("")
        self.priceText.setText("")

    def salebook(self):
        self.regno=int(self.regnoText.text())
        self.idn=int(self.idnText.text())
        self.title=self.titleText.text()
        self.author=self.authorText.text()
        self.bookyear=self.yearText.text()
        self.price=int(self.priceText.text())

        self.dbhelper=DBHelper()
        self.dbhelper.salebook(self.regno,self.idn,self.title,self.author,self.bookyear,self.price)
        
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.regnoToBeSearched=""
        self.vbox = QVBoxLayout()
        self.text = QLabel("Enter the Registration No. of the Student")
        self.editField = QLineEdit()
        self.btnSearch = QPushButton("Search", self)
        self.btnSearch.clicked.connect(self.showStudent)
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.editField)
        self.vbox.addWidget(self.btnSearch)
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Student Search")
        self.dialog.setLayout(self.vbox)

        self.regnoForPayment = 0
        self.vboxPayment = QVBoxLayout()
        self.textPayment = QLabel("Enter the Registration No. of the Student")
        self.editFieldPayment = QLineEdit()
        self.btnSearchPayment = QPushButton("Search", self)
        self.btnSearchPayment.clicked.connect(self.showStudentPayment)
        self.vboxPayment.addWidget(self.textPayment)
        self.vboxPayment.addWidget(self.editFieldPayment)
        self.vboxPayment.addWidget(self.btnSearchPayment)
        self.dialogPayment = QDialog()
        self.dialogPayment.setWindowTitle("Payment Search")
        self.dialogPayment.setLayout(self.vboxPayment)

        self.bookToBeSearched=""
        self.vboxBook = QVBoxLayout()
        self.textBook = QLabel("Enter the Book ID")
        self.editFieldBook = QLineEdit()
        self.btnSearchBook = QPushButton("Search", self)
        self.btnSearchBook.clicked.connect(self.Searchbook)
        self.vboxBook.addWidget(self.textBook)
        self.vboxBook.addWidget(self.editFieldBook)
        self.vboxBook.addWidget(self.btnSearchBook)
        self.dialogBook = QDialog()
        self.dialogBook.setWindowTitle("Search Book")
        self.dialogBook.setLayout(self.vboxBook)

        self.btnShowStudentDetails=QPushButton("Show Student Details",self)
        self.btnSearchBook=QPushButton("Search Book",self)
        self.btnShowPaymentDetails=QPushButton("Show Payment Details",self)
        self.btnShowBooks=QPushButton("View All Books",self)
        self.btnRentBook=QPushButton("Buy / Rent Book",self)
        self.btnSaleBook=QPushButton("Return / Sell Book",self)

        #picture
        self.picLabel=QLabel(self)
        self.picLabel.resize(150,150)
        self.picLabel.move(120,16)
        self.picLabel.setScaledContents(True)
        self.picLabel.setPixmap(QtGui.QPixmap("stud.gif"))

        self.btnShowStudentDetails.move(15,170)
        self.btnShowStudentDetails.resize(180,40)
        self.btnShowStudentDetailsFont=self.btnShowStudentDetails.font()
        self.btnShowStudentDetailsFont.setPointSize(13)
        self.btnShowStudentDetails.setFont(self.btnShowStudentDetailsFont)
        self.btnShowStudentDetails.clicked.connect(self.showStudentDialog)

        self.btnShowPaymentDetails.move(205,170)
        self.btnShowPaymentDetails.resize(180, 40)
        self.btnShowPaymentDetailsFont = self.btnShowStudentDetails.font()
        self.btnShowPaymentDetailsFont.setPointSize(13)
        self.btnShowPaymentDetails.setFont(self.btnShowPaymentDetailsFont)
        self.btnShowPaymentDetails.clicked.connect(self.showStudentPaymentDialog)

        self.btnSearchBook.move(15, 220)
        self.btnSearchBook.resize(180, 40)
        self.btnSearchBookFont = self.btnShowStudentDetails.font()
        self.btnSearchBookFont.setPointSize(13)
        self.btnSearchBook.setFont(self.btnSearchBookFont)
        self.btnSearchBook.clicked.connect(self.searchbookDialog)

        self.btnShowBooks.move(205, 220)
        self.btnShowBooks.resize(180, 40)
        self.btnShowBooksFont=self.btnShowStudentDetails.font()
        self.btnShowBooksFont.setPointSize(13)
        self.btnShowBooks.setFont(self.btnShowBooksFont)
        self.btnShowBooks.clicked.connect(self.showbooks)

        self.btnRentBook.move(15, 270)
        self.btnRentBook.resize(180, 40)
        self.btnRentBookFont=self.btnShowStudentDetails.font()
        self.btnRentBookFont.setPointSize(13)
        self.btnRentBook.setFont(self.btnRentBookFont)
        self.btnRentBook.clicked.connect(self.rentbook)

        self.btnSaleBook.move(205, 270)
        self.btnSaleBook.resize(180, 40)
        self.btnSaleBookFont = self.btnShowStudentDetails.font()
        self.btnSaleBookFont.setPointSize(13)
        self.btnSaleBook.setFont(self.btnSaleBookFont)
        self.btnSaleBook.clicked.connect(self.salebook)

        self.resize(400,325)
        self.setWindowTitle("Books Management System")

    def showStudentDialog(self):
        self.dialog.exec()
    def showStudentPaymentDialog(self):
        self.dialogPayment.exec()
    def searchbookDialog(self):
        self.dialogBook.exec()
    def salebook(self):
        saleBook=SaleBook()
    def rentbook(self):
        rentBook = Rentbook()
    def showbooks(self):
        showBooks = Showbooks()
    def showStudent(self):
        if self.editField.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error', 'You must give the Registration Number to view details.')
            return None
        showstudent = DBHelper()
        showstudent.searchStudent(int(self.editField.text()))
    def showStudentPayment(self):
        if self.editFieldPayment.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error', 'You must give the Registration Number to view details.')
            return None
        showpayment = DBHelper()
        showpayment.searchPayment(int(self.editFieldPayment.text()))
    def Searchbook(self):
        if self.editFieldBook.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error', 'You must give the Book ID to view details.')
            return None
        forbook = DBHelper()
        forbook.searchBook(self.editFieldBook.text())

#if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #window = Window()
    #window.show()
    #sys.exit(app.exec_())
