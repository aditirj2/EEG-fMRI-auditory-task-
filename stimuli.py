from scipy.io import wavfile 
import numpy as np 
import scipy.signal as sps 
import config 
from psychopy import sound 
from psychopy import visual 

# ========================= Helper functions: gives total samples and duration === #

def _secs2frames(frameRate, duration):
    return int(duration * frameRate) 

def _frames2secs(freq, samples) :
    return (samples / freq) 
    
# =========== loads any raw audio into numpy array ======== ##
def _load_audio(path, target_sample_rate) : 
    
    #load wav_file 
    rate, data = wavfile.read(path)
    
    #check if matches sample rate; if not, resample;
    if rate != target_sample_rate: 
        # Resample data
        number_of_samples = round(len(data) * float(target_sample_rate) / rate) # returns the new amount of samples needed for same duration 
        data = sps.resample(data, number_of_samples) 

    data = data.astype(np.float32) 
    data /= np.max(np.abs(data)) + 1e-9  # normalize to [-1, 1] 
    
    #check if mono file as well 
    if data.ndim > 1 : # is data 1-D (mono) or 2-D (stereo) 
        data = data.mean(axis=1)  # collapse to mono if the file is stereo; averages two columns together sample by sample to one mono channel 
    
    #check duration 
    #sampling freq is # of samples / 1 sec ; duration = (# of samples * freq) 
    duration = _frames2secs(target_sample_rate, len(data))
    
    return data, duration


# ===== load all audio (noise, statement1, statement2) ====##
def load_all_audio(noise, statement1, statement2, target_sample_rate): 
    output = {} #establish dictionary -> nested 
    audios = noise, statement1, statement2 
    file_names = ["noise", "target1", "target2"] 
    
    for j, i in enumerate(audios) :  #for j, i in enumerate(audios): can use this instead for future funct; enumerate returns both position and value 
        print(f"loading sound : {file_names[j]}") 
        data, duration = _load_audio(i, target_sample_rate) 
        individual_data = {
        "data": data,
        "duration": duration 
        } 
        
        print(f"finished loading sound {file_names[j]}") 
        output[file_names[j]] = individual_data 
        
    return output 
    
#SNR adjustment logic=====##

#def _compute_RMS(audio) :
#    total = 0 
#    for n in audio : 
#        total += n**2
#    RMS = np.sqrt(total/ len(audio)) 
#    return RMS

def _compute_RMS(audio) : #faster version of prev _compute_RMS NOTE: assuming noise L/R channels are equivalent for RMS purposes — unverified"
    print(f"{audio} datatype : {audio.dtype}") 
    total = np.mean(audio**2) #takes average of all samples squared 
    RMS = np.sqrt(total) 
    print(RMS) 
    return RMS

def _compute_sf(SNR, RMS_noise, RMS_signal) :
    sf = (SNR*RMS_noise) / RMS_signal 
    return sf

def _scale_audio(audio, scale_factor):
    adj_aud = scale_factor * audio 
    return adj_aud

def _adjust_audio(audio, SNR) :
    #load up data
    target1 = audio["target1"]["data"] 
    target2= audio["target2"]["data"] 
    noise = audio["noise"]["data"] 
    target_audio = []
    target_audio.append(noise) 
    
    #RMS noise first; takes longer must compute only once 
    RMS_noise = _compute_RMS(noise) 
    
    for i in [target1, target2] :
        RMS_signal = _compute_RMS(i)
        sf = _compute_sf(SNR, RMS_noise, RMS_signal)
        adj_target = _scale_audio(i, sf)
        target_audio.append(adj_target) 
        
    return target_audio  
    
#Loading sound objects================

def _build_stero_arr(target_audio, condition) :  
    
    arr_length = len(target_audio)
    stereo = np.zeros((arr_length, 2)) 
    
    if condition == "left" :
        stereo[:,0] = target_audio 
    elif condition == "right" : 
        stereo[:,1] = target_audio
    
    stereo = stereo.astype(np.float32)
    return stereo 

def load_sound(noise, statement1, statement2, target_sample_rate, SNR):
    
    audio = load_all_audio(noise, statement1, statement2, target_sample_rate) #returns dict w duration 
    keys =  ["noise", "target1", "target2"]
    adj_audio = _adjust_audio(audio, SNR) #returns a list of three elements (arr) 
    output = {}
    
    #load up 
    for j, i in enumerate(adj_audio) : 
    
        if keys[j] == "noise" :
            loaded_audio = sound.Sound(i, loops = -1, sampleRate = target_sample_rate, volume=0.1, stereo=True) #loop until stopped 
            individual_data = {
            "sound": loaded_audio,
            "duration": audio[keys[j]]["duration"]
            } 
            output[keys[j]] = individual_data
        else : 
            output[keys[j]] = {}
            
            for side in ["left", "right"] :
                
                stereo_arr = _build_stero_arr(i, side)
                loaded_audio = sound.Sound(stereo_arr, sampleRate = target_sample_rate, volume=0.1, stereo=True)
                
                individual_data = {
                "sound": loaded_audio,
                "duration": audio[keys[j]]["duration"]
                } 
                
                output[keys[j]][side] = individual_data
                
    return output 


#============Visual Stimuli =============#

def visual_stim(win, param, hware, condition) : 
    
    if condition == "left" :
        position =[-550, 0]  # [X, Y] coordinates
    elif condition == "right" :
        position = [550, 0]  # [X, Y] coordinates 
    # Create a circle stimulus
    circle = visual.Circle(
        win=win, units="pix", radius=50, pos= position, fillColor=config.scr["white"], lineColor=config.scr["black"]
    )
    return circle 

def draw_all(stim_list) :
    for stim in stim_list : 
        stim.draw()

#def build_audio_block(predetermined_list) : 
#    #ITI, cue side, cue target
#    return audio 
#    
## ========================= Scanner noise on =================================
#def load_scanner_noise(params, hware, ScannerNoisePath, sRate=44100):
#
#    ScannerNoise = sound.Sound(ScannerNoisePath, sampleRate=sRate, volume=0.1, stereo=True, speaker=hware['speaker'])
#    
#    return ScannerNoise
#