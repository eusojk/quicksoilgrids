from owslib.wcs import WebCoverageService
import os
import time
import pycountry
from glob import glob
# from country_bounding_boxes import country_subunits_by_iso_code
from pyproj import Transformer

CRS_V2 = "http://www.opengis.net/def/crs/EPSG/0/3857"
CRS_3857 = "urn:ogc:def:crs:EPSG::3857"
CRS = 3857
FORMAT = 'GEOTIFF_INT16'
LAYERS = ['bdod', 'phh2o']
LAYER_TYPES = ['Q0.5', 'Q0.05', 'Q0.95', 'mean', 'uncertainty']
VERSION_V1 = '1.0.0'
VERSION_V2 = '2.0.1'
URL_ROOT = "http://maps.isric.org/mapserv?map=/map/"
RESOLUTION = 250
SOIL_PROPERTIES = ['soc', 'bdod', 'clay', 'sand',]
SOIL_PROPERTIES_ALL = ['bdod', 'clay', 'ocs', 'sand', 'cec', 'cfvo', 'nitrogen', 'phh2o', 'silt', 'soc', 'ocd']
FDIR = {
    'bdod': 'bulkdensity',
    'clay': 'clay',
    'soc': 'organicsoil',
    'sand': 'sand',
}
BBOX = {'USA': (-100.02,29.74,-89.67,39.98),
        'Thailand': (97.3758964376, 5.69138418215, 105.589038527, 20.4178496363),
        'Australia': (113.338953078, -43.6345972634, 153.569469029, -10.6681857235),
        'Canada': (-140.99778, 41.6751050889, -52.6480987209, 83.23324),
        'Senegal': (-17.6250426905, 12.332089952, -11.4678991358, 16.5982636581)}
# BBOX = {'USA': (-171.791110603, 18.91619, -66.96466, 71.3577635769)}

def get_country_iso(country, alpha=3):
    """
    Find and return iso code of a country
    :param country: STR- Name of a country (e.g. Thailand)
    :param alpha: INT - iso code can be 2 or 3
    :return: STR - iso code of the country (e.g. TH or THA) or None if error
    """
    try:
        country_found = pycountry.countries.search_fuzzy(country)[0]
        if alpha == 3:
            return country_found.alpha_3
        else:
            return country_found.alpha_2
    except LookupError:
        return None



def from_4326_TO_3857(lon, lat):
    TRAN_4326_TO_3857 = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    return TRAN_4326_TO_3857.transform(lon, lat)

def download_soilgrids(country, layer='soc', depth_range=(0, 5), tile_no='tile_1', country_bbox=None):
    
    # country_bbox = BBOX[country]
    cover_id = f"{layer}_{depth_range[0]}-{depth_range[1]}cm_mean"

    # fdir = r'F:\dot_soil_project_avm'
    fdir = f"{os.getcwd()}\\data"
    os.makedirs(fdir)
    out_layer = f"{fdir}/{country}_{cover_id}_{tile_no}_espg{CRS}.tif"

    if os.path.isfile(out_layer):
        print(f"{out_layer} already exists!")
        return

    bbox_min = from_4326_TO_3857(country_bbox[0], country_bbox[1])
    bbox_max = from_4326_TO_3857(country_bbox[2], country_bbox[3])
    country_bbox_3857 = (bbox_min[0], bbox_min[1], bbox_max[0], bbox_max[1])

    url = f"{URL_ROOT}{layer}.map"
    # wcs = WebCoverageService(url, version=VERSION_V1)
    wcs_v2 = WebCoverageService(url, version=VERSION_V2)
    

    if cover_id not in wcs_v2.contents.keys():
        print(f"Could not find a layer that matches: {cover_id}")
        return

    crs = f"urn:ogc:def:crs:EPSG::{CRS}"

    # response = wcs.getCoverage(identifier=cover_id, crs=crs, bbox=country_bbox_3857, resx=250, resy=250, format='GEOTIFF_INT16')
    
    subsets = [('X', bbox_min[0], bbox_max[0]), ('Y', bbox_min[1], bbox_max[1])]
    response2 = wcs_v2.getCoverage(
        identifier=[cover_id], 
        crs=CRS_V2,
        subsets=subsets, 
        resx=250, resy=250, 
        format=wcs_v2.contents[cover_id].supportedFormats[0])

    with open(out_layer, 'wb') as file:
        file.write(response2.read())
    
    print(f"Downloaded and saved as: {out_layer}")


depth_ranges = [(0, 5), (5, 15), (15, 30), (30, 60), (60, 100), (100, 200)]
# depth_ranges = [(0, 30)]

tilebbox_dict = {
    'tile01': (-129.89,40.13,-119.88,50.01),
    'tile02': (-119.96,40.09,-109.96,49.98),
    'tile03': (-109.93,40.14,-99.93,50.02),
    'tile04': (-100.02,40.0,-90.02,49.9),
    'tile05': (-90.05,40.09,-80.05,49.98),
    'tile06': (-80.65,39.25,-69.2,49.95),
    'tile07': (-70.77,39.39,-59.31,50.07),
    'tile08': (-130.66,28.67,-119.21,41.01),
    'tile09': (-120.69,28.33,-109.23,40.72),
    'tile10': (-110.66,28.44,-99.2,40.82),
    'tile11': (-100.75,28.39,-89.29,40.77),
    'tile12': (-90.78,28.44,-79.32,40.82),
    'tile13': (-80.8,28.28,-69.35,40.67),
    'tile14': (-70.77,28.05,-59.31,40.48),
    'tile15': (-130.6,18.01,-119.14,31.66),
    'tile16': (-120.88,18.07,-109.43,31.72),
    'tile17': (-110.66,17.77,-99.2,31.45),
    'tile18': (-100.81,17.34,-89.35,31.06),
    'tile19': (-90.78,17.46,-79.32,31.17),
    'tile20': (-80.8,17.58,-69.35,31.28),
    'tile21': (-70.64,17.7,-59.18,31.39),
}

soilprop = SOIL_PROPERTIES
# soilprop = ['soc']

wait_sec = 10
counter = 1
for layer in soilprop:
    for dr in depth_ranges:
        for tile, bbox in tilebbox_dict.items():
            if counter % 5 == 0:
                print(f"waiting for {wait_sec} seconds...")
                time.sleep(wait_sec)

            download_soilgrids('USA', layer, dr, tile, bbox)
            counter += 1

# #test
# tile = 'tile01'
# download_soilgrids('USA', 'ocs', (0, 5), tile, tilebbox_dict[tile])



