import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

def contour_plot_xyzdf(data, cols):
    x = data[cols[0]].values
    y = data[cols[1]].values
    v = data[cols[2]].values

    fig,ax = plt.subplots(figsize=(12,8))
    

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)

    vmin = np.min(v)
    vmax = np.max(v)
    vdif = vmax - vmin
    interval = vdif / 10
    multfactor = 4 # Minimum 2!!!
    if(np.log10(interval) > 1):
        multfactor = 1/(10**np.floor(np.log10(interval))) * multfactor
    if(np.log10(interval) < 0):
        multfactor = 10**np.ceil(np.abs(np.log10(interval))) * multfactor
    interval = np.ceil(interval * multfactor)/multfactor
        
    levels = np.linspace(np.floor(vmin), np.floor(vmin)+interval*10,11)
    
    a0 = ax.tricontourf(x,y,v, levels = levels, cmap="jet")
    plt.gca().invert_yaxis()

#    ax.set_aspect('equal')
    horiz = True
    if(horiz):
        cbax1 =  fig.add_axes([0.265,0.925, 0.5, 0.04])
        cbar1 = fig.colorbar(a0, cax= cbax1, orientation='horizontal')
        cbar1.ax.set_xlabel("Amount of cats (wahw)", fontsize=14, labelpad=10)
        cbar1.ax.xaxis.set_label_position('top')
    else:
        cbax1 =  fig.add_axes([0.925,0.15, .04, 0.7])
        cbar1 = fig.colorbar(a0, cax= cbax1)
        cbar1.ax.set_ylabel("Amount of cats (wahw)", fontsize=14, labelpad=10)


    ax.set_xlabel(r" Year", fontsize=14)
    ax.set_ylabel(r" Julian Day", fontsize=14)

    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    
#    fig.savefig('cont_plt.pdf',bbox_inches='tight')
    fig.show()

def test_plot():

    x = np.linspace(0,10)
    y = np.linspace(0,10)
    v = np.random.rand(x.size,y.size)

    xx, yy = np.meshgrid(x,y)
    x = xx.flatten()
    y = yy.flatten()
    v = v.flatten()
    
    v = v * 565
    
    test = pd.DataFrame(np.vstack((x,y,v)).T,columns=['x','y','z'])
    
    contour_plot_xyzdf(test, ['x','y','z'])
    
    v = v / 100000
    
    test = pd.DataFrame(np.vstack((x,y,v)).T,columns=['x','y','z'])

    contour_plot_xyzdf(test, ['x','y','z'])

    

#import data
d=pd.read_csv("Book1.csv",header=[0,1])

test=d["mol/m2O2"]
test=test.dropna(axis=0, how='all', thresh=None, subset=None, inplace=False)


