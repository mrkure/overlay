import sys, os, math; sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), 'lib')))

from params import params
import lib_mouse as lmou
import lib_keyboard as lkey
import lib_bg_thread as bgt
import lib_recorder as lrec
from PyQt5 import uic, QtWidgets as qtw, QtCore as qtc, QtGui as qtg
from PyQt5.QtWidgets import QWidget, QShortcut, QApplication, QMessageBox, QPushButton

import numpy as np, ctypes as c, multiprocessing as mp
from multiprocessing import Process

import win32gui, win32com.client, win32con
import keyboard, mouse, pyperclip, time
"""
===============================================================================
UI
===============================================================================
"""
Main_window, Main_window_baseclass    = uic.loadUiType('U:/_python/project/poe_overlay/ui/main_window.ui')
Form_window, Buttons_window_baseclass = uic.loadUiType('U:/_python/project/poe_overlay/ui/buttons_window.ui')
icon_path = 'U:/_python/project/poe_overlay/resources/icons8-photo-gallery-64.png'
"""
===============================================================================
SECOND WINDOW
===============================================================================
"""
class ButtonsWindow(Buttons_window_baseclass):
    # custom signal definition, static variable shared by all instances of the class
    submitted = qtc.pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.ui = Form_window()
        self.ui.setupUi(self) 
        self.setWindowFlags ( qtc.Qt.WindowStaysOnTopHint ) 
        self.setWindowFlags ( qtc.Qt.FramelessWindowHint  | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.Tool ) 
        self.hooked = False
        # print(self.ui.pushButton_unhooked.palette().button().color().name())
        for widget in self.children():
            if isinstance(widget, QPushButton):
                widget.clicked.connect(self.on_button_clicked)
                widget.setStyleSheet(params['button_inactive'])
   
    def on_button_clicked(self):             
        self.submitted.emit(self.sender().text())

"""           
# =============================================================================
# MAIN WINDOW
# =============================================================================
"""
#%% TEMPLATE CODE, DO NOT CHANGE 
class MainWindow(Main_window_baseclass):     

#%% TEMPLATE CODE, DO NOT CHANGE      
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.ui = Main_window()
        self.ui.setupUi(self)  
        
        self.setWindowFlags (  qtc.Qt.Tool ) 
        
#%% USER CODE FOR WINDOW MANIPULATION - self == window -> methods for window manipulation        
        x, y, w, h,  = params['window_geo']
        self.move(x,y)
        self.resize(w,h)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags (  qtc.Qt.FramelessWindowHint  | qtc.Qt.WindowStaysOnTopHint | qtc.Qt.WindowTransparentForInput | qtc.Qt.Tool) 
        self.setWindowIcon(qtg.QIcon(icon_path))
        self.setWindowTitle("POE Overlay") 
        
        # MULTIPROCESSING, SHARED MEMORY
        self.mp_capture = mp.Array(c.c_ubyte, h * w * 4) 
        self.capture    = np.frombuffer(self.mp_capture.get_obj(),dtype=np.uint8).reshape((h , w , 4))
        self.mp_states  = mp.Array(c.c_uint, 10)   
        self.states     = np.frombuffer(self.mp_states.get_obj(),dtype=np.uint)               
        p = Process(target=bgt.capture_screen, args=(self.mp_capture, self.mp_states, [x, y, w, h]), daemon=True)
        p.start() 
        
        # DRIVER VARIABLES
        self.states[0]        = 1
        self.health_time_last = 0
        self.flask_pointer    = 2
        self.a                = True  
        self.healing_timeout  = 0
        self.increment        = 0
        self.stopwatch_running = False
        self.game_active, self.game_active_last = False, False
        # RECORDERS
        self.recorder    = lrec.Recorder()
        self.mymouse     = lmou.MyMouse()
        self.my_keyboard = lkey.MyKeyboard()
        self.healing_hooked = False
#%% USER CODE FOR ELEMENTS MANIPULATION - self.ui == elements in window -> elements manipulation 
       
        # GEOMETRY, STYLESHEETS
        self.ui.label.setStyleSheet        ( params['health_bar_css'])
        self.ui.label.setGeometry(qtc.QRect(*params['health_bar_geo']))
        self.ui.label2.setStyleSheet        ( params['stopwatch_css'])
        self.ui.label2.setGeometry(qtc.QRect(*params['stopwatch_geo']))      
        self.ui.label2.hide()
        self.ui.frame.setStyleSheet        ( params['frame_css'])
        self.ui.label.hide()       
        # TIMERS
        self.ui.timer_10_msec=qtc.QTimer()
        self.ui.timer_10_msec.timeout.connect(self.on_10_ms_timer)
        self.ui.timer_10_msec.start(10)
        
        self.ui.timer_100_msec=qtc.QTimer()
        self.ui.timer_100_msec.timeout.connect(self.on_100_ms_timer)
        self.ui.timer_100_msec.start(100)
            
        self.ui.timer_1000_msec=qtc.QTimer()
        self.ui.timer_1000_msec.timeout.connect(self.on_1000_ms_timer)
        self.ui.timer_1000_msec.start(1000)
        
        # SET FOREGROUND WINDOW
        self.hwndMain = win32gui.FindWindow(None, "Path of Exile")  

        # try:
        #     hwndMain = win32gui.FindWindow(None, "D:\\Anaconda\\python.exe") 
        #     win32gui.SetWindowPos(hwndMain,win32con.HWND_TOP,-800,100,700,400,0)
        #     win32gui.SetForegroundWindow(hwndMain)
        # except:pass        
 

#%% TEMPLATE CODE, DO NOT CHANGE          
        # self.showMaximized()        
        self.buttons_window = ButtonsWindow()
        # connecting slot to signal
        self.buttons_window.submitted.connect(self.update_on_form_submited)
        self.buttons_window.move(600,1100)
        self.buttons_window.show()    
    def closes(self):
        self.buttons_window.close()
        self.close()
# #%% USER CODE FOR EVENTS, METHODS   
    def on_1000_ms_timer(self): 
        self.game_active_last = self.game_active
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == 'Path of Exile':
            self.game_active = True
        else:
            self.game_active = False
        if not self.game_active and self.game_active_last:
            self.buttons_window.ui.pushButton_hooked.setStyleSheet(params['button_inactive']) 
            self.buttons_window.ui.pushButton_unhooked.setStyleSheet(params['button_active']) 
            self.recorder.unhook_all() 
            self.mymouse.unhook_all()      
            self.my_keyboard.unhook_all() 
            
        if self.game_active and not self.game_active_last:           
            self.buttons_window.ui.pushButton_hooked.setStyleSheet(params['button_active']) 
            self.buttons_window.ui.pushButton_unhooked.setStyleSheet(params['button_inactive']) 
            self.recorder.hook_all()  
            self.mymouse.hook_all()      
            self.my_keyboard.hook_all() 
          
        if self.stopwatch_running:
            self.update_stopwatch()
        
    def on_100_ms_timer(self): 
        self.healing_timeout += 1
        
    def on_10_ms_timer(self):
                                   
        healh_value       = self.states[5]        
        self.ui.label.setText(str(healh_value))
        
        if healh_value < 85 and healh_value > 13 and self.game_active: 
            if self.healing_timeout > 4: # 500 ms
                print(f'healing after {self.healing_timeout*0.1} s')
                keyboard.press('1')
                time.sleep(0.05)            
                keyboard.release('1')
                keyboard.press('2')
                time.sleep(0.05)            
                keyboard.release('2') 
          
                self.healing_timeout = 0
                print(f'healing after {self.healing_timeout*0.1} s')
                keyboard.press('1')
                time.sleep(0.05)            
                keyboard.release('1')
                next_val = '2' if not self.increment else '3'
                keyboard.press(next_val)
                time.sleep(0.05)            
                keyboard.release(next_val) 
                self.increment       = not self.increment            
                self.healing_timeout = 0
                  
    # signal slot function definition
    @ qtc.pyqtSlot(str) # optional for type safety
    def update_on_form_submited(self, string):
        try:
            keyboard.press('alt')
            if self.hwndMain == 0:
                self.hwndMain = win32gui.FindWindow(None, "Path of Exile") 
            win32gui.SetForegroundWindow(self.hwndMain)
            keyboard.release('alt')
        except:
            keyboard.release('alt')
        
        if  string == 'Hooked':
            self.buttons_window.ui.pushButton_hooked.setStyleSheet(params['button_active']) 
            self.buttons_window.ui.pushButton_unhooked.setStyleSheet(params['button_inactive']) 
            self.recorder.hook_all()  
            self.mymouse.hook_all()      
            self.my_keyboard.hook_all() 
 
        elif string == 'Unhooked':
            self.buttons_window.ui.pushButton_hooked.setStyleSheet(params['button_inactive']) 
            self.buttons_window.ui.pushButton_unhooked.setStyleSheet(params['button_active']) 
            self.recorder.unhook_all() 
            self.mymouse.unhook_all()      
            self.my_keyboard.unhook_all() 
            
        elif string == 'Links':
            pass
        elif string == 'Colours':
            pass
        elif string == 'Craft':
            pass
        elif string == 'Stop scan':
            pass
        elif string == 'Start Record':
            self.buttons_window.ui.pushButton_start_record.setStyleSheet(params['button_active']) 
            self.recorder.start_recording()
            print('rec started')
        elif string == 'Stop Record':
            self.buttons_window.ui.pushButton_start_record.setStyleSheet(params['button_inactive']) 
            self.recorder.stop_recording()  
            print('rec stopped')
        elif string == 'Play Record':
            self.buttons_window.ui.pushButton_play_record.setStyleSheet(params['button_active']) 
            # time.sleep(2)
            self.recorder.play_recording() 
            # self.buttons_window.ui.pushButton_play_record.setStyleSheet(params['button_inactive']) 
            # print('rec played')  
      
        elif string == 'Stopwatch':       
            if not self.stopwatch_running:
                self.buttons_window.ui.pushButton_stopwatch.setStyleSheet(params['button_active']) 
                self.minute, self.second, self.hour = 0,0,0
                self.ui.label2.show()
                self.stopwatch_running = True
            else:
                self.buttons_window.ui.pushButton_stopwatch.setStyleSheet(params['button_inactive']) 
                self.stopwatch_running = False
                self.ui.label2.setText('')
                self.ui.label2.hide()
                
        elif string == 'Close':
            self.close() 
        else:pass
        print(string)

    def update_stopwatch(self):
        if self.second < 59:
            self.second += 1
        else:
            if self.minute < 59:
                self.second = 0
                self.minute += 1
            elif self.minute == 59 and self.hour < 24:
                self.hour += 1
                self.minute = 0
                self.second = 0 
            else:pass
        time = "{:02d}:{:02d}:{:02d}".format(self.hour,self.minute,self.second)
        self.ui.label2.setText(time)
        return 
"""           
# =============================================================================
# MAIN LOOP
# =============================================================================
"""        
#%% TEMPLATE CODE, DO NOT CHANGE  - MAIN LOOP       
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())