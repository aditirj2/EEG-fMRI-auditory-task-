from psychopy import visual, core
import config 


#starting screen instructions : include win.flip() in this function 
def _build_instructions_text(params, hware):
    reward = params["incentive_value"]
    key_left = hware["keys"]["detection_key_left"].upper() 
    key_right = hware["keys"]["detection_key_right"].upper()
    space = hware["keys"]["wait_key"].upper()

    return (
        "In this task you will hear speech sentences mixed into background noise. Press a key as soon as you detect a sentence.\n\n"
        f"Press a {key_left} as soon as you detect a sentence on the left. Press a {key_right} as soon as you detect a sentence on the right.\n\n"
        f"Correct detections earn you +{reward}c each.False alarms (pressing a key when no sound played) or pressing the wrong key costs you -{reward}c each.\n\n"
        "A circle on the screen shows you which side (or sides) to listen to "
        "during each part of the task. Please stay still and keep your eyes "
        "on the center cross throughout.\n\n"
        f"Press {space} to begin."
    )

def _build_earnings_text(params, hware, tally_cents):
    total_dollars = tally_cents / 100
    sign = "-" if total_dollars < 0 else ""
    return (
        "Block complete!\n\n"
#        f"Correct detections: {n_hits} (+${reward_cents / 100:.2f})\n"
#        f"False alarms: {n_false_alarms} (-${penalty_cents / 100:.2f})\n\n"
        f"Total earned: {sign}${abs(total_dollars):.2f}\n\n"
        "Next session starting soon."
    )
    
def _end_experiment(params, hware, tally_cents):
    total_dollars = tally_cents / 100
    sign = "-" if total_dollars < 0 else ""
    return (
        "Experiment complete!\n\n"
#        f"Correct detections: {n_hits} (+${reward_cents / 100:.2f})\n"
#        f"False alarms: {n_false_alarms} (-${penalty_cents / 100:.2f})\n\n"
        f"Total earned: {sign}${abs(total_dollars):.2f}\n\n"
        "Thank you!."
    )

def starting_instructions(win, params, hware) : 
    print("printing starting instructions")
    starting = visual.TextStim(win, text=_build_instructions_text(params, hware), color=config.scr["white"])
    starting.draw() 
    win.flip() 
    core.wait(2) #waitkeys here 

def update_instructions(win,params,hware,tally) :
    print(f"printing update instructions... tally = {tally}")
    update = visual.TextStim(win, text=_build_earnings_text(params, hware, tally), color=config.scr["white"])
    update.draw() 
    win.flip() 
    
def end_instructions(win,params,hware,tally) :
    print(f"printing end instructions... tally = {tally}")
    print(f"printing update instructions... tally = {tally}")
    end = visual.TextStim(win, text=_end_experiment(params, hware, tally), color=config.scr["white"])
    end.draw() 
    win.flip() 
    

    
    