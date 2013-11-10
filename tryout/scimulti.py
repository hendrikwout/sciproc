
# aim: 
# scifunc: apply a certain function serveral times on a multidimensional matrix; calculate a certain
# function along a specified axis
# reddim: reduce the dimension of a multidimensional matrix


# todo for scifunc: 
# pass multiple variables for one function
# make an array attribute as a substitute for arraysel
# currently, it is expected that the function conserves the # of dimensions. If not, there will be problems.
#     so possibility to decrease dimension of matrix is still needed in which we may want to throw away a dimension automatically (like
#     for making averages by summing over an index for a certain dimension) 
#     we should detect automatically when it has to be removed, e.g. when the function reduces the # of dimensions of a matrix
#     
# coordinate build in as a array attributeis: 
#     array.arraysel(SEL) 
#     arraycrop (of zoiets)
# 

from numpy import *
from sciproc import arraysel
from operator import itemgetter

# apply a function for each element along various axis
# data: matrix to be processed
# axisref: a list of boolean which indicates along which axis the function has to be applied
#       if false: the function is applied seperately for each element along the current axis
#       if true: all elements of the current axis are used as input for the function
# example, if data is a 4x3x2 matrix and SEL=[False,True,False], the function deffunc will be applied
# for each of the 4 elements along the first axis and for each of he 2 elements along the third axis.
# So the function will be applied 4x2 times. Each time, the 3 elements along second axis are
# all passed to the function. The size of the output matrix depends on the function.
def multifunc(data,axisref,deffunc):
    # probably, we don't need this anymore
    #dataout = zeros(sizeout(data,axisref,deffunc)[0])

    reference = zip(axisref,range(len(shape(data))))
    refsorted = sorted(reference, key=itemgetter(0,1))
    
    trns = []
    trnsaxisref = []
    for irefsorted,erefsorted in enumerate(refsorted):
        trns.append(erefsorted[1]) 
        trnsaxisref.append(erefsorted[0])
    datatrns = transpose(data,trns)
    #dataouttrns = transpose(dataout,trns)
    print('data processing started')
    # dataouttrns = scandata(0,datatrns,array([]),trnsaxisref,deffunc)
    # 
    # create an array of correct dimension first to get performance increase
    shapeout, outcoords, typeout = getshapeout(datatrns,trnsaxisref,deffunc)
    dataouttrns = zeros(shapeout)
    # workaround to be able to work with datetimes
    if typeout == 'datetime':
        dataouttrns = [None]
        for eshapeout in shapeout:
            dataouttrns = dataouttrns*eshapeout
        dataouttrns = array([dataouttrns])
        dataouttrns.shape = shapeout
    dataouttrns = scandata(datatrns,trnsaxisref,deffunc,dataouttrns)

    # # old version
    # dataouttrns = scandata(0,datatrns,trnsaxisref,deffunc)

    print('data processing ended')
    
    #inverse permutation
    inv = range(len(trns))
    for itrns,etrns in enumerate(trns):
        inv[etrns] = itrns
    dataout = transpose(dataouttrns,inv)

    return dataout

# get data shape
def getshapeout(datain,axisref,deffunc,dimidx=0):
    iterate = False
    if (dimidx <= (len(axisref))):
        if (axisref[dimidx] == False):
            iterate = True
    if iterate == True:
        axidx = 0
        shapeout,outcoords, typeout = getshapeout(datain[0],axisref,deffunc,dimidx = dimidx+1)
        shapeout.insert(0,len(datain))
        dataout = None
    else:
        dataout = deffunc(datain)
        if ((type(dataout).__name__ == 'list') or (type(dataout).__name__ == 'tuple')):
            if (type(dataout[1]).__name__ == 'list' ): # multiple coordinate set stored as a list
                outcoords = dataout[1] 
            else:
                if (dataout[1] != None):
                    outcoords = list(dataout[1])
                else:
                    outcoords = None
            dataout = dataout[0]
        else:
            outcoords = None # function doesn't have output coordinates available
        shapeout = list(shape(dataout))
        typeout = type(dataout).__name__

    return shapeout, outcoords, typeout

def scandata(datain,axisref,deffunc,dataout,dimidx=0):
    iterate = False
    if (dimidx <= (len(axisref))):
        if (axisref[dimidx] == False):
            iterate = True

    if iterate:
        # get shape of nested dataout
        for axidx in range(len(datain)):
            dataout[axidx] = scandata(datain[axidx],axisref,deffunc,dataout[axidx],dimidx = dimidx+1)
    else:
        dataouttemp= deffunc(datain)
        if ((type(dataouttemp).__name__ == 'list') or (type(dataouttemp).__name__ == 'tuple')):
            dataout = dataouttemp[0]
        else:
            dataout = dataouttemp
    return dataout


#for eshape in shape(datain):


# old version
# def scandata(dimidx,datain,axisref,deffunc):
#     if ((axisref[dimidx] == False) & (dimidx <= (len(shape(datain)) ))):
#         # get shape of nested dataout
#         dataout = []
#         for axidx in range(datain.shape[0]):
#             dataout.append(scandata(dimidx+1,datain[axidx],axisref,deffunc))
#     else:
#         dataout= deffunc(datain[:])
#         if ((type(dataout).__name__ == 'list') or (type(dataout).__name__ == 'tuple')):
#             dataout = dataout[0]
#     return dataout


# reduce dimension of a multidimensional matrix
# input: 
#   data: matrix
#   indices: th dimension that has to be left away
#   el: which element has to be taken for the to be removed dimension (default: first element)
def reddim(data,indices,el = 0):
    #el = repeat(0,len(indices))
    for dim in range(len(shape(data))):
        if (dim in indices):
            SEL[dim] = el
        else:
            SEL[dim] = range(size(data,axis=dim))
    return data[arraysel(SEL,shape(data))]

# also called by multifunc, but may be used for other things also. 
# ----Isn't this just doing what's done at the inner scandata loop? maybe it has to be merged with that to have one
# single logic...---
# probably some room for simplification!
def sizeout(data,axisref,deffunc):
    SEL = list(repeat(None,len(shape(data))))
    sizeout = list(repeat(None,len(shape(data))))
    #before calculating the dataout matrix, its dimension has to be acquired
    for dim in range(len(shape(data))):
        if (axisref[dim] == True):
            SEL[dim] = range(size(data,axis=dim))
        else:
            SEL[dim] = [0] 
            sizeout[dim] = size(data,axis=dim)

    # the first item in this list contains dummy data which will not be used; 
    # the other items potentially contain the output coordinates if available


    dtempin = data[arraysel(SEL,data.shape)]
    SHAPE = []
    for iSHAPE in range(len(SEL)):
        if (axisref[iSHAPE] == True):  
            SHAPE.append(len(SEL[iSHAPE]))
    dtempin.shape = SHAPE

    dummydataout = deffunc(dtempin)

    dimout = 0
    for dim in range(len(shape(data))):
        if (axisref[dim] == True):
            # if list, get the output data size which is given by the first item in the list
            # if not list (no output coordinates given), just get the size of the data
            if ((type(dummydataout).__name__ == 'list') or (type(dummydataout).__name__ == 'tuple')):
                sizeout[dim] = size(dummydataout[0],axis=dimout)
            else:
                sizeout[dim] = size(dummydataout,axis=dimout)
            dimout = dimout + 1

    # shapedataout = sizeout(ncin.variables[evariable][:],\
    #                        axisref, \
    #                        lambda data: deffunc(data) )
    # get the output coordinates of the processed dimensions and save it as a seperate list
    if ((type(dummydataout).__name__ == 'list') or (type(dummydataout).__name__ == 'tuple')):
        if (type(dummydataout[1]).__name__ == 'list' ): # multiple coordinate set stored as a list
            outcoords = dummydataout[1] 
        else:
            if (dummydataout[1] != None):
                outcoords = list(dummydataout[1])
            else:
                outcoords = None
    else:
        outcoords = None # function doesn't have output coordinates available

    # sizeout: size of the output data if one would apply multifunc
    # outcoords: list of coordinate sets of each dimension where axisref == True
    return sizeout, outcoords



# # reduce multiple dimensions at ones
# # indices: list of indices
# # data: the multi-dim matrix we want to reduce
# # todo: rewrite it to make it more efficient
# def reddimmulti(data,indices):
#     dataout = data
#     for index in range(len(indices)):
#         dataout = reddim(dataout,indices[index])
#         #we have to correct the indices as dimension of the output matrix is reduced already
#         for index2 in range(index,len(indices)):
#             indices[index2] = indices[index2] - 1
#     return dataout

