import numpy as np 

def elipsoid_cut(X,Y,r_z,r_x,r_y,h,x0,y0,z0):
    Z = r_z*np.sqrt(1 - (X - x0) **2 / r_x**2 - (Y - y0) **2 / r_y**2 ) - r_z + h
    Z = np.nan_to_num(Z)
    Z[ Z < 0] = 0
    Z += z0
    return Z
