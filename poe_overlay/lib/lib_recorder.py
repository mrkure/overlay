# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 13:32:29 2022

@author: mrkure
"""

import mouse, keyboard, time, json, numpy as np, sys
from params import params
class Recorder:
    def __init__(self):
        self.hooks = []
        self.rec_hooked = False
        self.khook, self.mhook, self.mhook2, self.hooked = None, None, None, False
        self.file = r'U:/_python/project/poe_overlay/resources/recorder_sequence.txt'
        try:
            with open(self.file, "r") as fp:
                self.sequence = json.load(fp)
        except:
            self.sequence = []          
            
    def on_right_click(self):
        x, y = mouse.get_position()
        self.sequence.append(['mouse_move', [x, y]])
        self.sequence.append(['right_click', [None, None]])
        print('right click')  
        
    def on_left_click(self):
        x, y = mouse.get_position()
        self.sequence.append(['mouse_move', [x, y]])
        self.sequence.append(['left_click', [None, None]])
        print('left click')
           
    def on_key_pressed(self,event):
        name = event.name
        if name == 'num lock':
            print(f'{name} pressed skipped')  
        else:
            self.sequence.append(['key_press', [name, name]])
            print(f'{name} pressed')

    def start_recording(self):
        if not self.hooked:
            self.hooked = True
            self.sequence = []
            self.khook  = keyboard.on_press(self.on_key_pressed, suppress=False)
            self.mhook  = mouse.on_click(self.on_left_click)
            self.mhook2 = mouse.on_right_click(self.on_right_click) 

    def stop_recording(self):
        if self.hooked:
            keyboard.unhook(self.khook)
            mouse.unhook(self.mhook)    
            mouse.unhook(self.mhook2)  
            self.sequence = self.sequence[: len(self.sequence) - 3]  
           
            with open(self.file, "w") as fp:
                json.dump(self.sequence, fp)
            self.hooked = False
            
    def play_recording(self, delay = 0.05):        
        for val in self.sequence:
            print(val)
            if val[0] == 'mouse_move':
                mouse.move(val[1][0], val[1][1])
                time.sleep(delay)
            if val[0] == 'left_click':
                mouse.click()
                time.sleep(delay)                
            if val[0] == 'right_click':
                mouse.right_click()
                time.sleep(delay)                 
            if val[0] == 'key_press':
                keyboard.press(val[1][0])
                time.sleep(0.05)
                keyboard.release(val[1][0])                
                time.sleep(delay)  
                
#%% HOOK UNHOOK
    def hook_all(self):
        if not self.rec_hooked:
            self.hooks.append(keyboard.add_hotkey(params['use_aura_buffs_sequence'], self.play_recording, args=()) )   
        self.rec_hooked = True
       
    def unhook_all(self):
        if self.rec_hooked:
            for hook in self.hooks:
                keyboard.remove_hotkey(hook)
            self.hooks = []
        self.rec_hooked = False
#%% TEST                   
if __name__ == '__main__':             
    rec = Recorder()    
       
    rec.start_recording()
    for i in range(100):
        time.sleep(0.1)
    
    rec.stop_recording()
    
    sequence = rec.sequence
    
    rec.play_recording(1)





















