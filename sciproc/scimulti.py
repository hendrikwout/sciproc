from numpy import *
import inspect
from operator import itemgetter

def procdf(function,allvars,procaxis,dimidx=0):
    iterate = False
    if (dimidx <= len(shape(allvars[0]))):
        if (procaxis[dimidx] == False):
            iterate = True

    if iterate:
        #procaxis[dimidx] == False  !!!
        #so  the first item shape of each variable allvars is allvars[0].shape[0] 
        dataout = []
        for axidx in range(allvars[0].shape[0]):
            allvarsin = []
            for evar in allvars:
                allvarsin.append(evar[axidx])
            dtotmp, outcoords = procdf(function,allvarsin,procaxis,dimidx=dimidx+1)
            dataout.append(dtotmp)
    else:
        allvarstemp = []
        for evar in allvars:
            # workaround for memory leak when just running  'dataouttemp = function(allvars)' in case of netcdf file references
            if type(evar) != ndarray:
                allvarstemp.append(evar)
            else:
                allvarstemp.append(array(evar))
            # end workaround

        # # if only one variable, then don't pass it as a list
        # if len(allvarstemp == 1):
        #     allvarstemp = allvarstemp[0]

        dataouttemp = function(allvarstemp)

        if (type(dataouttemp).__name__ == 'list'):
            dataout = dataouttemp[0]
            outcoords = dataouttemp[1]
            # vardimsout...
        else:
            dataout = dataouttemp
            shapeout = shape(dataout)
            # print 'shapeout', shapeout
            outcoords = []
            for eshape in shapeout:
                # <False> means that the dimension given by the output of the 
                # function is not specified. Afterwards, it should be checked 
                # whether this dimension is the same as the input dimension
                # If so, this should become None
                outcoords.append(False)
            # print 'outcoords', outcoords
    return dataout, outcoords

def multifunc(function,allvars,procaxis,vardims):
    """
    function: the function that has to be applied on the variable
    procaxis:
          Description: indicates for each variable (ranked from 0 to ... ) that 
                       have to be processed 
          Dimensions: the amount of variables occuring in any variable: 
          Example: (False, True, True, False, ...).
        
    vardims: 
          Description: list of 'pointers' to dimensions for each variable array 
          Dimensions: (amount of variables, dimensions of that variable) ,
                          so the second dimension is not fixed for each row
          Example: [[3,     1   , 2   , 4    , ...],
                    [2,     3   , 4   , 6    , ...],
                    ....                     
                   ]
    """
    # add dimensions to variables (i.e. expand array) 
    #in case they are missing (tbi: make this unnecessary)
    dimcount = len(procaxis) 
    for ivar,evar in enumerate(allvars):
        for idim in reversed(range(len(vardims[ivar]))): #reversed(range(dimcount)):
            if vardims[ivar][idim] == None: # vardims[ivar]:
                # if a function has to be applied on that dimension, 
                #only add an 'axis' for that dimension
                if procaxis[ivar] == True:
                    # print 1,ivar,  allvars[ivar].shape
                    allvars[ivar] = allvars[ivar][newaxis,:]
                    # print ivar,  allvars[ivar].shape
                # else: length of dimension is 
                # considered the same for all variables! 
                # so multiple copies are made from the dimension 
                # of an arbitrary other variable 
                # (we just take the first that has this variable)
                else:
                    ldone = False
                    for ivar2,evar2 in enumerate(allvars):
                        if idim in vardims[ivar2]:
                            if ldone == False:
                                # print 2,ivar, allvars[ivar].shape
                                # dimension length: evar2.shape[vardims[ivar2].index(idim) 
                                allvars[ivar] = repeat(allvars[ivar][newaxis,:],evar2.shape[vardims[ivar2].index(idim)],0)
                                # print ivar,  allvars[ivar].shape
                            ldone = True
                vardims[ivar][idim] = -1
                for idim2 in range(len(vardims[ivar])): #reversed(range(dimcount)):
                    if vardims[ivar][idim2] != None:
                        vardims[ivar][idim2] = vardims[ivar][idim2] + 1

                    
    # put dimensions of all variables arrays in the same order 
    # as the standard order (which is implicitely given by vardims)

    # for ivar,evar in enumerate(allvars):
    #     print evar.shape, vardims[ivar]
    for ivar,evar in enumerate(allvars):
        allvars[ivar] = transpose(evar,vardims[ivar])
    # for ivar,evar in enumerate(allvars):
    #     print 'shape before transposition:',evar.shape, vardims[ivar]
    #     print 'procaxis:', procaxis


    # if a certain dimension has
    for idim in range(len(procaxis)):
        # get maximum dimension
        maxdim = 0
        for ivar,evar in enumerate(allvars):
            maxdim = max(shape(evar)[idim],maxdim)
        for ivar,evar in enumerate(allvars):
            if ((shape(evar)[idim] == 1) & (maxdim > 1)):
                # print maxdim,idim
                allvars[ivar] = repeat(allvars[ivar],maxdim,idim)
                # tmpdim = range(len(procaxis))
                # tmpdim[idim] = 0
                # print 'tmpdim 1', tmpdim
                # for idim2 in range(idim):
                #     tmpdim[idim2] = tmpdim[idim2] + 1
                # print 'tmpdim', tmpdim
                # allvars[ivar] = transpose(allvars[ivar],tmpdim)
                # allvars[ivar] = repeat(allvars[ivar][:],maxdim,0)
                # inv = range(len(tmpdim))
                # for idim2, edim2 in enumerate(tmpdim):
                #     inv[edim2] = idim2
                # allvars[ivar] = transpose(allvars[ivar],inv)

    # for ivar,evar in enumerate(allvars):
    #     print 'shape after expansion:',evar.shape, vardims[ivar]
    #     print 'procaxis:', procaxis

    
    # now transpose all matrices in a similar way in such a way that the dimensions 
    # to be processed are at the end
    
    refsorted = sorted(zip(procaxis,range(dimcount)), key=itemgetter(0,1)) 
    trns = [] # the transpose indices
    trnsprocaxis = [] # procaxis after transpose
    #print('data processing started')
    for irefsorted,erefsorted in enumerate(refsorted):
        trns.append(erefsorted[1])
        trnsprocaxis.append(erefsorted[0])
    for ivar,evar in enumerate(allvars):
        allvars[ivar] = transpose(evar,trns)
    # ...

    # for ivar,evar in enumerate(allvars):
    #     print 'shape after transposition:',evar.shape

    dataouttrns,outcoordstrnstmp = procdf(function,allvars,trnsprocaxis)

    # print 'dataouttrns',shape(dataouttrns)


    #print('shapedataouttrns', shape(dataouttrns), outcoordstrnstmp)
    # 
    # # in case the function introduces extra dimensions: Add these extra dimensions in front of the
    # # processed dimensions (we accually put them at the end here but this doens't matter

    # amount of processed input dimensions
    procdim = len(where(array(trnsprocaxis) == True)[0])
    # amount of non-processed input dimensions
    nonprocdim = len(where(array(trnsprocaxis) == False)[0])
    # amount of extra dimensions introduced by the function
    extradims = len(shape(dataouttrns)) - len(trnsprocaxis)
    # print('extradims',extradims)
    trnsoutaxis = list(trnsprocaxis)


    # from procdf, the extra dimension is assumed in front of the processed input dimensions 
    # (and after the previous extra dimensions). It is put in front of all output dimensions

    # We put each extra dimension in front of all the others for the output
    # so we raise each reference by the number of extra dimensions
    for i in range(extradims):
        for itrns, etrns in enumerate(trns):
            trns[itrns] = trns[itrns]+1
    for i in range(extradims):
        trnsoutaxis.append(True)
        # from procdf, the extra dimension is assumed in front of the processed input dimensions 
        # (and after the previous extra dimensions). It is put in front of all output dimensions
        trns.insert(nonprocdim+i,i)

    
    # Reorganize the output coordinate list, so that they 
    # are aligned with the standard dimension numbering. So add 'nones' where needed
    outcoordstrns = []
    iocttmp = 0
    for i,etrnsoutaxis in enumerate(trnsoutaxis):
        if etrnsoutaxis: # if the function is applied along the current dimension
            outcoordstrns.append(outcoordstrnstmp[iocttmp])
            iocttmp = iocttmp + 1
        else:
            # <None> means that the current dimension corresponds to the input data 
            # dimensions (is trivially none when this dimension isn't processed)
            outcoordstrns.append(None)
    
    #print('data processing ended')
    
    # build the 'inverse permutation operator'
    inv = range(len(trns))
    for itrns, etrns in enumerate(trns):
        inv[etrns] = itrns
    
    # inverse permutation of the output data
    # print dataout.shape, inv
    dataout = transpose(dataouttrns,inv)
    
    outcoords = []
    # inverse permuation of the output coordinates
    for iinv,einv in enumerate(inv):
        outcoords.append(outcoordstrns[einv])
    
    return dataout,outcoords

