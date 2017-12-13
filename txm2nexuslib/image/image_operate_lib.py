#!/usr/bin/python

"""
(C) Copyright 2014-2017 ALBA-CELLS
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
import shutil
import h5py
import numpy as np


def copy_hdf5(input, output):
    shutil.copy(input, output)

def extract_single_image_from_hdf5(f_handler):
    image = f_handler["data"].value
    try:
        workflow_step = f_handler["data"].attrs["step"]
    except:
        workflow_step = 0
    return image, workflow_step

def store_single_image_in_new_hdf5(hdf5_filename, image,
                                   dataset="data"):
    """Store a single image in an hdf5 file"""
    f = h5py.File(hdf5_filename, "w")
    f.create_dataset(dataset, data=image)
    f.flush()
    f.close()

def store_single_image_in_existing_hdf5(hdf5_filename, image,
                                        description="default",
                                        dataset="default"):
    """Store a single image in an hdf5 file"""
    f = h5py.File(hdf5_filename, "r+")
    precedent_step = int(f["data"].attrs["step"])
    workflow_step = precedent_step + 1
    if dataset == "default":
        data_set = "data_" + str(workflow_step)
    else:
        data_set = dataset
    f.create_dataset(data_set, data=image)
    f[data_set].attrs["step"] = workflow_step
    f[data_set].attrs["dataset"] = data_set
    f[data_set].attrs["description"] = description
    try:
        f["data"] = h5py.SoftLink(data_set)
    except:
        del f["data"]
        f["data"] = h5py.SoftLink(data_set)
    f.flush()
    f.close()
    return workflow_step

def add_images(image1, image2):
    shape1 = np.shape(image1)
    shape2 = np.shape(image2)
    if shape1 != shape2:
        raise "Images with different dimensions cannot be added"
    result_image = image1 + image2
    return result_image

def subtract_images(minuend_image, subtrahend_image):
    minuend_image = np.array(minuend_image)
    subtrahend_image = np.array(subtrahend_image)
    shape1 = np.shape(minuend_image)
    shape2 = np.shape(subtrahend_image)
    if shape1 != shape2:
        raise "Images with different dimensions cannot be subtracted"
    result_image = minuend_image - subtrahend_image
    return result_image

def add_cte_to_image(image, cte):
    image = np.array(image)
    result_image = image + float(cte)
    return result_image

def subtract_image_to_cte(cte, image):
    shape = np.shape(image)
    cte = float(cte)
    img_cte = cte*np.ones(shape)
    result_image = img_cte - image
    return result_image

def multiply_image_by_constant(image, cte):
    image = np.array(image)
    result_image = np.multiply(image, cte)
    return result_image

def divide_image_by_constant(image, cte):
    cte = float(cte)
    image = np.array(image)
    result_image = np.divide(image, cte)
    return result_image

def multiply_images_element_wise(image1, image2):
    result_image = np.multiply(image1, image2)
    return result_image

def divide_images_element_wise(numerator, denominator):
    numerator = np.array(numerator, dtype=float)
    denominator = np.array(denominator, dtype=float)
    result_image = np.divide(numerator, denominator)
    return result_image

def main():
    ars = np.array([[2, 3], [4, 5]])
    brs = np.array([[5, 1], [2, 1]])

    add_resulting_image = add_images(ars, brs)
    subtract_resulting_image = subtract_images(ars, brs)

    print(add_resulting_image)
    print(subtract_resulting_image)


if __name__ == "__main__":
    main()