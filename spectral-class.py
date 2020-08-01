# https://www.neonscience.org/classification-endmember-python
# Data: https://data.neonscience.org/data-products/DP3.30006.001

import this
import h5py, os, copy
import matplotlib.pyplot as plt
import numpy as np
import pysptools.util as util
import pysptools.eea as eea #endmembers extraction algorithms
import pysptools.abundance_maps as amap
import pysptools.classification as cls
import pysptools.material_count as cnt

import warnings
warnings.filterwarnings('ignore')

def read_neon_reflh5(refl_filename):
    """read in a NEON AOP reflectance hdf5 file and returns reflectance
    array, and metadata dictionary containing metadata
    (similar to envi header format)
    -------
    Parameters
    refl_filename -- full or relative path and name of reflectance hdf5
        file
    -------
    Returns
    -------
    reflArray:
        array of reflectance values
    metadata:
        dictionary containing the following metadata (all strings):
            bad_band_window1: min and max wavelengths of first water
                vapor window (tuple)
            bad_band_window2: min and max wavelengths of second water
                vapor window (tuple)
            bands: # of bands (float)
            coordinate system string: coordinate system information
                (string)
            data ignore value: value corresponding to no data (float)
            interleave: 'BSQ' (string)
            reflectance scale factor: factor by which reflectance is
                scaled (float)
            wavelength: wavelength values (float)
            wavelength unit: 'm' (string)
            spatial extent: extent of tile [xMin, xMax, yMin, yMax], UTM
                meters
    -------
    Example Execution:
    -------
    sercRefl, sercMetadata = 
h5refl2array('NEON_D02_SERC_DP1_20160807_160559_reflectance.h5;) """

    #Read in reflectance hdf5 file
    hdf5_file = h5py.File(refl_filename, 'r')

    #Get the site name
    file_attrs_string = str(list(hdf5_file.items()))
    file_attrs_string_split = file_attrs_string.split("'")
    sitename = file_attrs_string_split[1]

    #Extract the reflectance and wavelength datasets
    refl = hdf5_file[sitename]['Reflectance']
    reflData = refl['Reflectance']
    reflArray = refl['Reflectance'].value

    #Create dictionary containing relevant metadata information
    metadata = {}
    metadata['map info'] = (refl
                            ['Metadata']
                            ['Coordinate_System']
                            ['Map_Info'].value)
    metadata['wavelength'] = (refl
                              ['Metadata']
                              ['Spectral_data']
                              ['Wavelength'].value)

    #Extract no data value and set no data value to NaN
    metadata['data ignore value'] = float(reflData.attrs['Data_Ignore_Value'])
    metadata['reflectance scale factor'] =float(reflData.attrs['Scale_Factor'])
    metadata['interleave'] = reflData.attrs['Interleave']

    
