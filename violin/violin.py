
#import required pyhon libraries
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import matplotlib.markers as mmarkers
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)


def quantdf(d):

    #make a dataframe of quantile statistics. D.quantile.T will return a DF with depth columns as the rows and quartiles as the columns
    qd=d.quantile([.25, .5, .75], axis = 0).T
    
    #set the innerquartile range
    qd["IQR"]=qd[.75]-qd[.25]

    #set upperadjacent: q3+iqr*1.5
    qd["upperad"]=qd[0.75]+qd["IQR"]*1.5

    #set loweradjacent:q1-iqr*1.5
    qd["lowerad"]=qd[0.25]-qd["IQR"]*1.5

    
    return qd


def setpltdata(d):
    #transform dataframes to numeric arrays for violin plotting
    pltdatalst=[]

    for col in d.columns:
        print(col)
        pltdatalst.append(d[col][d[col].isna()==False].values)
        
    return pltdatalst
    
    
def part_set(pltdata,sp,colr,pr,alp=1):
    #customize violin plot parameters

    parts=sp.violinplot(pltdata,pr,vert=False,showmeans=False, showmedians=False,showextrema=False)
    for pc in parts["bodies"]:
        pc.set_facecolor(colr)
        pc.set_edgecolor("black")
        pc.set_alpha(alp)
    
    return parts

#import dataframe with multiindexing so can pull depth matched info per category
d=pd.read_csv("Book6.csv",header=[0,1])

#define individual frames
hnfd=d["HNF"]
bbfd=d["BB"]
chlafd=d["CHLA"]
BBtoHNFd=d["Bact/HNF"]

#stats

#quantiles...dataframe returned has depths as rows and stats as cols
HNFquantiles=quantdf(hnfd)
BBquantiles=quantdf(bbfd)
CHLAquantiles=quantdf(chlafd)
BBtoHNFquantiles=quantdf(BBtoHNFd)


#medians...returns dataframe with depth as rows and median as column
HNFmedians=hnfd.median(axis=0)
BBmedians=bbfd.median(axis=0)
CHLAmedians=chlafd.median(axis=0)
BBtoHNFmedians=BBtoHNFd.median(axis=0)


#convert data to arrays for plotting
hnfpltdata=setpltdata(hnfd)
bbpltdata=setpltdata(bbfd)
chlapltdata=setpltdata(chlafd)
BBtoHNFpltdata=setpltdata(BBtoHNFd)





#plotbody
pos=np.arange(1,len(hnfd.columns)+1)
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(12, 6), sharey=True)

plt.subplots_adjust(wspace=0.05)

parts1=part_set(hnfpltdata,ax1,"purple",pos)

ax1.yaxis.set_major_locator(MultipleLocator(1))

labs=list(hnfd.columns)
labs=[int(x) for x in labs]

ax1.plot(HNFmedians.values,pos,marker='o', mfc='white', mec=None,ms=5, zorder=3,color="dimgray",lw=0.75)
ax1.hlines(pos,HNFquantiles[0.25].values,HNFquantiles[0.75].values, color="k", linestyle="-", lw=8)
ax1.hlines(pos, HNFquantiles["lowerad"].values, HNFquantiles["upperad"].values, color='k', linestyle='-', lw=1)

ax1.xaxis.tick_top()
ax1.xaxis.set_label_position("top")
ax1.tick_params(axis="x", which="both", labeltop =True,labelbottom = False)
ax1.xaxis.set_tick_params(labelsize=12)

ax1.set_xlabel("HNF Mass $\mu$g L$^{-1}$",fontsize=14)
ax1.xaxis.set_label_coords(0.45, 1.1)

parts2=part_set(bbpltdata,ax2,"green",pos)

part_set(chlapltdata,ax2,"lime",[1],alp=0.4)

ax2.plot(BBmedians.values,pos,marker='o', mfc='white', mec=None,ms=5, zorder=3,color="dimgray",lw=0.75)
ax2.hlines(pos,BBquantiles[0.25].values,BBquantiles[0.75].values, color="k", linestyle="-", lw=8)
ax2.hlines(pos, BBquantiles["lowerad"].values, BBquantiles["upperad"].values, color='k', linestyle='-', lw=1)

ax2.xaxis.tick_top()
ax2.xaxis.set_label_position("top")
ax2.tick_params(axis="x", which="both", labeltop =True,labelbottom = False)
ax2.xaxis.set_tick_params(labelsize=12)

ax2.set_xlabel("Bacterial Mass $\mu$g L$^{-1}$",fontsize=14)
ax2.xaxis.set_label_coords(0.45, 1.1)

parts3=part_set(BBtoHNFpltdata,ax3,"gray",pos)

ax3.plot(BBtoHNFmedians.values,pos,marker='o', mfc='white', mec=None,ms=5, zorder=3,color="dimgray",lw=0.75)
ax3.hlines(pos,BBtoHNFquantiles[0.25].values,BBtoHNFquantiles[0.75].values, color="k", linestyle="-", lw=9)
ax3.hlines(pos, BBtoHNFquantiles["lowerad"].values, BBtoHNFquantiles["upperad"].values, color='k', linestyle='-', lw=1)

ax3.xaxis.tick_top()
ax3.xaxis.set_label_position("top")
ax3.tick_params(axis="x", which="both", labeltop =True,labelbottom = False)
ax3.xaxis.set_tick_params(labelsize=12)

ax3.set_xlabel("Prok/HNF gC gC$^{-1}$",fontsize=14)
ax3.xaxis.set_label_coords(0.45, 1.1)

#need to set ytick positions before labels or will label incorrectly
ax1.set_yticks(pos)
ax1.set_yticklabels(labs,fontsize=12)
ax1.set_ylabel("Depth (m)", fontsize=14)
ax1.yaxis.set_tick_params(labelsize=12)


plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("violinplotmanusc.pdf")
plt.close()

 
