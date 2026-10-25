import sys
import subprocess
import platform
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QPushButton, QMessageBox

if sys.platform != 'linux':    
    app = QApplication().setWindowIcon(QIcon("icon.png"))

    QMessageBox.critical(None, "Platform not supported", "Your platform - " + platform + " is not currently supported")
    sys.exit(1)

if(platform.freedesktop_os_release()["ID"] != 'fedora' and platform.freedesktop_os_release()["ID"] != 'arch'):
    app = QApplication().setWindowIcon(QIcon("icon.png"))
    
    QMessageBox.critical(None, "Distro not supported", "Your linux distribution - " + platform.freedesktop_os_release()["NAME"] + " is currently not supported")
    sys.exit(1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('harackit server manager')
        self.setWindowIcon(QIcon("icon.png"))

        container = QWidget()
        self.setCentralWidget(container)

        layout = QGridLayout(container)

        httpd_label = QLabel('httpd')
        is_active = subprocess.run(['systemctl', 'is-active', 'httpd'], text=True, capture_output=True).stdout.strip()
        if is_active == 'active':
            self.httpd_status_label = QLabel('running')
            self.httpd_status_label.setStyleSheet('color: green;')
        elif is_active == 'inactive':
            self.httpd_status_label = QLabel('stopped')
            self.httpd_status_label.setStyleSheet('color: red;')
        else:
            self.httpd_status_label = QLabel ('is-active returned a non-boolean value')

        httpd_button = QPushButton('start/stop')
        httpd_button.clicked.connect(self.manage_httpd)
        httpd_label.setAlignment(Qt.AlignCenter)
        self.httpd_status_label.setAlignment(Qt.AlignCenter)

        mariadb_label = QLabel('mariadb')
        is_active = subprocess.run(['systemctl', 'is-active', 'mariadb'], text=True, capture_output=True).stdout.strip()
        if is_active == 'active':
            self.mariadb_status_label = QLabel('running')
            self.mariadb_status_label.setStyleSheet('color: green;')
        elif is_active == 'inactive':
            self.mariadb_status_label = QLabel('stopped')
            self.mariadb_status_label.setStyleSheet('color: red;')
        else:
            self.mariadb_status_label = QLabel ('is-active returned a non-boolean value')

        mariadb_button = QPushButton('start/stop')
        mariadb_button.clicked.connect(self.manage_mariadb)
        mariadb_label.setAlignment(Qt.AlignCenter)
        self.mariadb_status_label.setAlignment(Qt.AlignCenter)

        sshd_label = QLabel('sshd')
        is_active = subprocess.run(['systemctl', 'is-active', 'sshd'], text=True, capture_output=True).stdout.strip()
        if is_active == 'active':
            self.sshd_status_label = QLabel('running')
            self.sshd_status_label.setStyleSheet('color: green;')
        elif is_active == 'inactive':
            self.sshd_status_label = QLabel('stopped')
            self.sshd_status_label.setStyleSheet('color: red;')
        else:
            self.sshd_status_label = QLabel ('is-active returned a non-boolean value')

        sshd_button = QPushButton('start/stop')
        sshd_button.clicked.connect(self.manage_sshd)
        sshd_label.setAlignment(Qt.AlignCenter)
        self.sshd_status_label.setAlignment(Qt.AlignCenter)

        httpd_label.setStyleSheet("font-size: 20px; font-weight: 900;")
        mariadb_label.setStyleSheet("font-size: 20px; font-weight: 900;")
        sshd_label.setStyleSheet("font-size: 20px; font-weight: 900;")

        layout.addWidget(httpd_label, 0, 0)
        layout.addWidget(self.httpd_status_label, 0, 1)
        layout.addWidget(httpd_button, 0, 2)

        layout.addWidget(mariadb_label, 1, 0)
        layout.addWidget(self.mariadb_status_label, 1, 1)
        layout.addWidget(mariadb_button, 1, 2)

        layout.addWidget(sshd_label, 2, 0)
        layout.addWidget(self.sshd_status_label, 2, 1)
        layout.addWidget(sshd_button, 2, 2)

        slopBottom = QLabel('harackit slop production 2026')
        slopBottom.setStyleSheet('font-size:7px; font-style: oblique 25deg;')
        slopRight = QLabel('.')
        slopRight.setStyleSheet('font-size:7px; font-style: oblique 25deg;')
        layout.addWidget(slopBottom, 3, 1)
        layout.addWidget(slopRight, 1, 3)

    def manage_httpd(self):
        is_active = subprocess.run(['systemctl', 'is-active', 'httpd'], text=True, capture_output=True).stdout.strip()
        if is_active == 'inactive':
            try:
                subprocess.run(['systemctl', 'start', 'httpd'], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                self.httpd_status_label.setText(e.stderr.decode('utf-8'))
            else:
                self.httpd_status_label.setText('running')
                self.httpd_status_label.setStyleSheet('color: green;')
        elif is_active == 'active':
            try:
                subprocess.run(['systemctl', 'stop', 'httpd'], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                self.httpd_status_label.setText(e.stderr.decode('utf-8'))
            else:
                self.httpd_status_label.setText('stopped')
                self.httpd_status_label.setStyleSheet('color: red;')
        else:
            self.httpd_status_label.setText('is-active returned a non boolean value')
        
    def manage_mariadb(self):
        is_active = subprocess.run(['systemctl', 'is-active', 'mariadb'], text=True, capture_output=True).stdout.strip()
        if is_active == 'inactive':
            try:
                subprocess.run(['systemctl', 'start', 'mariadb'])
            except subprocess.CalledProcessError as e:
                self.mariadb_status_label.setText(e.stderr.decode('utf-8'))
            else:
                self.mariadb_status_label.setText('running')
                self.mariadb_status_label.setStyleSheet('color: green;')
        elif is_active == 'active':
            try:
                subprocess.run(['systemctl', 'stop', 'mariadb'])
            except subprocess.CalledProcessError as e:
                self.mariadb_status_label.setText(e.stderr.decode('utf-8'))
            else:
                self.mariadb_status_label.setText('stopped')
                self.mariadb_status_label.setStyleSheet('color: red;')
        else:
            self.mariadb_status_label.setText('is-active returned a non-boolean value')

    def manage_sshd(self):
        is_active = subprocess.run(['systemctl', 'is-active', 'sshd'], text=True, capture_output=True).stdout.strip()
        if is_active == 'inactive':
            try:
                subprocess.run(['systemctl', 'start', 'sshd'])
            except subprocess.CalledProcessError as e:
                self.mariadb_status_label.setText(e.stderr.decode('utf-8'))
            else:
                self.sshd_status_label.setText('running')
                self.sshd_status_label.setStyleSheet('color: green;')
        elif is_active == 'active':
            try:
                subprocess.run(['systemctl', 'stop', 'sshd'])
            except subprocess.CalledProcessError as e:
                self.mariadb_status_label.setText(e.stderr.decode('utf-8'))
            else:
                self.sshd_status_label.setText('stopped')
                self.sshd_status_label.setStyleSheet('color: red;')
        else:
            self.sshd_status_label.setText('is-active returned a non boolean value')

app = QApplication()

window = MainWindow()
window.show()

app.exec()
