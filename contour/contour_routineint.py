import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import griddata
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

def contour_plot_xyzdf(data,cxlab,cols, uylim=0.0,lylim=0.0,uxlim=0.0,lxlim=0.0,uservmin=0.0,uservmax=0.0,axlimauto=True,autobounds=True):
    x = data[cols[0]].values
    y = data[cols[1]].values
    v = data[cols[2]].values

    fig,ax = plt.subplots(figsize=(12,8))
    

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)

    if autobounds:
        vmin=np.min(v)
        vmax = np.max(v)
    
    else:
        vmin=uservmin
        vmax=uservmax

    vdif = vmax - vmin
    
    interval = vdif / 10
    multfactor = 4 # Minimum 2!!!
    if(np.log10(interval) > 1):
        multfactor = 1/(10**np.floor(np.log10(interval))) * multfactor
    if(np.log10(interval) < 0):
        multfactor = 10**np.ceil(np.abs(np.log10(interval))) * multfactor
    interval = np.ceil(interval * multfactor)/multfactor
    
    if autobounds:
        levels = np.linspace(np.floor(vmin), np.floor(vmin)+interval*10,11)

    else:
        levels = np.linspace(vmin, vmin+interval*10,11)
    
    print("levels",levels)
    
#    a0 = ax.tricontourf(x,y,v, levels = levels)
    xx = np.linspace(np.min(x),np.max(x), 101)
    yy = np.linspace(np.min(y), np.max(y), 101)
    xx, yy = np.meshgrid(xx,yy)
    vv = griddata((x,y), v, (xx,yy), method='linear')
    a0 = ax.contourf(xx,yy,vv, levels = levels, cmap="jet")
    a1=ax.scatter(x,y,ec="black",fc="white",marker="o")
    
    if axlimauto:
    
        ax.set_ylim(np.min(y)-(np.min(y)*.2),np.max(y)+(np.max(y)*.005))
        #ax.set_xlim(np.min(x)-1,np.max(x)+1)
        ax.set_xlim(1995.8,2016.2)
        #1995.80,2016.20
    
    else:
        ax.set_xlim(lxlim,uxlim)
        ax.set_ylim(lylim,uylim)
    
        
    
    plt.gca().invert_yaxis()


#    ax.set_aspect('equal')
    horiz = True
    if(horiz):
        cbax1 =  fig.add_axes([0.265,0.925, 0.5, 0.04])
        cbar1 = fig.colorbar(a0, cax= cbax1, orientation='horizontal')
        cbar1.ax.set_xlabel(cxlab, fontsize=14, labelpad=10)
        cbar1.ax.xaxis.set_label_position('top')
    else:
        cbax1 =  fig.add_axes([0.925,0.15, .04, 0.7])
        cbar1 = fig.colorbar(a0, cax= cbax1)
        cbar1.ax.set_ylabel(cxlab, fontsize=14, labelpad=10)


    ax.set_xlabel(r"Year", fontsize=14)
    ax.set_ylabel(r"Julian Day", fontsize=14)

    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.xaxis.set_major_locator(MultipleLocator(2))
    

    fig.savefig(data.name+"cont_plt.pdf",bbox_inches='tight')
    plt.close()
#    fig.show()

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

#test=d["mol/m2O2"]
#test=test.dropna(axis=0, how="all", thresh=None, subset=None, inplace=False)
#
#contour_plot_xyzdf(test,list(test.columns), uxlim=2016.2,lxlim=1995.8,uylim=360,lylim=0,axlimauto=False)


lev0cols=list(d.columns.levels[0])

#vmin vmax list format=210 m PN flux,210 m POC flux,410 m PN flux,410 m POC flux,BB gC/m2,mol/m2O2

uservminlist=[0.0,0.004,0.0,0.004,0.2,0.25]
uservmaxlist=[0.025,0.2,0.025,0.2,4.0,8.0]
userxaxlablist=["PN flux", "POC flux","PN flux", "POC flux", "gC/m$^{2}$","mol/m$^{2}$"]

for count,col in enumerate(lev0cols):
    print("column: ",col)
    print("min: ",uservminlist[count])
    print("max: ",uservmaxlist[count])
    
    subd=d[col]
    subd=subd.dropna(axis=0, how="all", thresh=None, subset=None, inplace=False)
    
    if col=="BB gC/m2":
        subd=subd[subd[subd.columns[-1]]>0]

    subd.name="dat"+col.replace(" ","")
    subd.name=subd.name.replace("/","")
    
    print("name: ",subd.name,"\n")
        
    contour_plot_xyzdf(subd,userxaxlablist[count],list(subd.columns),uservmin=uservminlist[count],uservmax=uservmaxlist[count],axlimauto=True,autobounds=False)
