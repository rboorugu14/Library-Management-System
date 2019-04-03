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

    def addBook(self,idn,title,author,bookyear,price):
        try:
            self.c.execute("INSERT INTO books (idn,title,author,bookyear,price) VALUES (?,?,?,?,?)",(idn,title,author,bookyear,price))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Book is added successfully to the database.')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add Book to the database.')

    def addPayment(self,regno,fee,semester):
        reciept_no=int(time.time())
        date=time.strftime("%b %d %Y %H:%M:%S")
        try:
            self.c.execute("SELECT * from payments WHERE regno=" + str(regno))
            self.conn.commit()

            if not self.c.fetchone():
                if semester == 1:
                    self.c.execute("SELECT * from payments WHERE regno=" + str(regno) + " AND semester=0")

                    if not self.c.fetchone():
                        QMessageBox.warning(QMessageBox(), 'Error','Student with Registration No. ' + str(regno) + ' has Odd Semester fee pending.Pay that first.')
                        return None
                else:
                    self.c.execute("INSERT INTO payments (reciept_no,regno,fee,semester,reciept_date) VALUES (?,?,?,?,?)",(reciept_no, regno, fee, semester, date))
                    self.conn.commit()
                QMessageBox.information(QMessageBox(), 'Successful','Payment is added successfully to the database.\nReference ID=' + str(reciept_no))
            else:
                self.c.execute("SELECT * from payments WHERE regno=" + str(regno))
                self.data = self.c.fetchall()

                if len(self.data) == 2:
                    QMessageBox.warning(QMessageBox(), 'Error','Student with Registration No. ' + str(regno) + ' has already paid both semester fees.')
                
                elif semester==1:
                    self.c.execute("SELECT * from payments WHERE regno=" + str(regno)+" AND semester=0")
                    if not self.c.fetchone():
                        QMessageBox.warning(QMessageBox(), 'Error','Student with registration no ' + str(regno) + ' has Odd Semester fee payment due.Pay that first.')
                    else:
                        self.c.execute("INSERT INTO payments (reciept_no,regno,fee,semester,reciept_date) VALUES (?,?,?,?,?)",(reciept_no, regno, fee, semester, date))
                        self.conn.commit()
                        QMessageBox.information(QMessageBox(), 'Successful','Payment is added successfully to the database.\nReference ID=' + str(reciept_no))

                elif self.data[0][3] == semester:
                    QMessageBox.warning(QMessageBox(), 'Error','Student with Registration No. ' + str(regno) + ' has already paid this semester fees.')

                else:
                    self.c.execute("INSERT INTO payments (reciept_no,regno,fee,semester,reciept_date) VALUES (?,?,?,?,?)",(reciept_no, regno, fee, semester, date))
                    self.conn.commit()
                    QMessageBox.information(QMessageBox(), 'Successful','Payment is added successfully to the database.\nReference ID=' + str(reciept_no))

        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add payment to the database.')

        self.c.close()
        self.conn.close()

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

    def deletebook(self,idn):
        self.c.execute("SELECT * from books WHERE idn="+str(idn))
        self.data=self.c.fetchone()
        if not self.data:
            QMessageBox.warning(QMessageBox(),'Error', 'Could not find any Book with ID '+str(idn))
            return None
        self.c.execute("DELETE from books WHERE idn="+str(idn))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        QMessageBox.information(QMessageBox(), 'Successful','Book is deleted successfully from the database.\nBook ID=' + str(idn))

    def updatebook(self,idn,title,author,bookyear,price):
        self.c.execute("SELECT * from books WHERE idn="+str(idn))
        self.data=self.c.fetchone()
        if not self.data:
            QMessageBox.warning(QMessageBox(),'Error', 'Could not find any Book with ID '+str(idn))
            return None
        self.c.execute("UPDATE books SET title=?, author=?, bookyear=?, price=? WHERE idn=?",(title,author,bookyear,price,idn))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        QMessageBox.information(QMessageBox(), 'Successful','Book is updated successfully.\nBook ID=' + str(idn))

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

    table.horizontalHeader().setStretchLastSection(True)
    table.show()
    dialog = QDialog()
    dialog.setWindowTitle("Book Details")
    dialog.resize(500, 300)
    dialog.setLayout(QVBoxLayout())
    dialog.layout().addWidget(table)
    dialog.exec()

class AddBook(QDialog):
    def __init__(self):
        super().__init__()
        idn = -1
        title = ""
        author = ""
        bookyear = ""
        price = ""
        
        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnAdd=QPushButton("Add",self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.idnLabel=QLabel("Book ID")
        self.titleLabel=QLabel("Book Title")
        self.authorLabel = QLabel("Book Author")
        self.bookyearLabel = QLabel("Book Year")
        self.priceLabel = QLabel("Book Price")
    
        self.idnText=QLineEdit(self)
        self.titleText=QLineEdit(self)
        self.authorText = QLineEdit(self)
        self.bookyearText = QLineEdit(self)
        self.priceText = QLineEdit(self)

        self.grid=QGridLayout(self)
        self.grid.addWidget(self.idnLabel,1,1)
        self.grid.addWidget(self.titleLabel,2,1)
        self.grid.addWidget(self.authorLabel, 3, 1)
        self.grid.addWidget(self.bookyearLabel, 4, 1)
        self.grid.addWidget(self.priceLabel, 5, 1)

        self.grid.addWidget(self.idnText,1,2)
        self.grid.addWidget(self.titleText,2,2)
        self.grid.addWidget(self.authorText, 3, 2)
        self.grid.addWidget(self.bookyearText, 4, 2)
        self.grid.addWidget(self.priceText, 5, 2)

        self.grid.addWidget(self.btnReset,7,1)
        self.grid.addWidget(self.btnCancel,7,3)
        self.grid.addWidget(self.btnAdd,7,2)

        self.btnAdd.clicked.connect(self.addBook)
        self.btnCancel.clicked.connect(self.close)
        self.btnReset.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Add Book Details")
        self.resize(500,300)
        self.show()
        #sys.exit(self.exec())
        self.exec()

    def reset(self):
        self.idnText.setText("")
        self.titleText.setText("")
        self.authorText.setText("")
        self.bookyearText.setText("")
        self.priceText.setText("")

    def addBook(self):
        self.idn=int(self.idnText.text())
        self.title=self.titleText.text()
        self.author=self.authorText.text()
        self.bookyear=self.bookyearText.text()
        self.price=int(self.priceText.text())

        self.dbhelper=DBHelper()
        self.dbhelper.addBook(self.idn,self.title,self.author,self.bookyear,self.price)

class UpdateBook(QDialog):
    def __init__(self):
        super().__init__()
        idn = -1
        title = ""
        author = ""
        bookyear = ""
        price = ""
        
        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnUpdate=QPushButton("Update",self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnUpdate.setFixedHeight(30)

        self.idnLabel=QLabel("Book ID")
        self.titleLabel=QLabel("Book Title")
        self.authorLabel = QLabel("Book Author")
        self.bookyearLabel = QLabel("Book Year")
        self.priceLabel = QLabel("Book Price")
    
        self.idnText=QLineEdit(self)
        self.titleText=QLineEdit(self)
        self.authorText = QLineEdit(self)
        self.bookyearText = QLineEdit(self)
        self.priceText = QLineEdit(self)

        self.grid=QGridLayout(self)
        self.grid.addWidget(self.idnLabel,1,1)
        self.grid.addWidget(self.titleLabel,2,1)
        self.grid.addWidget(self.authorLabel, 3, 1)
        self.grid.addWidget(self.bookyearLabel, 4, 1)
        self.grid.addWidget(self.priceLabel, 5, 1)

        self.grid.addWidget(self.idnText,1,2)
        self.grid.addWidget(self.titleText,2,2)
        self.grid.addWidget(self.authorText, 3, 2)
        self.grid.addWidget(self.bookyearText, 4, 2)
        self.grid.addWidget(self.priceText, 5, 2)

        self.grid.addWidget(self.btnReset,7,1)
        self.grid.addWidget(self.btnCancel,7,3)
        self.grid.addWidget(self.btnUpdate,7,2)

        self.btnUpdate.clicked.connect(self.updatebook)
        self.btnCancel.clicked.connect(self.close)
        self.btnReset.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Update Book Details")
        self.resize(500,300)
        self.show()
        #sys.exit(self.exec())
        self.exec()

    def reset(self):
        self.idnText.setText("")
        self.titleText.setText("")
        self.authorText.setText("")
        self.bookyearText.setText("")
        self.priceText.setText("")

    def updatebook(self):
        self.idn=int(self.idnText.text())
        self.title=self.titleText.text()
        self.author=self.authorText.text()
        self.bookyear=self.bookyearText.text()
        self.price=int(self.priceText.text())

        self.dbhelper=DBHelper()
        self.dbhelper.updatebook(self.idn,self.title,self.author,self.bookyear,self.price)
        
class AddPayment(QDialog):
    def __init__(self):
        super().__init__()

        self.reciept_no=-1
        self.regno=-1
        self.fee=-1
        self.semester=-1
        self.date=-1

        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnAdd=QPushButton("Add",self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.semesterCombo = QComboBox(self)
        self.semesterCombo.addItem("Odd")
        self.semesterCombo.addItem("Even")

        self.regnoLabel=QLabel("Registration No.")
        self.feeLabel=QLabel("Total Fee")
        self.semesterLabel = QLabel("Semester")

        self.regnoText=QLineEdit(self)
        self.feeLabelText=QLineEdit(self)


        self.grid=QGridLayout(self)
        self.grid.addWidget(self.regnoLabel,1,1)
        self.grid.addWidget(self.feeLabel,2,1)
        self.grid.addWidget(self.semesterLabel, 3, 1)


        self.grid.addWidget(self.regnoText,1,2)
        self.grid.addWidget(self.feeLabelText,2,2)
        self.grid.addWidget(self.semesterCombo, 3, 2)

        self.grid.addWidget(self.btnReset,4,1)
        self.grid.addWidget(self.btnCancel,4,3)
        self.grid.addWidget(self.btnAdd,4,2)

        self.btnAdd.clicked.connect(self.addPayment)
        self.btnCancel.clicked.connect(self.close)
        self.btnReset.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Add Payment Details")
        self.resize(400,200)
        self.show()
        #sys.exit(self.exec())
        self.exec()
        
    def reset(self):
        self.regnoText.setText("")
        self.feeLabelText.setText("")

    def addPayment(self):
        self.semester=self.semesterCombo.currentIndex()
        self.regno=int(self.regnoText.text())
        self.fee=int(self.feeLabelText.text())

        self.dbhelper=DBHelper()
        self.dbhelper.addPayment(self.regno,self.fee,self.semester)

# Default username and password are admin and pass respectively.
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

        self.setWindowTitle("Librarian Login")

    def handleLogin(self):
        if (self.textName.text() == 'admin' and self.textPass.text() == 'pass'):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad Username or Password')

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.idnToBeSearched=0
        self.vbox = QVBoxLayout()
        self.text = QLabel("Enter the Book ID")
        self.editField = QLineEdit()
        self.btnSearch = QPushButton("Search", self)
        self.btnSearch.clicked.connect(self.deleteBook)
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.editField)
        self.vbox.addWidget(self.btnSearch)
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Delete Book")
        self.dialog.setLayout(self.vbox)

        self.regnoForPayment = 0
        self.vboxPayment = QVBoxLayout()
        self.textPayment = QLabel("Enter the Student Registration No.")
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


        self.btnEnterPayment=QPushButton("Add Payment Details",self)
        self.btnEnterBook=QPushButton("Add Book",self)
        self.btnShowPaymentDetails=QPushButton("Show Payment Details",self)
        self.btnDeleteBook=QPushButton("Delete Book",self)
        self.btnUpdateBook=QPushButton("Update Book",self)
        self.btnSearchBook=QPushButton("Search Book",self)
        

        #picture
        self.picLabel=QLabel(self)
        self.picLabel.resize(150,150)
        self.picLabel.move(120,20)
        self.picLabel.setScaledContents(True)
        self.picLabel.setPixmap(QtGui.QPixmap("user.png"))

        self.btnEnterPayment.move(15,170)
        self.btnEnterPayment.resize(180,40)
        self.btnEnterPaymentFont=self.btnEnterPayment.font()
        self.btnEnterPaymentFont.setPointSize(13)
        self.btnEnterPayment.setFont(self.btnEnterPaymentFont)
        self.btnEnterPayment.clicked.connect(self.enterpayment)

        self.btnEnterBook.move(15, 220)
        self.btnEnterBook.resize(180, 40)
        self.btnEnterBookFont = self.btnEnterPayment.font()
        self.btnEnterBookFont.setPointSize(13)
        self.btnEnterBook.setFont(self.btnEnterBookFont)
        self.btnEnterBook.clicked.connect(self.enterbook)

        self.btnShowPaymentDetails.move(205,170)
        self.btnShowPaymentDetails.resize(180, 40)
        self.btnShowPaymentDetailsFont = self.btnEnterPayment.font()
        self.btnShowPaymentDetailsFont.setPointSize(13)
        self.btnShowPaymentDetails.setFont(self.btnShowPaymentDetailsFont)
        self.btnShowPaymentDetails.clicked.connect(self.showStudentPaymentDialog)

        self.btnDeleteBook.move(205, 220)
        self.btnDeleteBook.resize(180, 40)
        self.btnDeleteBookFont = self.btnEnterPayment.font()
        self.btnDeleteBookFont.setPointSize(13)
        self.btnDeleteBook.setFont(self.btnDeleteBookFont)
        self.btnDeleteBook.clicked.connect(self.deleteBookDialog)

        self.btnUpdateBook.move(15, 270)
        self.btnUpdateBook.resize(180, 40)
        self.btnUpdateBookFont=self.btnEnterPayment.font()
        self.btnUpdateBookFont.setPointSize(13)
        self.btnUpdateBook.setFont(self.btnUpdateBookFont)
        self.btnUpdateBook.clicked.connect(self.updatebook)

        self.btnSearchBook.move(205, 270)
        self.btnSearchBook.resize(180, 40)
        self.btnSearchBookFont=self.btnEnterPayment.font()
        self.btnSearchBookFont.setPointSize(13)
        self.btnSearchBook.setFont(self.btnSearchBookFont)
        self.btnSearchBook.clicked.connect(self.searchbookDialog)
        
        self.resize(400,325)
        self.setWindowTitle("Books Management System")

    def enterbook(self):
        enterBook=AddBook()
    def enterpayment(self):
        enterpayment=AddPayment()
    def searchbookDialog(self):
        self.dialogBook.exec()
    def deleteBookDialog(self):
        self.dialog.exec()
    def showStudentPaymentDialog(self):
        self.dialogPayment.exec()
    def updatebook(self):
        updateBook=UpdateBook()
    def deleteBook(self):
        if self.editField.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error', 'You must give the Book ID to delete.')
            return None
        forbook = DBHelper()
        forbook.deletebook(int(self.editField.text()))
    def showStudentPayment(self):
        if self.editFieldPayment.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error', 'You must give the Registration No. to show the details.')
            return None
        showpayment = DBHelper()
        showpayment.searchPayment(int(self.editFieldPayment.text()))
    def Searchbook(self):
        if self.editFieldBook.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error','You must give the Book ID to show the details.')
            return None
        forbook = DBHelper()
        forbook.searchBook(self.editFieldBook.text())
