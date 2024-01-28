



# 

# spawn tone generator with drift inputs 
# tone generator  drifts down on z ( fades out if not refreshed )

# this will update drifting 
# generator.x( Voltage  )
# generator.2( Voltage2  )

# if no update for a while it sinks 


# analyzer 
# reads all probes and determines if new values need to update generator 
# has access to spectrum , continuum 
# analyzer can synthesize multiple channels to 


# workers collect signal readings and write to matrix 
# hardware controls set live parameters to matrix 



while True:
    analyzer.update()
    generator.x( matrix['gsr'] )
    generator.y( matrix['capacitance'] )



# 