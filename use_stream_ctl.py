


import rotaryd
import ads



def rotary_update( x_in , y_in ):
    print( x_in , y_in  )


# rotaryd.setup_rotary_listener( 16  , 20,  21 , 23 , 24 , 25 , rotary_update    )


while True:
    valz = ads.read()
    print( valz )
