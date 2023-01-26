# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 16:03:13 2022

@author: mrkure
"""
import os, sys, time
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'lib')))
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QAction, QMenu, QApplication
import _main_exe as me

class TrayAppTradeWhisper(QSystemTrayIcon, QWidget):
    def __init__(self):
        super(QSystemTrayIcon, self).__init__()
        super(QWidget, self).__init__()
        
#%% TRAY SETTINGS
        self.dir            = os.path.dirname(os.path.realpath(__file__))   
        self.icon_running   = QIcon('{}\{}'.format(self.dir, r'resources\running.png'))          
        self.icon_stopped   = QIcon('{}\{}'.format(self.dir, r'resources\stopped.png'))   

        self.menu           = QMenu() 
        self.setContextMenu(self.menu)
        self.setIcon(self.icon_running)
        self.option_close = QAction("Close")
        self.menu.addAction(self.option_close)
        self.running = True       
        self.setVisible(True)  
        
#%% TRAY SIGNALS
        self.option_close.triggered.connect(self.on_close)   
        self.activated.connect(self.on_icon_click_right)
  
#%% MAIN WINDOW   
        self.create_main_window()
        
    def create_main_window(self):      
        self.main = me.MainWindow()
        self.main.showMaximized()    

#%% CALLBACKS      
    def on_main_window_closed(self, par):
        self.setIcon(self.icon_stopped) 
        self.running = False

        
    def on_icon_click_right(self, button):
        if str(button) == '3':           
            if self.running:
                self.setIcon(self.icon_stopped) 
                self.running = False
                self.main.closes()

            elif not self.running:
                self.setIcon(self.icon_running) 
                self.running = True   
                self.main = me.MainWindow()
                self.main.showMaximized()      
                
    def on_close(self): 
        self.main.closes()
        self.hide()
        self.close()       

#%% MAIN  
if __name__ == "__main__":
    app = QApplication([])
    tray_app_trade_whisper = TrayAppTradeWhisper()
    app.exec()  
    # sys.exit(app.exec_())