
import random

while True:
    r1 = 'field: '+str( random.randint(11, 80) )
    r2 = 'zerog: '+str( random.randint(11, 90) )
    
    print(r1+'   '+r2+'      '+'_', end='\r')


# print('', end=f'\rUpdate {i}') # For Linux 