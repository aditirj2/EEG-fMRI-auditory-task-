import numpy 
import config
import predetermined
import instructions 
import stimuli
from psychopy import visual, core, event 
from psychopy import sound 


def _correct_Keys(key_pressed, cue_side_aud) :
    if key_pressed == None :
        return 0 
    if key_pressed == cue_side_aud :
        return 10
    else :
        return -10 

def dichotic_task_block(win, block, audio, params, hware, SNR, clock) : 
    
    keys = ["participant_id", "trial_num", "condition", "stim_dur", "ITI",
            "cue_side_vis", "cue_side_aud", "target_type", "SNR"]  # final predetermined.py keys

    possible_keys_rt = [hware["keys"]["detection_key_left"], hware["keys"]["detection_key_right"]]
    
    tally = 0 
    
    results_per_block = []
    
    for trial in block: #each element in block is a dictionary 
    
        #extract elements per trial 
        condition = trial[keys[2]]
        stim_dur = trial[keys[3]]
        iti = trial[keys[4]]
        cue_side_vis = trial[keys[5]]
        cue_side_aud = trial[keys[6]]
        target_type = trial[keys[7]] 
        
        #load visual stim 
        if cue_side_vis == "none" :
            vis = visual.TextStim(win, text="+", height=0.1, color=config.scr["white"])
            vis.draw()
        else :
            vis = [stimuli.visual_stim(win, params, hware, cue_side_vis), visual.TextStim(win, text="+", height=0.1, color=config.scr["white"])]
            stimuli.draw_all(vis) 
        
        #load audio stim   ["target1", "target2"]  
        if cue_side_aud == "left" :
            if target_type == "target1" :
                aud = audio["target1"]["left"]["sound"]
            elif target_type == "target2":
                aud = audio["target2"]["left"]["sound"]
        elif cue_side_aud == "right":
            if target_type == "target1" :
                aud = audio["target1"]["right"]["sound"]
            elif target_type == "target2":
                aud = audio["target2"]["right"]["sound"]

        #trial 
        
        win.flip()
        core.wait(iti) 
        trial_clock = core.Clock()
        stim_dur_onset = clock.getTime()
        aud.play()
        Keys = event.waitKeys(maxWait=stim_dur, keyList=possible_keys_rt, modifiers=False, timeStamped=trial_clock, clearEvents=True) #turn this into a waitkeys, with stim_dur being max time waited  
        
        if Keys == None : 
            key_pressed = None
            rt = None
        else :
            key_pressed = Keys[0][0]
            rt = Keys[0][1]
        
        this_t_tally = _correct_Keys(key_pressed, cue_side_aud) #returns how much money added or subtracted
        tally += this_t_tally
        
        trial["stim_start"] = stim_dur_onset
        trial["key_pressed"] = key_pressed
        trial["rt"] = rt 
        trial["this_trial_tally"] = this_t_tally
        trial["total_tally"] = tally
        
        results_per_block.append(trial) 
    
    return results_per_block , tally  



