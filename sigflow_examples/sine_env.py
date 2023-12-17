



from signalflow import *

graph = AudioGraph()
sine = SineOscillator([52, 50])
#sine = SquareOscillator([34, 36])

print( sine )
envelope = ASREnvelope(6, 4.6, 5)
output = sine * envelope * 0.1
output.play()
graph.wait()

