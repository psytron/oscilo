import numpy as np
import cv2
import soundcard as sc        # Get it from https://github.com/bastibe/SoundCard
imWidth, imHeight = 1024, 1024                       # screen size

previous_time = 1000

def draw_wave(screen, mono_audio, xs, title="oscilloscope", gain=5 ):
    global previous_time
    #print(mono_audio.shape)
    screen *= 0                                     # clear the screen
    ys = imHeight/2*(1 - np.clip( gain * mono_audio[0:len(xs)], -1, 1))  # the y-values of the waveform
    pts = np.array(list(zip(xs,ys))).astype(int) # pair up xs & ys
    cv2.polylines(screen,[pts],False,(25,255,0))     # connect points w/ lines
    
    random_number = np.random.randint(100)           # generate a random number
    cv2.putText(screen, f'Random Number: {random_number}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA) # draw text on screen
    current_time = cv2.getTickCount()
    time_elapsed = (current_time - previous_time) / cv2.getTickFrequency() * 1000
    
    cv2.putText(screen, f'DSP Path: {time_elapsed} ms', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(screen, f'tick Count: {cv2.getTickCount()} -', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (233, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(screen, f'Tick  Freq: { cv2.getTickFrequency() } -', (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 122, 255), 2, cv2.LINE_AA)
    
    fps = 1000 / time_elapsed
    cv2.putText(screen, f'FPS: {fps}', (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    cv2.imshow(title, screen)                       # show what we've got
    previous_time = current_time


default_mic = sc.default_microphone()
screen = np.zeros((imHeight,imWidth,3), dtype=np.uint8) # 3=color channels
xs = np.arange(imWidth).astype(int)                  # x values of pixels



while (1):                               # keep looping until someone stops this
    with default_mic.recorder(samplerate=44100) as mic:
        audio_data = mic.record(numframes=1024)  # get some audio from the mic
    draw_wave(screen, audio_data[:,0], xs)             # draw left channel
    key = cv2.waitKey(1) & 0xFF                        # keyboard input
    if ord('q') == key:                                # quit key
        break
