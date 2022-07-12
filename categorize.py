import os
import shutil
from glob import glob 


fdir = r'F:\dot_soil_project_avm'
fout = r'F:\dot_soil_project_avm\data_v2'

tiff_files = glob(f"{fdir}/data_v1/*/*/*.tif")

for fpath in tiff_files:
    f = fpath.split('\\')[-1]

    tileno = f.split('_')[4]
    soilprop = f.split('_')[1]

    

    if 'sand' in f:
        fdd = 'sandfraction'
    elif 'clay' in f:
        fdd = 'clay'
    elif 'bdod' in f:
        fdd = 'bulkdensity'
    elif 'soc' in f:
        fdd = 'organicsoil'

    # fdir = r'F:\dot_soil_project_avm'
    # # fd = os.path.join(fdir, f"/{fdd}/{f}")
    fd = f"{fout}\\{tileno}\\{fdd}"
    # print(f"tileno: {tileno}, file: {f}, fd: {fd}")
    # # print(fd)
    if not os.path.exists(fd):
        os.makedirs(fd)

    shutil.copy(fpath, fd)
    print(f"copied: {fd}\\{f}")







