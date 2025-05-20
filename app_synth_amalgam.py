




#  # Launch Matrix ( starts manages memory )
import matrix
import wavegeneratorV1 as waveform
import sensormonR4 as sensor
#import sensormonR5 as sensor  # For Raspberry Pi 5 
import rotorv2 as rotary
#import autorotorV3 as rotary  #  automatically emits controller messages 
import overdrivedistort as fx 


def main():
    procs = []
    manager = Manager()
    evnt = manager.Event()
    m = multiprocessing.Process(target=matrix, args=( evnt, ))
    w = multiprocessing.Process(target=waveform, args=( evnt, ))
    s = multiprocessing.Process(target=sensor, args=( evnt, ))
    r = multiprocessing.Process(target=rotary, args=( evnt, ))
    f = multiprocessing.Process(target=fx, args=( evnt, ))
    procs.extend([m, w, s, r, f])
    m.start()
    w.start()
    s.start()
    r.start()
    f.start()        
    #set_realtime_priority( w.pid )
    for proc in procs:
        proc.join()
 

if __name__ == "__main__":
    main()


#  