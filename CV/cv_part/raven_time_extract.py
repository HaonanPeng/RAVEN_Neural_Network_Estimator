from io import StringIO

import numpy as np 
A =np.loadtxt("bagfiles/raven_state.txt")

np.savetxt('bagfiles/raven_state_time.txt', A[:,0], fmt='%10.6f')   # use exponential notation




