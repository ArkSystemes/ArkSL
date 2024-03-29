#!/usr/bin/python3 

from i3 import disable_scr, enable_scr, ws_backup, ws_restore

import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QHBoxLayout, QLineEdit, QDesktopWidget
from PyQt5.QtGui import QMovie, QGuiApplication

from PyQt5.QtWebEngineWidgets import *

from functools import partial

import os
import pam 
import argparse
import glob
import random
import re 
import time

## background = sys.argv[1]



# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self, args):
        self.args = args
        super().__init__()


        self.setWindowTitle("ArkScreenLocker v1")
        self.setCursor(Qt.BlankCursor)
        self.setStyleSheet("background-color: black;")


        screen_resolution = QDesktopWidget().screenGeometry()
        self.main_width, self.main_height = screen_resolution.width(), screen_resolution.height()

        widget = QWidget()
        self.setCentralWidget(widget)
        self.setFixedSize(self.main_width, self.main_height+30)
        #self.setFixedSize(1366,768)
        #self.setFixedSize(500, 500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)

        self.background_to_display = ""

        self.background_type = self.args.t

        if self.background_type == 'gif':
            if self.args.r == True:
                self.background = random_gif()
            if self.args.g:
                self.background = self.args.g

            #animation = QMovie("circle.gif")
            animation = QMovie(self.background)
            self.anim = QLabel()
            self.anim.setAlignment(QtCore.Qt.AlignCenter)
            self.anim.setMovie(animation)
            animation.start()
            self.background_to_display = self.anim



        if self.background_type == 'web':
            ## URL DEFAULT
            if self.args.u:
                url = self.args.u
            else:
                url = 'https://earth.nullschool.net/#current/bio/surface/level/annot=fires/overlay=bleaching_alert_area/orthographic=-311.32,-10.23,305'
            web = QWebEngineView()
            web.load(QUrl(url))
            web.show()
            self.background_to_display = web


        layout_box = QHBoxLayout(widget)
        layout_box.setContentsMargins(0, 0, 0, 0)
        ##layout_box.addWidget(self.anim)
        #layout_box.addWidget(web)
        layout_box.addWidget(self.background_to_display)

        pwdbox = QLineEdit(self)
        pwdbox.setEchoMode(QLineEdit.Password)
        pwdbox.returnPressed.connect(partial(self.returnPressed, pwdbox))
        if self.args.g and re.search('as[0-9]{0,5}\.gif', self.args.g):
        #if self.args.g == '/tmp/as.gif':
            x = (self.main_width - 200) // 2
            y = self.main_height - 100 - 100
            pwdbox.move(x, y)
            #pwdbox.move(590, 700)
        else:
            pwdbox.move(590, 350)
            #pwdbox.move(50, 50)
        pwdbox.resize(200,20)
        pwdbox.setStyleSheet("QLineEdit"
                                "{"
                                "background : #171819; color: #FFFFFF;"
                                "}")
        self.pwdbox = QLabel(widget)


    def returnPressed(self, pwdbox):
        #print(pwdbox.text())
        user = os.getlogin()
        p = pam.authenticate(user, pwdbox.text())
        if p:
            print('login')
            # Re-enable the Alt key at login
            os.system("xmodmap -e 'keycode 64=Alt_L'")
            os.system("xmodmap -e 'keycode 68=F2'")
            os.system("dunstctl set-paused false")
            enable_scr()
            time.sleep(2)
            ws_restore(ws_keep) 

            sys.exit(0)
        else:
            print('pas login')



def random_gif():
    gifs_path = '/home/nao/.config/arksl/*'
    gifs = glob.glob(gifs_path)
    random.shuffle(gifs)
    return gifs[0]

if __name__ == '__main__':

    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = "--no-sandbox"

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', help='Random gif, each run gif change.', action="store_true")
    parser.add_argument('-g', help='Gif to display.', type=str)
    parser.add_argument('-t', help='Background type, gif or web.', type=str, choices=['gif','web'])
    parser.add_argument('-u', help='Url to display.', type=str)
    args = parser.parse_args()

    # Disable Alt key at startup to prevent Alt+ combination
    os.system("xmodmap -e 'keycode 64=NoSymbol'") #Alt
    os.system("xmodmap -e 'keycode 68=NoSymbol'") #F2
    # Disable dunst notification 
    os.system("dunstctl set-paused true")

    # Keep i3 ws placement
    ws_keep = ws_backup()
    ## disable screen 1 2, keep 0
    disable_scr()

    app = QApplication(sys.argv)

    window = MainWindow(args)
    window.show()

    app.exec()
