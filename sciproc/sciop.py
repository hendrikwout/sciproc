from numpy import zeros,nan
import numpy as np
import math as mt

# def getidx(idxs,numfac):

def steinalp(f,numfac):
    '''  factor seperation procedure following Stein and Alpert (1993), Factor
    Seperation in Numerical Simulations (JAS). Example will follow.

    f: data set with factors
    numfac: amount of factors investigated

    f
    
    '''

    #a few preparations
    #print f
    frav = np.array(f)
    fshp = frav.shape #np.shape(frav)[:numfac]
    nmshape = 2**numfac
    lshf = numfac
    print 'frav.shape',frav.shape
    
    ishape = 0
    while nmshape > 1:
        nmshape = nmshape / frav.shape[ishape]
        ishape = ishape + 1
    newshape = [nmshape] 
    if len(frav.shape) > ishape:
        newshape = newshape +list(frav.shape[ishape:])

    fsep = np.zeros_like(frav)
    
    #print (frav)
    # here we go...
    fsep[0] = np.array(frav[0])
    for posfsep in range(1,len(fsep)):
    
        fsep[posfsep] = np.array(frav[posfsep])
        idxs = []
        posfseptmp = int(posfsep)
    
        # we discover the indices from which we take combinations
        for ishp in reversed(range(lshf)):
            if np.mod(posfseptmp,2) == 1:
                idxs.append(ishp)
                posfseptmp = (posfseptmp - 1)
            posfseptmp = posfseptmp/2
    
        idxs.sort()
    
        l = len(idxs)
    
        # a loop over the different kind of combinations :
        # 0 1 2 3...m -- ... l
        # l l l l   ...      l
#        print 'idxs', idxs
        for m in range(1,l):
            # determine the number of possible combinations of the current kind
            numcomb = mt.factorial(l)/mt.factorial(m)/mt.factorial(l-m)
    
            # print 'm l',m,l
            # print 'posfsep', posfsep
            # print 'numcombb',numcomb
    
            # now we make the combinations of the indices
            pos = range(m) # start position (e.g. (1,2,3,4)
            if pos != []:
                for inumcomb in range(numcomb):
    #                print('pos',pos)
                
                    curidxs = []
                    for ipos,epos in enumerate(pos):
                        # the current matrix index
                        curidxs.append(idxs[epos])
    
   #                  print (curidxs,'curidxs')
                    posf = 0
                    for i in range(lshf):
                        if i in curidxs:
   #                         print 'i curidxs',i,curidxs,(lshf-i-1)
                            posf = posf + 2**(lshf-i-1)
                    
   #                 print ('posf',posf,np.float((-1)**(l-m) *frav[posf]))
                    fsep[posfsep] = fsep[posfsep] +  (-1)**(l-m) * frav[posf]
   #                 print('posone',pos)
                    pos[-1] = pos[-1] +1 
                    for ipos,epos in reversed(list(enumerate((pos)))):
   #                     print ipos,epos,l
                        if (ipos >= 1) and (epos == l):
                            pos[ipos - 1] = pos[ipos -1] + 1
                            pos[ipos] = 0 #pos[ipos] + 1
#                    print('postwo',pos)
        fsep[posfsep] = fsep[posfsep] + (-1)**l * frav[0]
#        print ('lposf',0,np.float(frav[0]))
        #print 'posfsep fsep',posfsep,fsep[posfsep]
        
    fsep.shape = fshp
    if type(f).__name__ == 'list':
        # print 'fsep.shape',fsep.shape
        # print 'list'
        return list(fsep)
    elif type(f).__name__ == 'tuple':
        # print 'fsep.shape',fsep.shape
        # print 'tuple'
        return tuple(fsep)
    else:
        # just array?
        return fsep

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

