" created by @AditiJindal 9-20-2026" 

# main file that runs task takes from config.py 

import config 
import calibration
import instructions 
import predetermined
import dichotic_task 
import stimuli 
import output 
from psychopy import visual, core, event
import random 
import os 
import pandas as pd 

def test(audio) :
     for i in range(5) :
        
        targets = [audio["target1"]["left"]["sound"], audio["target2"]["left"]["sound"], audio["target1"]["right"]["sound"], audio["target2"]["right"]["sound"]]
        names = ["target1L", "target2L", "target1R", "target2R"] 
        single_pick = random.choice(targets) 
        position = targets.index(single_pick) 
        print(names[position]) 
        single_pick.play() 
        core.wait(3) 
        
def end_experiment():    
    #savecsv
    # Force the Python process to terminate immediately
    os._exit(0) 

def main() : 
    print("running dichotic auditory task")
    # Add a global key 'esc' to trigger the function
    event.globalKeys.add(key=config.hware["keys"]["quit_key"], func=end_experiment)
 
    #GUI: ask for participant ID 
    print("asking for participant ID") 
    participant_id = "001"
    
    #config: set up window + session objects (keyboard -> for me, window, button -> for the patient etc.) 
    
    # Initialize Window 
    win = visual.Window(size=(1440, 900), color=config.scr["darkgrey"], fullscr=True)
    # Fixation Cross object stim 
    fixwin = visual.TextStim(win, text="+", height=0.1, color=config.scr["white"])
    
    #keyboard
        
    #results list -> in BIDs look for later 
    results = []
    
    #run calibration.py
    print("running calibration")  
    SNR = calibration.staircase() #returns 1.0 as SNR can change 
    
    #load audio 
    print("loading audio") 
    audio = stimuli.load_sound(config.SCANNER_NOISE_PATH, config.target1_path , config.target2_path , config.params["default_sample_rate"], SNR) 
    
    #run predetermined.py returns 3 separate lists 
    print("running predetermined.py") 
    session = predetermined.trials_per_block(participant_id, audio, config.params, SNR) #saves session as tuple: each is one block order is either fixed or random 
    check = predetermined.check_session_ITIs(session) #print this block to check 
    
    #start background audio noise 
    audio["noise"]["sound"].play() #should loop until end 
    print("about to draw")
    
    #instruction screen; waitkeys()
    instructions.starting_instructions(win, config.params, config.hware) 
    event.waitKeys(keyList = [config.hware["keys"]["wait_key"]])
    fixwin.draw()
    win.flip()
    
    running_tally = 0 
    exp_clock = core.Clock() 
    
    for i, block in enumerate(session): 
        print(f"session:{i}")
        results_per_block , tally = dichotic_task.dichotic_task_block(win, block, audio, config.params, config.hware, SNR, exp_clock)
        results.append(results_per_block)
        running_tally += tally
        
        #print update screen after one block with new tally 
        instructions.update_instructions(win, config.params, config.hware, running_tally) 
        event.waitKeys(keyList = [config.hware["keys"]["wait_key"]])
    
    #end screen 
    instructions.end_instructions(win, config.params, config.hware, running_tally) 
    event.waitKeys(keyList = [config.hware["keys"]["wait_key"]])
    
    #turn results into csv for export in BIDs format 
    df = output.dict_to_df(results)
    df.to_csv(config.DATA_PATH/ f"{participant_id} output.csv", index=True)
  
main()
    
    
    