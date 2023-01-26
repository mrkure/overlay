# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 09:54:40 2022

@author: 42073
"""
import mouse, keyboard, time, threading, random

class MyMouse:
    def __init__(self):
        self.stop_repeated_middle_click = False        
        self.flasks_pointer = 0 
        self.last_time_wheel_forward  = 0
        self.last_time_wheel_backward = 0
        self.dic   = {}    
#%% FUNCTIONS            
    flasks = [ [4,5] ]
    flasks = [  [4],[5] ]
    def flask_use_rotation(self):    
        for key_to_send in self.flasks[self.flasks_pointer]:
            keyboard.send(str(key_to_send))
            time.sleep(0.1)
        self.flasks_pointer += 1
        if self.flasks_pointer == len(self.flasks):
            self.flasks_pointer = 0
        return 

    wheel_forward_timeout  = 2
    def mouse_wheel_forward(self):
        self.flask_use_rotation()
        return
    
    wheel_backward_timeout = 2
    def mouse_wheel_backward(self):
        keyboard.send('y')
        time.sleep(0.1)
        return
    
    mouse_on_middle_click_running = False
    # use skill repeatidly - for example molten shell
    def use_skill_repeatidly_on_middle_click(self, func_name):
        time_to_sleep = 8
        x = 0
        while True:
            x += 1
            print("Mouse middle click ", x)
            if self.stop_repeated_middle_click == False:
                mouse.click(button = 'middle') 
                keyboard.send('u')
            time.sleep(0.1)
            self.dic[func_name+'stop'] = False 
            for i in range(time_to_sleep):
                time.sleep(1)
                if self.dic[func_name+'stop']:
                    self.skill_running = False
                    print('returning from mouse middle click')
                    self.dic[func_name+'running'], self.dic[func_name+'stop'] = False, False; return  
                time.sleep(random.randint(1,500)/500)
        return    
#%% FUNCTION LOADER  
    def on_mouse_wheel(self, wheel):                
        if hasattr(wheel, 'delta'): 
            # on wheel forward
            if wheel.delta == 1.0:             
                delay_time = wheel.time - self.last_time_wheel_forward
                if delay_time > self.wheel_forward_timeout:
                    self.last_time_wheel_forward = wheel.time
                    forward_thread = threading.Thread(target = self.mouse_wheel_forward)
                    forward_thread.start()
            # on wheel backward
            elif wheel.delta == -1.0:
                delay_time = wheel.time - self.last_time_wheel_backward
                if delay_time > self.wheel_backward_timeout:
                    self.last_time_wheel_backward = wheel.time
                    backward_thread = threading.Thread(target = self.mouse_wheel_backward)
                    backward_thread.start()
            return
#%% FUNCTION LOADER REPEAT        
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
        self.stop_repeated_middle_click = False
        mouse.hook(self.on_mouse_wheel)
        mouse.on_middle_click(self.function_loader, args=(self.use_skill_repeatidly_on_middle_click,))
        return

    def unhook_all(self):
        self.stop_repeated_middle_click = True
        mouse.unhook_all()
        return
#%% TEST   

if __name__ == '__main__':
    my_mouse = MyMouse()
    my_mouse.hook_all()
    time.sleep(30)
    my_mouse.unhook_all()
