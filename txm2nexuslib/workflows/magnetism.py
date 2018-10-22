#!/usr/bin/python

"""
(C) Copyright 2018 ALBA-CELLS
Author: Marc Rosanes Siscart
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


import os
import time
import subprocess
import argparse
from argparse import RawTextHelpFormatter

from txm2nexuslib.images.multiplexrm2h5 import multiple_xrm_2_hdf5
from txm2nexuslib.images.util import copy2proc_multiple
from txm2nexuslib.images.multiplecrop import crop_images
from txm2nexuslib.images.multiplenormalization import normalize_images
from txm2nexuslib.images.multiplealign import align_images
from txm2nexuslib.images.multipleaverage import average_image_groups
from txm2nexuslib.images.imagestostack import many_images_to_h5_stack

def main():
    """
    - Convert from xrm to hdf5 individual image hdf5 files
    - Copy raw hdf5 to new files for processing
    - Crop borders
    - Normalize
    - Create stacks by date, sample, energy and jj position,
      with multiple angles in each stack
    """
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    description = "magnetism: many repetition images at different angles." \
                  " Normally using 2 different polarizations by setting the" \
                  " JJ positions to change to circular left and right" \
                  " polarizations"
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=RawTextHelpFormatter)
    parser.register('type', 'bool', str2bool)

    parser.add_argument('txm_txt_script', type=str,
                        help=('TXM txt script containing the commands used ' +
                              'to perform the image acquisition by the ' +
                              'BL09 TXM microscope'))

    parser.add_argument('--crop', type='bool',
                        default='True',
                        help='- If True: Crop images\n'
                             '- If False: Do not crop images\n'
                             '(default: True)')

    parser.add_argument('--table_for_stack', type=str,
                        default='hdf5_averages',
                        help=("DB table of image files to create the stacks" +
                              "(default: hdf5_averages)"))

    args = parser.parse_args()

    print("\nWorkflow for magnetism experiments:\n" +
          "xrm -> hdf5 -> crop -> normalize -> align for same angle, same"
          " jj position and variable repetition ->"
          " average all images with same angle and"
          " same jj position ->" + " make normalized stacks")
    start_time = time.time()

    # Align and average by repetition
    variable = "repetition"

    # Multiple xrm 2 hdf5 files: working with many single images files
    multiple_xrm_2_hdf5(args.txm_txt_script)

    # Copy of multiple hdf5 raw data files to files for processing
    db_dir = os.path.dirname(os.path.abspath(args.txm_txt_script))
    db_filename = db_dir + "/index.json"
    copy2proc_multiple(db_filename)

    # Multiple files hdf5 images crop: working with single images files
    if args.crop:
        crop_images(db_filename)

    # Normalize multiple hdf5 files: working with many single images files
    normalize_images(db_filename)

    # Align multiple hdf5 files: working with many single images files
    align_images(db_filename, variable=variable)

    # Average multiple hdf5 files: working with many single images files
    average_image_groups(db_filename, variable=variable)

    # Build up hdf5 stacks from individual images
    # Stack of variable angle. Each of the images has been done by
    # averaging many repetitions of the image at the same energy, jj,
    # angle... The number of repetitions by each of the images in this
    # stack files could be variable.
    many_images_to_h5_stack(
        db_filename, table_name=args.table_for_stack,
        type_struct="normalized_magnetism_many_repetitions",
        suffix="_FS")

    print("magnetism preprocessing took %d seconds\n" %
          (time.time() - start_time))


if __name__ == "__main__":
    main()