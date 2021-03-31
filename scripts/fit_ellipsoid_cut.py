"""

"""
from SURFtools.io import read_sur
from SURFtools.shapes import elipsoid_cut

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.optimize import least_squares

from scipy.ndimage import gaussian_filter

from sys import argv

import glob
import os


def residuals(p,X,Z):
    Z_0 = elipsoid_cut(X[0,:,:],X[1,:,:],p[0],p[1],p[2],p[3],p[4],p[5],p[6])
    return (Z-Z_0).flatten()


def preprocessing(Z, sigma):
    Z_processed = Z
    Z_processed= gaussian_filter(Z_processed,sigma,order=0, mode='nearest')
    return Z_processed

def fit_ellipsiod(X,Y,Z,p0, bounds = (0, np.inf), fscale=0.1 ):

    res_robust = least_squares(residuals, p0,
                           bounds = bounds,
                           loss='soft_l1',
                           f_scale=fscale,
                           args=(np.array([X,Y]),Z ))
    return res_robust

def post_processing(p):
    """
    Calcs the values for (dx/dy/h/R/V) the ellipsoid cap
    :param p:
    :return:
    """
    r_z, r_x, r_y, h, x0, y0, z0 = p
    delta = (1.-h/r_z)
    rho = np.sqrt(1. - delta**2)
    dx = 2.*r_x*rho
    dy = 2.*r_y*rho
    R = r_z
    x = r_z - h
    V = np.pi*r_x*r_y*(2*r_z/3 - x + x**3 / (3*r_z**2))

    return dx, dy, h, R, V

def plot_xyy0(x,y,y0):

    f = plt.figure()
    plt.plot(x,y0, 'k')
    plt.plot(x,y, 'r--')

    plt.show()


if __name__ == '__main__':

    # Process a whole folder
    _, folder, output = argv

    # r_z, r_x, r_y, h, x0, y0, z0
    p0 = [2, 2, 2, 0.2, 1.5, 1.5, 0.1]

    output_data = []

    for file in glob.glob(folder+'/*.sur'):
        data = read_sur(file)
        X, Y = np.meshgrid(data['x_axis'], data['y_axis'], indexing='ij')
        Z = data['points']
        Z_prep = preprocessing(Z, 4)

        res = fit_ellipsiod(X, Y, Z_prep, p0, bounds = (0,5))

        file_name = os.path.basename(file)

        dx, dy, h, R, V = post_processing(res.x)

        this_output_data = {
            'file_name': file_name,
            'height': h,
            'diameter_x': dx,
            'diameter_y': dy,
            'radius_curvature': R,
            'Volume': V,
        }

        #Z_fit = elipsoid_cut(X, Y, *res.x)
        #plot_xyy0(X[:,150], Z_fit[:,150], Z_prep[:,150])

        output_data.append(this_output_data)

    output_data = pd.DataFrame(output_data)

    output_data.to_csv(output)



