
# testing the library nestings on a 3D-netcdf file


from Scientific.IO import NetCDF
from numpy import *
from meteo import *
from sciproc import *
from ncdfextra import *

# todo:
# gemiddelde maken over de 5 dagen
# lkj....lkjd...

from matplotlib import rc
from matplotlib.pyplot import *
from matplotlib.dates import *
from datetime import *
from pytz import *
from numpy import *


ncmean = NetCDF.NetCDFFile('/home/hendrik/data/paris2006/arps/01000/diatranscycle.nc','r')
ncanomaly = NetCDF.NetCDFFile('/home/hendrik/data/paris2006/arps/01000/anomalytranscycle.nc','w')




function = lambda aa, bb: list([anomaly(aa), list([bb])])


ncin = ncmean
ncout = ncanomaly
seldimensions =('xy',) 
#ncmultifunc(ncmean,ncanomaly,seldimensions,function)
for i in range(1):
    dimensions = []
    for edimension in ncin.dimensions:
        dimensions.append(edimension)
    variables = []
    for evariable in ncin.variables:
        if evariable not in dimensions:
            variables.append(evariable)
    for evariable in variables:
        # get the axis along which the function has to be applied
        axisref = repeat(False,len(ncin.variables[evariable].dimensions))
        incoords = list()
        for edimension in seldimensions:
            axisref = axisref + (array(ncin.variables[evariable].dimensions) == edimension)
            if (edimension in ncin.variables):
                incoords.append(ncin.variables[edimension][:])
            # indien dimensie niet gekend als variable: maak dan gewoon een generieke index aan
            else:
                incoords.append(arange(ncin.dimensions[edimension]))
        # indien slechts 1 dimensie, g
        if (len(incoords) == 1):
            incoords = incoords[0]
        # we zitten hier ---->>>
        #if incoordsneeded == True:
        # define function that has to be applied multiple times
        deffunc = lambda x: function(x,incoords)

        data = ncin.variables[evariable][:]
        # get the shape of the function output
        shapedataout, outcoords = sizeout(data,axisref,lambda x: deffunc(x))

        ishapedataout = 0
        # create the necessary dimensions in the output netcdf-file for current variable (evariable)
        for idimension,edimension in enumerate(ncin.variables[evariable].dimensions):
            if (axisref[idimension] == True):
                if ((edimension in ncout.dimensions) == False):
                    ncout.createDimension(edimension,shapedataout[idimension])
                    if ((outcoords != None) & \
                        (edimension in ncin.variables) == True) & \
                        ((edimension in ncout.variables) == False \
                        ) :
                        nccopyvariable(ncin,ncout,edimension)
                        ncout.variables[edimension][:] = outcoords[ishapedataout]
                ishapedataout = ishapedataout + 1
            else:
                if ((edimension in ncout.dimensions) == False):
                    nccopydimension(ncin,ncout,edimension)
        nccopyvariable(ncin,ncout,evariable)
        ncout.variables[evariable][:] = multifunc(ncin.variables[evariable][:],axisref, lambda aa: deffunc(aa))
#         data = ncin.variables[evariable][:]
# 
# #def multifunc(data,axisref,deffunc):
#         #enige wat we eigenlijk nodig hebben voor scandata is shape(data) en shape(dataout) en dataout
#         dataout = zeros(sizeout(data,axisref,deffunc)[0])
#         SEL = list(repeat(None,len(shape(data))))
#         SELout = list(repeat(None,len(shape(dataout))))
#         scandata(0,axisref,SEL,data,deffunc,SELout,dataout)
#         # dimidx = 0
#         # print(evariable)
#         # # we lopen elk element van een as af
#         # axidx = 0
#         # while (((axisref[dimidx] == True) & (axidx == 0)) | \
#         #         ((axisref[dimidx] == False) & (axidx < size(data,axis=dimidx)) )):
#         #     if (axisref[dimidx] == False):
#         #         SELout[dimidx] = [axidx]
#         #         SEL[dimidx] = [axidx]
#         #     else:
#         #         SELout[dimidx] = range(size(dataout,axis=dimidx))
#         #         SEL[dimidx] = range(size(data,axis=dimidx))
#         #     # we gaan naar een hogere dimensie
#         #     if (dimidx < (len(shape(data)) - 1)):
#         #         scandata(dimidx + 1,axisref,SEL,data,deffunc,SELout,dataout)
#         #         #dimidx2 = dimidx + 1
# 
#         #         ## we lopen elk element van een as af
#         #         #axidx2 = 0
#         #         #while (((axisref[dimidx2] == True) & (axidx2 == 0)) | \
#         #         #        ((axisref[dimidx2] == False) & (axidx2 < size(data,axis=dimidx2)) )):
#         #         #    if (axisref[dimidx2] == False):
#         #         #        SELout[dimidx2] = [axidx2]
#         #         #        SEL[dimidx2] = [axidx2]
#         #         #    else:
#         #         #        SELout[dimidx2] = range(size(dataout,axis=dimidx2))
#         #         #        SEL[dimidx2] = range(size(data,axis=dimidx2))
#         #         #    # we gaan naar een hogere dimensie
#         #         #    if (dimidx2 < (len(shape(data)) - 1)):
#         #         #        scandata(dimidx2 + 1,axisref,SEL,data,deffunc,SELout,dataout)
#         #         #        # dimidx3 = dimidx2 + 1
# 
#         #         #        # # we lopen elk element van een as af
#         #         #        # axidx3 = 0
#         #         #        # while (((axisref[dimidx3] == True) & (axidx3 == 0)) | \
#         #         #        #         ((axisref[dimidx3] == False) & (axidx3 < size(data,axis=dimidx3)) )):
#         #         #        #     if (axisref[dimidx3] == False):
#         #         #        #         SELout[dimidx3] = [axidx3]
#         #         #        #         SEL[dimidx3] = [axidx3]
#         #         #        #     else:
#         #         #        #         SELout[dimidx3] = range(size(dataout,axis=dimidx3))
#         #         #        #         SEL[dimidx3] = range(size(data,axis=dimidx3))
#         #         #        #     # we gaan naar een hogere dimensie
#         #         #        #     if (dimidx3 < (len(shape(data)) - 1)):
#         #         #        #         scandata(dimidx3 + 1,axisref,SEL,data,deffunc,SELout,dataout)
#         #         #        #     else:
#         #         #        #         dtemp= deffunc(data[arraysel(SEL,data.shape)])
#         #         #        #         if type(dtemp).__name__ == 'list':
#         #         #        #             dataout[arraysel(SELout,dataout.shape)] = dtemp[0]
#         #         #        #         else:
#         #         #        #             dataout[arraysel(SELout,dataout.shape)] = dtemp
#         #         #
#         #         #        #     axidx3 = axidx3 + 1
#         #         #
#         #         #    else:
#         #         #        dtemp= deffunc(data[arraysel(SEL,data.shape)])
#         #         #        if type(dtemp).__name__ == 'list':
#         #         #            dataout[arraysel(SELout,dataout.shape)] = dtemp[0]
#         #         #        else:
#         #         #            dataout[arraysel(SELout,dataout.shape)] = dtemp
#         #     
#         #         #    axidx2 = axidx2 + 1
# 
#         #     else:
#         #         dtemp= deffunc(data[arraysel(SEL,data.shape)])
#         #         if type(dtemp).__name__ == 'list':
#         #             dataout[arraysel(SELout,dataout.shape)] = dtemp[0]
#         #         else:
#         #             dataout[arraysel(SELout,dataout.shape)] = dtemp
#     
#         #     axidx = axidx + 1
#         print(dataout)
# 
# 
# 
# 
# 
# 
# 
# 
# 
# # #copy dimensions, except  'datetime'
# # for edimension in ncout.dimensions:
# #     if (edimension != 'datetime'):
# #         nccopydimension(ncout,ncmean,edimension)
# # 
# # sizeout(ncout.variable[0
# # 
# # ncmean.createDimension('datetime')
# # 
# # #copy skeletton of variables
# # for evariable in ncout.variables:
# #     nccopyvariable(ncout,ncout,evariable,values=False)
# # 
# # for evariable in ncout.variables:
# #     for i in range(100):
# #         for ihgt in range(35):
# #             ncanomaly.variables['d'+evariable][itimes,ihgt,i] =  \
# #                        ncout.variables[evariable][itimes,ihgt,i] - mean(ncout.variables[evariable][itimes,ihgt,:])
# #     ncread.close()
# # ncout.close()
