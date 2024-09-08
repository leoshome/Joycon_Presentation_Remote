# Joycon_Presentation_Remotes

## Turn a right Joy-con controller into a presentation remote like Logitech Spotlight

This is a project on [hackster.io](https://www.hackster.io/leo49/right-joy-con-controller-as-a-presentation-remote-5810e4 "hackster.io"), which can turn a right Joy-con controller into a presentation remote like Logitech Spotlight.

## Instructions/steps
0. Prepare a Nintendo Switch right Joy-Con, and connected to PC via Bluetooth
1. Download the code ( https://github.com/leoshome/Joycon_Presentation_Remote/blob/main/joycon_presentation_remote.py )
2. prepare python package
`pip install joycon-python hidapi pyglm pyautogui pywin32`
3. Execute the code on your Windows PC
`python joycon_presentation_remote.py`

## Usage
Joy-Con(R)’s button mapping:
- Hold “R” or “ZR” → Spotlight mode / Highlight(yellow circle) mode
- Press “X” → Page Up
- Press “B” → Page Down
- Press “Y” or “A” → Right click
- Press “SR” → switch Spotlight mode or Highlight mode
- Press “+” → Pressed if movement is not stable or not working
- Press “Home” → End joycon_presentation_remote.py

## Demo video
[![](https://markdown-videos-api.jorgenkh.no/youtube/BOlwXtNee78)](https://youtu.be/BOlwXtNee78)
