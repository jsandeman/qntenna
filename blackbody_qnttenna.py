'''
A test script for qnttenna module

Displays the output of a Delta calculation for a solar spectrum given by
a 5500K blackbody spectrum.
'''
from qnttenna import delta_integral, load_spectrum_data, find_optimum_peaks, gauss

from matplotlib.colorbar import ColorbarBase
import matplotlib.colors as colors
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

import numpy as np
import matplotlib.pyplot as plt
from os.path import join

if __name__ == '__main__':
    xinches = 5.0
    yinches = 8.75
    fig1 = plt.figure('Blackbody', figsize=(xinches, yinches), facecolor='w')

    width = 3.75
    xmargin = 0.7
    height = width
    ymargin = 0.5
    yint = 0.5

    ax1 = plt.axes([xmargin/xinches, (ymargin + height + yint)/yinches, width/xinches, height/yinches])
    ax2 = plt.axes([xmargin/xinches, ymargin/yinches, width/xinches, height/yinches])

    # File for the blackbody spectrum
    spectrumfile = join('spectra', 'BB-5500K.txt')

    calc_data, spectrum = delta_integral(spectrumfile, [10, 15, 25], autosave=False)
    [l0, dl, w, A, B, Delta] = calc_data

    pk1, pk2 = find_optimum_peaks(spectrum, l0, dl, w, Delta)

    display_width = 15 # nm

    wi = np.searchsorted(w, display_width)

    cmap = plt.get_cmap('viridis')
    cnorm  = colors.Normalize(vmin=0.0, vmax=1.0)
    scalarMap = cm.ScalarMappable(norm=cnorm, cmap=cmap)
    scalarMap.set_array(Delta)

    d = Delta[:,:,wi]/np.max(Delta[:,:,wi]) # normalized data

    # np.flipud is used to get the vertical axis into the normal orientation
    ax1.imshow(np.flipud(d), cmap=cmap, norm=cnorm, extent=(np.min(l0), np.max(l0), np.min(dl), np.max(dl)), aspect='auto')
    ax1.plot(pk1[wi,1], pk1[wi,2], 'bo')
    ax1.plot(pk2[wi,1], pk2[wi,2], 'ro')

    ax1.set_ylabel(r'$\Delta \lambda$ (nm)')
    ax1.set_xlabel(r'$\lambda_{0}$ (nm)')
    ax1.set_title(r'$\Delta$ for T = 5500K Blackbody Spectrum, w =' + str(display_width) + ' nm')

    axpbar = plt.axes([0, 0, 101, 101], zorder=2)
    axpbar.spines['bottom'].set_color('w')
    axpbar.spines['top'].set_color('w')
    axpbar.spines['left'].set_color('w')
    axpbar.spines['right'].set_color('w')
    axpbar.tick_params(axis='x', colors='w')
    axpbar.tick_params(axis='y', colors='w')
    axpbar.set_axes_locator(InsetPosition(ax1, [0.45, 0.91, 0.45, 0.05]))
    cb1 = ColorbarBase(axpbar, cmap=cmap, norm=cnorm, orientation='horizontal', ticks=[0.0, 0.25, 0.5, 0.75, 1.0])
    cb1.outline.set_edgecolor('w')
    cb1.set_label(r'$\Delta = A-B$ (arb.)', color='w')

    ax2.plot(spectrum[:,0], spectrum[:,1]/np.max(spectrum[:,1]), '-k')

    xs = np.linspace(np.min(l0), np.max(l0), 400)
    norm = w[wi]*np.sqrt(2*np.pi)
    ax2.plot(xs, norm*gauss(xs, w[wi], pk1[wi,1]-pk1[wi,2]/2), color='blue')
    ax2.plot(xs, norm*gauss(xs, w[wi], pk1[wi,1]+pk1[wi,2]/2), color='blue')
    ax2.plot(xs, norm*gauss(xs, w[wi], pk2[wi,1]-pk2[wi,2]/2), color='red')
    ax2.plot(xs, norm*gauss(xs, w[wi], pk2[wi,1]+pk2[wi,2]/2), color='red')

    ax2.text(0.025, 0.95, r'$\lambda_0 = $' + str(pk1[wi,1]) + ' nm', color='blue', ha='left', transform=ax2.transAxes)
    ax2.text(0.025, 0.91, r'$\Delta \lambda = $' + str(pk1[wi,2]) + ' nm', color='blue', ha='left', transform=ax2.transAxes)
    ax2.text(0.9975, 0.95, r'$\lambda_0 = $' + str(pk2[wi,1]) + ' nm', color='red', ha='right', transform=ax2.transAxes)
    ax2.text(0.9975, 0.91, r'$\Delta \lambda = $' + str(pk2[wi,2]) + ' nm', color='red', ha='right', transform=ax2.transAxes)

    ax2.set_ylim(0.0, 1.25)
    ax2.set_xlim(np.min(l0), np.max(l0))
    ax2.set_xlabel('wavelength (nm)')
    ax2.set_ylabel('spectral irradience (arb.)')

    fig1.show()

    plt.show()
#