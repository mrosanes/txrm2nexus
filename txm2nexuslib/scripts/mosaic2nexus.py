#!/usr/bin/python

"""
(C) Copyright 2014-2017 Marc Rosanes
The program is distributed under the terms of the 
GNU General Public License.

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

from txm2nexuslib import mosaicnex
import datetime
import argparse


def main():

    print("\n")
    print(datetime.datetime.today())
    print("\n")

    parser = argparse.ArgumentParser(description = 'Converts a file from ' +
                                                   '.xrm to a NeXus ' +  
                                                   'complying .hdf5 file.')

    parser.add_argument('files', metavar='fname',type=str, nargs='+', 
                        default=None,
                        help="Mosaic, BrightField and DarkField " +
                             "xrm files in the order that have to be " +
                             "processed")
    parser.add_argument('-o','--files_order', type=str, default='s', 
                        help="Indicates the order in which the sample " + 
                             "file 's', bright fields 'b' and dark " +
                             "fields 'd' have to be processed")   
    parser.add_argument('--title', type=str, default='X-ray Mosaic', 
                        help="Sets the title of the mosaic")             
    parser.add_argument('--instrument-name', type=str, default='BL09 @ ALBA', 
                        help="Sets the instrument name")
    parser.add_argument('--source-name', type=str, default='ALBA', 
                        help="Sets the source name")
    parser.add_argument('--source-type', type=str, 
                        default='Synchrotron X-ray Source', 
                        help="Sets the source type")
    parser.add_argument('--source-probe', type=str, default='x-ray', 
        help=("Sets the source probe. " +  
              "Possible options are: 'x-ray', 'neutron', 'electron'"))        
    parser.add_argument('--sample-name', type=str, default='Unknown', 
        help="Sets the sample name") 

    args = parser.parse_args()

    nexusmosaic = mosaicnex.MosaicNex(args.files, args.files_order, args.title,
                                      args.source_name, args.source_type, 
                                      args.source_probe, args.instrument_name, 
                                      args.sample_name)

    if nexusmosaic.exitprogram != 1:
        nexusmosaic.NXmosaic_structure()  
        nexusmosaic.convert_metadata() 
        nexusmosaic.convert_mosaic()
    else:
        return 

    print(datetime.datetime.today())
    print("\n")

if __name__ == "__main__":
    main()
