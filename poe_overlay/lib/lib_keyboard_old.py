
import keyboard, time, threading, random, mouse
def revert(val):
    if val == 0: val = 1
    else: val = 0
    return val
"""
Created on Tue Jul 26 15:55:25 2022
"""





# =============================================================================
# f2 - send or stop repeatedly ctrl+r molten shell
# =============================================================================
f2_pressed_run = [0]

def on_f2_pressed():
    while True:
        if f2_pressed_run[0]:            
            # keyboard.send('ctrl+r')
            mouse.click(button = 'middle')
            time.sleep(10)
            time.sleep(random.randint(1,1000)/1000)
        else:return
        
def on_f2_pressed_worker(running):
    f2_pressed_run[0] = revert(f2_pressed_run[0])
    if not f2_pressed_run[0]:
        return
    else:
        forward_thread = threading.Thread(target = on_f2_pressed)
        forward_thread.start()
    return  

# =============================================================================
# f4 - clear any stash
# =============================================================================
f4_pressed_run = [0]

def on_f4_pressed():
    sleep  = 0.03
    keyboard.press('ctrl')
    time.sleep(sleep)
    while True:
        if not f4_pressed_run[0]:
            keyboard.release('ctrl')
            return
        mouse.click()
        time.sleep(sleep)            
    keyboard.release('ctrl')
    f4_pressed_run[0] = 0
    return    

def on_f4_pressed_worker(running):
    f4_pressed_run[0] = revert(f4_pressed_run[0])
    if not f4_pressed_run[0]:
        return
    else:
        forward_thread = threading.Thread(target = on_f4_pressed)
        forward_thread.start()
    return 
# =============================================================================
# f5 - use currency to identify etc ...
# =============================================================================
f5_pressed_run = [0]

def on_f5_pressed():
    sleep  = 0.03
    keyboard.press('shift')
    time.sleep(sleep)
    while True:
        if not f5_pressed_run[0]:
            keyboard.release('shift')
            return
        mouse.click()
        time.sleep(sleep)            
    keyboard.release('shift')
    f5_pressed_run[0] = 0
    return    

def on_f5_pressed_worker(running):
    f5_pressed_run[0] = revert(f5_pressed_run[0])
    if not f5_pressed_run[0]:
        return
    else:
        forward_thread = threading.Thread(target = on_f5_pressed)
        forward_thread.start()
    return 

# =============================================================================
# tilde - hideout port
# =============================================================================
def on_tilde_pressed():
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

def on_tilde_pressed_worker():
    threa = threading.Thread(target = on_tilde_pressed)
    threa.start() 
    return

# =============================================================================
# flasks    
# =============================================================================
flasks_pointer, flasks = [0],         [ [1], [2] , [3], [4] , [5],   ]
def flask_use_rotation():    
    for send in flasks[flasks_pointer[0]]:
        keyboard.send(str(send))
        time.sleep(0.1)
    flasks_pointer[0] += 1
    if flasks_pointer[0] == len(flasks):
        flasks_pointer[0] = 0
    return 
 
def flasks_use():
    keyboard.send('5')
    time.sleep(0.1)
    
# =============================================================================
# hook unhook 
# =============================================================================
def hook_all():
    
    # key remaps
    keyboard.remap_key('caps lock', 'u')
  
    # longterm instant buffs  - molten shell      
    keyboard.add_hotkey('f2', on_f2_pressed_worker, args=(f2_pressed_run,), suppress=True, timeout=1, trigger_on_release=False)    

    # general space itemizing (alch, identify, alternation ...)   
    keyboard.add_hotkey('f4', on_f4_pressed_worker, args=(f4_pressed_run,), suppress=True, timeout=1, trigger_on_release=False)   
        
    # general space itemizing (alch, identify, alternation ...)   
    keyboard.add_hotkey('f5', on_f5_pressed_worker, args=(f5_pressed_run,), suppress=True, timeout=1, trigger_on_release=False)     
   
    # use portal
    keyboard.add_hotkey('`',  on_tilde_pressed_worker,   args=(),           suppress=True, timeout=1, trigger_on_release=False)     
    
    return   
 
def unhook_all():
    f5_pressed_run[0] = 0
    keyboard.unhook_all()
    return   
# =============================================================================
# 
# =============================================================================
if __name__ == '__main__':

    keyboard.add_hotkey('f4', on_f4_pressed_worker, args=(f4_pressed_run,), suppress=True, timeout=1, trigger_on_release=False)    
    keyboard.add_hotkey('f5', on_f5_pressed_worker, args=(f5_pressed_run,), suppress=True, timeout=1, trigger_on_release=False)    
    keyboard.add_hotkey('`',  on_tilde_pressed_worker,   args=(),           suppress=True, timeout=1, trigger_on_release=False)
    # keyboard.unhook_all()
    input()
















