




import time
import socket
import datetime
import random
import platform

# Pin configuration
# DEFAULT: 

px = 0  # Initial value of px
px2 = 0


def setup_random_emitter( callback_in=print  ):
    global px    
    global px2
    import math
    iteration =0
    while True:
        time.sleep( 0.01 )

        px = 50 * (1 + math.sin(2 * math.pi * iteration / 120))
        px2 = 50 * (1 + math.sin(2 * math.pi * iteration / 300))
        iteration = (iteration + 1) % 120
        callback_in( px , px2 )



def setup_rotary_listener( CLK = 16  , DT = 20, SW = 21 , CLK2=23 , DT2=24 , SW2=25 , callback_in=print  ):
    #CLK = 16  # Clock pin
    #DT = 20  # Data pin
    #SW = 21  # Switch pin   
    # Variables
    import RPi.GPIO as GPIO
    last_CLK_state = False
    last_CLK_state2 = False

    GPIO.setmode( GPIO.BCM )
    GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT, GPIO.IN)
    GPIO.setup(CLK, GPIO.IN)
    
    GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT2, GPIO.IN)
    GPIO.setup(CLK2, GPIO.IN)

    # GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(DT3, GPIO.IN)
    # GPIO.setup(CLK3, GPIO.IN)    


    def handle_CLK_edge(channel):
        nonlocal last_CLK_state
        global px
        current_CLK_state = GPIO.input(CLK)
        if current_CLK_state != last_CLK_state:
            if current_CLK_state and GPIO.input(DT) != current_CLK_state:
                px += 1  # Increment px on clockwise rotation
            elif current_CLK_state and GPIO.input(DT) == current_CLK_state:
                px -= 1  # Decrement px on counterclockwise rotation
        last_CLK_state = current_CLK_state
    def handle_SW_press(channel):
        print("Switch pressed!")

    def handle_CLK_edge2(channel):
        nonlocal last_CLK_state2
        global px2
        current_CLK_state2 = GPIO.input(CLK2)
        if current_CLK_state2 != last_CLK_state2:
            if current_CLK_state2 and GPIO.input(DT2) != current_CLK_state2:
                px2 += 1  # Increment px on clockwise rotation
            elif current_CLK_state2 and GPIO.input(DT2) == current_CLK_state2:
                px2 -= 1  # Decrement px on counterclockwise rotation
        last_CLK_state2 = current_CLK_state2
    def handle_SW_press2(channel):
        print("Switch pressed2!")       

    # def handle_CLK_edge3(channel):
    #     nonlocal last_CLK_state3
    #     nonlocal px3
    #     current_CLK_state3 = GPIO.input(CLK3)
    #     if current_CLK_state3 != last_CLK_state2:
    #         if current_CLK_state3 and GPIO.input(DT3) != current_CLK_state3:
    #             px2 += 1  # Increment px on clockwise rotation
    #         elif current_CLK_state3 and GPIO.input(DT3) == current_CLK_state3:
    #             px2 -= 1  # Decrement px on counterclockwise rotation
    #     last_CLK_state3 = current_CLK_state3
    # def handle_SW_press3(channel):
    #     print("Switch pressed2!")                

    # Add event listener for CLK pin
    GPIO.add_event_detect(CLK, GPIO.BOTH, callback=handle_CLK_edge)    
    GPIO.add_event_detect(SW, GPIO.FALLING, callback=handle_SW_press)
    GPIO.add_event_detect(CLK2, GPIO.BOTH, callback=handle_CLK_edge2)    
    GPIO.add_event_detect(SW2, GPIO.FALLING, callback=handle_SW_press2)     


    try:
        while True:
            time.sleep(0.01) # CPU LIMIT
            callback_in( px , px2 )
    except KeyboardInterrupt:
        GPIO.remove_event_detect(CLK)
        GPIO.remove_event_detect(DT)
        GPIO.remove_event_detect(SW)
        GPIO.cleanup()



def stream_to_address_on_port( address_in , port_in ):
    HOST = address_in
    PORT = port_in
    global px
    global px2



    # Create a socket object using socket.socket() method
    # AF_INET is the address family of the socket. This is the Internet address family for IPv4.
    # SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        def callback_fun( pars ):
            print( 'pars' )
            print( pars )

        if platform.system() == 'Darwin':  # Darwin indicates MacOS
            setup_random_emitter( callback_fun )
        elif platform.system() == 'Linux':  # Raspberry Pi runs on a Linux OS
            setup_rotary_listener( 16, 20, 21, 23, 24, 25, callback_fun )        
        
        while True:
            message = ( {'x':px , 'y':px2 } )
            print(' is this streaming ? ')
            # override to send timestamp 
            # message = str(datetime.datetime.now())
            
            s.sendall( json.dumps( message ).encode() )
            
            data = s.recv(1024)
            print(f'Received: {data.decode()}')




if __name__ == "__main__":
    def print_px_a(px , px2):
        print("A px value: ", px , px2)
    setup_rotary_listener( 16,20,21,23,24,25,print_px_a)

 
