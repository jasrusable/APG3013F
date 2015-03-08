import numpy as np
import matplotlib.pyplot as plt

xvalues=np.arange(0,10)
yvalues=xvalues**2

fig1=plt.figure()

#nothing with give a line representation, ',o' gives dots...',o-' gives dots on the line
plt.plot(xvalues,yvalues,'o')
plt.show()
