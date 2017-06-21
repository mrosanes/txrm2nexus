#!/usr/bin/python

"""
(C) Copyright 2014-2017 Marc Rosanes
The program is distributed under the terms of the 
GNU General Public License (or the Lesser GPL).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import numpy as np
import h5py


class MosaicNormalize:

    def __init__(self, inputfile, ratio=1):

        # Input File: HDF5 Raw Data
        filename_nexus = inputfile
        self.input_nexusfile = h5py.File(filename_nexus, 'r')

        # Output File: HDF5 Normalized Data
        outputfilehdf5 = inputfile.split('.')[0]+'_mosaicnorm'+'.hdf5'
        self.mosaicnorm = h5py.File(outputfilehdf5, 'w')
        self.norm_grp = self.mosaicnorm.create_group("MosaicNormalized")
        self.norm_grp.attrs['NX_class'] = "NXentry"

        self.ratio_exptimes = ratio
            
        # Mosaic images
        self.nFrames = 0                
        self.numrows = 0
        self.numcols = 0
        self.dim_imagesMosaic = (0, 0, 1)
        self.energies = list()

        # FF images (FF is equivalent to brightfield)
        self.nFramesFF = 1
        self.numrowsFF = 0
        self.numcolsFF = 0
        self.dim_imagesFF = (1, 1, 0)

        return

    def normalizeMosaic(self):

        nxtomo_grp = self.input_nexusfile["NXtomo"]
        instrument_grp = nxtomo_grp["instrument"]

        #####################
        # Retrieving Angles #
        #####################
        try:
            self.angles = nxtomo_grp["sample"]["rotation_angle"].value
            self.norm_grp.create_dataset("rotation_angle", data=self.angles[0])
        except:
            print("\nAngles could not be extracted.\n")

        #######################
        # Retrieving Energies #
        #######################
        try:
            self.energies = instrument_grp["source"]["energy"].value
            self.norm_grp.create_dataset("energy", data=self.energies[0])
        except:
            print("\nEnergies could not be extracted.\n")

        ####################################
        # Dimensions from Data Image Stack #
        ####################################
        # Main Image Stack DataSet
        sample_image_data = instrument_grp["sample"]["data"]

        # Shape information of data image stack
        self.dim_imagesMosaic = sample_image_data.shape
        self.numrows = self.dim_imagesSpec[1]
        self.numcols = self.dim_imagesSpec[2]
        print("Dimensions mosaic: {0}".format(self.dim_imagesMosaic))

        ##################################
        # Dimensions from FF Image Stack #
        ##################################
        # FF Image Stack Dataset
        FF_image_data = instrument_grp["bright_field"]["data"]

        # Shape information of FF image stack
        self.dim_imagesFF = FF_image_data.shape
        self.numrowsFF = self.dim_imagesFF[1]
        self.numcolsFF = self.dim_imagesFF[2]
        print("Dimensions FF: {0}".format(self.dim_imagesFF))




        """
        #########################################
        # Normalization                         #
        #########################################
        
        rest_rows_mosaic_to_FF = float(self.numrows) % float(self.numrowsFF)
        rest_cols_mosaic_to_FF = float(self.numcols) % float(self.numcolsFF)
        
        if rest_rows_mosaic_to_FF == 0.0 and rest_cols_mosaic_to_FF == 0.0:

            rel_cols_mosaic_to_FF = int(self.numcols / self.numcolsFF)
        
            self.norm_grp['mosaic_normalized'] = nxs.NXfield(
                            name='mosaic_normalized', dtype='float32' , 
                            shape=[self.numrows, self.numcols])

            self.norm_grp['mosaic_normalized'].attrs[
                                                    'Pixel Rows'] = self.numrows    
            self.norm_grp['mosaic_normalized'].attrs[
                                                 'Pixel Columns'] = self.numcols
            self.norm_grp['mosaic_normalized'].write()
               
               
            self.input_nexusfile.opengroup('bright_field')
            self.input_nexusfile.opendata('data')                
            FF_image = self.input_nexusfile.getslab(
                 [0, 0], [self.numrowsFF, self.numcolsFF])               
            #print(np.shape(FF_image))
            #print(len(FF_image[0])) 
            self.input_nexusfile.closedata()
            self.input_nexusfile.closegroup()                   
        
            self.input_nexusfile.opengroup('sample')
            self.input_nexusfile.opendata('data')   

            #########################################
            # Normalization row by row              #
            #########################################
            for numrow in range (0, self.numrows):

                individual_FF_row = list(FF_image[numrow%self.numrowsFF])
                collageFFrow = individual_FF_row * rel_cols_mosaic_to_FF 

                individual_mosaic_row = self.input_nexusfile.getslab(
                                [numrow, 0, 0], [1, self.numcols, 1])    

                # Formula #
                numerator = np.array(individual_mosaic_row)
                numerator = numerator.astype(float)
                numerator = numerator[0,:,0]

                denominator = np.array(collageFFrow)
                denominator = denominator.astype(float)
                
                self.norm_mosaic_row = np.array(numerator / (
                        denominator * self.ratio_exptimes), dtype = np.float32) 
                
                slab_offset = [numrow, 0]
                imgdata = np.reshape(self.norm_mosaic_row, (1, self.numcols), order='A')

                self.norm_grp['mosaic_normalized'].put(
                imgdata, slab_offset, refresh=False)
                self.norm_grp['mosaic_normalized'].write()
                
                if (numrow % 200 == 0):
                    print('Row %d has been normalized' % numrow)
            
            self.input_nexusfile.closedata()
            self.input_nexusfile.closegroup()
            self.input_nexusfile.close()
            print('\nMosaic has been normalized using the FF image.\n')

        else:
            print("Normalization of Mosaic is not possible because the " +
                  "dimensions of the Mosaic image are not a multiple of the " + 
                  "FF dimensions.")
        """

        self.input_nexusfile.close()
        self.mosaicnorm.close()
