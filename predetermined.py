import random 
import config 


def _constant_fill(arr_length, fill_condition) :  #returns list with all elements the same 
    filled = [fill_condition] * arr_length #list 
    return filled 
    
def _balanced_shuffle(split_A, condition_A, condition_B, arr_length):  #returns a list with elements randomly shuffled, however elements maintain ratio 
    num_A = int(split_A*arr_length)
    num_B = arr_length - num_A 
    arr_A = _constant_fill(num_A, condition_A)
    arr_B = _constant_fill(num_B, condition_B)
    arr = arr_A + arr_B 
    #shuffle 
    random.shuffle(arr) 
    return arr

def _indepen_rand_draw(lower_bound, upper_bound, arr_length) : #function, give a range and number, returns a list with number and random values within the number 
    arr = []
    for _ in range(arr_length) : #repeating this N times, the index doesn't matter convention says _
        rand = random.uniform(lower_bound, upper_bound) 
        arr.append(rand) 
    return arr 
    
def _ITI_arr_compute_block(num_trials, params):
    
    ITI = [] 
    trials = ["short" , "long"] 
    trial_type = _balanced_shuffle(params["short_to_long_ITI_ratio"], trials[0], trials[1], num_trials) #list with what trial when 
    
    for trial in trial_type : 
        if trial == "long" : 
            iti = _indepen_rand_draw(params["min_ITI_long"], params["max_ITI_long"], 1)
        elif trial == "short" : 
            iti = _indepen_rand_draw(params["min_ITI_short"], params["max_ITI_short"], 1)

        ITI.extend(iti)  #change to append if redundant 
        
    return ITI

def _vis_aud_stim_order(num_trials, condition, params):
    
    stim = ["left", "right", "none"] 
    split = params["attnd_aud_split"] 
    
    if condition == "AttR" :
        visual = _constant_fill(num_trials, stim[1])
        aud = _constant_fill(num_trials, stim[1])
    elif condition == "AttL" :
        visual = _constant_fill(num_trials, stim[0])
        aud = _constant_fill(num_trials, stim[0])
    elif condition == "AttND" :
        visual = _constant_fill(num_trials, stim[2]) 
        aud = _balanced_shuffle(split, stim[0], stim[1], num_trials)
    else :
        visual = [] #raise error here 
        aud = [] 
    
    return visual, aud 

def _target_type(num_trials, params) : #takes num of trials and different trials and returns random conditon
    
    targets = params["target_types"] 
    ratio = params["target_ratio"] 
    target_types = _balanced_shuffle(ratio, targets[0], targets[1], num_trials)
    
    return target_types

def _trial_order_one_block(participant_id, params, condition_type, duration1, duration2, SNR):

    trials_per_block = params["trials_per_block"]
    block = []  # list
    keys = ["participant_id", "trial_num", "condition", "stim_dur", "ITI",
            "cue_side_vis", "cue_side_aud", "target_type", "SNR"]  # final predetermined.py keys

    if duration1 != duration2:
        print("duration1 is not equal to duration2; wrong audio files")

    # per block compute ITIs, lists
    
    ITI = _ITI_arr_compute_block(trials_per_block, params)
    stim_info = _vis_aud_stim_order(trials_per_block, condition_type, params)
    cue_side_vis = stim_info[0]
    cue_side_aud = stim_info[1]
    target_type = _target_type(trials_per_block, params) 

    for i in range(trials_per_block):

        trial = {}
        # constants
        trial[keys[0]] = participant_id
        trial[keys[1]] = i + 1
        trial[keys[2]] = condition_type
        trial[keys[3]] = duration1  # how relevant is this to keep in output not sure, but important in building itis and other arrays
        trial[keys[4]] = ITI[i]
        trial[keys[5]] = cue_side_vis[i]
        trial[keys[6]] = cue_side_aud[i]
        trial[keys[7]] = target_type[i]
        trial[keys[8]] = SNR
        
        block.append(trial)

    return block

def trials_per_block(participant_id, audio, params, SNR):

    session = []  # list

    duration1 = audio["target1"]["left"]["duration"] #picked any side returns same duration 
    duration2 = audio["target2"]["left"]["duration"]
    conditions = params["conditions"]

    for condition in conditions:
        block = _trial_order_one_block(participant_id, params, condition, duration1, duration2, SNR)
        session.append(block)

    return session


def check_session_ITIs(session) :  #returns list of ITIs per block and returns total ITI per block 
    ITIs = []
    total_itis = []
    
    for block in session : 
        ITIs_this_sesh = []
        total_iti = 0 
        for trial in block:
            iti = trial["ITI"]
            ITIs_this_sesh.append(iti)
            total_iti += iti 
        ITIs.append(ITIs_this_sesh)
        total_itis.append(total_iti)

    return ITIs, total_itis 


