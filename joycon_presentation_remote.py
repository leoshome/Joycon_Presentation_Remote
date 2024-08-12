import tkinter as tk
import pyautogui
from time import sleep, time
from pyjoycon import JoyCon, get_R_id, GyroTrackingJoyCon

# parameter define
RADIUS = 200      # circle size
MOVE_SPEED = 1500 # speed of mouse pointer, larger is faster
MODE = 0          # default mode for Mouse Cursor, 0: Spotlight 1: Hightlight
ALPHA_BACKGROUND = 0.7 # opacity of balck background(form 0 to 1, 0 is no effect)
ALPHA_HIGHTLIGHT = 0.3 # opacity of yellow circle(form 0 to 1, 0 is no color)

pyautogui.FAILSAFE = False # prevent FailSafeException when cursor move to corner

# init joycon controller state
joycon_id = get_R_id()
joycon = JoyCon(*joycon_id)
state = joycon.get_status()
sleep(1)
joycon_gyro = GyroTrackingJoyCon(*joycon_id)
joycon_gyro.reset_orientation()
state_gyro = joycon_gyro.direction
pre_pos_x = state_gyro[1]
pre_pos_y = state_gyro[2]
mode = MODE
previous_x = previous_y = previous_a = previous_b = previous_sr = previous_sl = 0
screen_width, screen_height = pyautogui.size()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

tk.Canvas.create_circle = _create_circle
root = tk.Tk()
root.attributes('-alpha',0)
canvas = tk.Canvas(root, width=screen_width, height=screen_height,highlightthickness=0 ,background='#000000')
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
    state_gyro = joycon_gyro.pointer
    cur_pos_x = state_gyro[0]
    cur_pos_y = -state_gyro[1]

    global pre_pos_x, pre_pos_y
    global previous_x, previous_y, previous_a, previous_b, previous_sr
    global mode
    
    move_x = cur_pos_x - pre_pos_x
    move_y = cur_pos_y - pre_pos_y
    # update pos
    pre_pos_x = cur_pos_x
    pre_pos_y = cur_pos_y
        
    if state['buttons']['right']['x'] != previous_x:
        previous_x = state['buttons']['right']['x']
        if state['buttons']['right']['x']:   # pressdown x to trigger pageup
            pyautogui.press('pageup') 

    if state['buttons']['right']['b'] != previous_b: 
        previous_b = state['buttons']['right']['b']
        if state['buttons']['right']['b']:   # pressdown b to trigger pageup
            pyautogui.press('pagedown')  
        
    if state['buttons']['right']['y'] != previous_y: 
        previous_y = state['buttons']['right']['y']
        if state['buttons']['right']['y']:   # pressdown y to click
            pyautogui.click()  

    if state['buttons']['right']['a'] != previous_a: 
        previous_a = state['buttons']['right']['a']
        if state['buttons']['right']['a']:   # pressdown a to click
            pyautogui.click()  

    if state['buttons']['right']['sr'] != previous_sr: 
        previous_sr = state['buttons']['right']['sr']
        if state['buttons']['right']['sr']:   # change mode
            mode = 0 if mode else 1  


    if state['buttons']['shared']['plus']:
        print("Pressed Plus and reset")
        joycon_gyro.reset_orientation()     

    if state['buttons']['shared']['home']:
        print("Pressed Home and Exiting")
        root.destroy()
        return     

    if state['buttons']['right']['r'] or state['buttons']['right']['zr']:
        if abs(move_x)>0.00001:
            dx = int( move_x*MOVE_SPEED )
        else:
            dx = 0

        if abs(move_y)>0.00001:
            dy = int( move_y*MOVE_SPEED )
        else:
            dy = 0
        
        pyautogui.moveRel(dx,dy, _pause=False)      

        if mode == 0: 
            # black background for Spotlight mode
            root.wm_attributes('-transparentcolor','yellow') # make yellow color as transparent to spotlight effect
            root.attributes('-alpha',ALPHA_BACKGROUND)  # make circle disappeared
        else:        
            # yellow circle for Hightlight mode
            root.wm_attributes('-transparentcolor','#000000') # make yellow color as transparent to spotlight effect
            root.attributes('-alpha',ALPHA_HIGHTLIGHT)  # make circle disappeared

        # start draw cirle around mouse cursor
        x, y = pyautogui.position()
        canvas.coords(circle, x-RADIUS, y-RADIUS, x+RADIUS, y+RADIUS)
    else: 
        root.attributes('-alpha',0) # remove effect by using alpha
    canvas.after(20,move_circle_per)    # make a loop 

canvas.after(20,move_circle_per)        # make a loop 

root.mainloop()
