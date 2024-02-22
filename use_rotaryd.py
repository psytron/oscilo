

import rotaryd




def rotary_update( par_in ):
    print( par_in )


rotaryd.setup_rotary_listener( 16  , 20,  21 , 23 , 24 , 25 , rotary_update    )
