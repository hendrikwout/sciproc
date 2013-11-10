#!/usr/bin/python
# Filename: scisel.py

from numpy import *
from dtrange import *

# aim:
# get the indices of coords which occur in outcoords
# notes:
# - ordered data is needed for both coords and outcoords.
# - we expect that the data at the asked sample time (outcoords) exists in the original sample (coords). If not, a nan will be produced.

# crop = option whether the unavailable ones should be filled out with nan, or whether the unavailable ones
# should be ignored. In the latter, the output array will not have the same size as outcoords!


def cosel(coords = None, outcoords = None, crop=False):
    steps = len(outcoords)
    selout = repeat(None,steps)
    idx = 0
    outidx = 0
    for datetime in coords:
        if ((datetime >= outcoords[0]) & (datetime <= outcoords[steps - 1]) & \
            (outidx < steps)):
            if ((datetime >= outcoords[outidx])):
                while ((outidx < steps) & (outcoords[outidx] < datetime)):
                    outidx = outidx + 1
                if (datetime == outcoords[outidx]):
                    #outdata[outidx] = indata[idx]
                    selout[outidx] = idx
                outidx = outidx + 1
        idx = idx + 1
    if (crop == True):
        selout = selout[selout !=None]
    return selout

# someone may want to do this (if it's possible) instead of interpolation
def datacosel(indata, cocosel = None, coords = None, outcoords = None, \
              start= None,end= None,step = None,  \
              outstart = None, outend = None, outstep = None, \
              crop = False):
    ''' indata: input data
    '''
        
    if (cocosel == None):
        # if coordinates not given, make it from the start, end, step arguments
        if (coords == None):
            coords = dtrange(start, end, step)
        if (outcoords == None):
            if ((outstart != None) & (outend != None) ):
                if (outstep != None):
                    outcoords = dtrange(outstart, outend, outstep)
                else: 
                    outcoords = coords[(coords >= outstart) & (coords <=outend)]
            else:
                outcoords = coords
        cocosel = cosel(coords = coords, outcoords = outcoords)
    else:
        if (outcoords == None):
            outcoords = cocosel

    # remove NA (None) values if specified
    # would be more elegant if we could simply do cosel = cosel[cosel!=None], but None inside [] does strange things
    if (crop == True):
        tempcosel = []
        tempoutcoords = []
        for icosel,ecosel in enumerate(cosel):
            if (ecosel != None):
                tempcosel.append(ecosel)
                tempoutcoords.append(outcoords[icosel])
        cocosel = array(tempcosel)
        outcoords = array(tempoutcoords)

    dataout = tile(nan,len(cocosel))
    #dataout = indata[cosel[cosel!=None]]
    #dataout[cosel==None] = nan
    #dataout[cosel!=None] = indata[cosel[cosel!=None]]
    for iel, el in enumerate(cocosel):
        if (el != None):
            dataout[iel] = indata[el]
        else:
            dataout[iel] = None
    return(list([array(dataout), array(outcoords)]))


# # aim: build an array (boolean) selection from indices of any dimension
# # the coordinates from which elements of the multi-dim matrix are selected
# #      wrapper function for a more advanced array selection
# # SHAPE: shape of the multidim-matrix
# # SEL: list indices of each dimension of a matrix we want to selected. e.g. with SEL=[[0,1,2],[0],[0]],
# # we select a 3x1x1 matrix 
# # usage: datasel = data[arraysel([[0,1,2],[0,2,4],[22,23]],SHAPE=shape(data))
# def arraysel(SEL,SHAPE = None):
#     if (SHAPE == None):
#         SHAPE = []
#         for eSEL in SEL:
#             SHAPE.append(max(eSEL) + 1 )
#     lfirst = True
#     #ntruefalse: the matrix we want to construct, which can be used to select the data.
#     ntruefalse = True
#     for axidx,dimsize in reversed(list(enumerate(SHAPE))):
#         # build a boolean array for current dimension
#         curdimarray = (zeros(dimsize) == 1)
#         for element in SEL[axidx]: 
#             if (element != None): # workaround: data[None] selects all data
#                 curdimarray[element] = True 
#         otruefalse = ntruefalse
#         # for the first dimension, we initialize ntruefalse(shape)
#         if (lfirst):
#             ntruefalseshape = dimsize
#             lfirst = False
#         else:
#             ntruefalseshape = list(ntruefalse.shape)
#             ntruefalseshape.insert(0,dimsize)
#         ntruefalse = (zeros(ntruefalseshape) == 1)
#         for ielement,element in enumerate(curdimarray):
#             if (element == True):
#                 ntruefalse[ielement] = otruefalse
#             else:
#                 ntruefalse[ielement] = False
#     return ntruefalse
 
