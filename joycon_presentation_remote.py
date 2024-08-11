import tkinter as tk
import pyautogui
from time import sleep, time
from pyjoycon import JoyCon, get_R_id, GyroTrackingJoyCon

pyautogui.FAILSAFE = False # prevent FailSafeException when cursor move to corner

# init joycon controller
joycon_id = get_R_id()
joycon = JoyCon(*joycon_id)
state = joycon.get_status()
sleep(1)
joycon_gyro = GyroTrackingJoyCon(*joycon_id)
joycon_gyro.reset_orientation()
state_gyro = joycon_gyro.direction
pre_pos_x = state_gyro[1]
pre_pos_y = state_gyro[2]

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

tk.Canvas.create_circle = _create_circle

root = tk.Tk()

root.attributes('-alpha',0)
canvas = tk.Canvas(root, width=1920, height=1080,highlightthickness=0 ,background='#000000')
canvas.pack()
root.overrideredirect(True)
root.wm_attributes('-transparentcolor','yellow') # make yellow color as transparent
root.wm_attributes('-topmost', True)

if state['battery']['level'] == 1 :
    # show battery low in screen
    pass

# make a canvas with a yellow circle
x, y = pyautogui.position()
circle = canvas.create_oval(x-150, y-150, x+150, y+150, fill='yellow', outline='', stipple='')

# make the cicle position at mouse cursor
def move_circle_per():
    # get info from joycon
    state = joycon.get_status()
    state_gyro = joycon_gyro.direction
    cur_pos_x = state_gyro[1]
    cur_pos_y = state_gyro[2]
    global pre_pos_x, pre_pos_y
    move_x = cur_pos_x - pre_pos_x
    move_y = cur_pos_y - pre_pos_y
    # update pos
    pre_pos_x = state_gyro[1]
    pre_pos_y = state_gyro[2]    
        
    if state['buttons']['right']['x']: # press x to trigger pageup
        pyautogui.press('pageup') 
    elif state['buttons']['right']['b']: # press b to trigger pagedown
        pyautogui.press('pagedown')  
        
    if state['buttons']['right']['y'] or state['buttons']['right']['a']:
        pyautogui.click()

    if state['buttons']['shared']['plus']:
        print("Pressed Plus and reset")
        joycon_gyro.reset_orientation()     

    if state['buttons']['shared']['home']:
        print("Pressed Home and Exiting")
        root.destroy()
        return     

    if state['buttons']['right']['r'] or state['buttons']['right']['zr']:
        if abs(move_x)>0.00001:
            dx = int( (move_x)*1500 )
        else:
            dx = 0

        if abs(move_y)>0.00001:
            dy = int( (move_y)*1500 )
        else:
            dy = 0
        
        pyautogui.moveRel(dx,dy, _pause=False)      

        # yellow circle 
        root.wm_attributes('-transparentcolor','yellow') # make yellow color as transparent to spotlight effect
        root.attributes('-alpha',0.7)  # make circle disappeared
        
        # start draw cirle around mouse cursor
        x, y = pyautogui.position()
        canvas.coords(circle, x-150, y-150, x+150, y+150)
    else: 
        root.attributes('-alpha',0) # remove effect by using alpha
    canvas.after(20,move_circle_per)    # make a loop 

canvas.after(20,move_circle_per)    # make a loop 

root.mainloop()
