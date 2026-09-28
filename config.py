"created by AditiJindal 09-20-2026"

import os
from pathlib import Path 
from psychopy import prefs
from psychopy.hardware import keyboard

#ALL PATHS HERE
ROOT_DIR= Path(r"C:\Users\aditi\Downloads\CONNECTLAB\auditory_task") #change later 
STIM_PATH = ROOT_DIR/"stim_files"
DATA_PATH = ROOT_DIR/"data"

SCANNER_NOISE_PATH = STIM_PATH/"noise"/"testing_noise.wav" #sample noise is 5 seconds long 
target1_path = STIM_PATH/"target"/"target1.wav" 
target2_path = STIM_PATH/"target"/"target2.wav"

stim_duration = 2.980045351473923 #hardcoded

params = {}  #anything related to the actual trial 

#AttR; target only from right), attend left (AttL; target only from left), and attend non-directionally (AttND; target from either side).
params["conditions"] = ["AttR", "AttL", "AttND"]
params["trials_per_block"] = 8
params["attnd_aud_split"] = 0.5
params["target_types"] = ["target1", "target2"]  
params["target_ratio"] = 0.5 
params["min_ITI_long"] = 7
params["max_ITI_long"] = 9
params["min_ITI_short"] = 3
params["max_ITI_short"] = 5
params["short_to_long_ITI_ratio"] = 0.1
#constants 
params["incentive_value"] = 10 
params["default_sample_rate"] = 44100 #both audios match this  might move to hware later idk

# _______________________________________________________ Set Screen Parameters 
scr = {

    "white": [1, 1, 1],                                 # Fixation cross / text
    "grey": [0, 0, 0],                                  # Fixation cross / text
    "darkgrey": [-0.5, -.5, -.5],                       # Brighter background
    "black": [-1, -1, -1],                              # Background
    "red": [0.83, 0, 0],                                # FA;  luminance 50%
    "green": [0, 0.42, 0],                              # Hit; luminance 50%
    "yellow": [0.49, 0.49, 0],                          # Miss
    "dist": 50,                                         # cm
    "width": 30,                                        # cm
    "skipChecks": False,                                # Equivalent for timing checks
}

#fill in with hware preferences -> later after trial starts working 
hware  = {}

## _______________________________________ hardware
## [IMPORTANT] Monitor that we are gonna use (e.g StimPCmonitor)
#hware['mon'] = monitors.Monitor('StimPCmonitor')
#
## import button as inlet
#hware['button']          = importPylsl()
#hware['marker_bpress']   = [32513] # prisma 2 button marker for #2 button - right index finger #need to change based on trial 
##hware['trigger']         = keyboard.Keyboard()   #= sign from TR sync
#
#hware['keyboard'] = keyboard.Keyboard()
#hware['speaker']  = speaker.SpeakerDevice(resample=True) # 0 is headphones, 2 is external speaker

# ---------------------------------------------------------------------------
# Response keys
# ---------------------------------------------------------------------------

hware["keys"] = {} 
hware["keys"]["detection_key_left"] = 'left'
hware["keys"]["detection_key_right"] = 'right'
hware["keys"]["quit_key"]= "escape"
hware["keys"]["wait_key"]= "space"







