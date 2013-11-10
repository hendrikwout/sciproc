===========
sciproc
===========


Sciproc in experimental stage provides tools to select, edit, convert scientific (observed, model-generated)
data. It needs Numpy. It's very experimental, as some functions aren't tested or only tested in 'idealised
cases', so please be careful.  Please let me know if you would like to contribute. Currently selection
from 1D data by coordinates or certain timestep and applying a function repeatedly on a
multidimensional matrix is implemented. However selecting, interpolating and editing procedures for
multidimensional data is planned in the near future.  You might want to use it if you have have any
observational data and you want to select a period, make a selection with a certain timestep or make
an interpolation. The aim is to make an addition to the cdo climate data operators with python power
(see also ncdftools). It should be working with normal numpy data. However, if you want to process
netcdf-files, we recommend to use the ncdftools interface which acutally uses sciproc. Typical usage
often looks like this::

    #!/usr/bin/env python

    from numpy import *
    from sciproc import *

    # select data from a 1-D array:
    data = array([1.0,2.0,4.0,2.5])
    incoords = array([0.0,1.0,2.0,3.0])
    print(datatimeco(data,coords = incoords,outcoords = array([1.0,2.0]))

    a = array([[[1,3,2],[2,1,3],[4,1,3]],[[1,2,3],[4,1,2],[3,0,1]]])
    print('copy')
    print( multifunc(a,[False,False,True],lambda x: copyfunction(x)))
    print('take only elements 2 and 3 from third dimension')
    print(multifunc(a,[False,False,True],lambda x: secondandthirdelement(x)))
    print('take only elements 2 and 3 from second dimension')
    print(multifunc(a,[False,True,False],lambda x: secondandthirdelement(x)))
    print('reduce dimension')





A Section
=========


A Sub-Section
-------------


