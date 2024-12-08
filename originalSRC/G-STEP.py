import keyboard
from ctypes import *
import time
import threading
import winsound as sd
import requests
import os
import datetime
from datetime import timedelta
import sys
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
dd_dll = windll.LoadLibrary('.\\SuddenAttack.dll')
st = dd_dll.DD_btn(0)

def beepsound():
    fr = 2000
    du = 300
    sd.Beep(fr, du)

def 고텝(result):
    try:
        with open('.\\setting.json', 'r') as f:
            json_data = json.load(f)
        ON_OFF_KEY = json_data['G-STEP']['ON_OFF_KEY']
        OFF_KEY_1 = json_data['G-STEP']['OFF_KEY_1']
        OFF_KEY_2 = json_data['G-STEP']['OFF_KEY_2']
        END_KEY = json_data['G-STEP']['END_KEY']
    except:
        pass
    if st == 1:
        print('OK')
    else:
        print('Error')
        exit(101)
    while True:
        try:
            if keyboard.is_pressed(END_KEY):
                beepsound()
                print('종료')
                return
            if keyboard.is_pressed(ON_OFF_KEY):
                print('고텝 켜짐')
                time.sleep(0.1)
                while True:
                    try:
                        if keyboard.is_pressed(ON_OFF_KEY) or keyboard.is_pressed(OFF_KEY_1) or keyboard.is_pressed(OFF_KEY_2):
                            print('고텝 꺼짐')
                            time.sleep(1)
                            dd_dll.DD_key(401, 2)
                            dd_dll.DD_key(403, 2)
                            continue
                        if is_expired(result):
                            beepsound()
                            print('라이센스 만료됨')
                            continue
                        dd_dll.DD_key(401, 1)
                        time.sleep(0.01)
                        dd_dll.DD_key(401, 2)
                        time.sleep(0.1)
                        dd_dll.DD_key(403, 1)
                        time.sleep(0.01)
                        dd_dll.DD_key(403, 2)
                        time.sleep(0.01)
                    except:
                        pass
            else:
                if is_expired(result):
                    beepsound()
                    print('라이센스 만료됨')
                    return
                pass
        except:
            print('Error')
            dd_dll.DD_key(401, 2)
            dd_dll.DD_key(403, 2)
            break

def is_expired(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if (ExpireTime - ServerTime).total_seconds() > 0:
        return False
    return True

def 로그인():
    import psutil
    try:
        for process in psutil.process_iter():
            if 'HTTPDebuggerUI.exe' in process.name():
                sys.exit(0)
    except:
        pass
    code = input('License : ')
    try:
        for process in psutil.process_iter():
            if 'HTTPDebuggerUI.exe' in process.name():
                sys.exit(0)
    except:
        pass
    try:
        result = requests.get(f'http://discord-link.xyz:309/api/?code={code}')
        result = result.text
    except:
        beepsound()
        print('서버와의 연결이 끊겼습니다.\n잠시후 다시 시도해주세요.')
        s = input()
        sys.exit(0)
    if is_expired(result):
        beepsound()
        print('만료되거나 존재하지 않는 라이센스 입니다.')
        s = input()
        sys.exit(0)
    else:
        try:
            for process in psutil.process_iter():
                if 'HTTPDebuggerUI.exe' in process.name():
                    sys.exit(0)
        except:
            pass
        beepsound()
        print(f'로그인 성공\n사용 가능 기간 : {result}')
        try:
            t1 = threading.Thread(target=고텝(result), args=())
            t1.start()
        except:
            return None
    
    t1 = threading.Thread(target=고텝(result), args=())
    t1.start()
로그인()