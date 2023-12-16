



from signalflow import *

graph = AudioGraph()
sine = SineOscillator([55, 50])
envelope = ASREnvelope(0.6, 4.6, 0.5)
output = sine * envelope * 0.1
output.play()
graph.wait()

