import sympy as sp

#define variables
sp.var('xA yA xB yB sxA2 syA2 sxB2 syB2 s')

#define equations
s=sp.sqrt((xB-xA)**2+(yB-yA)**2)
theta=sp.atan((yB-yA)/(xB-xA))

#define matrix of functions
f=sp.Matrix([[s],[theta]])

#get the jacobian
J=f.jacobian([xA,yA,xB,yB])

#covariance matrix of variables
cov_v=sp.Matrix([[sxA2,0,0,0],
                 [0,syA2,0,0],
                 [0,0,sxB2,0],
                 [0,0,0,syB2]])

#covariance matrix of unknowns
cov_x=J*cov_v*J.T

#substitues the equation as s in the matrix
cov_x=cov_x.subs('sqrt((xB-xA)**2+(yB-yA)**2)',s)


import numpy as np
import matplotlib.pyplot as plt

Y, X = np.mgrid[-3:3:100j, -3:3:100j]
U = -1 - X**2 + Y
V = 1 + X - Y**2
speed = np.sqrt(U*U + V*V)

plt.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=plt.cm.autumn)
plt.colorbar()

f, (ax1, ax2) = plt.subplots(ncols=2)
ax1.streamplot(X, Y, U, V, density=[0.5, 1])

lw = 5*speed/speed.max()
ax2.streamplot(X, Y, U, V, density=0.6, color='k', linewidth=lw)

plt.show()
