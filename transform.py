## To be run inside QGIS

import os
import shutil
from glob import glob
from qgis import processing


def transform_tiff(file_espg3857, file_espg4326):
    function_id = 'gdal:warpreproject'
    parameter_dictionary = {'INPUT': file_espg3857, 'OUTPUT': file_espg4326, 'SOURCE_CRS': 'EPSG:3857', 'TARGET_CRS': 'EPSG:4326'}
    out = processing.run(function_id, parameter_dictionary)
    print(f"converted: {out.get('OUTPUT', None)}")
    

def get_dest_folder(root_dir, fpath):
    f = fpath.split('\\')[-1]
    fcols = f.split('_')
    fd1 = fcols[1]
    fd2 =  fcols[2]
    
    fd = f"{root_dir}\\{fd1}\\{fd2}"
    
    if not os.path.exists(fd):
        os.makedirs(fd)
        
    fcols[-1] = 'espg4326.tif'
    out_name = '_'.join(fcols)
    out_path = f"{fd}\\{out_name}"
    
    return fd, out_path


root_dir = r'F:\dot_soil_project_avm'
tiff_files = glob(f"{root_dir}/*.tif")


for fpath in tiff_files:
    fd, out_path = get_dest_folder(root_dir, fpath)
    transform_tiff(fpath, out_path)
    





