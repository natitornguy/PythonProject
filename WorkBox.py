import sys
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QDate, QDateTime, QSortFilterProxyModel
from library.publicLibrary import *
from Ui_WorkBox import Ui_MainWindow


class MainWindow:
    username = ""
    _id = ""

    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.content.setCurrentWidget(self.ui.Login)

        self.ui.btnLogIn.clicked.connect(self.checkLogin)
        self.ui.btnAdminLogout.clicked.connect(self.logOut)
        self.ui.btnLogout.clicked.connect(self.logOut)
        self.ui.btnReset.clicked.connect(self.resetInsertForm)
        self.ui.btnInsert.clicked.connect(self.InsertUser)
        self.ui.btnRegister.clicked.connect(self.showRegisterPage)
        self.ui.btnBackFromRegis.clicked.connect(self.logOut)
        self.ui.btnDeleteUser.clicked.connect(self.deleteUser)
        self.ui.btnConfirmChangePass.clicked.connect(self.changePassword)
        self.ui.btnResetUserPassword.clicked.connect(self.setNeedChange)
        self.ui.btnPromoteUser.clicked.connect(self.promoteUser)
        self.ui.btnEditUser.clicked.connect(self.editUser)
        self.ui.btnSaveEdit.clicked.connect(self.saveEdit)
        self.ui.btnBackTable.clicked.connect(self.backtoUsersPage)
        self.ui.btnCreateTask.clicked.connect(self.createTaskPage)
        self.ui.btnReturn.clicked.connect(self.backToBoard)
        self.ui.btnClearDetails.clicked.connect(self.clearDetailsPage)
        self.ui.cboStatus.addItem("Waiting")
        self.ui.cboStatus.addItem("Inprogress")
        self.ui.cboStatus.addItem("Ready for QA")
        self.ui.cboStatus.addItem("DONE")
        self.ui.btnSave.clicked.connect(self.creatTask)
        self.ui.tableWaiting.doubleClicked.connect(self.getWaitingTask)
        self.ui.tableInprogress.doubleClicked.connect(self.getInprogressTask)
        self.ui.tableReady.doubleClicked.connect(self.getReadyTask)
        self.ui.tableDone.doubleClicked.connect(self.getDoneTask)
        self.ui.btnDeleteTask.clicked.connect(self.deleteTask)

    def deleteTask(self):
        if self.confirmDialog("ต้องการลบงาน ใช่หรือไม่", "ยืนยัน"):
            if deleteTask(self._id):
                self.showSuccesDialog("ลบเรียบร้อย", "สำเร็จ")
                self.backToBoard(True)
            else:
                self.showErrorDialog("เกิดข้อผิดพลาด", "ผิดพลาด")

    def clearTasksTable(self):
        model = QStandardItemModel(0, 0)
        self.ui.tableWaiting.setModel(model)
        self.ui.tableInprogress.setModel(model)
        self.ui.tableReady.setModel(model)
        self.ui.tableDone.setModel(model)

    def createTaskPage(self):
        self.ui.btnDeleteTask.setEnabled(False)
        self.ui.label_15.setText("Create Task")
        self.ui.btnSave.setText("CREATE")
        self.ui.cboStatus.setDisabled(True)
        self.ui.cboStatus.setCurrentIndex(0)
        self.ui.dtCreateDate.setMinimumDate(datetime.now())
        self.ui.dtDeadline.setMinimumDate(datetime.now())
        self.ui.content.setCurrentWidget(self.ui.details)

    def editTask(self, data):
        self.ui.btnDeleteTask.setEnabled(True)
        self.ui.label_15.setText("Edit Task")
        self.ui.btnSave.setText("SAVE")
        self.ui.dtCreateDate.setMinimumDate(QtCore.QDate(2021, 1, 1))
        self.ui.txtHeader.setText(data[0])
        self.ui.txtDetail.setText(data[1])
        self.ui.cboStatus.setCurrentText(data[2])
        self.ui.cboOwner.setCurrentText(data[3])
        createdate = data[4].split("/")
        self.ui.dtCreateDate.setDate(QDate(int(createdate[2]), int(createdate[1]), int(createdate[0])))
        self.ui.dtDeadline.setMinimumDate(QDate(int(createdate[2]), int(createdate[1]), int(createdate[0])))
        deadline = data[5].split("/")
        self.ui.dtDeadline.setDate(QDate(int(deadline[2]), int(deadline[1]), int(deadline[0])))
        self.ui.content.setCurrentWidget(self.ui.details)

    def getWaitingTask(self):
        self.ui.cboStatus.setEnabled(True)
        index = self.ui.tableWaiting.currentIndex()
        self._id = self.ui.tableWaiting.model().index(index.row(), 0).data()
        topic = self.ui.tableWaiting.model().index(index.row(), 1).data()
        detail = self.ui.tableWaiting.model().index(index.row(), 2).data()
        status = self.ui.tableWaiting.model().index(index.row(), 3).data()
        owner = self.ui.tableWaiting.model().index(index.row(), 4).data()
        createdate = self.ui.tableWaiting.model().index(index.row(), 5).data()
        deadline = self.ui.tableWaiting.model().index(index.row(), 6).data()
        data = [topic, detail, status, owner, createdate, deadline]
        self.editTask(data)

    def getInprogressTask(self):
        self.ui.cboStatus.setEnabled(True)
        index = self.ui.tableInprogress.currentIndex()
        self._id = self.ui.tableInprogress.model().index(index.row(), 0).data()
        topic = self.ui.tableInprogress.model().index(index.row(), 1).data()
        detail = self.ui.tableInprogress.model().index(index.row(), 2).data()
        status = self.ui.tableInprogress.model().index(index.row(), 3).data()
        owner = self.ui.tableInprogress.model().index(index.row(), 4).data()
        createdate = self.ui.tableInprogress.model().index(index.row(), 5).data()
        deadline = self.ui.tableInprogress.model().index(index.row(), 6).data()
        data = [topic, detail, status, owner, createdate, deadline]
        self.editTask(data)

    def getReadyTask(self):
        self.ui.cboStatus.setEnabled(True)
        index = self.ui.tableReady.currentIndex()
        self._id = self.ui.tableReady.model().index(index.row(), 0).data()
        topic = self.ui.tableReady.model().index(index.row(), 1).data()
        detail = self.ui.tableReady.model().index(index.row(), 2).data()
        status = self.ui.tableReady.model().index(index.row(), 3).data()
        owner = self.ui.tableReady.model().index(index.row(), 4).data()
        createdate = self.ui.tableReady.model().index(index.row(), 5).data()
        deadline = self.ui.tableReady.model().index(index.row(), 6).data()
        data = [topic, detail, status, owner, createdate, deadline]
        self.editTask(data)

    def getDoneTask(self):
        self.ui.cboStatus.setEnabled(True)
        index = self.ui.tableDone.currentIndex()
        self._id = self.ui.tableDone.model().index(index.row(), 0).data()
        topic = self.ui.tableDone.model().index(index.row(), 1).data()
        detail = self.ui.tableDone.model().index(index.row(), 2).data()
        status = self.ui.tableDone.model().index(index.row(), 3).data()
        owner = self.ui.tableDone.model().index(index.row(), 4).data()
        createdate = self.ui.tableDone.model().index(index.row(), 5).data()
        deadline = self.ui.tableDone.model().index(index.row(), 6).data()
        data = [topic, detail, status, owner, createdate, deadline]
        self.editTask(data)

    def taskTypeFilter(self):
        alltasks = getAllTasks()
        waiting = []
        inprogress = []
        ready = []
        done = []
        for i in alltasks:
            if i['status'] == 'Waiting':
                waiting.append(i)
            elif i['status'] == 'Inprogress':
                inprogress.append(i)
            elif i['status'] == 'Ready for QA':
                ready.append(i)
            elif i['status'] == 'DONE':
                done.append(i)
        if len(waiting) > 0:
            self.addTasksToWaitingTable(waiting)
        if len(inprogress) > 0:
            self.addTasksToInprogressTable(inprogress)
        if len(ready) > 0:
            self.addTasksToReadyTable(ready)
        if len(done) > 0:
            self.addTasksToDoneTable(done)

        print("Waiting: {}\n".format(waiting))
        print("Inprogress: {}\n".format(inprogress))
        print("Ready for QA: {}\n".format(ready))
        print("DONE: {}\n".format(done))

    def addTasksToWaitingTable(self, task):
        model = QStandardItemModel(len(task), 7)
        model.setHorizontalHeaderLabels(['_ID', 'TOPIC', 'DETAIL', 'STATUS', 'OWNER', 'CREATEDATE', 'DEADLINE'])

        for i, j in enumerate(task):
            id = QStandardItem(str(j['_id']))
            topic = QStandardItem(j['topic'])
            detail = QStandardItem(j['detail'])
            status = QStandardItem(j['status'])
            owner = QStandardItem(j['owner'])
            createdate = QStandardItem(j['createdate'])
            deadline = QStandardItem(j['deadline'])
            model.setItem(i, 0, id)
            model.setItem(i, 1, topic)
            model.setItem(i, 2, detail)
            model.setItem(i, 3, status)
            model.setItem(i, 4, owner)
            model.setItem(i, 5, createdate)
            model.setItem(i, 6, deadline)

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(1)

        self.ui.txtSearch.textChanged.connect(filter_proxy_model.setFilterRegExp)

        self.ui.tableWaiting.setModel(filter_proxy_model)
        self.ui.tableWaiting.setColumnHidden(0, True)
        self.ui.tableWaiting.setColumnHidden(2, True)
        self.ui.tableWaiting.setColumnHidden(3, True)
        self.ui.tableWaiting.setColumnHidden(4, True)
        self.ui.tableWaiting.setColumnHidden(5, True)
        self.ui.tableWaiting.setColumnHidden(6, True)

    def addTasksToInprogressTable(self, task):
        model = QStandardItemModel(len(task), 7)
        model.setHorizontalHeaderLabels(['_ID', 'TOPIC', 'DETAIL', 'STATUS', 'OWNER', 'CREATEDATE', 'DEADLINE'])

        for i, j in enumerate(task):
            id = QStandardItem(str(j['_id']))
            topic = QStandardItem(j['topic'])
            detail = QStandardItem(j['detail'])
            status = QStandardItem(j['status'])
            owner = QStandardItem(j['owner'])
            createdate = QStandardItem(j['createdate'])
            deadline = QStandardItem(j['deadline'])
            model.setItem(i, 0, id)
            model.setItem(i, 1, topic)
            model.setItem(i, 2, detail)
            model.setItem(i, 3, status)
            model.setItem(i, 4, owner)
            model.setItem(i, 5, createdate)
            model.setItem(i, 6, deadline)

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(1)

        self.ui.txtSearch.textChanged.connect(filter_proxy_model.setFilterRegExp)

        self.ui.tableInprogress.setModel(filter_proxy_model)
        self.ui.tableInprogress.setColumnHidden(0, True)
        self.ui.tableInprogress.setColumnHidden(2, True)
        self.ui.tableInprogress.setColumnHidden(3, True)
        self.ui.tableInprogress.setColumnHidden(4, True)
        self.ui.tableInprogress.setColumnHidden(5, True)
        self.ui.tableInprogress.setColumnHidden(6, True)

    def addTasksToReadyTable(self, task):
        model = QStandardItemModel(len(task), 7)
        model.setHorizontalHeaderLabels(['_ID', 'TOPIC', 'DETAIL', 'STATUS', 'OWNER', 'CREATEDATE', 'DEADLINE'])

        for i, j in enumerate(task):
            id = QStandardItem(str(j['_id']))
            topic = QStandardItem(j['topic'])
            detail = QStandardItem(j['detail'])
            status = QStandardItem(j['status'])
            owner = QStandardItem(j['owner'])
            createdate = QStandardItem(j['createdate'])
            deadline = QStandardItem(j['deadline'])
            model.setItem(i, 0, id)
            model.setItem(i, 1, topic)
            model.setItem(i, 2, detail)
            model.setItem(i, 3, status)
            model.setItem(i, 4, owner)
            model.setItem(i, 5, createdate)
            model.setItem(i, 6, deadline)

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(1)

        self.ui.txtSearch.textChanged.connect(filter_proxy_model.setFilterRegExp)

        self.ui.tableReady.setModel(filter_proxy_model)
        self.ui.tableReady.setColumnHidden(0, True)
        self.ui.tableReady.setColumnHidden(2, True)
        self.ui.tableReady.setColumnHidden(3, True)
        self.ui.tableReady.setColumnHidden(4, True)
        self.ui.tableReady.setColumnHidden(5, True)
        self.ui.tableReady.setColumnHidden(6, True)

    def addTasksToDoneTable(self, task):
        model = QStandardItemModel(len(task), 7)
        model.setHorizontalHeaderLabels(['_ID', 'TOPIC', 'DETAIL', 'STATUS', 'OWNER', 'CREATEDATE', 'DEADLINE'])

        for i, j in enumerate(task):
            id = QStandardItem(str(j['_id']))
            topic = QStandardItem(j['topic'])
            detail = QStandardItem(j['detail'])
            status = QStandardItem(j['status'])
            owner = QStandardItem(j['owner'])
            createdate = QStandardItem(j['createdate'])
            deadline = QStandardItem(j['deadline'])
            model.setItem(i, 0, id)
            model.setItem(i, 1, topic)
            model.setItem(i, 2, detail)
            model.setItem(i, 3, status)
            model.setItem(i, 4, owner)
            model.setItem(i, 5, createdate)
            model.setItem(i, 6, deadline)

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(1)

        self.ui.txtSearch.textChanged.connect(filter_proxy_model.setFilterRegExp)

        self.ui.tableDone.setModel(filter_proxy_model)
        self.ui.tableDone.setColumnHidden(0, True)
        self.ui.tableDone.setColumnHidden(2, True)
        self.ui.tableDone.setColumnHidden(3, True)
        self.ui.tableDone.setColumnHidden(4, True)
        self.ui.tableDone.setColumnHidden(5, True)
        self.ui.tableDone.setColumnHidden(6, True)

    def creatTask(self):
        topic = self.ui.txtHeader.toPlainText()
        detail = self.ui.txtDetail.toPlainText()
        status = self.ui.cboStatus.currentText()
        owner = self.ui.cboOwner.currentText()
        createdate = self.ui.dtCreateDate.text()
        deadline = self.ui.dtDeadline.text()
        data = {'topic': topic, 'detail': detail, 'status': status,
                'owner': owner, 'createdate': createdate, 'deadline': deadline}
        if self.ui.btnSave.text() == "CREATE":
            if createTask(data):
                self.showSuccesDialog("สร้างงานเรียบร้อย", "สำเร็จ")
                self.backToBoard(True)
            else:
                self.showErrorDialog("เกิดข้อผิดพลาด", "ผิดพลาด")
        elif self.ui.btnSave.text() == "SAVE":
            if updateTask(self._id, data):
                self.showSuccesDialog("อัพเดตเรียบร้อย", "สำเร็จ")
                self.backToBoard(True)
            else:
                self.showErrorDialog("เกิดข้อผิดพลาด", "ผิดพลาด")

    def clearDetailsPage(self):
        self.ui.txtHeader.setText("")
        self.ui.txtDetail.setText("")
        self.ui.dtDeadline.setDate(datetime.now())

    def backToBoard(self, reload):
        if reload:
            self.clearTasksTable()
            self.taskTypeFilter()
        self.ui.content.setCurrentWidget(self.ui.board)
        self.clearDetailsPage()

    def changePassword(self):
        password = self.ui.txtNewPass.text()
        recheck = self.ui.txtConfirm.text()
        if self.checkNewpassandConfirm(password, recheck):
            if changePassword(self.username, password):
                self.showSuccesDialog("ทำการเปลี่ยนรหัสผ่านเรียบร้อย", "Success")
            self.logOut()

    def addTaskOwnerCbo(self):
        self.ui.cboOwner.clear()
        users = getAllGeneralUser()
        for i in users:
            self.ui.cboOwner.addItem(i['name'])

    def checkEditPage(self):
        res = True
        if self.ui.txtEditFirstName.toPlainText() == "":
            res = False
        if self.ui.txtEditLastName.toPlainText() == "":
            res = False
        if self.ui.txtEditEmail.toPlainText() == "":
            res = False
        if self.ui.txtEditPhonenum.toPlainText() == "":
            res = False
        return res

    def backtoUsersPage(self, reload):
        if reload:
            self.insertDataToUserTable()
        self.ui.admingpages.setCurrentWidget(self.ui.admin_Userpage)
        self.enableLeftBar()

    def saveEdit(self):
        if self.checkEditPage():
            name = self.ui.txtEditFirstName.toPlainText()
            lastname = self.ui.txtEditLastName.toPlainText()
            phone = self.ui.txtEditPhonenum.toPlainText()
            email = self.ui.txtEditEmail.toPlainText()
            userdata = [self.username, name, lastname, phone, email]
            if updateUser(userdata):
                self.backtoUsersPage(True)
                self.showSuccesDialog("แก้ไขเรียบร้อย", 'สำเร็จ')
            else:
                self.showErrorDialog("เกิดข้อผิดพลาด", "ไม่สามารถแก้ไขได้")
        else:
            self.showWarningDialog("กรุณากรอกข้อมูลให้ครบถ้วน", "คำเตือน")

    def disableLeftBar(self):
        self.ui.btnPromoteUser.setDisabled(True)
        self.ui.btnEditUser.setDisabled(True)
        self.ui.btnDeleteUser.setDisabled(True)
        self.ui.btnResetUserPassword.setDisabled(True)

    def enableLeftBar(self):
        self.ui.btnPromoteUser.setDisabled(False)
        self.ui.btnEditUser.setDisabled(False)
        self.ui.btnDeleteUser.setDisabled(False)
        self.ui.btnResetUserPassword.setDisabled(False)

    def editUser(self):
        if self.userTableIsSelect():
            self.disableLeftBar()
            self.username = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 0).text()
            name = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 1).text()
            lastname = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 2).text()
            email = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 3).text()
            phone = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 4).text()
            self.ui.txtEditFirstName.setText(name)
            self.ui.txtEditLastName.setText(lastname)
            self.ui.txtEditEmail.setText(email)
            self.ui.txtEditPhonenum.setText(phone)
            self.ui.admingpages.setCurrentWidget(self.ui.admin_EditPage)
        else:
            self.showWarningDialog("ไม่มีผู้ใช้ที่ถูกเลือกไว้", 'Warning')

    def setNeedChange(self):
        if self.userTableIsSelect():
            if self.confirmDialog("ต้องการรีเซ็ตรหัสผ่านของผู้ใช้ใช่หรือไม่", "กรุณายืนยัน"):
                username = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 0).text()
                # print(username)
                setNeedChange(username)
                self.showSuccesDialog("ทำการเปลี่ยนสถานะเรียบร้อย", "Success")
                self.insertDataToUserTable()
        else:
            self.showWarningDialog("ไม่มีผู้ใช้ที่ถูกเลือกไว้", 'Warning')

    def checkNewpassandConfirm(self, password, recheck):
        if password == "" or recheck == "":
            self.showWarningDialog("กรุณากรอกรหัสผ่านทั้งสองช่อง", "Warning")
            return False
        elif password != recheck:
            self.showErrorDialog("กรุณากรอกรหัสผ่านทั้งสองช่องให้ตรงกัน", "Error")
            return False
        return True

    def checkLogin(self):
        username = self.ui.txtUsername.text()
        password = self.ui.txtPassword.text()
        if (checkLogin(username, password)):
            self.checkNeedChange(username)
        else:
            self.LoginErrorDialog()

    def checkNeedChange(self, username):
        if checkIfNeedChange(username):
            self.username = username
            self.ui.content.setCurrentWidget(self.ui.changePasswordPage)
        else:
            self.checkAdmin(username)

    def checkAdmin(self, username):
        if (checkAdmin(username)):
            self.showAdminPages()
        else:
            self.showBoard()
            self.addTaskOwnerCbo()
            self.taskTypeFilter()

    def LoginErrorDialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText("กรุณากรอก Username และ Password ให้ถูกต้อง")
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def RegisterWithBlankFields(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText("กรุณากรอกข้อมูลให้ครบถ้วน")
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def passwordNotTheSame(self):
        self.showWarningDialog("รหัสผ่านไม่ตรงกัน กรุณากรอกใหม่", "Warning")

    def show(self):
        self.main_win.show()

    def showRegisterPage(self):
        self.resetInsertForm()
        self.ui.content.setCurrentWidget(self.ui.registerPage)

    def userTableIsSelect(self):
        res = True
        if self.ui.tableUsers.selectedIndexes() == []:
            res = False
        return res

    def deleteUser(self):
        if self.userTableIsSelect():
            if self.confirmDialog("ต้องการลบผู้ใช้หรือไม่", "กรุณายืนยัน"):
                username = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 0).text()
                deleteUser(username)
                self.showSuccesDialog("ทำการลบผู้ใช้เรียบร้อย", "Success")
                self.insertDataToUserTable()
        else:
            self.showWarningDialog("ไม่มีผู้ใช้ที่ถูกเลือกไว้", 'Warning')

    def promoteUser(self):
        if self.userTableIsSelect():
            if self.confirmDialog("ต้องการยกระดับผู้ใช้ใช่หรือไม่", "กรุณายืนยัน"):
                username = self.ui.tableUsers.item(self.ui.tableUsers.currentRow(), 0).text()
                promoteToAdmin(username)
                self.showSuccesDialog("ทำการเปลี่ยนสถานะผู้ใช้เรียบร้อย", "Success")
                self.insertDataToUserTable()
        else:
            self.showWarningDialog("ไม่มีผู้ใช้ที่ถูกเลือกไว้", 'Warning')

    def InsertUser(self):
        username = self.ui.txtCreateUsername.text()
        password = self.ui.txtNewPassword.text()
        confirmpass = self.ui.txtConfirmPass.text()
        name = self.ui.txtName.text()
        lastname = self.ui.txtLastname.text()
        email = self.ui.txtEmail.text()
        phone = self.ui.txtPhone.text()

        if self.checkUserForm():
            if password == confirmpass:
                info = {'username': username, 'password': password, 'name': name, 'lastname': lastname, 'email': email,
                        'phone': phone,
                        'isAdmin': 0}
                if insetUser(info):
                    self.showSuccesDialog("ทำการสมัครเรียบร้อย\nสามารถใช้บัญชีนี้ล็อกอินได้ทันที", "Register Succesful")
                    self.logOut()
                else:
                    self.showErrorDialog("Username ซ้ำ กรุณากรอกใหม่", "Error")
            else:
                self.passwordNotTheSame()

        else:
            self.RegisterWithBlankFields()

    def showAdminPages(self):
        self.insertDataToUserTable()
        self.ui.content.setCurrentWidget(self.ui.adminPage)
        self.ui.admingpages.setCurrentWidget(self.ui.admin_Userpage)

    def insertDataToUserTable(self):
        self.ui.tableUsers.clear()
        self.ui.tableUsers.setRowCount(getUserCount())
        self.ui.tableUsers.setColumnCount(5)
        header = self.ui.tableUsers.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        header1 = QtWidgets.QTableWidgetItem("USERNAME")
        header2 = QtWidgets.QTableWidgetItem("FIRSTNAME")
        header3 = QtWidgets.QTableWidgetItem("LASTNAME")
        header4 = QtWidgets.QTableWidgetItem("EMAIL")
        header5 = QtWidgets.QTableWidgetItem("PHONE")
        self.ui.tableUsers.setHorizontalHeaderItem(0, header1)
        self.ui.tableUsers.setHorizontalHeaderItem(1, header2)
        self.ui.tableUsers.setHorizontalHeaderItem(2, header3)
        self.ui.tableUsers.setHorizontalHeaderItem(3, header4)
        self.ui.tableUsers.setHorizontalHeaderItem(4, header5)
        row = 0
        users = getAllGeneralUser()
        for i in users:
            self.ui.tableUsers.setItem(row, 0, QTableWidgetItem("{}".format(i['username'])))
            self.ui.tableUsers.setItem(row, 1, QTableWidgetItem("{}".format(i['name'])))
            self.ui.tableUsers.setItem(row, 2, QTableWidgetItem("{}".format(i['lastname'])))
            self.ui.tableUsers.setItem(row, 3, QTableWidgetItem("{}".format(i['email'])))
            self.ui.tableUsers.setItem(row, 4, QTableWidgetItem("{}".format(i['phone'])))
            row += 1
        self.ui.tableUsers.selectRow(0)

    def showBoard(self):
        self.ui.content.setCurrentWidget(self.ui.board)

    def showManageUser(self):
        self.ui.adminpages.setCurrentWidget(self.ui.ManageUser)

    def showCreateUser(self):
        self.ui.adminpages.setCurrentWidget(self.ui.CreateUser)

    def logOut(self):
        self.ui.content.setCurrentWidget(self.ui.Login)
        self.ui.txtUsername.setText("")
        self.ui.txtPassword.setText("")

    def resetInsertForm(self):
        self.ui.txtCreateUsername.setText("")
        self.ui.txtNewPassword.setText("")
        self.ui.txtConfirmPass.setText("")
        self.ui.txtName.setText("")
        self.ui.txtLastname.setText("")
        self.ui.txtPhone.setText("")
        self.ui.txtEmail.setText("")

    def checkUserForm(self):
        result = True
        if self.ui.txtCreateUsername.text() == "":
            result = False
        elif self.ui.txtNewPassword.text() == "":
            result = False
        elif self.ui.txtConfirmPass.text() == "":
            result = False
        elif self.ui.txtName.text() == "":
            result = False
        elif self.ui.txtLastname.text() == "":
            result = False
        elif self.ui.txtPhone.text() == "":
            result = False
        elif self.ui.txtEmail.text() == "":
            result = False
        return result

    def showSuccesDialog(self, Text, Header):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(Text)
        msg.setWindowTitle(Header)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def showErrorDialog(self, Text, Header):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(Text)
        msg.setWindowTitle(Header)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def showWarningDialog(self, Text, Header):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(Text)
        msg.setWindowTitle(Header)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def confirmDialog(self, Text, Header):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(Text)
        msg.setWindowTitle(Header)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msg.exec()
        if returnValue == QMessageBox.Ok:
            return True
        elif returnValue == QMessageBox.No:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
