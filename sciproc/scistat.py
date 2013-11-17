# calculate mean
from numpy import *
from dtrange import *
from scisel import *

# 1. [2. 3. 4.] 
#average(


def avgcycle(data, timeco = None, timewarp = None, cclose=False,skipnan=False):
    """ calculate averaged cycle
input:
   data: input data
   timeco: data coordinates
   timewarp: length of the cycle
   skipnan: skip nan-values
option:
   cclose: add an additional point at the end identical the beginning to close the cycle
 todo: add an option to count the amount of samples for each member of the cycle -> then crop in cosel should
 be set to True so that we still take the mean even though there is no data available.
"""
    if (timeco == None):
        timeco = arange(len(data))
    if (timewarp == None):
        timewarp = timeco[1] - timeco[0]
    iscounted = tile(False,len(data))
    tempco = dtrange(timeco[0],timeco[len(timeco)-1],timewarp)
    dataout = []
    timecoout = []
    for idata in range(len(data)):
        if (iscounted[idata] == False):
            tempco2 = tempco + (timeco[idata] - timeco[0])
    
            #coordinates of data taken into account for this timestamp
            tempcosel = cosel(timeco,tempco2)
    
            # include some option to ignore the times on which there is no data
            # include some option to ignore the nan data
    
            # if some data could not be selected, a nan will be produced
            # in cosel, crop is left to False, because we want to discover whenever data is not available
            tdatacosel = datacosel(data,cocosel = tempcosel)[0]

            # we don't want to end up with an error if None is met: we just want a 'nan' from the mean.
            for edata in tdatacosel:
                if (edata == None):
                    edata = nan
            if skipnan:
                tdatacosel = array(tdatacosel)
                tdatacosel = tdatacosel[where(isnan(tdatacosel) == False)]
            dataout.append(mean(tdatacosel))
            timecoout.append(timeco[idata])
            #dataout.append(mean(scisel(data,timeco,tempco2) )
    
            #it would be much more elegant if we could simple do: iscounted[tempcosel] = True
            #but None inside [] does strange things,
            #          (tempcosel!=None : manually crop (same as if we did cosel(...,crop=True)))
            for etempcosel in tempcosel:
                if (etempcosel != None): # None inside [] does strange things
                    iscounted[etempcosel] = True
        # add an additional point to close the cycle
    if (cclose == True):
        timecoout.append(timeco[0]+ timewarp)
        dataout.append(dataout[0])
    return(list([array(dataout),array(timecoout)]))    
    
# calculate deviation from mean
def anomaly(x):
    y = zeros(len(x))
    meanx = mean(x)
    for ix,ex in enumerate(x):
        y[ix] = ex -meanx
    return (y)



def avgglide(x,avlen):
    xout = np.zeros_like(x)
    xwork = np.zeros_like(x)
    if np.mod(avlen,2) == 0:
        xwork[-1] = np.nan
        xwork[:-1] = (x[1:] + x[:-1])/2.
    else:
        xwork = x
    lenxout = xout.shape[0]
    avlen2 = int(avlen/2.)
    xout[:avlen2] = np.nan
    xout[-avlen2:] = np.nan
    for i in range(0,avlen,1):
        xout[avlen2:(-avlen+avlen2)] = xout[avlen2:(-avlen+avlen2)] + xwork[i:(-avlen+i)]
    return xout/avlen

    # # the slow way
    # for j in range(len(x)):
    #     xout[j] = np.mean(x[max(0,(j-int(avlen/2.))):min((j+int(avlen/2.)),lenxout)],axis=0)
    # return (xout,)

