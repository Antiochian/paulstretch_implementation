# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 03:48:22 2020

@author: Hal
"""


import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt

filename="testfile.wav"
outfile = "testout.wav"
def convert_to_mono(input_data):
    #average channels
    res = [0.5*frame[0]+0.5*frame[1] for frame in input_data]
    print("Converted to mono.")
    return np.array(res)

def make_window(width, samplerate):
    #width in frames
    win = []
    for i in np.linspace(0,width,width):
        eq0 = (i-width/2)
        eq1 = eq0*2/width
        eq2 = (1 - eq1**2)**1.25
        win.append(eq2)
    return np.array(win)

def convert_to_windows(sample_rate, input_data, window_size, step):
    amplitude_mask = np.ones(len(input_data))
    N = len(input_data)
    offset = -int(np.ceil(window_size/2))
    win_list, offset_list = [], []
    win = make_window(window_size, sample_rate)
    while offset < N:
        if offset < 0:
            inp_slice = input_data[:window_size+offset]
            win_slice = win[-offset:]
            #inp_slice = np.concatenate([[0]*int((-offset)), input_data[:offset+window_size]])
        elif offset > N - window_size:
            inp_slice = input_data[offset:]
            win_slice = win[:N-offset]
        else:
            inp_slice = input_data[offset:offset+window_size]
            win_slice = win 
        if np.size(win_slice) != np.size(inp_slice):
            print("Ow!")
        padded_win_slice = np.concatenate([np.zeros(max(0,offset)), win_slice, np.zeros(N-len(win_slice) - max(0,offset))])
        amplitude_mask += padded_win_slice
        
        win_list.append(win_slice*inp_slice)
        offset_list.append(offset)
        offset += step
    return win_list, offset_list, amplitude_mask

def plot_wave(sample_rate, data):
    xdata = [i/sample_rate for i in range(len(data))]
    plt.plot(xdata, data)
    return

def reconstitute_waveform(winlist, offsetlist, amplitude_mask, sample_rate):
    output_data = []
    # cropval = offsetlist[0]
    # for i in range(len(winlist)):
    #     frametime = [offsetlist[i] + j for j in range(len(winlist[i]))]
        
    N = len(input_data)
    output_data = np.zeros(N)
    for i in range(len(winlist)):
        #puff up win
        puffed = np.concatenate([np.zeros(max(0,offsetlist[i])), winlist[i], np.zeros(N-len(winlist[i]) - max(0,offsetlist[i]))])
        output_data += puffed
    
    return output_data*amplitude_mask
        
sample_rate, input_data = scipy.io.wavfile.read(filename)
#crop for debug, only get 10s
input_data = input_data[:sample_rate*10]
if len(input_data[0]) == 2:
    input_data = convert_to_mono(input_data)
else:
    input_data = np.array(input_data)
winlist, offsetlist, amplitude_mask = convert_to_windows(sample_rate, input_data, 110250, 4000)
# output_data = [window[i]*input_data[i] for i in range(len(input_data))]
# plot_wave(sample_rate, input_data)
# plot_wave(sample_rate, output_data)
# for i in range(len(winlist)):
#     xdata = [offsetlist[i] + j for j in range(np.size(winlist[i]))]
#     plt.plot(xdata, winlist[i])


output_data = reconstitute_waveform(winlist, offsetlist, amplitude_mask, sample_rate)
#terrible scaling hack
#scalefactor = np.mean([input_data[i]/output_data[i] for i in range(len(input_data)) if (input_data[i]) and (output_data[i])] )
scalefactor = np.mean(input_data)/np.mean(output_data)
output_data *= scalefactor
output_data = output_data.astype('int16')
plt.plot(output_data)
plt.plot(input_data)
plt.title("Reconstituted window buffer Connie.wav")
scipy.io.wavfile.write(outfile, sample_rate, output_data)