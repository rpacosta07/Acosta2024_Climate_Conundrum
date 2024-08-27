import numpy as np
import math

def BiasAnalysis(Prectvar,MIOMAP,MIOLat,MIOLon,MIOMAPmin,MIOMAPmax): 
    VAR = Prectvar
    MIOMAPvar = MIOMAP
    MIOLatvar = MIOLat
    MIOLonvar = MIOLon
    MIOMAPminvar = MIOMAPmin
    MIOMAPmaxvar = MIOMAPmax

    modelmaxes=[]
    modelmins=[]

    modellons=VAR.lon #assumes 0-360
    modellats=VAR.lat

    originlat=MIOLatvar #(data) lats
    originlon=MIOLonvar  #(data) lons

    paleolats=[MIOMAPvar,MIOLatvar]
    np.shape(paleolats)
    paleolons=[MIOMAPvar,MIOLonvar]
    np.shape(paleolons)


    if modellats.max() >90: #automatically convert lats to -90,90
        modellats[:]-=90
    # if originlat.max() >90:
    #     originlat[:]-=90
    
    def find_nearest(modelcoords, datacoord): #return index of model coord nearest to data coord (either lat or lon, not both at once)
        array = np.asarray(modelcoords)
        indx = (np.abs(modelcoords - datacoord)).argmin()
        return indx

    for ex in range(len(VAR)): #all experiments
        modelmaxes.append([])
        modelmins.append([])
        for i in range(len(MIOLatvar)): #for each proxy datum
            tmpmax=[]
            tmpmin=[]
            
            ref_lat=find_nearest(modellats,MIOLatvar[i])
            ref_lon=find_nearest(modellons,MIOLonvar[i])
            if ref_lon==359: 

                 #for each model, find the max/min value in the 9 adjacent model grid cells, considering both early/late data locations
                    tmpmax.append( np.nanmax( [ VAR[ex,ref_lat+1,ref_lon-1], \
                                    VAR[ex,ref_lat+1,ref_lon], \
                                    VAR[ex,ref_lat+1,0], \
                                    VAR[ex,ref_lat,ref_lon-1], \
                                    VAR[ex,ref_lat,ref_lon], \
                                    VAR[ex,ref_lat,0], \
                                    VAR[ex,ref_lat-1,ref_lon-1], \
                                    VAR[ex,ref_lat-1,ref_lon], \
                                    VAR[ex,ref_lat-1,0]  ] ) )
                    tmpmin.append( np.nanmin( [ VAR[ex,ref_lat+1,ref_lon-1], \
                                    VAR[ex,ref_lat+1,ref_lon], \
                                    VAR[ex,ref_lat+1,0], \
                                    VAR[ex,ref_lat,ref_lon-1], \
                                    VAR[ex,ref_lat,ref_lon], \
                                    VAR[ex,ref_lat,0], \
                                    VAR[ex,ref_lat-1,ref_lon-1], \
                                    VAR[ex,ref_lat-1,ref_lon], \
                                    VAR[ex,ref_lat-1,0] ] ) )
            else:
                    tmpmax.append( np.nanmax( [ VAR[ex,ref_lat+1,ref_lon-1], \
                                    VAR[ex,ref_lat+1,ref_lon], \
                                    VAR[ex,ref_lat+1,ref_lon+1], \
                                    VAR[ex,ref_lat,ref_lon-1], \
                                    VAR[ex,ref_lat,ref_lon], \
                                    VAR[ex,ref_lat,ref_lon+1], \
                                    VAR[ex,ref_lat-1,ref_lon-1], \
                                    VAR[ex,ref_lat-1,ref_lon], \
                                    VAR[ex,ref_lat-1,ref_lon+1] ] ) )
                    tmpmin.append( np.nanmin( [ VAR[ex,ref_lat+1,ref_lon-1], \
                                    VAR[ex,ref_lat+1,ref_lon], \
                                    VAR[ex,ref_lat+1,ref_lon+1], \
                                    VAR[ex,ref_lat,ref_lon-1], \
                                    VAR[ex,ref_lat,ref_lon], \
                                    VAR[ex,ref_lat,ref_lon+1], \
                                    VAR[ex,ref_lat-1,ref_lon-1], \
                                    VAR[ex,ref_lat-1,ref_lon], \
                                    VAR[ex,ref_lat-1,ref_lon+1] ] ) )
            modelmaxes[ex].append(max(tmpmax))
            modelmins[ex].append(min(tmpmin))
    #np.shape(modelmaxes)
    np.shape(modelmins)

    # method part 2: find biases based on overlapping uncertainty bounds

    bias=[]

    for ex in range(len(VAR)):
    
        bias.append([])
    
        for i in range(len(MIOMAPvar)):
            diff1 = MIOMAPminvar[i]-modelmaxes[ex][i]
        
            diff2 = modelmins[ex][i]-MIOMAPmaxvar[i]
        
            if diff1>0:
                prbias=-diff1
            elif diff2>0:
                prbias=diff2
            elif np.isnan(diff2):
                prbias=np.nan
            else:
                prbias=0
            bias[ex].append(prbias)
        
    biasmean=np.nanmean(bias,axis=1)
    #print(biasmean)
    biasrmse=np.sqrt(np.nanmean(np.square(bias),axis=1))
    print(biasrmse) 
    #print(bias)
    #np.shape(bias)
    
    return(biasrmse)
