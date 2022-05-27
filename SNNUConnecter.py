
import os
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox, QSystemTrayIcon, QMenu
from certifi import contents
import requests
from MainWindow import Ui_MainWindow
from connect import connect_plan, plan_stop
import threading
import logging

logging.basicConfig(filename='./log/connect.log', format='%(asctime)s: %(message)s', level=logging.INFO)

class SNNUConnect(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(SNNUConnect, self).__init__()
        self.setupUi(self)  
        self.init()


    def init(self):
        self.dir_init()

        self.timer = QTimer()
        self.timer.timeout.connect(self.log_print)
        self.pushButton.clicked.connect(self.run) #开始自动连接
        self.pushButton_2.clicked.connect(self.stop) #停止
        self.pushButton_3.clicked.connect(self.hide) #隐藏窗口
        
        # 设置托盘
        self.trayIcon = QSystemTrayIcon(self)  
        self.trayIcon.setToolTip('SNNU Connect')  
        self.icon = QtGui.QIcon("./resource/tray.ico")  
        self.trayIcon.setIcon(self.icon)  
        self.trayIcon.activated.connect(self.trayClick)  
        self.createMenu()  
        self.trayIcon.show()  
        
        # 读取帐密
        if os.path.exists('./config/user.config'):
            with open('./config/user.config', 'r') as user:
                user_text= user.read().split()
                self.lineEdit.setText(user_text[1])
                self.lineEdit_2.setText(user_text[3])
        self.logfile = open('./log/connect.log','w+')


    def dir_init(self):
        if not os.path.exists('./config'):
            os.mkdir('./config')
        if not os.path.exists('./resource'):
            os.mkdir('./resource')
        if not os.path.exists('./log'):
            os.mkdir('./log')
        #FIXME 当没有托盘图标文件时，窗口仍可以被隐藏，但不能通过点击托盘图标重新显示
        if not os.path.exists('./resource/tray.ico'): 
            logging.error("./resource/tray.ico not found.")


    def get_ico(self):
        #FIXME 在线获取托盘图标
        data = {
            'e': '1653648000',
            'token': 'P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:uPscH9Ej4TuWvdf75utYAcsgQ24=',
        }  

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Content-Type': 'image/x-icon',

        }
    
        try:
            response = requests.get(
                'https://s1.aigei.com/src/img/ico/b1/b185c87ef6f349f4b5773c8d80d4e8b7\
                    .ico?download/%E6%89%8B%E7%BB%98%E7%BD%91%E7%BB%9C%E5%B7%A5%E5%85%\
                        B7%E5%9B%BE%E6%A0%87h8-ico_%E7%88%B1%E7%BB%99%E7%BD%91_aigei_co\
                            m.ico&e=1653648000&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJ\
                                axypL:uPscH9Ej4TuWvdf75utYAcsgQ24=', data=data, headers=headers)
        except Exception as e:
            pass
        finally:
            return response



    def createMenu(self):
        self.menu = QMenu()  
        self.quitAction = QtWidgets.QAction("退出", self, triggered=self.close)
        
        self.menu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.menu)  
        
    def hide(self):
        self.setVisible(False)

    def trayClick(self, reason):
        # 点击托盘图标显示窗口
        if reason == 2 or reason == 3:
            if self.isMinimized() or not self.isVisible():
                self.showNormal()
            else:
                self.setVisible(False)


    def run(self):
        #从UI获取帐密
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        #将帐密保存到文件
        if os.path.exists('./config/user.config'):
            with open('./config/user.config', 'r') as user:
                content = user.read()
        else:
            content = ''
        with open('./config/user.config', 'w+') as f:
            if not content.split()[1] == username:
                f.writelines('username %s\npassword %s\n'%(username, password))
            f.writelines(content)

        if not (username and password):
            QMessageBox.warning(self, "error", "username or password is empty.")
            return
        
        t = threading.Thread(target=connect_plan, args=(username, password))
        self.timer.start(1000)
        self.log_print()
        try:
            t.start()
        except Exception as e:
            logging.info("start error.")
        
        

    def stop(self):
        # 停止自动连接
        plan_stop()

    
    def log_print(self):
        # 从文件输出log到UI
        text = self.logfile.readline()
        if text:
            self.textBrowser.append(text) 
            self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
        
        

    

if __name__ == '__main__':
    

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 自适应分辨率

    app = QtWidgets.QApplication(sys.argv)
    ui = SNNUConnect()
    ui.show()
    sys.exit(app.exec_())

