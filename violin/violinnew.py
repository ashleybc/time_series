
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
    outup = qd[0.75]+qd["IQR"]*1.5
    up = d.max(axis=0)
    qd["upperad"]= (outup>up).astype(int)*up + (outup<up).astype(int)*outup


    #set loweradjacent:q1-iqr*1.5
    outdown = qd[0.25]-qd["IQR"]*1.5
    down = d.min(axis=0)

    qd["lowerad"]=(outdown<down).astype(int)*down + (outdown>down).astype(int)*outdown

    
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

def run_plot():
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
    HNFmedians=HNFquantiles[0.5]
    BBmedians=BBquantiles[0.5]
    CHLAmedians=CHLAquantiles[0.5]
    BBtoHNFmedians=BBtoHNFquantiles[0.5]


    #convert data to arrays for plotting
    hnfpltdata=setpltdata(hnfd)
    bbpltdata=setpltdata(bbfd)
    chlapltdata=setpltdata(chlafd)
    BBtoHNFpltdata=setpltdata(BBtoHNFd)





    #plotbody
    
    #label indices and labs as requested
    fullpos=np.arange(15)
    fulllabs=[0,"",100,"",200,"",300,"",400,"",500,"",600,"",700]
    
    samplepos=[1,4,8,13]
    
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(12, 6), sharey=True)

    plt.subplots_adjust(wspace=0.05)

    parts1=part_set(hnfpltdata,ax1,"purple",samplepos)

    ax1.yaxis.set_major_locator(MultipleLocator(1))

    labs=list(hnfd.columns)
    labs=[int(x) for x in labs]

    ax1.plot(HNFmedians.values,samplepos,marker='o', mfc='white', mec=None,ms=5, zorder=3,color="dimgray",lw=0.75)
    ax1.hlines(samplepos,HNFquantiles[0.25].values,HNFquantiles[0.75].values, color="k", linestyle="-", lw=4)
    ax1.hlines(samplepos, HNFquantiles["lowerad"].values, HNFquantiles["upperad"].values, color='k', linestyle='-', lw=1)

    ax1.xaxis.tick_top()
    ax1.xaxis.set_label_position("top")
    ax1.tick_params(axis="x", which="both", labeltop =True,labelbottom = False)
    ax1.xaxis.set_tick_params(labelsize=12)

    ax1.set_xlabel("HNF Mass ($\mu$g C L$^{-1}$)",fontsize=14)
    ax1.xaxis.set_label_coords(0.45, 1.1)

    parts2=part_set(bbpltdata,ax2,"green",samplepos)

    part_set(chlapltdata,ax2,"lime",[0.7],alp=0.4)
    
    ax2.plot(BBmedians.values,samplepos,marker='o', mfc='white', mec=None,ms=5, zorder=3,color="dimgray",lw=0.75)
    ax2.hlines(samplepos,BBquantiles[0.25].values,BBquantiles[0.75].values, color="k", linestyle="-", lw=4)
    ax2.hlines(samplepos, BBquantiles["lowerad"].values, BBquantiles["upperad"].values, color='k', linestyle='-', lw=1)

    ax2.plot(CHLAmedians.values,[0.7],marker='o', mfc='white', mec=None,ms=5, zorder=3,color="dimgray",lw=0.75)
    ax2.hlines([0.7],CHLAquantiles[0.25].values,CHLAquantiles[0.75].values, color="k", linestyle="-", lw=4)
    ax2.hlines([0.7], CHLAquantiles["lowerad"].values, CHLAquantiles["upperad"].values, color='k', linestyle='-', lw=1)

    ax2.xaxis.tick_top()
    ax2.xaxis.set_label_position("top")
    ax2.tick_params(axis="x", which="both", labeltop =True,labelbottom = False)
    ax2.xaxis.set_tick_params(labelsize=12)
    ax2.set_xscale("log")

    ax2.set_xlabel("Bacterial Mass ($\mu$g C L$^{-1}$)",fontsize=14)
    ax2.xaxis.set_label_coords(0.45, 1.1)

    parts3=part_set(BBtoHNFpltdata,ax3,"gray",samplepos)

    ax3.plot(BBtoHNFmedians.values,samplepos,marker='o', mfc='white', mec=None,ms=5, zorder=3,color="dimgray",lw=0.75)
    ax3.hlines(samplepos,BBtoHNFquantiles[0.25].values,BBtoHNFquantiles[0.75].values, color="k", linestyle="-", lw=5)
    ax3.hlines(samplepos, BBtoHNFquantiles["lowerad"].values, BBtoHNFquantiles["upperad"].values, color='k', linestyle='-', lw=1)

    ax3.xaxis.tick_top()
    ax3.xaxis.set_label_position("top")
    ax3.tick_params(axis="x", which="both", labeltop =True,labelbottom = False)
    ax3.xaxis.set_tick_params(labelsize=12)
    ax3.set_xscale("log")

    ax3.set_xlabel("Prok/HNF (gC gC$^{-1}$)",fontsize=14)
    ax3.xaxis.set_label_coords(0.45, 1.1)

    #need to set ytick positions before labels or will label incorrectly
    ax1.set_yticks(fullpos)
    ax1.set_yticklabels(fulllabs,fontsize=12)
    ax1.set_ylabel("Depth (m)", fontsize=14)
    ax1.yaxis.set_tick_params(labelsize=12)
    ax1.set_xscale("log")


    plt.gca().invert_yaxis()
    plt.tight_layout()

    plt.savefig("violinplotmanusc2.pdf")
    plt.close()

     
