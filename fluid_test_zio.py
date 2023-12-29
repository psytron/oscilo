import fluidsynth
import time 

fs = fluidsynth.Synth(gain=0.8)
fs.start(driver="coreaudio")

sfid = fs.sfload("./data/ZFont.sf2")
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 30)
time.sleep(1.0)
fs.noteon(0, 67, 30)
time.sleep(1.0)
fs.noteon(0, 76, 30)

time.sleep(1.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

time.sleep(1.0)

fs.delete()
