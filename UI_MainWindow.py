# Form implementation generated from reading ui file 'UI_MainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(700, 400)
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Form.setSizeIncrement(QtCore.QSize(13767, 13767))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/Icon1.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Form.setWindowIcon(icon)
        Form.setAutoFillBackground(False)
        self.bgLabel = QtWidgets.QLabel(parent=Form)
        self.bgLabel.setGeometry(QtCore.QRect(0, 0, 700, 400))
        self.bgLabel.setAutoFillBackground(True)
        self.bgLabel.setText("")
        self.bgLabel.setScaledContents(True)
        self.bgLabel.setObjectName("bgLabel")
        self.operationText = QtWidgets.QPlainTextEdit(parent=Form)
        self.operationText.setEnabled(True)
        self.operationText.setGeometry(QtCore.QRect(205, 40, 300, 200))
        self.operationText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.operationText.setReadOnly(True)
        self.operationText.setObjectName("operationText")
        self.setting_toolButton = QtWidgets.QToolButton(parent=Form)
        self.setting_toolButton.setGeometry(QtCore.QRect(675, 30, 30, 30))
        self.setting_toolButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/tools_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon1.addPixmap(QtGui.QPixmap("resources/tools_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.setting_toolButton.setIcon(icon1)
        self.setting_toolButton.setIconSize(QtCore.QSize(16, 16))
        self.setting_toolButton.setAutoRaise(True)
        self.setting_toolButton.setObjectName("setting_toolButton")
        self.start_button = QtWidgets.QToolButton(parent=Form)
        self.start_button.setGeometry(QtCore.QRect(-3, 40, 30, 30))
        self.start_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resources/startbutton.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.start_button.setIcon(icon2)
        self.start_button.setIconSize(QtCore.QSize(16, 16))
        self.start_button.setAutoRaise(True)
        self.start_button.setObjectName("start_button")
        self.stop_button = QtWidgets.QToolButton(parent=Form)
        self.stop_button.setEnabled(False)
        self.stop_button.setGeometry(QtCore.QRect(-3, 80, 30, 30))
        self.stop_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("resources/stopbutton.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.stop_button.setIcon(icon3)
        self.stop_button.setIconSize(QtCore.QSize(16, 16))
        self.stop_button.setAutoRaise(True)
        self.stop_button.setObjectName("stop_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "钓鱼"))
        self.bgLabel.setAccessibleDescription(_translate("Form", "11111"))
        self.operationText.setPlainText(_translate("Form", "----------------------------------------------------------\n"
"\n"
"      请前往钓鱼水域\n"
"\n"
"       进入钓鱼模式并显示抛竿UI后点击开始按钮\n"
"\n"
"----------------------------------------------------------"))
