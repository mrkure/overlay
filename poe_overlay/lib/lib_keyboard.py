# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 11:34:49 2022

@author: mrkure
"""
import threading
import keyboard, mouse, time, random
from params import params
class MyKeyboard:
    def __init__(self):
        
        self.dic   = {}
        self.hooks = []
        self.hooked = False
#%% TEMPLATE CODE
    def function_repeated(self, func_name):
        while True:
            # CODE HERE
            time.sleep(1)
            keyboard.send('a')
            # END OF CODE HERE
            if self.dic[func_name+'stop']:
                self.dic[func_name+'running'], self.dic[func_name+'stop'] = False, False; return                    
            
    def function_once_long(self, func_name):
            # CODE HERE
            keyboard.send('a')
            # END OF CODE HERE
            self.dic[func_name+'running'] = False
            self.dic[func_name+'stop']    = False                  

    def function_once_fast(self, func_name):
            # CODE HERE
            keyboard.send('a')
            # END OF CODE HERE
            
#%% FUNCTIONS
    def use_portal_scroll(self):
        print('using portal scroll')
        small_delay = 0.1            
        time.sleep(small_delay)
        keyboard.send('i')
        time.sleep(small_delay)
        mouse.move(1872, 891)
        time.sleep(small_delay)
        mouse.right_click()
        time.sleep(small_delay)
        keyboard.send('i')
        time.sleep(small_delay)
        mouse.move(961, 440)
        time.sleep(small_delay)
        mouse.click()  
        return
   
    # move items
    def fast_click_left_with_ctrl_down(self, func_name):
        sleep  = 0.03
        keyboard.press('ctrl')
        time.sleep(sleep)
        i = 0
        while True:
            i += 1
            print(f'sending ctrl+click {i}')
            mouse.click()   
            # mouse.press()
            # time.sleep(0.05)
            # mouse.release()
            time.sleep(sleep)  
            if self.dic[func_name+'stop']:
                keyboard.release('ctrl')
                self.dic[func_name+'running'], self.dic[func_name+'stop'] = False, False; return          
        return 
    
    # identify items etc...
    def fast_click_left_with_shift_down(self, func_name):
        sleep  = 0.03
        keyboard.press('shift')
        time.sleep(sleep)
        while True:
            mouse.click()
            time.sleep(sleep)  
            if self.dic[func_name+'stop']:
                keyboard.release('shift')
                self.dic[func_name+'running'], self.dic[func_name+'stop'] = False, False; return            
        return 
    
    # use skill repeatidly - for example molten shell
    def use_skill_repeatidly(self, func_name):
        time_to_sleep = 8
        x = 0
        while True:
            x += 1
            print("Mouse middle click ", x)
            mouse.click(button = 'middle')            
            for i in range(time_to_sleep):
                time.sleep(1)
                if self.dic[func_name+'stop']:
                    self.dic[func_name+'running'], self.dic[func_name+'stop'] = False, False; return  
                time.sleep(random.randint(1,500)/500)
        return

    # use flasks in given loop
    flasks_pointer  = 0 
    flasks          = [ [1], [2] , [3], [4] , [5], ]
    def flask_use_rotation(self):   
        
        for key_to_send in MyKeyboard.flasks[MyKeyboard.flasks_pointer]:
            keyboard.send(str(key_to_send))
            time.sleep(0.1)
        MyKeyboard.flasks_pointer += 1
        if MyKeyboard.flasks_pointer == len(MyKeyboard.flasks):
            MyKeyboard.flasks_pointer = 0
        return    
    
#%% FUNCTION LOADER         
    def function_loader(self, foo_to_run):
        func_name = foo_to_run.__name__
        if not func_name in self.dic:
            self.dic[func_name]           = False  
            self.dic[func_name+'running'] = False
            self.dic[func_name+'stop']    = False       

        if self.dic[func_name+'running'] == False:
            self.dic[func_name+'running'] = True            
            t = threading.Thread(target = foo_to_run, args=(func_name,))
            t.start()
        else:
            self.dic[func_name+'stop'] = True  
        return
#%% HOOK UNHOOK
    def hook_all(self):
        print("hooked")
        if not self.hooked:
            # fast
            keyboard.remap_key('caps lock', params['caps lock'])
            self.hooks.append(keyboard.add_hotkey(params['use_portal_scroll'], self.use_portal_scroll, args=()))
            # self.hooks.append(keyboard.add_hotkey('space', self.flask_use_rotation, args=()))
           
            # repeated
            self.hooks.append(keyboard.add_hotkey(params['fast_click_left_with_ctrl_down'], self.function_loader, args=(self.fast_click_left_with_ctrl_down,)))   
            self.hooks.append(keyboard.add_hotkey(params['fast_click_left_with_shift_down'], self.function_loader, args=(self.fast_click_left_with_shift_down,))) 
            # self.hooks.append(keyboard.add_hotkey('f6', self.function_loader, args=(self.use_skill_repeatidly,))) 
        self.hooked = True
       
    def unhook_all(self):
        print("unhooked")
        if self.hooked:
            self.dic = {}
            for key, value in self.dic.items():
                if 'stop' in key:
                    self.dic[key] = True
            for hook in self.hooks:
                keyboard.remove_hotkey(hook)
            keyboard.unhook('caps lock')
            self.hooks = []
        self.hooked = False

#%% TEST      
if __name__ =="__main__": 
    clicker = MyKeyboard()        
    clicker.hook_all()
    time.sleep(25)
    clicker.unhook_all()
