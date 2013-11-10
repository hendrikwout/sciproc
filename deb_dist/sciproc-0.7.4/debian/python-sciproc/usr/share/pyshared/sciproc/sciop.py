from numpy import zeros,nan

def tsfill(valin,dtin,dtout):
    # purpose: regrid timeseries... fill missing timesteps in a timeseries with nan values, or leave out unwanted timesteps
    # valin: time series values
    # dtin: time steps of the timeseries
    # dtout: desired output timesteps

    valout = zeros(len(dtout))*nan
    lendtin = len(dtin)
    idtin = 0
    for idt,edt in enumerate(dtout):
        while((dtin[idtin] < edt) & (idtin < (len(dtin)-1))):
            idtin = idtin + 1
    
        if edt == dtin[idtin]:
            valout[idt] = valin[idtin]
    return valout

def mergedata(x):
    x1 = x[0]
    x2 = x[1]
    xout = zeros((len(x1)+len(x2))) 
    for ix1,ex1 in enumerate(x1):
        xout[ix1] = ex1
    for ix2,ex2 in enumerate(x2):
        xout[ix2+len(x1)] = ex2

    return xout

