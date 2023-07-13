#!/usr/bin/env python
# coding: utf-8

# # **Monitoring and Mapping Wildfires Using Satellite Data**
# 
# 
# **Content creators:** Brittany Engle, Diana Cadillo
# 
# **Content reviewers:** Yuhan Douglas Rao, Abigail Bodner, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Zane Mitrevica, Natalie Steinemann, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google DeepMind

# In[ ]:


# @title Project Background
# This will be a short video introducing the content creator(s) and motivating the research direction of the template.

# @markdown
from ipywidgets import widgets
from IPython.display import YouTubeVideo
from IPython.display import IFrame
from IPython.display import display


class PlayVideo(IFrame):
    def __init__(self, id, source, page=1, width=400, height=300, **kwargs):
        self.id = id
        if source == "Bilibili":
            src = f"https://player.bilibili.com/player.html?bvid={id}&page={page}"
        elif source == "Osf":
            src = f"https://mfr.ca-1.osf.io/render?url=https://osf.io/download/{id}/?direct%26mode=render"
        super(PlayVideo, self).__init__(src, width, height, **kwargs)


def display_videos(video_ids, W=400, H=300, fs=1):
    tab_contents = []
    for i, video_id in enumerate(video_ids):
        out = widgets.Output()
        with out:
            if video_ids[i][0] == "Youtube":
                video = YouTubeVideo(
                    id=video_ids[i][1], width=W, height=H, fs=fs, rel=0
                )
                print(f"Video available at https://youtube.com/watch?v={video.id}")
            else:
                video = PlayVideo(
                    id=video_ids[i][1],
                    source=video_ids[i][0],
                    width=W,
                    height=H,
                    fs=fs,
                    autoplay=False,
                )
                if video_ids[i][0] == "Bilibili":
                    print(
                        f"Video available at https://www.bilibili.com/video/{video.id}"
                    )
                elif video_ids[i][0] == "Osf":
                    print(f"Video available at https://osf.io/{video.id}")
            display(video)
        tab_contents.append(out)
    return tab_contents


video_ids = [("Youtube", "W5o_HTsef0I"), ("Bilibili", "BV1ho4y1C7Eo")]
tab_contents = display_videos(video_ids, W=730, H=410)
tabs = widgets.Tab()
tabs.children = tab_contents
for i in range(len(tab_contents)):
    tabs.set_title(i, video_ids[i][0])
display(tabs)


# **In this project**, you will be working with wildfire remote sensing data from Sentinel 2 to extract Burn Perimeters using multiple Burn Indices and other relevant information related to wildfires. By integrating this data with information from other global databases, you will have the opportunity to explore the connections between wildfires and their impact on both the ecosystem and society.

# # Project Template
# 
# ![Project Template](https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/projects/template-images/wildfires_template_map.svg)
# 
# *Note: The dashed boxes are socio-economic questions.*

# # Data Exploration Notebook
# ## Project Setup
# 

# In[ ]:


# installs
# !pip install gdal
# !pip install pandas
# !pip install geopandas


# In[ ]:


# imports
import random
import numpy
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import os
import matplotlib


# ## Satellite Data
# 
# 

# 
# **Global Wildfire Information System (GWIS)** is a global, joint initiative created by the GEO and the Copernicus Work Programs. The goal of this program is to bring together sources at a regional and international level to provide a global, comprehensive understanding of fire regimes and their effects. 
# 
# The Globfire dataset uses the MODIS burned area product (MCD64A1) to determine the amount of burnt area per event ([Artés et al., 2019](
# https://www.nature.com/articles/s41597-019-0312-2)). The MCD64A1 product that Globfire is built on top of combines imagery from the Terra and Aqua satellites with thermal anomalies to provide burnt area information ([Website](https://modis-land.gsfc.nasa.gov/burn.html), [MODIS C6 BA User Guide](https://modis-land.gsfc.nasa.gov/burn.html) & [User Guide](http://modis-fire.umd.edu/files/MODIS_C6_BA_User_Guide_1.2.pdf)). 
# 
# **Sentinel 2**
# Launched by the European Space Agency in June of 2015 (S2-A) and March of 2017 (S2-B), the Copernicus Sentinel-2 mission combines two polar-orbiting satellites to monitor variability in land surface conditions. Together, they have a global revisit time of roughly 5 days. 
# 
# 
# 
# In the provided Project Template, we load the following datasets:
# - [Global Wildfire Information Systems](#dataset1-1)
# - [Sentinel-2](#dataset1-2)
# 

# <a name="dataset1-1"></a>
# ## Global Wildfire Information Systems: Climate Action Large Wildfire Dataset
# 
# 
# The Climate Action Large Wildfire Dataset is a filtered version of the Globfire dataset (created by GWIS). 
# 
# 
# The resolution of this dataset is 500m. It has been pre-filtered to include only fires that are Class F or greater. Per the National Wildfire Coordinating Group, a Class F fire is defined as a fire that is 1,000 acres or greater, but less than 5,000 acres (note that a 2000m square region is roughly 1000 acres). For this dataset, all fires greater than 1,000 acres are included. Additional columns indicating area (acres), landcover number and landcover description, and country in which they are located within, were added. The landcover number and description were added using the Copernicus Global Land Cover Layers: CGLS-LC100 Collection 3 [User Guide](https://zenodo.org/record/3938963#.ZEeQEnZBwuU). 
# 
# Table Information: 
# ID: Globfire fire ID (unique to each fire)
# 
# 1. IDate: Globfire Initial (start) date of the fire
# 2. FDate: Globfire Final (end) date of the fire
# 3. Continent: Location of the fire 
# 4. Area_acres: size of fire in acres 
# 5. Landcover: land cover value from ESA, if the landcover of the fire cover is greater than 51%, then it is labeled as that landcover
# 6. LC_descrip: land cover description from ESA
# 7. Country: country the fire is located in

# In[ ]:


# code to retrieve and load the data
url_climateaction = "~/shared/Data/Projects/Wildfires/ClimateAction_countries.shp"
Dataset = gpd.read_file(url_climateaction)  # need to update to OSF and pooch.retrieve


# We can now visualize the content of the dataset.
# 
# 

# In[ ]:


# code to print the shape, array names, etc of the dataset
Dataset.head()


# In[ ]:


# plot the dataset
Dataset.plot()


# Great work! Now you are all set to address the questions you are interested in! Good luck!

# <a name="dataset1-2"></a>
# ## Sentinel-2
# 
# Each of the two satellites contain a Multi-Spectral Instrument (MSI) that houses 13 spectral bands, at various resolutions. The MSI uses a push-broom acquisition technique and measures in the Visible and Near Infrared (NIR) and the Short Wave Infrared (SWIR) domains. There are:
# 
# - Four bands with 10m resolution: B2-Blue (490 nm), B3- Green (560 nm), B4- Red (665 nm) and Band 8- Near Infrared (NIR) (842 nm). 
# - Six bands with 20m resolution: B5, B6, B7 and B8A (705 nm, 740 nm, 783 nm and 865 nm respectively) Vegetation Red Edge bands, along with B11 and B12 (1610 nm and 2190 nm) SWIR bands. These bands are mostly used for vegetation characterisation, vegetation stress assessment and ice/cloud/snow detection. 
# - Three additional bands: B1 - Coastal Aerosol (443 nm), B9- Water Vapor (945 nm), and B10-SWIR-Cirrus (1375 nm) which are typically used for corrections of the atmosphere and clouds.
# 
# 
# *[Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2)

# In[ ]:


# view image
def showImage(Output):
    plt.imshow(Output)
    plt.show()


# In[ ]:


# data source-specific imports

# root folder location of where the imagery is currently saved
rootFolder = "~/shared/Data/Projects/Wildfires"

continet = "Asia"

# import pre images
# pre_fire_paths = glob.glob(rootFolder + continet + id +"/pre_fire_*.npy")
pre_fire_paths = [
    fileName
    for fileName in os.listdir(os.path.join(rootFolder, continet))
    if (fileName.endswith(".npy") & fileName.startswith("pre_fire_"))
]
pre_fires_numpy = [
    numpy.load(os.path.join(rootFolder, continet, x)).astype(int)
    for x in pre_fire_paths
]

# import post images
post_fire_paths = [
    fileName
    for fileName in os.listdir(os.path.join(rootFolder, continet))
    if (fileName.endswith(".npy") & fileName.startswith("post_fire_"))
]
post_fires_numpy = [
    numpy.load(os.path.join(rootFolder, continet, x)).astype(int)
    for x in post_fire_paths
]

# import Pre-SCL Mask for cloud coverage
scl_fire_paths = [
    fileName
    for fileName in os.listdir(os.path.join(rootFolder, continet))
    if (fileName.endswith(".npy") & fileName.startswith("scl_pre_fire_"))
]
scl_fires_numpy = [
    numpy.load(os.path.join(rootFolder, continet, x)) for x in scl_fire_paths
]

# import Post-SCL Mask for cloud coverage
scl_fires_post_paths = [
    fileName
    for fileName in os.listdir(os.path.join(rootFolder, continet))
    if (fileName.endswith(".npy") & fileName.startswith("scl_post_fire_"))
]
scl_fires_post_numpy = [
    numpy.load(os.path.join(rootFolder, continet, x)) for x in scl_fires_post_paths
]


# In[ ]:


# print list of pre_fires
print("\n".join(pre_fire_paths))


# In[ ]:


# print list of post_fire
print("\n".join(post_fire_paths))


# In[ ]:


# print list of SCL
print("\n".join(scl_fire_paths))
print("\n".join(scl_fires_post_paths))


# In[ ]:


# view pre-fire satellite image that was taken right before the fire start date
showImage(
    numpy.clip(pre_fires_numpy[2][:, :, [3, 2, 1]] / 10000 * 3.5, 0, 1)
)  # RGB bands for Sentinel 2 are Bands: 4,3,2


# In[ ]:


# view post-fire satellite image that was taken right before the fire start date
showImage(
    numpy.clip(post_fires_numpy[0][:, :, [3, 2, 1]] / 10000 * 3.5, 0, 1)
)  # RGB bands for Sentinel 2 are Bands: 4,3,2


# ### Sentinel-2: Vegetation Health & Burnt Areas
# 
# [Sentinel-2 Imagery - Vegetation Health & Burnt Areas](https://drive.google.com/drive/folders/1u7UMz8gIkTPWUv6p5OhlE4jXaZAh-oP4?usp=sharing)
# 
# Continents included:
# 
# * Asia
# * Africa
# * Austrailia 
# * Europe
# * North America
# * South America
# 
# 
# **Vegetation Health:** Vegetation indices define and monitor the health of vegetation using the radiance values of the visible and near-infrared channels. The Normalized Difference Vegetation Index (NDVI) is used to measure “greenness” of vegetation.
# As one of the most widely used vegetation indexes, the NDVI takes advantage of how strongly Chlorophyll absorbs visible light and how well the leafs cellular structure reflects near-infrared. Its values range from +1.0 to -1.0, with areas of sand, rock, and snow typically having a value of 0.1 or less. Shrubs and spare vegetation are roughly 0.2 to 0.5, while higher NDVI values (0.6 to 0.9) indicate dense vegetation that is typically found in tropical forests. 
# 
# The NDVI can also be used to create the Vegetation Condition Index (VCI). The VCI depends on the current NDVI along with the extreme NDVI values within the dataset (NDVImax and NDVImin). Specifically, $$VCI = \frac{NDVI-NDVImin}{NDVImax-NDVImin}\times 100\%$$ 
# 
# This number is then compared to the threshold to determine the drought severity. For this project, up to 3 months of pre-fire imagery will be used to determine current drought conditions.
# 
# *   [NDVI, the Foundation for Remote Sensing Phenology | U.S. Geological Survey](https://www.usgs.gov/special-topics/remote-sensing-phenology/science/ndvi-foundation-remote-sensing-phenology#overview)
# *   [Application of NDVI in Vegetation Monitoring using Sentinel -2 Data for Shrirampur Region of Maharashtra](https://www.researchgate.net/publication/349763642_Application_of_NDVI_in_Vegetation_Monitoring_using_Sentinel_-2_Data_for_Shrirampur_Region_of_Maharashtra)
# 
# 
# **Burnt Area Severity:** Burn severity describes how the intensity of the fire affects the functioning of the ecosystem in which it occurred. The degree to which it alters the ecosystem is typically found using a burn index, which then (typically) classes the severity of the fire as: unburned, low severity, moderate severity, or high severity.  One of the most common burn indices is the Normalized Burn Ratio (NBR). This index is designed to highlight burnt areas in fire zones. The formula is similar to NDVI, except that the formula combines the use of both near infrared (NIR) and shortwave infrared (SWIR) wavelengths. Healthy vegetation shows a very high reflectance in the NIR, and low reflectance in the SWIR portion of the spectrum - the opposite of what is seen in areas devastated by fire. Recently burnt areas demonstrate low reflectance in the NIR and high reflectance in the SWIR. The difference between the spectral responses of healthy vegetation and burnt areas reach their peak in the NIR and the SWIR regions of the spectrum. The difference between normalized burn ratios before and after a fire is called the dNBR, and is one of many useful indices. 
# 
# Specifically, the dNBR isolates the burned areas from the unburned areas, and subtracts the pre-fire imagery from the post-fire imagery. This removes any unchanged, and thus unburned, pixels as their values result in near zero. The results of the dNBR are based on burn severity, and correspond to the gradient of burn severity for every pixel. The dNBR has an unscaled range of -2.0 to +2.0 with burned areas tending to show more positively.
# 
# * [Fire intensity, fire severity and burn severity: A brief review and suggested usage](https://www.researchgate.net/publication/228638145_Fire_intensity_fire_severity_and_burn_severity_A_brief_review_and_suggested_usage)
# * [Quantifying burn severity in a heterogeneous landscape with a relative version of the delta Normalized Burn Ratio (RdNBR)](https://www.researchgate.net/publication/222816542_Quantifying_burn_severity_in_a_heterogeneous_landscape_with_a_relative_version_of_the_delta_Normalized_Burn_Ratio_RdNBR)
# * [A methodology to estimate forest fires burned areas and burn severity degrees using Sentinel-2 data. Application to the October 2017 fires in the Iberian Peninsula](https://www.researchgate.net/publication/346200185_A_methodology_to_estimate_forest_fires_burned_areas_and_burn_severity_degrees_using_Sentinel-2_data_Application_to_the_October_2017_fires_in_the_Iberian_Peninsula)
# 

# **SCL Mask**
# Importing the SCL in order to mask out clouds form imagery

# In[ ]:


# compute SCL Mask to 0s and 1s, masking out clouds and bad pixels
def computeSCLMask(image):
    rImage, cImage = image.shape
    sclOutput = numpy.zeros((rImage, cImage))
    for x in range(cImage):
        for y in range(rImage):
            sclOutput[y, x] = 1 if image[y, x] in [0, 1, 3, 8, 9, 11] else 0

    return sclOutput


# In[ ]:


# create Pre-fire and post-fire SCL masks
print(scl_fires_numpy[5])
pre_SCL_Mask = computeSCLMask(scl_fires_numpy[5])
post_SCL_Mask = computeSCLMask(scl_fires_post_numpy[0])


# In[ ]:


# view SCL imagery for image closests to the start fire date
# -------  Save SCL as colored image based on SCL classification

# No Data (0) = black
# Saturated / Defective (1) = red
# Dark Area Pixels (2) = chocolate
# Cloud Shadows (3) = brown
# Vegetation (4) = lime
# Bare Soils (5) = yellow
# Water (6) = blue
# Clouds low probability / Unclassified (7) = aqua
# clouds medium probability (8) = darkgrey
# Clouds high probability (9) light grey
# Cirrus (10) = deepskyblue
# Snow / Ice (11) = magenta
#  colors: https://matplotlib.org/3.1.1/gallery/color/named_colors.html#sphx-glr-gallery-color-named-colors-py


def showSCL(image):
    cmap = matplotlib.colors.ListedColormap(
        [
            "black",
            "red",
            "chocolate",
            "brown",
            "lime",
            "yellow",
            "blue",
            "aqua",
            "darkgrey",
            "lightgrey",
            "deepskyblue",
            "magenta",
        ]
    )
    plt.imshow(image, cmap=cmap)
    plt.show()


showSCL(scl_fires_numpy[5])


# ### Dataset-specific Functions: NDVI

# In[ ]:


# this code computes the NDVI for an image
"The NDVI can be computed on any image (pre or post)."
"Compute the NDVI on the pre-fire image"

# compute NDVI
def computeNDVI(image, mask):
    r, c, ch = image.shape
    ndviOutput = numpy.zeros((r, c))
    for x in range(c):
        for y in range(r):
            if (image[y, x, 7] == 0 and image[y, x, 3] == 0) or mask[y, x] == 1:
                ndviOutput[y, x] = numpy.nan
            else:
                ndviOutput[y, x] = (image[y, x, 7] - image[y, x, 3]) / (
                    image[y, x, 7] + image[y, x, 3]
                )

    return ndviOutput


# In[ ]:


# TA Code
computeNDVI_value = computeNDVI(pre_fires_numpy[2], pre_SCL_Mask)


# In[ ]:


# plot NDVI without remap
showImage(computeNDVI_value)


# In[ ]:


# use this code to remap the NDVI to specific colors for values
def remapNDVI(NDVI):
    remapped = numpy.zeros((NDVI.shape[0], NDVI.shape[1]))
    for x in range(remapped.shape[0]):
        for y in range(remapped.shape[1]):
            if numpy.isnan(NDVI[x, y]):
                remapped[x, y] = numpy.nan
            elif NDVI[x, y] <= -0.2:
                remapped[x, y] = 1
            elif NDVI[x, y] <= 0:
                remapped[x, y] = 2
            elif NDVI[x, y] <= 0.1:
                remapped[x, y] = 3
            elif NDVI[x, y] <= 0.2:
                remapped[x, y] = 4
            elif NDVI[x, y] <= 0.3:
                remapped[x, y] = 5
            elif NDVI[x, y] <= 0.4:
                remapped[x, y] = 6
            elif NDVI[x, y] <= 0.5:
                remapped[x, y] = 7
            elif NDVI[x, y] <= 0.6:
                remapped[x, y] = 8
            elif NDVI[x, y] <= 0.7:
                remapped[x, y] = 9
            elif NDVI[x, y] <= 0.8:
                remapped[x, y] = 10
            elif NDVI[x, y] <= 0.9:
                remapped[x, y] = 11
            elif NDVI[x, y] <= 1:
                remapped[x, y] = 12
            else:
                remapped[x, y] = 13
    return remapped


# In[ ]:


# TA Code
NDVI_remap = remapNDVI(computeNDVI_value)


# In[ ]:


# view remapped NDVI
def showNDVI(image):
    cmap = matplotlib.colors.ListedColormap(
        [
            "#000000",
            "#a50026",
            "#d73027",
            "#f46d43",
            "#fdae61",
            "#fee08b",
            "#ffffbf",
            "#d9ef8b",
            "#a6d96a",
            "#66bd63",
            "#1a9850",
            "#006837",
        ]
    )
    plt.imshow(image, cmap=cmap)
    plt.show()


showNDVI(NDVI_remap)


# ### Dataset-specific Functions: VCI

# In[ ]:


# compute the SCL mask for all the SCLs and apply it to the pre_fire_NDVIs
pre_fires_scl = [computeSCLMask(x) for x in scl_fires_numpy]
pre_fires_NDVI = [computeNDVI(x[0], x[1]) for x in zip(pre_fires_numpy, pre_fires_scl)]


# In[ ]:


# compute for VCI
def computeVCI(for_ndvi_image, ndvi_dataset):
    rImage, cImage = for_ndvi_image.shape
    vciOutput = numpy.zeros((rImage, cImage))
    ndvi_dataset.append(for_ndvi_image)
    for x in range(cImage):
        for y in range(rImage):
            pixels = [z[y, x] for z in ndvi_dataset]
            filtered_pixels = [f for f in pixels if not numpy.isnan(f)]
            if len(filtered_pixels) == 0 or len(filtered_pixels) == 1:
                vciOutput[y, x] = 1
            elif numpy.isnan(for_ndvi_image[y, x]):
                vciOutput[y, x] = 1
            else:
                max_val = max(filtered_pixels)
                min_val = min(filtered_pixels)
                if max_val == min_val:
                    vciOutput[y, x] = 1
                else:
                    vciOutput[y, x] = (for_ndvi_image[y, x] - min_val) / (
                        max_val - min_val
                    )

    return vciOutput


# ### VCI Drought Threshold
# * image and more information: [Spatial and Temporal Variation of Drought Based onSatellite Derived Vegetation Condition Index in Nepal from 1982–2015](https://www.researchgate.net/publication/330521783_Spatial_and_Temporal_Variation_of_Drought_Based_on_Satellite_Derived_Vegetation_Condition_Index_in_Nepal_from_1982-2015)
# 
# ![droughtthreshold.png](data:image/png;base64,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)

# In[ ]:


# compute the VCI for the last pre-fire to view the drought over the time period
last_pre_fire_NDVI = pre_fires_NDVI.pop(2)
last_pre_fire_vci = computeVCI(last_pre_fire_NDVI, pre_fires_NDVI)


# In[ ]:


# view the non-thresholded VCI
showImage(last_pre_fire_vci)


# In[ ]:


# map specific colors to values to show the severity of the droughts
def remapVCI(vci):
    remapped = numpy.zeros(vci.shape)
    for x in range(remapped.shape[0]):
        for y in range(remapped.shape[1]):
            if vci[x, y] < 0.35:
                remapped[x, y] = 1
            elif vci[x, y] <= 0.50:
                remapped[x, y] = 2
            else:
                remapped[x, y] = 3
    return remapped


# In[ ]:


# define the VCI mapped/thresholded values
def showVCI(vci_image):
    cmap = matplotlib.colors.ListedColormap(["red", "yellow", "green"])
    plt.imshow(remapVCI(vci_image), cmap=cmap)
    plt.show()


# In[ ]:


# view the mapped VCI values
showVCI(last_pre_fire_vci)


# ### Dataset-specific Functions: NBR and dNBR Code
# 

# In[ ]:


# this code creates the NBR for each image then uses the NBR to create the dNBR. It can easily be updated for other burnt area indices


def computeFireMasks(pre_fire, post_fire):

    rows, columns, channels = pre_fire.shape
    nbrPost = numpy.zeros((rows, columns))
    nbrPre = numpy.zeros((rows, columns))
    dnbr = numpy.zeros((rows, columns))

    for x in range(columns):
        for y in range(rows):
            nbrPost[y, x] = (post_fire[y, x, 7] - post_fire[y, x, 11]) / (
                post_fire[y, x, 7] + post_fire[y, x, 11]
            )
            nbrPre[y, x] = (pre_fire[y, x, 7] - pre_fire[y, x, 11]) / (
                pre_fire[y, x, 7] + pre_fire[y, x, 11]
            )
            dnbr[y, x] = nbrPre[y, x] - nbrPost[y, x]

    return dnbr


# In[ ]:


# TA Code
# run computeFireMasks
dnbr = computeFireMasks(pre_fires_numpy[2], post_fires_numpy[0])


# In[ ]:


# this code applies a threshold to the dNBR to show the level of burn intensity (unburned, low severity, moderate severity, or high severity)


def remapDNBR(dnbr):
    remapped = numpy.zeros((dnbr.shape[0], dnbr.shape[1]))
    for x in range(remapped.shape[0]):
        for y in range(remapped.shape[1]):
            if numpy.isnan(dnbr[x, y]):
                remapped[x, y] = numpy.nan
            elif dnbr[x, y] <= -0.251:
                remapped[x, y] = 1
            elif dnbr[x, y] <= -0.101:
                remapped[x, y] = 2
            elif dnbr[x, y] <= 0.099:
                remapped[x, y] = 3
            elif dnbr[x, y] <= 0.269:
                remapped[x, y] = 4
            elif dnbr[x, y] <= 0.439:
                remapped[x, y] = 5
            elif dnbr[x, y] <= 0.659:
                remapped[x, y] = 6
            elif dnbr[x, y] <= 1.3:
                remapped[x, y] = 7
            else:
                remapped[x, y] = 8
    return remapped


# In[ ]:


# TA Code
dnbr_remapped = remapDNBR(dnbr)


# ### dNBR Threshold
# * image and more information: [Normalized Burn Ratio (NBR) UN-SPIDER Knowledge Portal](https://un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/in-detail/normalized-burn-ratio)
# 
# ![threshold.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABNcAAAFQCAYAAACcZpjjAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAHl2SURBVHhe7d09s+TKutD5XINxjcEBcyDitr1U7uCePhGDSwwRrWqw9t7W8A0uXqm8yzfA23s7wKrqCGJwMU4fF7u07L4x4GJh3BsBseZ5UpmplEpSSVlSvf5/52h3rSq9vzzKTGWmXj6EAQAAAAAAADDZ/+b+BQAAAAAAADARhWsAAAAAAABAIgrXAAAAAAAAgEQUrgEAAAAAAACJKFwDAAAAAAAAElG4BgAAAAAAACSicA0AAAAAAABIROEaAAAAAAAAkIjCNQAAAAAAACARhWsAAAAAAABAopcP4T4/lJeXF/cJAAAAAAAAmG5MsdnDFq59//7dfQIAAAAAAACm+fz5s/s0jGahAAAAAAAAQCIK1wAAAAAAAIBEFK4BAAAAAAAAiShcAwAAAAAAABJRuAYAAAAAAAAkonANAAAAAAAASEThGgAAAAAAAJCIwjUAAAAA+PHDfN/+Yn754x/NH/3wy9b8/sP9DgBADwrXAAAAADy5H+b37S9m+/2HfIr8+G5+++UXCtgAAIMoXAMAAADw5LRQ7ZP5vPnV/PqnP5k/yfDrz5/Cb9//TOkaAKAfhWsAAAAAntxns/n1V7P5/Mn4IrVPf/gcPgMAMITCNQAAAABo+GG+//6bayL6yXz+A8VsAIB+Lx/CfX4o379/d58AAAAA4JTvZvvHrfw38umz+XmzMT9RtgYAT+nz58/u0zBqrgEAAABAF32hwZY3hgIAhlG49nS+m+0v/vXivPloEZII24ZXuLOPAeCkdtyk8jkm+L71584fzS+3ftO9Rhoh5fr68bv5JUyzNd+fJi3z2WzcywzsCw02P1d9rmkB2y91jbYfv//i9o0MWwJWEuI+znBXcf9e3dj96h7i7vMWrsmB09dt1wmH6gD+IjfO3x85BfH9z1EC6RbefCTHIRT2aXB8hDvr37j+OdQP8+OBTycAmEcrbrpPlR+N+4S9V/QmquJ7SjsheDyf5lClAb73Bu1T08t6JaUhlprvk/jxe5T4vod+sa6RRhi6vnrIisXT/I37dG0/vm8baffT+SvtN02maVxj/lp3owz49Pkn81NoDST7wU3TeNHBdzkHR+1UNBH3u+bnB+L+gLuL+/fqtu5X9xB3n7Jwzd6YJWD9JgGreUz0pHnsqt8/fKrghsQX6mUuWgDA3fgRPxSq6H28L5/Vfx85lTCs0gDbXySz1TnzU9PrsjUN8Yv5o2bW3HenLTXf5/Djz99lDzqfPhvyWA9KH4r/UhWwnLhcItX1vP1NpmlM5K/1VuGc1tZrF2jId3KKOZ/MX/rz69MfzOdwrt3Cw+oHQ9xPnO9zIO4/qTuIu89XuCY3ye3JG/PpgHevPv3hp+ikPC7pb1S3/OX3E/sJAIDr+F7neGc3lIkbRTNrZ82gx1LzvVvfze+/1SmVT5//UD/VxsP4YWuebU10qEfQmkFaI8n92eP7tlXTyRdohLTwb6Fg49PPkoZ2nzUN/Yc6QW1+/PY7BSAXQNzHLcd98tFLu/24+3SFa/UrtSufN7+GfhX+9OuvZvOzVjeU/z1q6uzTZ7P51fcl8StvPgIA3JHo/nxmk4BPP0f3f7kfbn5u3hBPZuI+b6LptW+mqLmCSl2/peb7iLSrC/dRzw2aBj0gfSiuNc/0s6ZhfR9op8h1EhfGfZLr6ld/TTWu9aj2w6efzK+/bsznVibgk007/2p+bSWaG02U5ExcsNznyRH3ifsR4v5Tu/W4+2SFa3VfCdann81PUemnRu7PP+nNl0InAABuj9ynw337h/lttn46q/t/M88d9/txmmbemxm1eWrBLzXfR9Do6oKmQQ/NFo7Zgi/3xQnNQpLP5qeosOJT61r/IZn1cCa5grRGQUdHgZvVaKLUOh8xI+L+XPN9BMT9J3fjcfd5X2igJEpNOxw9naJuf29VO5fxojeY9FUL1aroYZyj6r5jl+VoPxGNeek61PPf+om0arEfL+r001dj/SV+zPfjt+abosZu10Xe5HHDxwIA0E3vQb9E8VZi6Xbi4/i//ClqmtV4gj2zT38ZMuNjfQodMs3r9Hz9fSret+5e1dc07ijdoIenda/T/qoGbnRH43cNi91Tf5g/xxP0HS9J6+k9vvECK90uyaB3L27K+iXs91ES99EM19eQH99/t/2UhfkfnR+6r+PfZ0gnam2yrpo8g1oP0z9LZsx9rER9p6nJ+QGvOZ9GIR1qxP0kxP0uI+L+DNuoy6niXWvfyt+238fWpOPy0SNwv3I/DrntuPtkhWutm6mc5ls5mUa9icVeqHLQuzpF/f6bPTnqOKLVlxtH3Rz3t6fVGOsvm+NPWVaXvzG/23HqiX+E1zx1v/XjRztKdBq5XXE7+K4nfee6q2MBALAkcWs7Zm4EU0mU/SaJK02sum9O+2z+UOeyzO+zFB5UicP69vXJ/Fy/InC05hPUqCnTmQbn27hPtfeF3uc1rdPxVkUZtx5b0w2us/h4FvKHTeh37GMtROnKZAya9Z6q2+Y+is70hi7PpYeai9PzbnuckNd9Nbh+UQYpdb+fkrqPZru+utnzYPtbM7Ok+9F+71foRtKJdv+7j6JrGc3vWoVxEzS3t3WeYcbzkrjfPGWJ+6ozfsgI9SjTt9HeB2SdqnjX+l3nbQvqmus8Lh99Aver0XHhluPu09Vc+/xTq68GOZmqN7FUJ3M3PeGafbUdqy5Sf9432wPLb+3URaPa8aeovfj0ZR2RkzkuOB+jMzh1SN+uudzZsQAACImnQ6m2o8TesPhentqh7Q9NxMVPTP2N89Nn8/OvU7uHkMSdZNLCPNQszVVGzHdkwvL7Nkpot51INxztY0kYT06Ez31PbTXf6qrl0e5nd9gP8/vQPmqbY78fSd1H815fx2RbB+ahmU2/+OunE0Xr3OgyV22j5nzSC+keE3E/DXG/14i43zB1G2Xu9j5wcl2a6zw2Hz2E+5UzIi7cctx9vmahWr28q2q5HEg9+FqK2r64f/zevPA+/Rx1itroWDVKRLTbA7eqLPa9QjhpWT3qaX81mxOR/tNPVf8SjU5eP/0clv2nP22q6tiJ2zWXez0WAPDMjuKp9p8U4mnHPfkUuZfXFQy09rH7OIcf3yWRO+ItX/rkNcqk/aJPbt1PsoLm581P07dLTZ2vJOr170+ffz7uK6rVZ8+pBGicbvi5UYGjuY8b/VlFx/JPv8b3RllXfYGSHF81+z21kVnoqi3SXOfPG7eOdj03sn2tCb43O8BvbJemo2R8zUCFqWbc717qPpr9+ur0yXyOzo/ejuCvnE7scrogTc6lkcfoSHxOnDOfB0Tcn4C4P1Pc7zZ2G7VQ89R9oFb3/zc6H92L+1U13ci4cMNx9zn7XNOD2NcpqtZk+yUuYW217dZpJbL7ST99/qmRwKgTEc1Xxep86/Oqr7146rKO6dtw6mnHB5/TPpmf6jubrMRvpu5XtLn+878a+T6PBQA8u2atl1bn4hpfEzJacS2GUZmiCbQ5g+2DxP09hU+8zv1ipN75hj6pfpJ0TfPHZi2iYe10w0/tmv5BnPiWjFR0b2xmfuME7zXuqc20j54jYRU+6TnYfPtjuwP8TeOc/CSrLOP/GmVwZ9rvtfR9tMT11abbv4nOj89xH1gq1Ci5ZjoRt4S4fz7i/vmmbGNjfbVw7Og+cN4LMPpxv1Jz3a+u6XlfaCAn6kZL1rtKg+Xw/7b1AbtZGvrJ/I35/v17Y4hPkVhv1fgff25UN/0s41XSl9UkF9WSjwJbHcOGC7yxXUuswz0eCwB4dq0noUedi4tWYm+UOEHfyMCPownu+OmtTQ/Eq/EjvV+flM0ZY2i+vvPlZkfIcZON5n2tqeOePapj7+rJvZ+trkN9HOLMwjXuqe0Ha9r/i+6TqhuQ5vJGnKM9ztvvsdR9tND11dD1kPZz1AeWkJUPq3G1dGK302+TO+MhdOs6Ob2sZ0Hcn8vQfIn7p0zZxtb6yjl7PF77vhLFvbNwvwrGXEg3HHeft3DNc6XBzSqtolG7qWY759tum0NcLzO+yNpV4/1Z2LgQW4mTyKRlXVRrnb+7t/Y0tn35qv4cCwC4BxIfowA5R98kXqMWQ+NJbgJND2itdvenGnyS/nnjMmjNpiK29sP0jmlqk+er/Z5oh81V58vL34tamYDv25BQ13Wol99+iVTtUvdUbarTbMYjZN7aDUjz7Wgp5+iy+338PkpZ96XdRjpxyGyZsdlqrjya5c5L4r4i7j8a7lcT3HDcpXDN+9SsvpisUcrdDkRV4qJxI5hQ2nyks0T9MuIbm16wuknxdt1EVf8nORYAcNuatUKaTQLOFNdi0KfnZ886pQbLJ8kXtWo/zLQuY+ZrOyAO38n6f/7Z/CzTbXT4eZnmFZ+0SeDgjKt1v4V7qjaP+dOvkmlp74sf2qmyb6Uw/Ry9xn5vCPtowevrDFdNJ7ZrNXTsk+Z3/QUCU831ooT7t+B5Sdwn7j8o7ldpbinuUrh2UvMkOKpO3B5a7YSbzRE1cVElMLy6GaI6b1kX1aoJ9v3P22i7JLgu8jiSYwEAd6/riaMksFKTWHUmXpv8/439dHmtfqZkXXxHx+c5Nd/mfcx2KLzRjOdn81mHhaoGxQn15pNnuXe6PoLkthi58j1VFv75J9k3WiskzrX2tFI4/VR8if0+0z6a+fryjvNAzX2gK99Yn6ukE73mvpSFy9rGWk2T2uuO+RH3JyDuX0dzfbtrMLb7ZVsgdsg8uV/drycrXPtutrb6qnYS2Dxwtg1yXH0xVFdvPs368dv2uO2zzOv771vzyy9/PH5FcTtx0eh8s90M8cxlzS26iI9Llts1wb7XCZfFqvo/8bEAgLvVul9oXyKSUajiqYuj5wTRKLb/6O3nYwSJ6b9vf2m8gWtS7ZrPPy1Qi0FMmO+PH1FmwD7pjpvrzCVOqLuuNUIi+lebaI8Pd2WBe2ojUyPzOtpQTfP9Ys+t+jeZJl6R4PgctdO5P3X+dt3+KJlL901snv2euo8Wvr4smY9cG7o+9d/NfXF8rVwjnei1li1L/r21T+LrXF/OkLw6ckzqWTUznM+NuH8W4n63k3H/HB3nbPs+IHFv9LkymI9u434lf1TjjzkRZN71sm4r7j5X4ZorHbXtglud+TXbizdvtM2q7XphNae1nQ3qK5MbZ5TXPomik0EuyEZ5jjhvWedrXsQ/zG9yQdj980vztbnKVg92n2NnVfVvvIo6GtyF9kzHAgAeRfttVJoQq+Kpi6Pu+zTRU/44rp/w47df6njuYrqsSkQyEJNe/XZc2yB+/Xy6ofm2EpXaP0/YnrqWwXIkYe7SCfF+1P5hfm8ltGe/p47q0FjWQfsGitaxkXCPCnmO0jRRn0LH5+ky+z11Hy17fXnV+oT90bhWumuizZNO1ExnvA+a6fXv2+i3aKXay27uk2gOn36umxgmaJ53zQznsyPun4O432nhjuyPztn2faCxc4/PlSn56GPcr8bGhVuOu89VuNb7dpAmrdrYqNb66Sdzzmth2yeR12yG6Jy5rLN1FDL1a9f2UgtX9X+mYwEAj0Li6WC/ppLB/Xn8zedY+yn/uSQRu2l1cj1K6x7647cxCeoReucrGbBNnMC9hPZr/1s0o/vju/lNE9qSoQhJ4Nnvqc0Mw/S+W7TpTVxj6cR2NSy031P30eLXl0w/MHvtJ6i7POLC6cRGE6Mxx1PHOaPWmmicd3JCLrRl94m4fx7ifodz4/4JY9e371yZlI+egvtV7Jbj7pM1C/1s3wjz8+dWCa7SA2Pbi//J/NqVQvi8Mb/6DgY7pv3sppVz7JhWXW5/LydOV3mOdc6yJunYD3qxarBo/aBPGbsWd1QoFZWqj9O1Difc1bFI2D4AeED6JqxfJYEXVyC2cdR24PuT+cveYDnmwViVeGzPu/k081Q81t8/m5/t+uh90H0diafvnpekMxqJxlbfTj3Omq8mcLvu2zbx33pYGJPxOxc1gnZMPypL8+M383ucy5w1fdOqjX7Ur1aVnrFpPvdNRf62y+nYN3b9hqaJMlOp+71B5tveD4n7KP366iHj11P8paSf3Tq5b1S1rcPH6/x04gTth+h9x1P3i/Y79Kfu63y85vV9VsuNB0Xc73fWfIn7laO4L87YRmtgff25Uu1792VDdd8Zm4+ucb+y44+6X9123H35EO7zQ/n+/ehSwyK0un7dpltr/XUWTgIAgPv3fRs1v/MZCfen+vG72f7y22XSBY11+WR+lkQ+SZBb88DpRDnXf4maqX7ejC0gAO4McR+34kpxV1/+MAZvC8VZfvweV33+ZBZtEgoAAK5Kay8EHU+XtbnGqNoNc2jUBpirryPM6ZHTiT8aNXm6msACj4G4j1tx63GXwjWcof064gWr+gMAgKv7FGesfugLoqIOjGVovrXs88TOwadqNpv68T16CxpuwCOnE5vb9unn7pc3AI+AuI/bcPtxl8I1pPv+e/qrqwEAwN2xbykbdbPX/lOiPl8W0nhR0Y/vhkoMN+SR04k//hy9ZY+WG3hsxH3chDuIuxSuIVn7NbgkLAAAeHRVB8hVZ8TH932t4VB1Fj+2k+QzffrJ/BRyfTQRuiWPnE6MmyZ9+iznIElgPDTiPq7vHuIuLzQAAAAAAAAAWnihAQAAAAAAALAwCtcAAAAAAACARBSuAQAAAAAAAIkets+1l5cX9wkAAAAAAACYbkyx2cMWrgEAAAAAAABLo1koAAAAAAAAkIjCNQAAAAAAACARhWsAAAAAAABAIgrXAAAAAAAAgEQUrgEAAAAAAACJKFwDAAAAAAAAEr18CPd5lH/9b/6J+3R5f/1X/8V9AgAAAAAAAK6PmmsAAAAAAABAIgrXLqI029WLeXl5Meu9+won7dfVPnthp92JS5/nt3JdLbwe+3V1Hay2sqRnVpr9dmVWui/csNpeOTZwbAAAAACIpyxcKyWD5jNn/cPaUKRzf4aO7Wq1Nts9WWBUyu3arNdbc+unxH5fRaJ8szGZ/fSc9uuVWRdlVYiVZXZflPv3UKh1leOZb0xRrYj5RmgBeoWHZQPD0MOJcr+We3g8/sqsRlzvqdPdm3K/NetVK/0jf68HNvTcY1IpbWyuxifdDKSaM1YRb5c397YSwx/HUxauvZcPeJXDGjq2pWSACw0g1DJBuTVfi73Z7wuzvnbtpyGyntXq5SbP7TdPSo9V9SnffZiPw8EcPvRfV+B4teOZmS+5LV0zxS2fR8DdqmoGrySH0Ly9l5IZkevdZj7cVw2p092bvWyLbmchmbpWykb+tpmmhTbUZwaHMn8ATrmlWEW8PW3ubSWGP5rnbhaa74y+z6F72El2Fnfr6NgezM5mgkVZ2KCIifYP1AQuezWv7mOe+0+3p/wmN2/5Nys29xmP5jpnynfzbj/0FDJe8XhmX/KqgG+/54kfcIItHG/cm+th13Fta8aisMEjk2kP9fgHSaNVJesyzvHT9tTpet3q/U9jY5mZTNI8h4PbxsZ2Cln3oSTP1GNS7TutpaGZQdnDfjkAJps9VkWIt/ObfVuJ4Q+HPtfwJKogGIIMGeEnl5tduPHc6l1lb7bVHdy8vj75ne+9PJHAuuLxzL64BFBduw7ADELNXc08RA/IVCbX/Fshd3YlsXIbRYjU6e5RtjGHj4M5SOKmkUFqbKcmeeYLTpopszUddBlai3jTmXsDcMotxSri7WlLbCsx/OFQuIan8hoilz4pcB+BW3SqthZuhG8aOm/iB3h2vuauyQrTmfaXTIn/vtx/CwXwqdM9nFDwL97r/inP9SoZMs1YVjUr4twggCluKVYRb0+7+LYSw+8ShWujVW2stcNCWxhd7s12HXc8uLJ9/Yw78avqmOOnlfG32nFiPM2L/bu7nfQc6+qXWS9PO1Y8bmPuaVvzlM4dXdXUMI1rx+5+Xc6rBBf3sSFtO6p26/E0x0Ndpbd9fOJp3XctXR1d9h5/X526Z166vGp/9/xu9mbtlqHrHF4S4TdAm9W63+16dM9ETD3PzzVlef4YdHf2Oe14ts2z3fVNPAtNHmt+/X3V8/Z15K5V+1u/SedV0HHNrmQ9oknSz5mmo/lE52bz/O07nlOvtbTrP3t1R4gascBsQh+qcn31Jf/DAzMZt3oYkT5dl5RYlhZX70e22TVrbABIMmesOhfx9rRbOl7nIIYvi8K1FN8087U2RePClQxnId83c3bH3rVgo33RD02rmUkZv5CMsl7UctFm7sLVv20mtyPYBEnrqp0r+mW6r5T8YTOeX9tt4DUD6zLz+kNYRx2/6tyxexXdtsm6NRajy9BCgwWiUgiMsn7dBRbTt8MeA9duXSZy00TcfDrDmByfl5WfVsmyGttdFQ50dXTpj/9RnwR57vrnas+rEgpt5L/7rlcchgICV2NKbyKt9bd/u6GzyeLk8/xMMy7vrOM543r4czXLv3Qvy7OFpe3rSM9Zdx25b5oSziurukb8svx+0JeFNK6PlHOmS8d85As3n74C8h6jrrWUOCbCNUeNWGAekjFx16de631CwXa49lKn6zEplqXG1aW8V7FM6Xa4jwBuwcyx6izE29OucbyI4feIwrXJSlNooZOc4rZKpe3nJ2p3LRnaoTz0viimTWubhsn4xc69He9gDjLotIeimq4svvZk+lLWVYOVr4WSmSJMVy27q6RbA5jtGiorzE47YwzrqOPrGLIenQVyPuMfL0emKbSD8H2UCZ6Bq73ntzffuLcMRpK2w7a/txO5bWhPI1439rvjKsTV8dFCLLs8t4/j8cI6yfz1GNpzIOwntwVHL2hwhWKiq5laKGAUZUfpW+nvHq7AoOpkU5btN0j2z5v+7YawnZHJ5/mZZlveWcdzzu2ub+LDtFCrvUyJDWFl5feOhaadV7p7voZrRKex54BOF3e8KlLOmS5H87HXip+PLNN9e9qEa21SHGtrF9gBiOl1prUK/LC2tUK7rqooUzFEMltR6BGp03WbEstS4+piopq0uU8UdBh/TADMZ95Y1YV4O2e8Xf54HSGG36XnLlyTzG5cjbQe+mp7eFUGry5o0gv7zfhr+X2wqHritFnV0eFOcoHtizXb+DcIDmXoJi5vvw3BqpDpNo0ccxXAPg5RwZQtjNAPMv6brE9jJXV8lwGWAFeN55TfQuGZzrNejkyz0eBad+KYpH1sfe29LJft6nh7SuJ2hFpgubazjyfS7XDbMNhUTPdzVDARP7EJ61TtIz2G9RJ0/nIz8QdSjltcwBqC8NGy5e/4i6PfS/PNHZihQH7aOddIinmWd/7xnGu765v46Vpe7WXKUjWBEs6N1vqecV711qZznaJuGl/emjHX2sQ4FujT1urT/Oc28EgkvSJxxA97VytU79F9cXV0TdeW1OmSnBFXlxE9WJEMatfDoNr0YwJgPsvFqunXNvH2tMtsKzH8XlFzLYHNaB1dV1pdtfrUVRvIO2faY3WGrs/U5YVaS5JZ/jIidjQKIzrHr2tRxZnOuj+p051CzkczzrvO9UzdjnPZgsWe/XxyH4nsiy90lYAaH0pZ2WqSVrVkGcmOpp1Z2i9ahW2h0LPe3hTznuenXXp5fWZbD3+cZNqB2udW9zJlynBuNI/xOeeV70uiLIb7ILtFo6615Ov/8ucacE/yndZ09TUL3KAPBXwGyDYtv2STyXmddb9ewH7tM1XVA4OusPboxwR4VsTby8bbJRDD79dzF67lu+YJGQbJrLpRpgidGCY4PW1p9tutWTeqfromWgn6ljems8ZYGH+/jtarOfiC9zjTOXU5k8XH9rBzNYdKU8j6dD3BSN2O0Lb+6MlIabZbba4nQkHXNKP2UfQmmWam3xcGyHkT9avmb0hZvukuLJDP9i85P06U6SQ55xpJMXV5Sx3PS2+3lb12HsNzzitbW9Z+rzds7TRWbv5+fpPtqz7Ouoblq3U0pF7/wHObdg0fhUH5QmsYfPiq5D01Q1MfaKVOl+K8+3WX9Pio/W3WFR7eeh8qqNRjAmDItOt3iVhFvF0u3i69rcTw+0bNtTtQvT1FMndFYfb7UjJ39TCvcZ019onXKx68lHnOIsvN5nCoC9hO9JvUtQ06eI3tyDdRwZ02Qa2Csf5ru3iSsF8kVcEb2+dWP1+gE78OurohSeD9IoMrXYt/9320nexE/1EtdjxvxbnnVbMJqn+Rgb5JuOqrbpqu66warleA1b0+Pdc/8OS6rpVqmHANRw8s6kyLZJrG3IRk/GoK/4KT1OnOcf79ukv3ftVhYGH6gMDlyrLiYA5DubIhnccEwFjd164O/vq9RqwSxNtO3cdKhwsfL2L43aNw7dbpReaqp1UdPcY17HyB0VzOaNrUWwuwHpIDxCwys/GFIuXedL0k05q6HXvXR50GMRt1q2Csy8ty7Rg9tR+q+likClWiw/b65oEu4PvAe/R7Vfj2lBY7nrfi/PPKnh+7g1wLctPfyTlmd1NpinVdu2uc3Ow6ri87+Cdul3bzcQy4JZe5hofSI6Eriw6p0003R1xtS9i35bbOlGl6kVgFXMm06/dyseo04m1ruOTxIoY/BArXblx426NeZHKBjyo1n4MEB1veckJo7jZyfC91urOEUvzSFK06sqnrUx0frc20swUvdUDWgod2x+iJhtYpejHEUQeboUp0KcFe/pF1tVsd9oP8az+43+U/9pYwsr+9R3SR4zlGaNLpjk0KfzxlezorW6WeV4EWOGqBv9Zkq77pejvtPTg/Hp1X6xdAW5SBGrguQ/OgcF9LnW4mZ8fVRJops2+OFi69COCWXTlWNRBvT1t4W4nhD4PCtTvRnWEbCCqJwhsi+2p32Yu/blYZ+qgaqg3WoZ6upy34fr1AG/HcbHxVP1/Q5KRth89Qa79mrnPNGdXHor+9fOjUU7bNj17LzBdXGqSFHv5pSvwWUP/Z/h76YzvRJFRuHKnlPbdt2eOZ6lR17v22+21Ae99HXKtq+vnnVVvdxLg3wXHj50xqHKvJdrvpLvMWKeBxlNuti2HNWtMnY5WkR/z3Xfe1qdON0hPLTi5TTIurU2jzfBfvs2KWTFnfMQEwn0VjVQ/ibbrltpUY/kgoXLtxod+s9tv5JBO4tp2Ju7/nIsGguqS1z6lmP0rawWIoVffiPqq+dq9Pud9W6+r+tsJ0ElLW8UsG9MUNK/OyXqZwI36D4jbupDJpO+qnGGUh++ZF++hyg+w72xHmWo9b4pa09tG6eQLY70KT4WLjjltT2N69bK+dvnWTec1avw8EYT+u7AHt+8+SbUvdvDY9v6r91zpXLmbh4zlJ3bfDUPVzS2PBS3ytVteQb6J5dG4kn1el7fB1LSmH5h7Qlz24hckObJw9C58zs0mNY96pWoLAE9uvq5efaIxqXFoSCOJ4o9dhoxVMK1Y10yPRU/72G+NSpxtyKpYlx9VzaVx2cUkzZYfut8q1JR8TAPNJjlV6nfr0abMfaeLtgvF2geOlvxHDH8zHRH/11//n1Ya57HLzoZs+PGQfxcFNYB0+5IKyv+U791XLociqaY9GOGfa3Ydcn9VvOmTZh1wj7m/5LH8fz/ec5YlDES2jPWQd85R1dMvz4+h6ZY3vchmrZZf3LyeT8eV3+7lvIzqEY9s7Tb1vJIjJX7GU7YjmF8Z3+zYassbJdPr4BIPHohqywZnE6yfD0Taf+j3WGtcN9bad3q6h8y781nWudDpneX3Txts43/EcvN56hGk6j0m0zHzoOuo5nknnVbxvZDh5bajWNG5o7r8RfCzoPTf6jsHpY1NLjGPq5PoBz2tMmkvjTVKs0rSCG7UhdbpeI2LZ2ffr6er75oghWvY5x2T0MmfeVuAhJcWqOG/Y/J14Ww9zx1tr5uNFDH88T1lzLfSvcxdyszvsTOE7e9KSe/nHd67+NltxfCTbmINbZryn/DLlgm7RdZTvC98nnD5dqJ4wSObU5IX2y7Q7fnJg+2uS7xvHY2D8WQy92CBhO/a+A3ztCP0gv1eDXFv2753cHZSteWg/TaTHws6n3d+eHJusWt/h6sN101B13OTz1O8x2Xdvcl7EKyLrMHt1Y5n/1Sr/LH08J6ibKp5oUtl1HYXztecJWNJ5Jcdfvg/TuGvDTqPr8NF1zV7onJlFYhwToQNbGY+Ka0CTvgDlsCtsjGpe+Ro7qnSFxpvOqOBjVSs9otfaYFohdbpeI2LZ2ffr6cJ9YqKzjgmA+STFqte6FYqMF0cB4q2sw0Lx1pr5eBHDH8+LlrC5z6P863/zT9yny/vrv/ov7hNwC7Q5nlbllSDeWbCg/DiZKSTQUTW3T9XkUAu2snNePX2WWzuefll6E/2QG3n1baXeX8e/4bJu4dwFAAAAcE30uQakar0UoVPoiwmDfI2xrDBv1yqcuLnjWfePd69v4XwK4Y1U2Y3WyAMAAACwNArXgFRRh5vaobvNX8dK+f6r79wyN+S7+5SuQ/zMFG/jOvJcxA0ez3xTVOs0puAPVxHeSEWnsQAAAMDTonANSJVJZjqvctPh7ZL6Rkkd7Oe1q42lbf+vWGh061yttax4u27hxC0ez+yLqVZJ35hkv8FNKc0397aoya+YBwAAAPAwKFwDznDUoaTtAF0G+agdahb6++SOPJ+MfXnAx030VXV7xzMLL+DYb9uv78bVRc2ZR79iHgAAAMDD4YUGAAAAAAAAQCJqrgEAAAAAAACJKFwDAAAAAAAAEk1uFgoAAAAAAACg8rCFay8vL+4TAAAAAAAAMN2YYjNqrgEAAAAAAACJ6HMNAAAAAAAASEThGgAAAAAAAJCIwjUAAAAAAAAgEYVrAAAAAAAAQCIK1wAAAAAAAIBEk98W+h/+/M/dp8v7F3/4j+4TAAAAAAAAcH3UXAMAAAAAAAASUbgGAAAAAAAAJKJw7SJKs129mJeXF7Peu69w0n5d7bMXdtqduPR5/iDX1X5dneerrWzRMyvNfrsyK90Xblhtr3xgOTYAAAAARnjKwrVSMnA+89Y/rA1FOvdn6NiuVmuz3ZNFxm3Z76tIk282JrOfntN+vTLroqwKsbLM7oty/x4Ktcrt2qzXW3PRSzjfmKJaEfON0AGcpdxvzXrVukfL3+uBizo8ZBsYhh6ulPu13Pvj8Vdmdek4clGljaXVto5Lx563j6YvD8CxuWMV8XZZy20rMfzePWXh2nv5gFc5rKFjW0oGudAAQi0U3Ipya6rKWbnJc/vNk9obV8Zo8t2H+TgczOFD/3UFjrKfvhY6TmHWF63NlpkvuS1dM8W1a9EBd2svmbwXSewXkthv3X3lb5uwn736cVWzeSXzbS6ylIyIxBGbyXRfPQifmR7KPDedt4+mLw/AsbljFfF2WcttKzH8MTx3s9B8Z/Rlqd3DTrK7uFtHx/ZgdjaTLMrCBiJMtKeJ3NzKb3JDlH+zYnOf8Wauc6J8N+/2Q08hY/ZqXt3HPPefLiP7klcFfPs9T/SAFHp9l5nJ5L58OET35YOks9xtWWPJ0G3ZFro37un1sOuIGZqBLGxQymTaQz1+WKZmMic8pb/p+1+VYa4y07LFfp+ekL6P0pYH4NjssYp4u6jZt9VKi6np65K2PIxDn2t4ElXgCTcFMsq4ur3ZVndF8/r65He29/JEAio3O5doCIXkl5J9cYmUunYdgAmyjTl8HMxBbsCNRHwm1/VbIXfnim8if7ZQI1gzidGDNdVYpsTg7XDkuQeaSbI1D3TbtNbvZsSjmjP2UdLyABxbIlYRb5ez0LYSwx8LhWt4Kq/hTqNPdtxH4BpO1dbCjfBNQyVBQukaMK9QeC3e6z4Wz+FrBJusMJ15Bsl8+u/L/bdZlnlNr5JB0sxVVVshymANOGcfpSwPwLGLxyri7VmW2lZi+GOhcG20ql2zdhJoC4DLvdmufQeA1ffaF9C4C6mqjjl+Whl/q50VxtO82L+720nPsa5+mfXytCPM43bdnrbvTulQ0VVNDdO4tuPu1+W8SnBxHxvStqNqtx5PczzUVbDbxyee1n3X4tvFx/PrPf6+OnXPvHR51f7u+d3szdotQ9c5vCTCb4A2q3W/2/XonomYep7P75r77ZT6xpiFJo81f4746tzt68Rdi/a3fpO2P+i4JleyHtEk6edE09F8on3Y3M9+f7T37dRrKe36zl7dEaLGK3DzQt+rct32ZRvCgzYZt3rI0S0l1qXF3XTZZtestTDCOfsoZXkAjs0Zq67lmeLtUseLGP5YKFxL8U0zZ2tTNC5cyZAW8n0z53fsXTPo7Yt+aFrNbMr4hRZqyTRyoWTuYtG/bSa4I9gESeuqnWH6ZbqvlPxhM6Zf223gNYPrMvv6Q1hHHb/qULF7Fd22ybo1FqPL0EKFBe4iIRjJ+nUXaEzfDnsMXLt1mchNE3Hz6QxjcnxeVn5aJctqbHdVeFDNv7lwf/yP+iTIc9d/V3telVCoI//dd70CMRQgyHx0Rhq4W+tv/3ZDZ5PGyef53G5gv53gz8Us/9J7Y7RsoV77OtFz0l0n7pumhO23qmvAL8sfd30ZSOP8TzknunTMR75w8+krAO8x6lpKiVMinBvUeAXm9V5dj2ogkzCeZCLcda8xpE8oMD91TU+Kdalx99Jm3kcAElzjOiTepruluEkMv2UUrk1WmkILneTSt1UqbT9AUVtnyfAOlR3si2LatLbpmIxf7Nzb8w7mIINOeyiq6cria0+mMGVdNVj5WiqZKcJ01bK7Sro1gNmuo7LC7LTzzLCOOr6OIevRWSDnCwbi5cg0hXYgvo8yyTNwtff89uYb9xbCSNJ2lNrm3U7ktqE9jXjd2O+Oq+1Wx0cLY+zy3D6OxwvrJPPXY2jPgbCf3BYcvaChLtzpasYWChhF2VGKVPqI7QoUqk5RZdl+g2T/vOnfbgjbGZl8ns/sFvbbsPrGOEwLtdr7Uq79sNPl946dmbb98tX2a7gGdBp7jHW60DlqJeWc6HI0H3st+PnIMt23p024libFqbZ2gR2As0S1QXMfgDvo9au1EfywtrVNu67WKPM4RDJpUUjrNSXWpcbdy5t3HwFIcYXrkHh7hluKm8TwW/bchWuSyY+rkdZDX20Qr8oA1gVNemG/GX8tvw8WD0+cNqs6ptxJLrF9gWQb/4bBoQzfxOXttyFYFTLdppGjrgLYxyEqmLKFS/pBxn+T9WmspI7vMsgS4KrxnPJbKDzTedbLkWk2GlzrTjeTtI+tr72X5bJdHW+7SdyOUJsp17bt8US6HW4bopvZMd3PUcFF/MQmrFO1j/QY1kvQ+cvNxB9IOW5xAWu4aR4tW/6Ovzj6vTTf3IEZuvGeds41cqa72G/1jfF0La/2vpSt0ARI2IbWupyx/b216eS60XXYNL68NWOupYlxKtCnqdWnRc9d4KlEDwckE3X8ACom6RyJT37Yu9qmem/vvGTF6Bq0czgj7l7TRfcRgE6XuQ6Jt3O5pbhJDL891FxLYDNiR+eyVletPnXVavHOmfZYneHrM3V5ofaNZKa/jLheG4VLnePXtYHiTGnd39TpjhjnoxnrXed6pm7HufSm0FdgcXIfieyLL3SVG2B8KGVlq0laVYFlJDuadmZpv2gVGoVCz3p7U8x7nk9zF/vNz0/WYqBGt9W9L+NtaK7LOdvv+2coi1N9Jd6eUddS8vV9mXMXeCb7dVR7/e24NrnKd1qD1tdIcIM+bPAZJ9tk/fpNLc+67wDAwoi3wGU8d+FavmsGkDBIZtaNMkXoODDB6WlLs99uzbpRVdc14UrQt7zQ9E1ykmO2Joy/X0fr1Rz8g5I4Uzp1OZPFx/awczWmSlPI+nQ9wUjdjtCe/ejJSGm2W23OJ0KBzTSj9lH05p9moYAvLJDzJuofzN+QsnzTXZggn+1fcn6cKPNJcs41MtYj7rdO2Wvnss7Zflsb1n6vCagXOe8lMebnN9m+6uOsa7hwtY3U6xvAkPRrXPuMrCtRvPUWjKuj24Z8oTUTPnwV9J4ap83Yvqzz7jtdLhM/L7mPgOcx7fpd+jok3p5at9s6XlMQw28PNdfuQPX2FMn8FYXZ7yUTL0HFD/Ma10Fin3i94sFLmecsstxsDoe6gO1Ev0pd26CD19iOfBMV3GkT1CoY67+2CygJ+0XfY5VBY/vk6hdqIUWvYK5uSHKj/CKDKyWKf/d9jZ3sZP9mPft+O3f7m01Q/YsM9E3BVd+C03RdR9VwvQKs7vWpt+1qcQq4Q13XUjUMXONayO1yellxMIehnN4QicX+7lpnMCSzNWZ2Mn41xcQXp3Q6/77TpXu/6nDuwq6xj4Dn0n3t6uCv3wtdh8TbUbqPlQ4XPl6jEMNvGYVrt06DoqueVnX0GNew8wVGczmj6VNvLcB6SA7os8jMxhdylXvT9bJHa+p27F0fdXrTsZGuCsa6vCzXjtNT+6mqj0WqUCU6bK9vPuiCrL9RHv1eFSLdp2ffb+dvv92OXdXRv3YqW53WpSnWde2ucXKz67h+7HDU6eGF3HycAu5JwjVebuuMnqZpFrzehtIxoQuMWcwRd9suEz8vt4+AZzLt+l3sOiTejnQjxysBMfz2ULh248JbCzUoygU+qqR6DnJB2nKDE0Izv5Hje6nTnSU8dSlN0arTnLo+1fHR2mk7W5BWB2QtmGh3nJ5oaJ2iF0McdWoZqkSXEmDlH1lXu9VhP8i/9oP7Xf5jw/DI/vZu3i3vt9Ck080jhV+unH+dla1Stz/QAmIt0NeabNU3XW9RvQfnx5v6SSk124BEmtGzbz8WLk0zvyjjNXC9h2ZFIa7P5Oy4ewlX3kcAxMLXIfF25nh7S3GTGH7LKFy7E90ZuoGgkii86bCvdpcN1nWzytDnWN/4Perpet7Ot193f3+W3Gx8VT9fYOKkbYfPcGv/XK5zzRnVx6JnH4nQqadsmx+9lpkvrnRPC0X8E4z4bZb+s/099Ct2ommjBOvU8qBLuNn91uNUfwn7bffbmfa+T79Wde/zt7+tbgrbexO/8XMiNU7VZLvddNfNFAP3SpuYu5iVFbNk9Mrt1sXGZq3hkzFQ0jH++ziuj9IT6+aPu8tadB8BGGW565B4u0S8XXRbJ7qldUEThWs3LvT/1H57n2QS17azcff3XOQCrC5B1/l/tADtEDM8BfHiPse+dq9Pud9W6+r+tsJ0cgtYxy8Z0Bc3rMzL2gfFedVvj9mbbdxJZdJ21E8OykL2zYv2ueYG7QRTh7Uet8Qtae2jdfMEsN+FJsPFxh23prC9e9leO33rJvPqXl8dfh9o2ujHlT2gff9Zsm2pm9em51e1/1rnylS3tt861f0lDFXptvRaf4mvxeoa8U00j7YheftL26HrWu7G8RT2e3+HlhO+sZULnxOzSbq+I6dqCQIYoLHFXVua0Tt0v6mubb+uXqqisa9xyUqAieOYXt+N1k6tGFjHzuo6D+mYgTfNHTkV62a471zUEvsIwDTJ16HGFJ/faPcjTbyN13fWeLvI8Uq0xH7HPD4m+vff/++rDXPZ5eZDN314yD6Kg5vAOnzISWx/y3fuq5ZDkVXTHo1wzrS7D7kmqt90yLIPuZbc3/JZ/j6e7znLE4ciWkZ7yDrmKevolufH0fXKGt/lMlbLLu9fTibjy+/2c99GdAjHtneaet9IwJG/YinbEc0vjO/2bTRkjZPp9PEJBo9FNWSDM4nXT4ajbT71e6w1rhvqbTu9XUPnXfit61zpNLC8m9pv3cL2dk4bbVs+dJ30LDdp+9vbNOIabk/jhub5PoK/1nuPfbQ/GiP0fd8lMU6pk+sHoE8d20cM0YU8Jq2mcSwpBmoaw406zohYd/Z9J83o/dteduI+Sl4egGNJ12GcN2z+TrythyXi7dzHSxHDH8tT1lwL/e/chdzsDjtTuGZqtuRe/vGd5b8tURqdbczBLTPeU36Zx7WLdR3l+8L3CadPF6onDJJ5NXmh/Tbtjp8c2P6c5PvG8RgYfxZDLzZI2I69f6GBdpR+kN+rQa4t+/dO7g7K1jy0nybSY2Hn49fJk2OTVes7XN27buKojpsunvo9JvvuTc6LeEVkHWbvxF/mf3bloJvab93qpoonmlR2XSfyuTofe55IJm2/HF/5Pkzjzn07ja7DR9c1eaFzYhaJcUqETmFlPCquAdOEWDeRvljlsCts7GtGFI1JVXpE41hntPExsJWO0Ws4LY0xItadfd+5sNn3EYDJkq7D17o1hYwXR1jirazDkvF25uN1FmL4TXrREjb3eZT/8Od/7j5d3r/4w390n4BboM31tOq1BPHOggflx8lMIYGeFxH2qZokakFlds6rwu+KPzc0UfMhN8fq20q9P45/w2U947kJAAAAYAr6XANS7ZsvRegU+mrCIF8DMCvM29MUXtT9uN3rWzifQnjjVHajNfIAAAAAXBuFa0CqqMNN7fDd5r9jpXz/1XcomRvy5X1K12F+Zoq3cR2vPop8U1TbO6agFlcR3jjV7sQXAAAAABwK14BUmWS28yq3Hd4Wqm8I1cF+XrvaWNr2/7kKjSZxtday4u35Ci+yL6Y6hfSNSPYb3JTSfHNvYOJV5gAAAAD6ULgGnOGoA1DbQboM8lE71Cz0dzqUHGZfBvHxpH1ZZeEFG/vtTK/nxnyi5sq8yhwAAABAH15oAAAAAAAAACSi5hoAAAAAAACQaHLNNQAAAAAAAAAVaq4BAAAAAAAAiR625trLy4v7BAAAAAAAAEw3ptiMZqEAAAAAAABAIpqFAgAAAAAAAIkoXAMAAAAAAAASUbgGAAAAAAAAJKJwDQAAAAAAAEhE4RoAAAAAAACQaPLbQv/+f/2n7tPl/Y9//J/dJwAAAAAAAOD6qLkGAAAAAAAAJKJwDQAAAAAAAEhE4dpVlGa7ejEvLy9mvXdf4aT9utpnL+w0AAAAAABwI56ycG1KIQ0FOgAAAEspJa21qtJaL2szJrVV7tdm5R5SVsPKrNZbsy/dCD1Sp3sIZbWfV2Hb/fbv5QgMSJ0OQLLlYhXx9lJm335i+F2g5hoAAAAurtxvzXq1MuvRuY2q5r/NFDQmKWVehZuX+6ohdboHUW4lk1ftZ938LMtMVv3gMoA9mezU6QAkWi5WEW8vZYHtJ4bfDQrXAAAAcEHuSfq6sE/xJb0/ik5T2MxKZvLdwegL7+1w2JnczkPne5xZSJ2ul2RK7NP/1dZmWG7bXjJzRbWe+c4cZLsPh4P99+NQVBmtUsY5yu2lTgcg1eyxyiLeXtL8x5AYfk8oXAMAAMDFaObD1p7IcrPTxP4md78MKLdm6/IAmmHZVbmUis7nzWUWJEOx3UZZsNTpHkS53bpMnGzrLnfb6mQbc5DvrL3sp8ZuS5sOQKKFYhXx9oIW2H5i+H2hcA0AAAAX8yqZDM14VE/yG0n+XuW3ffUEPitMZ95QMgv++3L/LdRwSJ3u9u3N2vadM1QDojTfNFOtctnn1aem8H1pynf7QaROByDVUrGKeDuHMfF2ie0nht8bCteSVe2ptUNAW9pb7s127TuIrL5fb90FdpKrrhtNa9tpu1+b/MXd/6bR/pcwtNdZ2967cf131hzb5tty+2mq6U535NjeF67NuvsVAADct2yzaz7RH+Hdd17z+tp8Ah959RlHGdfnFVKn61JuXVrIp6/Kople6Xj87/s58uPY8VwfOJeUZa/uU5vsF7f57+/H65Q6HYBp5oxVMeLt5eLtUsdQEcPvA4Vrc/hWdQhYNC7c0uwL+b6vBMx730qgqC76empfMDWlPfZEss4vq6rtfaWn1Dpp27RwzhUQ6mRy5WoHitV2VR05dsRDoQWH7X0hU+m+0CcFUyIQAAB4EJIJcWmA/oyC/CYZmsq7ZHL039TpemiGSdM07k9l/3bD62v8i+/UWtNazZmW8rc+SLyNPoR0vatP5aTqC6nTATg2c6w6C/E2zbWOITH8llC4drbSFIXWrIo7LYzaWO/XvTXM1L7QjgabHR6GNtCLdTJYrbMxudkdqmV+HA4d1VfTtk0DmO3IMSuq+Wv7fhmqaXUMme/XdoDToOgLEzNTxMsrtJ34/kSNNwAA8JjeJfHvPg6RzFac3UqfrlumnUJrmsan0ySd8+bSODr4r1VIC7k0lO1EOqRr3NK0JsYi6TwvyjyNaYIkOcNqnNTpAKSZN1adh3ibZoljSAy/NxSuzUILqfQi95eKXthvxl/Lw1Ut29PK1BpM/MT7/UK11zJThLeW6J99F/rEbQsdOcr83zb1/C2dVpapHyXA+Q4frfJbKDzToLiJl7fR4Oo7gAQAAM+qWVthvNTpknR0al0vXdM1kvkL6bxlO5POc5cDlXTX185mVOtmesxJnQ7AeS4aq04g3qaZc/uJ4feFwrUZ2AKjo2toXFXL7mll6i/+rR57LV+bnS3AGnHdT9220JFjvumZf679J1pxwdyUDiABAABu1ck0jajTeT3dcjTU/e3Wg6/tP/SbyLW/pepjWVR9EWkfRL5PXNuFR/Wz5gjdOonU6QDggm4q3i6BGH5XKFxbUOiwMEX2alz51U3q27bQkeNe+2rTC/h48DVy44K5MR1AAgCAW7Wv+lvtGmasKpDa8fIlO2welabJvoSHl0uvW76ruhzxSTftg0hXMcty2w2Hz4C1pU4HIDYtNl4yVp1CvE0z9zKI4feDwjUsprqAjwdvqLNHAABwX7ru+dVwsqrACZJp6s01RSRDU6UyXrVbG/tv2nTnqDu1nk9udqEPIT+4bjYGf6tV/Rc1xzscdlE3HN3pstTpANS646IOPlhcI1b1Id6mxdtlt58Yfh+eu3DtZOd94976gQ5yIccXcddwGNMuFQAA3IGuTIcbZnw8PlRQVw7kslKnm67uOuM+1N2PTOsnKHU64NlMi42Xi1WnEW/TXPYYEsNvyVMWroUmjWVphk/v+q0fFz/p5KKs1i3TFqJ3I+xbCRzDBZdNqdMBAIBHF2WgBtIJoXlQnruaBKnTzWQoTRO9yOmqGRvJXVX5q7pP3FFSpwPQ4cqxqoF4m+ZK208MvylPWbgWvyxg7TsA61But4ufdPttdyeI+23hLsp2ldG6yuneFzfHojemXEPmo0q5N996I9yxerrWW0Q93mgCAMDTit981pkeiN8YFyXaUqcbRTJJXQ9pTy5ThE64r5mxkbSaTwdnxWZ8Ri91OgC9Fo1VE6Wuy6LbcAfxdtHt70IMvznP2Sw025i38EretVmtt6E025KLd79emVVRfbnoSacn98tKLjS/ArLsbd3p//GyM/PFt5GWdV83ptOXCPhCuSvJN6bataUpvq6b+9Up91uzXrUKFcN0ulmyP8J01f54kR1y1e0CAADX004nRAkMTVeE9E/7jXGp0w15zcJD2r2fn6QdfYWE9jLrtJq6YBpTSWZuLbk57d+pJutqXzzl0mKy7W/trjpSpwOQJjlWaUxxb65cbatxzkW8TbPEMSSG35ePif73/+//utowr8PHLs8+dBcMDVlxcOO3HT7k4rHj5Dv3VcuhcPM/GsFPm33kRf4hp3RYXmPIChmzy+5DrseeafKPwm9X73L717lyzrYpWT83fTVkH1mmQ/xdLmO17Ib2hYwvv9vPwysPAABuWEhDnBra9/tD0Z9O0EHTCm7UhtTpetXppHhopBlPLVOG7BLpGZ926hv60pqp0wFIlxSr4nzh8e/E22q4SLxVcx9DYvhdeeIXGmQSQw72bRl55kvEPfk7L8zusHyn+9kXfYNHtQ6BfM4L/X7TWi8vl3XbmSJ6y4fdHjvNznxZdpVH0PU7mF3hX/2rTxeqJwxZ2LbjN1nJATneF9F2HY0PAACeR7Yxhw9JX0j6p5HUGUpbqNTpemVm8ybpsDi9kuUmjxNgfpkhLeTJOsi4mk46zPiih175pmMddNNzU0g6+KMvrZk6HYB0SbHqtW7qKOP5br/ORrxNM/cxJIbflRctYXOfR/n7//Wfuk+X9z/+8X92nwAAAAAAAIDre+KaawAAAAAAAMB5KFwDAAAAAAAAElG4BgAAAAAAACSicA0AAAAAAABIROEaAAAAAAAAkIjCNQAAAAAAACDRy4dwnwEAAAAAAABMQM01AAAAAAAAINHD1lx7eXlxnwAAAAAAAIDpxhSb0SwUAAAAAAAASESzUAAAAAAAACARhWsAAAAAAABAIgrXAAAAAAAAgEQUrgEAAAAAAACJJr/Q4O/+1z90ny7vL/7ef3efAAAAAAAAgOuj5hoAAAAAAACQiMI1AAAAAAAAIBGFawAAAAAAAEAiCtcAAAAAAACARE9ZuLZfv5iXFxnWe/fNgyj3ZrtemZVumx9WK7Pe7k1ZunEeVLldm/V6a/YPvp0AANy3UtJhK5dOWZsxKbFyvzarVZS2eZG0zoh7fup0j6Dcb81a0oD1tsugacKRG19KmrJr+pWknTvnIAlNPa6NNKjd3z3jAwiWi1XE20uZe/uJ4XdK3xY6xd/+z39wtWEuu9zoG1I/TL5z39y/wy6vtqlvyIqPgxv34RyKj8xv5wMdUwAAHslhV3zkWZQ2MfnH8F378FE0xm8P2Uf3bT91ukewa+3jjmFw42Xf5Vlj/CzLZPB/Zx9FO0EZp8P8+NHfJjt1nIFntVysIt5eytzbTwy/ZxSuPYL4gsiKj110wRwOu+oCe+TCNQ1CbvvzeOOVL3R86O0HAOCWHeR2XCf260T+cII9pNds5iRO3MSZj+N5pE7X657SEjZNKBkjSeMe4pVtbLuml9z3LfG+K9ppKnHYyXzd50qdBtN0deM3Hn4Cg2aPVRbx9pJm335i+F2jcO0BHAofQKcG3ydA4RoAAFcV0l369FtzC6G2/UC6JUrUdybXot+z+DF86nRDHiUtcSqjFI5LR82GHifToAnzBJ7CErFKEG8vaIntHxLNjxh+m3ihwQN49x2qZZl5rT4BAAAsaG/Wtk+W0/34vGa55AMO5uOwM7mkVcYov7l+XrLCbHL7VVO2Cd+X+2+hT5jU6W7f+P3dK/si+999fn9vbXtptttqzlnxZjajDlNpvvn+f3I5xtWnpvB9acp3+wF4cOOu1aViFfF2Dtc9hr2I4TePwrUJujoWXPV1LLhfu3FWZtt1JZVb12Fgz+/hon6R+buverz6wFmWZvo5LxfKyA4Yy63b9tW2dTFHBrdr/LIqEiTsuG5eMu91mDaevx+v3ldhXcMXRaODxpVMfP72AACAU7LNzuxCjmCc8ODw9dX0TdmV/kmdrsuYtETbpLTiTZGMml3FzORfph0rlWV9j3flOLjZvb/f+j4ALmfOWBUj3l4u3i51DNMQw28BhWujVIU3q3Vh9v4ickr5276FpV1Ac6KUN5R0y3/33zpO1P3elZTLfDqLkWvZl9xd0HsJMOsJbyXR7XJvAdFp5MrJ7NWjhWCFDVZxHAvLkWDnCsaP1CX4uWle19OWdeTbWvax7n/3t043FKE0yOky3J/K/u2G11f596ztAQAAy5BMiLvH9yf45Te511feJZOj/6ZO12NEWqKWkFa8OJ/5Eu3MYEh3vkpm0H6Yie6n6lNJtQfAmTlWnYV4m+Yax5AYfusoXBtBL9DCnsiZrWZ7qPqqk+FgdoU7e7V03Ze0W3Wh2F5O9rZQ0i26TtTSX619VTRj2ca8hfXQAjYNNqdf/Ru2KyvM7iDbc5Btk8Ful11oaYqvUWCKqqJ2bZOO76uWZvmXxgU/eVkN8luhy8uraXXfy7Sd1W+dLN/Z+R+qmdvlvrll6mC/PmN7AADAUqIMxBB9UOY+VlKn6zYqLeGkpRUvLGS+NHnZTESFdKdmYiUtuZXtiWuNVC0N/INhL8p0jWnyJMsYc3iAxzdvrDoP8TbNFY4hMfzmUbh2SrkNtZr04tVqtvUFIhf0Ri5ofxHvZdzojAsnfXQhVOTv+Iuj3+tCnfaF0yfT9ZCo49etqg02UMgWtiszxdumbr9taaDaVYV6jVpdmflSl0a11lmU39yyZPq4mlfSstpkWtt3gP9zjkCVuD0AAOAimrUVxkudLskZacXL2Zu1z2hKprX3AaVmSFdrU0gCqJR1r2uSaEuDtWTWmn0QhXSqTPe1s9nWeiBtB+CiseoE4m2ay2w/MfweULh2wsmOCkXdLLPVVFFO1mqSVjVQGcmOph1O2i9ahW2hUOd0k9CYLfG3JfbtQrbjtudhu/JNT4eH9bLj9tVxE9TGOou+JpSpy4pp8BzXMeM02WbTfQwETUIBAFB1P7D14BPoQ789h7PSip3m39/7tR+netDZn6yRjJhNT1a1QGytEfl82BUh/RcyeErG9TVKyqLq+0j7PPL96zZqSrSbMQF3j9h4afcQb5dADL8PFK6dMKajwrh5YbNwyBcaNftV80EhyzfdhUry2f6l1TrtF1NoiX27kE3bnn9tlNyH7bIvGNAL6Hjw112j2WpvU8r+JpTJy7qIumBv7PYAAIDLSO1AOXW6FOelFZenNQ98OuvkW+Sy3LxFLSE8TbOGLkgkvRSnmPKdZtxkGvez9nmkuySTeRW2Zkn1PYBjl44HQ4i3aZZeBjH8flC4NqjuqDCVf0NI3I65CgpVU0NfFTP+3RfynFeo4wrZDr6UujRFT53O6gI6HrxmJ42Z2fjHBPGFGdW22wxc8V3L0cEb6hByKZ3Nd0duDwAAjy83O/sUPB5clw6Dv6WSTNOYW69kaKoUhO/AOXW6c5yfVjw24/7WB5suV5YVB3M4I01Td8x9rOovqbleh8PObHwOV1wjjQcsK/VavUas6kO8veljSAy/KxSuDao7+UtVv5Fyb6rKa775obvA8ry6QI9+rwrfzpZt6iqzXZ0QyoUUX0Rdw9FF7Nc5rKuWRbkqo+G3DinLuoRoe7auet+o7QEAAIsaqtEeOnDukDrddOenFRdTbutMmWacBtJYIdNVSua1+jSTOq14S31LAbficrHqNOJtmsW2nxh+dyhcG0sujKOCKS/Ucuo46UK11FIuLvlHzk57foZCG/nXfnC/y3/sBbFwP1++Rt3gdvXy66ybo1sz/AKG85Z1CbnZuGqyVQ3C6S+UAAAAc4kyUANph9A8KKSpUqebSWpacQmaKVsV1fpopuxUux5Zp2qtWv0ER5IyiT7dG6UdAVw5VjUQb9MsvP3E8LtE4doJ8Rs0+t6UEWo5dZ509RsptSDKn9RxoY3/bH8P/bHN1c9XXdqsEcDPsy7d9jXmpgnrrxfcvm5Cebz95y9rFhLYhsJJo4bhie0BAADLOpn+it8YF92sU6cbpSctcXKZYjitOLe9WftMWVaczpSp7NVUqbW+bkTqB4+6AaM2QdJUvuPsrPAvkAKgFo1VE6Wuy6LbcAfxdrntJ4bfrY+J/vZ//oOrDXOR8/NDN1177zvt8FFkbnyTfeS7g/teHWRemfvNfGRF/FvkUHxkdpz8I7fzyj8aSz76Pfvom9Wx3Yec6B9ZXnzsDgdZo8hBfovWvTnPaLsyWZ+O5R12hUzfWtegWq7d7sztg979mbqserrhQzUwXti3+ptbsO6no3WIj7MbRp0fAAA8I58O6EsnDNjl7l47NG18X5Y0TJR40DSDv7dLil/GjKVON+BkWqK5zKS04klj93e0LlO2URyKeD139bSSnmzs08bmSfpNx20krGTfyDFO2tfA3Uu4VifGuJCXHXNtEW8TXPMYRvOcst8EMfz6nrtwbWBoXIzRRd43ZIMFMfGFJ8PQRdT5+5C6kKt/0MDjRm+QaePlynhaUJY1vusPKs392LpQj6Qsq94vyYVr7X3rhq5gGwek09sDAADGaN5fB4b2TfxU+qvvAWDqdL1GpCXOTivOY/S+1uFofbq3sx460pMh494zkCkD+iXFqjjvd/w78bYaLhFvrZmPITH8vj1l4dqYk/a48OXwsSvyVmGQFg7JBdEo6e0WL/NUwU7X74O0NNquW2u7tPBKrqDh1evaLlkHmbYqxXajdYmDyagLb+qy6gAxHB9PjGdL66N9I8esexdHgY5AAgDALJIze1ZVE6GRefHpBjdGt9TpeoxKS5yXVpzFqYxSPPTt765tsC0k3CgNfWk72T/dEwBomBqrdHw/3nF+hXh7wXgbzHgMieF37UX/IztwtL/7X//Qfbq8v/h7/919ApZQmu1qZYpSQtCZrzoGAAAAAADPgRcaAF54s0xm8iVf1QoAAAAAAB4GhWuAs9/6t7LkhrI1AAAAAAAwBoVrgLU3e/fW4iz/YihbAwAAAAAAY1C4Bqj93lRla7nZ0NcaAAAAAAAYiRcaAAAAAAAAAIkmF64BAAAAAAAAqNAsFAAAAAAAAEhE4RoAAAAAAACQ6GGbhb68vLhPAAAAAAAAwHRjis3ocw0AAAAAAABIRLNQAAAAAAAAIBGFawAAAAAAAEAiCtcAAAAAAACARJP7XPu7//RH9+ny/uKf/cl9AgAAAAAAAK6PmmsAAAAAAABAIgrXAAAAAAAAgEQUrgEAAAAAAACJKFwDAAAAAAAAElG4dmf26xfz8iLDeu++Qb/SbFfV/mJ3AQAAAACAJTxl4Vq5XVUFVHZYme2Ugpdya1Zh2hez2pbuB2AB5d5s16vGOfeyWpm1nLTlg5965XZt1uut2XOJAcDdK/dbs5b7V7iX+ftZT5APDxPHDKut6ZpLuV+blXvIVg1yP33S+8pe0hKn9pfsscnHKZBEiS6jkV6x+1vSK24UAN3mjlXE28tbevuJ4ffhKQvX3hulEqUptn0n6LH9tmiMW5bv7hMwLw3SL6u1KSQYNs5PDX6FBPCv48/bu1Nuzddib/b7whYkAgDu1V4S+i+SQC8kk9G6a7nE/Py18aua6zZT0LyByr1V7is2o+G+egZyT92ezOHpcdKMVMJx0gfPLvOmU2ZZZrLqB5fhXMvcARybO1YRby/vAttPDL8bz90s1J845d58O3W+Knti64fc5Ln9BqdoAZEtMX/ggqAlyLn21QfArDC7w4f5+KiGw2FnirwKeQ8rezWv7mOe+08O5xQA3I/y3byXkt7Kd3L/qu9lH3IvC7cyievtNH++i8btHA6mcNNn+ReXEahoJqKwN4hM5nOopwnL1IzGhMzCXd93JOP3tXownA8lXhOPk3wpGTr34FmnlWkOh4P99+NQhHT2+uzcJfB4Zo9VxNuLm337jxDD78lzF669bszGnqNae+30CVN+c9Ui5cSmbA1LCueanGm7w6YOiiLLcrPR4C3fR18/GNlud1PYxRsPALgv2UYS6ZJQ3+X6TLMm97Ldm0u4i/1+YsJ9v60zNF+iGYcHoZpPODTvIY1l7s32Gbr28PspK1yat0ficSq3W5dplPF0WvvZ0XnKd5asBz2pAJElYhXx9rIusf3E8Lvy9C80CCXAcqINhxm5KKqoMlxqDMwgNF2W6NiqtwUAwA3Ym7Xtk+WMJ/LZl/rh0fu7e6g0Tsgg5BuziXID4eFUX0ZEMgv++3L/bdIyrytlf/vaBpkp3s54IBcfp4bSfPNNlfoePIfvS61YATyBcdfqxWMV8XaCWzmGxPB78/SFa/UJo/072Q/dfOHbqVLjSFeHgr4987CqXXTjxQlyYY27IH3b6Hra4Q4Vq3biOo4tjS51nevpmiXUsl5bnffpbQovjfBVSMvixIsgpq73PCYdI19N+Wi/OLLvqm3s+T0E6tNvL331jxzK0kyPY+P3ZThOQ1WvB7drqfPNj1fvqzHn1PnbAwC4eRLHQ20BScfFwsOp19fejMjYe+z0tIyMkpz2m1+okdDKEJ8jy7of+fV9L3s71KJ4f+emC3hzxqpFEW97LX0MieH3h8I1k2v5mrUfeLGBL7FvtzPvVhUMdHUoWMrfWnDWn/nXApgqKMS/2wIMLT0fvCp1uVqwsdfrV68S+b+urRaAVB0qDhYmfFvLeuk6u791urA8t16FzltGCPOut6kR9DTI6DjuT2X/dsPra/zLmeudJOEYnSi5r5tyyvRdnfj5AtronOuTffHVcmW/ayeSo7d/2r4My5EbmL9xttVPZXIT1wSfuqwjg+dbhxHn1HnbAwC4rPfq/qEGMidt4eVSRw88JfPi7iP9GQX5TZZV0T5q3Mcuk9MyqWm/BUiG+KttcVE19TmLZGBd443WNo+h+6n6xEvAAG/mWDUK8XZeCx9DYvhdonBN5BvXDrnvxQahxD43mxHFxnpBVydw1bGh7RDQDgez871Bamm8L5kPNFD46qeZKWTaejotNNgPFrKE5Urwsx3ga2eEMtjp7TVZmqL3DZPyW6FLlgvYd4Io04YgKhfTu25PUXV0WM/7wxzcNpXF11CYUnWmWLX7rr4ozJubRoc4Rpy33mnSjlFUENtRzTE8vRBdwaf0ETgU0g3INuYtrIcWsOkN5HQtvsn7Mqom3LVNOr6vLtzbgekS51uHUefUGdsDALiw8NBJb40DN4CGuqXBcRyPMo9D9GGM+zgkKS0zKV2xHJ8hzorN6TTHAK0ZEtZZ9ke8zbqtIdM1psmTpIPGHB7g8c0bq0Yh3s5s2WNIDL9PFK6pkCHvrnEUarqMKRSJq87Kxa4dG9YXlASAjQQAf9HLyd6o2VN+C4UnOu0mNI7W6TTg1J0RHgnLrdpkh0ktDTy7at0HavTYaeM3isRPD7Kqk8TdptXRocg2/qI/UfOoyyzrPdEZxyjcjKIbVKW++VhHv9eFOmNvaJmuh0RAv25VbbCBQrakfZmZL37Eo3UW4ZyU6Ts7MF3ofEuWuD0AgAvb128fk0zU0MOVWNz58tADz+lP589wRrpiEXv3RjjNnE5sS6SZVm1WpYNtYrXWDJ5sQ3EwH81cmRXSNHK//9qxYdryoj8dAOAysYp4u6TZt58YfrcoXLPqDHlZ+CDi+RcZZKYYEYlOdmwo6iZ/zcKok9NGnSK21QWAfW2y61pXfe2lbYFeUmzQarzu40RzrPdU5xwjXZlqklbVXluzT2T+91ZhWyjUqbdnDPsUxz6FaReyHfcnkLov4yaojXUW9b5qNqG87vk2rC7sHb89AIAh2jVE3adNNfia9kO/9duvo5r6oztqrl8uVd+Pr++sdEWnc/Z3abYuJ5TL/XDarU6bOcn6ldVQK82++Nrdj1FUE6IsXGbOZuyqddMaE2EqbfblPgKPYf7YuATi7ZBbO4bE8HtG4ZrTmyH3tV9GZsbHdGwoV3yorRMXPIyatkeYVvtmc6XV7cE/sDivvbRcnNutWUel4qvVV1c1d7q09ZZg3zGeHUY8njjnGEkEcoVGzVqOPtBnuZxHLkA1ptNAp/9qnwH2iyn0KUy7kE2Wv66b4arkc6C3KWV/E8rLnW8p6oK9sdsDALgcfRLu7xFZ8Tb+QYtPk0kEP/XAs3nvXtZ56Yp5lVuXJjtq/jNGZja+qwY3HA47U9gV13SH3N/9gYvkOxlPFuYftFYZO5mbpJ21i5Pp6wE8j6VjFfF2+XWbcxnE8PtG4VoQZcjDiw3qkuNxmfG6Y8Nr8qXV7cEb6nRxSPUWl5VZF4XE2+55nyOeXzx48Xp3jVcNpw7A+cfIv/UlbpteBfrMNjX01Wvj330hz3mFOq6QLTQPLk3RU0+3e99070ud78bfNMONVES17YaqgnctRwcv9Xw7R2fz3ZHbAwBoy80uSqxXg2v+P/hbB30o4xL3WXEwh9HxuE6T9dealszWmNlJRqi6S71qdzhnWiLtl7q/p7W2GEMzV5soc6X993Q9x6z6S2qul2bq6i5OrpMeAJaVeq1eKFYRb0e4pWNIDL93FK5F6jbH7sUGkzPjdaeAVyMXRnxRdA3jA2tEg7OrnnZ88R2Mb9qebNJ6dwU6N5wsWj//GIWqxuEFGHstwxEuaMp5ZNfi6Peq8O1scfPgro4lU84Bv85hXfX0d9WAw28dljrfzhVtz9bdQUZtDwBgOWXdsbJNS0y5P4Q0mYbx01F86GFbeMHQLG4g7eeFB0qlKVyTnsbgayyUhVm57zoqMXQKL/+SeXe+Eb1Xna64aL9MwJ1YLFYRby9mtu0nht89Ctdi+cYVElUnXXj1cEpmvKvQw4sCVnyS+hpRg9P2OGfaMULzOg3OUbXRcy293oMSjpEVqhqXVTt+HwjDeSL/2g/ud/mPDasjmxanOm9f+nX2x3r4BQxXPW6j5GbjSnyrGoTTXygBAJiRZvRWPl1VpSWmCGmygX52GhmvgftTaFYU7tszSU1XPLKQWazTGQAWjlXE2wvE2ytv/6UQwyehcK0hfrGB7zNqWrXMuvZb/1sSQw2a1kma+Su0b9p9/9s66ml9balldFcHHQhungSWrnL7S6137JxjVKnPEy2I8k8k4kIb/9n+Hvpjm6ufr/oJgkZ1P89z92VYfw2ie39T6g6k1zhuR3rOKa9Rw/DE9gAAlrQ3a5/Rk8za1IyeZhT9/frUvfTkPT6aV3zfHqXnvnNymWI4XTETyUR31SAPg9/vegzcd2MPRb3+EzKrcv/1byjMCt+3MQC1XKwi3l4k3orZt58YfvcoXGup3y7iTK1tFGq/SWhbawGdP42V60jQN69sn6Staev20FqLbmWrgsZza4hq3RVf16G0PqZtrNertDec+JpK9m2qjU3SAN69PEsu3mpKLbBxI0mwlP9XFl7vTuccIyecJ/u9BE0dtxW8/XaH36c0CZV9+qJvZ9F97dvpO35/2z9aBb/n7kvZgGpu2pTSnWvhu5ZrHDfv1DnlRTUMC/saatG3PQCAhZRm6+8FmiE4TH37mcwhyiid7KajdY+v7sEVvS+F2hyyLqOfnY5Oy1TLTElXXJvtV1eOk+6v5v20SoP69T/ab5J5XGuaoTGRzEO7E4mO+9s1uogAbllyrNKY4poJrnw/4R7x9qLxdpFjmIYYfiM+Jvrb//fz1Ya57HLzoZtu8p37Jnb4kIuk+l2GrDi475sG53EoPuT0C/PoGrLOZYtd3j9tln/s5Hf7uXP63UcerbtcCR9ZpkP8nczDjV2pt7dvlSoy7zAPGXS+4e9qOd3zaO5PPzT3a8p6jzGwbeccI6u1XVkh38RO/T6kta87h6zneJ23L8N57abtOf2dJc+3ofFa+9YNXdfqoajOy2o4tT0AgLk14/CJofPGEN0Th28ctVP3eE1PuVHHGXHfOTtdcQE+DdmRJhl1nLr2m59n3zAp/QM8maRYFecTmr8Tb+vhYvF25mM4iBh+86i5diR6c+KYEvsu2cYcPg5mV7T7Jsvk79zsDof+KrraLv6wM3ljwszkhfvefdOtmne9XC25rkqvM/li3Dz66Lz9q3yFzlf+yfLCLvOtd6ayP99kunh7ZB80a3Etud49zjlGVt00VB1Xmz71+xC3r+26taaSv22npLq/OlfvvH1Zd3YpTtbavMJxs8acU5VsEz2xOrk9AIC5hW4EUmlXBfbDhG46/D1e7sONsJ98bxpx3zk7XXFd2UbWT9Meus9a90pd/2JX/X60BfmmY5vraT4Sas4ATyMpVr3WrWVkvDjCEm+vEG9nPoapiOG34UVL2NznUf7uP/3Rfbq8v/hnf3KfAGAMrR6/MloTOpv0CnIAAAAAAMah5hqAxxXeFpRN6PMOAAAAAIDxKFwD8LDqV4nTJBQAAAAAsAwK1wA8KH3LUPVpWp93AAAAAACMR+EagMcUOmVNfDEJAAAAAAAjTH6hAQAAAAAAAIAKNdcAAAAAAACARBSuAQAAAAAAAIkoXAMAAAAAAAASPWyfay8vL+4TAAAAAAAAMN2YYjNeaAAAAAAAAAAkolkoAAAAAAAAkIjCNQAAAAAAACDR5Gahf/ev/pH7dHl/8W//m/sEAAAAAAAAXB811wAAAAAAAIBEFK4BAAAAAAAAiShcAwAAAAAAABJRuAYAAAAAAAAkonANAAAAAAAASETh2g3Zr1/My4sM6737Bv1Ks11V++u6u+tW1gMAAAAAAFzDUxauldtVVYhlh5XZTikUKbdmFaZ9Matt6X6oldu1Wa+3Zn/8E27EXRyjcm+261XjfHtZrcxaTtjywc8triEAeGx7ub/V97atGRvup0xX7tdm5R6AVYPcU5/s3lJKWmItaYd6H8ggf6/WkpZw43jhIe/A0PsgURImemwaaRa7v4+XA6Bp6VhFvF3eUttPDL8vT1m49t4omShNsZ0QZLZFY9yyfHefnHJrvhZ7s98XthAEN+gOjpEG6JfV2hQSkRvnpga+QoL31/Hn7N3hGgKAxyZxfpuS4xg9XVWr3GYKmjdRub/KvUUfVD387UX2gWaUJC2xdzshyzIZ9CfdD1vzba6EhByXld2nVZrFLqf6wWU4ZR3s3wCaLhCriLcLW2r7ieH36LmbhfoTp9yPOzltkNEPuclz+82x7NW8uo957j89KC0A0lLtCU9AbsKtHyM5z776KJwVZnf4MB8f1XA47EyRV+HuYQ0dn3s95wAAjmQYvlYPKvPexFSX8dPp0/fC3iQyk+8O4R76IffQ6haqT+gnZBbu8N5j94HNGGemcPvgcDjI4NITu4350pOcyHd1uqM97I52vdaqcA+e8505yDh2OTr+oQjp7PVj566BJLPHqiPE26UtdQyJ4ffpuQvXXjdmY08wrb12+oQpv7lqkRJk+sNMbnbh5O0543Flt32Mwnmm63nYuMBcybLcbDTAyvePe3ZxDQHAw9pvq4xIVrg02EhjpwsPQuVuIvfLxn1E7qG7N5dZkAzFtqNrj4cgmdMqHySZMskkbTrupZmkZee4w5bbrcs0yr6VXFtjntlGMoDuYMnxe9TdDSS5RKwi3i5rqe0nht+tp3+hQSiN3+/didVHLoqqWHpiyT8wTWi2nGWhBhcAALdlb9a2T5YpT+T902/JMLxNeUg0frrwgKovUyiZBf99uf/mHmbdg7H7u5RMXDVGVryZzRy5r16l+eabjfU9eA7fl6bdkwrwmMZdq8vHKuJtumseQ2L4PXv6wrX6hNE+nuyHbr7w7VQJvl4QrjPDqsS5TauGNjsLHN9RoG/3XE873FmiX5dVVdJcbs06TOu+C2S9tjrvZoeJvv11LLwQwm9gWZx4ycPU9U5R7dd4/rbjf/dr0/Ax0jbs9X7qHrqPrZqyHt1ebWN6UZZmegwbv6/DcRyqdi3nTHVs2+eLWup8PD4+Y86587cHALCk8IQ8lwzHhAzDlOnCA6rX195M4dj77PT0joxi0xBxOqA7LbWcd9fvT2byvjZDC8iyvseBchzcary/c+MFvDljVRfi7fKWOYbE8HtG4ZrJtXzN2ksw6Ttl9q7kLcu/9F48p2kpeHXBx8uxBRRaMj54xWmBgxZc7KsLTs5y7WxQv/edJQ4WFnzTDvKLqNBDpgvLc+tV6LxlhDBvjQOuMDCeuQYQHcf9qaoOFqvh9TX+5cz1HuNdC0zagVTWWzv+9wF6JLuta7+f6v0QuPVvfVuZaT2yL75KrhwX24ml/WOEafs6LEduXr5Kc1v9RCZvtetf8nzsMOKcO297AACLKvVlNRqBq6Yno02aTjIv7l7Sn1GQ3+SeUnmXzJH72GVyekcydjYN0ZypT0tdpA+h0BLjVTJ19sOV6X6qPh29BAx4WjPHqjbi7QXi7ULHkBh+1yhcE/mm7qyv88UGEmiqzHpuNsl1MzUI+KqlWeiY8OPjYHaFFgrIhTRwwWmQsLEucx3c2w4NdR7avlvHKE3R+wZJ+a3QJUug9J3j2/bb1a9aqvEua5AXVSeG9bw/zKGotrcsvobCkkw7O9RxfNCVdXpz0+gQx+Lz1nucfaGdMMadSEZt3ve+zfoI9jjblXXHp72u4nVjv+uqvTjbemQb8+b2u56TWrtrTC2/yfs6+xL6c/OFx011VeF2ofKi52OHUefcGdsDAFiWf9t6Vmwk+o83bTr/xP8EfSDjPg5JSu+4dIBNT/m0QLinF/ah1JLKOrdnXiUNYd82F9XqqGqYuwdNPXRbtPaHH9Y2DdI1RZTpGtPkSdZtzOEBHt+8saqNeCsWj7fLHENi+H2jcE2FTHlp9h2la6G2S19b5DHKb6FwRINA3TGhBIWNBhPf4WGHULhXtX0Pk1oaVHbVeg3U2LHThreW6J/RhZ5tJChJMNq0OjEU2cYH1xM1i7rMst5jaCGNBt2wcTLvN+Nj69gqrPVx1vbx8crqMXLHJzxN6DLPeqhsU91c/Jyq2mADhWxJ+zozX/yIXdsVzlmZPq7mtfT5mCxxewAAy/IPmDSzNOUhZep0olnLYWHhvlil8TQdUC9d7jl6T/eJgUt1Cq0Zy9Xavm1OH/zVNUK0hrlrMWH/7iLjSEbMD3tXI/0lPCSuhX6IZXlfOzZMl9WfFgAwe6wi3l483i6y/cTwu0ThmlVnysvCtTMP/IsMMlMMd7Y2aEqHh22NQp/Oa7du2tpXgGML9JKu+7qd9VRzrPcYtjDnaP6Xr8I693rYJzj2CUy7kK3d9DR9X8dNUNuVvepzttmE8rrn47C6MHj89gAATvGdO8eDT6QP/abK0DlzLjF6fPhNne7y6vtLf7+89f1WMjsnkwPn7G9PMmI2HVHV5rC1P+TzYVe/va7qtLyW7+R3X6PcD/rQMNQEkWnaTa1kGb5GSVlUfR9VtSWqdWvUsJAE0S0fR2C6Oa7VORFv1eXj7RKI4feIwjWnN1Pua8CcmSEf0+FhnzCtllLbk/148NfWeQVJpdF+59aNqqRfXbXb6dLWe1/15dU1THz0EDqQHCm0iT96yqE3nKqatJYa9cTxXlPXo0mfwLQL2bQvgbqZrko+R3qbUvY3obzc+ZiiLtgbuz0AgOWUW5eOiBLwY6RO553z0G6qUWm86H57kXWTdOtbVAPey/Ko6wmfxo0cJVnkC60J8lHnvo5qMdgMnS7LTVvVltBJc9vNRsrxA57FnPGAeOtcON4usgxi+F2icC2IMuXhxQZ1Kf6tZMjjKp7x4A11qDikekPLyqyLQq7T7nmfI55fPHjxeneNVw0LF9RIsKpiVWkKW1pfFRTpv7aLMDkDzqm9eB5XyBaaD8s6tiOj073v+s6RzGz8NsUBOjShHO5nsGs5Onip5+M5QvXmhO0BAHTJzS5+Em4H1wXA4G+ptf9Tp5PM1pgQLxmh6k41R4fRdafW80nd3+PUHWxPED1c7MpIVv0lNdfrcNg1utm4RpoAWFbqtbpErCLeprmlYzgOMfx2UbgWqdscuxcb3FqGXE76+ITvGg4p66k1kGxQ7bqwDqHPsGST1rsriLlh6WLz/dY9tZHgY6OlLyjSarnacf8yTRkniZsPd3UqmXKOhGC71/Ioq276WQfiI0udj+eKtmfrqveN2h4AwLzCQw7/0Ko1hGrOReiw2X6VOl1k6IFc6DB6FnX3D7cgZLok/bLwI8mR6rTFRftlAu7EbLGKeHs1c24/Mfy+UbgWi2ou6YsN/BtT5siQh6aBXQUiJ5wz7Rih+ZwWrEVVQs+19HrPrdoP+tRmZwvS6kKig+yXdsf9t+W8fS3ntzvBq31QN6EMBc6R2z+uudm4EuHqzTfD2wMAeBRRxmvgHhWaFc39wGXovhge2Mp9dMkMisy7mvu7VpjoNG9m94SQca/TGgCuHKtm8ezxdqHtJ4bfNQrXGuIXG/h+o6ZWke1Wl0L3vEFx3/8mjnpaV6NuId1VPQcCl9dTsn6p9Z6Hr2asBatRx403p356oBHd3y7O3deNppT7usZmVxC9iePac855oSNTXccT2wMAWMipGs6+RnpWuE6bP6q+XVKnE3UrhJ70Vvymuak3hZ57z8llilCDeul7kaTlqrt0X/cR9QMnXZGxq1Ju/Qu/svFv3JZ7sO9wOyt838YA1OyxingbXCreLrL9xPC7RuFaS/12EefMFxkEoVaclqOtos7otYbcyla5DV+1xX2BfV2HkvhYud+adcfrdcfwNZHsm1LjeesFpfPsW7FQsq4FMm4kCYTy/8rC6z2v+ulDWaxDtWc7+I7617p/+nbGXGSfyzL9shpL88fD/tEq9D13X4fgrE0pTzShvOZxPXXOeaEjU1nH9Xw1UAEAN66d3opuUnpvWq3cPWHgTXNHRqd3qmU23+itLyGSNITvfmPxDEpde1sf3K78PV1JOkJfGlWtSjMdsV/rG+L0QW877dFcf93WRo8Pknlc6zIaN2KZh33pkUsHyL5+u3q/GsCNSY5Vek36PErrzY+X9uzxdpFjSAy/ax8T/e3/839cbZjLLjcfuukm37lvYocPOZ+r32XIioP7vql/HvX0Rz/t8g85LcO8G0OWf+zkd/u5c712H3m0XnKWf2SZDvF3Mg83dmVgXRpk3mEeMuh8w9/Vcrrn0dxXfmjus5T1HuP0th2Kar3HH6N4e/x6unlEQ3P7zlmPLq1j0TlkPcs6b1+Hc9pN23PqO0uej0PjxceoHrqu07Df7XBqewAAF+fTPVkh0X2CU9Mdiv70lg6a5nKjjjPi3nNqmTJko9IBc+he33o4Tkc00wDdg67/0f72x6JvmHpsgWeSFKvivMKEWEa8XcYix5AYfq+ouXYkenuilhzPWUqrfZoddq6zfC8zeeG+d990y20/YLvC94mmJfhVKX4mX4ybRx+d984UVVUfW8KtZde+E/+33pnKvnqT6eLtyfJWVdMl13tme/9CA60efZD1qga5TuzfO4lyytbws5+W4I6F3V/xfhTyd/XCib5XIp+3r/ONfxOpOFlj81rHdcw5V8k20dOquWqgAgBuX7YxB71vS7qmEfqT708j7j1+meG+6Mk6yLh6z9R+bS9D1rdxj/Y0HVGl7dqrku90/QqbRm1MEk1j++V13wb5pmM5MpVscyHz/DhsjqcBUEmKVa/aGKMi47mGN9fz7PF2kWNIDL9XL1rC5j6P8nf/6h+5T5f3F//2v7lPwNy0OaZWfZWA3PtKez9OZgoJUNSOvXVlqDqdFXJD4YABAAAAABZAzTVAhTehDCjfBzvRx40JbwrKxnfcCQAAAADARBSuASrqPDN06B/TDiS/+k4paWJ4D/ZbjhcAAAAAYHk0CwWcozfO+Dbr2peY/ULYdvxT+w7A5fkmvHLIaBIKAAAAAFjQ5MI14JHpa5O15tp7XKAmtFPHfLMxX9qdVeI27dfmZa1Fa0N96AEAAAAAcD4K1wAAAAAAAIBE9LkGAAAAAAAAJKJwDQAAAAAAAEhE4RoAAAAAAACQ6GH7XHt5eXGfAAAAAAAAgOnGFJvxQgMAAAAAAAAgEc1CAQAAAAAAgEQUrgEAAAAAAACJJjcL/fcvpft0ef/yI3OfAAAAAAAAgOuj5hoAAAAAAACQiMI1AAAAAAAAIBGFawAAAAAAAEAiCtcAAAAAAACARBSuAQAAAAAAAIkoXLu60mxXL+bl5cWs9+4rAAAAAAAA3IWnLFzbr6vCrJdTpVn7dTXey8psS/edU27XZr3emn3r+5tS7s12vTIruw1uWK3Mers35S2v9wzu4vgAAPCASkl/rCW9EdIeLv2xknTX0G05ZbpS0mor95CyGnT8Z7v/l5Jk9fttbYZTt6Xss23nfl6P2Gmp+5vjBPRb6vogFl/alFg8hDh9tz4m+nfmcLVhLrvcfOimm3znvumxy6vxTPZRxIs/FB+Z/X7EPE46fBRZNa+zZxU5hHXvGbJClvygZj0+AABgHEnT5FkjvZFlmQz+71Z6KkiZrk4/dQ/ZrOmqW3XYFR95Yz/kH/2bvWuN2zH07rTU/c1xAvotdX2kxFSVMh3XuJoWi4cQp+8ZzUJTZK/m1X3Mc//phpRb89XXyssKszt8aCGqHQ6HnZGgWf32qIaOz97VRlxtB5/YAACAafSJfWEfcWem2B1cuuMgg0uD7DbmS0cSJGU6O429kWeSz6imsYOkc6pkjtYgmFBz4O7SB1UNidW6sLUKJPN7Wvlu3svMZPku7NvmPhOyH3wSMpa6v2c/TsADWer6sPMlFl9IQiweQpy+b7LjJumqUXapYS5n11ybVV1SPFeJ8KHwTxxSS8wfmD+mj1xzDwCAS0tNM6VMF9VQ70w7Rb9nY2d6Z+mDkJbNJK0nObB6Pyam/YZq/afu7yWOE/Aolro+iMUXNXssHhLtT+L0baLm2gN69x2qZVmowQUAADDN3qxtvyunnliXZrutxsiKN7ORlPg4adOV31y/P1lhNrn9qinbhO/L/bdq3Lswdn8b85rlVQ0DW7Ng9A7vl32pa0W0pO7vxz1OwJBx1/Ey1wexeB5XjMVDiNM3j8K1JMNv+Kw6IKx+7xu6pqtUVUvrcd0LCNyvY7z6C7sszXv1aQLtQHFcZ4bl1q3nULXdcuteqHD8Uogpy6r4/e7mJfOu93M8/+PjE9Y1fFE0XvSwkonP3x4AAJ7RuyY5RGbyrrZGvdKmCw8RX19lym5j00Jj0gdtXR1Nr0Z2ND2XbLMzu75c1pmyrPloNnV/z3mcgEezzPVBLH6kWDyEOH2bKFybWdzmWgNU5k9GT/7W7zpP3nctuGkHhNLsi7XMs7c07kj2JXfz1ze9rHsKqrpooZSu/74KsG5d9ftyX9jgFce1sBwJfu5hx5G6NDxvtdGftqwj39bmZeX3s5Lphq52DRit/W7/dsPrq/x71vYAAPCk9nv3dP9VEuH2wzhJ00ni3t3v25mLWCb3/Yr2X+M+dhmRPqhVD++qdF5zpqX8bR+O3mufrpJJrfrc0V3S3Oa0/T3zcQIeykLXB7H4/mPxEOL0zaNwbU7l1mxtaY/vBFI7gKz+3flqlq8b+11Xtct9UcgpHnckqNO5C6en48JO2ca8FW46+yplDT6nX6MbOjPM3EsQbAeW8fqXpvgaBaqoaupegvKx0nxzC83yL41gOXlZDfJbocvL65c19OxTr+oUUpbhD4Qs980tUwf79RnbAwDAsyrr1Ll5lXTHVh80RjUJqlrpx7Xw06bzNSxOkIzHmPv0qPSBE9IuLq128J0+a9olpLsKu873RGt/hHWW/RFvc/r+nvc4AY9lmeuDWHzfsXgIcfo+PHfhmn8bSd8w8YIMtZpybZscn4Jy4W+K6qQMTwa6aGGRBg8/rQaMN+NjxPuEouJsUwUnP6eqNthAIZstGNQPmSneNq323LoeO1k70ajVlZkvdWnU8XaV39yyZPq4mlfSstpk2vitKXIzaMwmSeL2AAAAe99erdb2bXP6sLCuhaC10teSWevpvyZxuuaT+4WFtIvma6q0Wr10SRdoussn2CQTdMtdR2jGVJtO6aDpXa39YR/uFgejvXP3Sd3fFz1OwJ1Z5PogFld/3ngsHkKcvk/UXLshtlDp6LzWarDVp3Kw3eMx+wTAluC3C9mO26I3CgY7r63c5O46jgv54iao7cpefU0oU5cV02A6vpPO8bLNpirYm7A9AADcP9+Bczz4jNTQbzHJ5Ni0R1WDwNY4kM+HnXvAqPPpfHCZOt3l1GmAnk6fRZ0mkozoySTbHPs7hTYDkvUrq6Gm3ZB8vWhfRcD9u9Z1fAqx+PZj8RDi9L167sI1CR5VFdKeYaBUuEtoj3xUSl6a7VZLm0Weu8Kb8UIngkm0BL9dyKZt0b821jF0ZqhPJVwpeXvwsbRRyNfblLK/CWXysi6iLtgbuz0AAEBkuXmLas17WR51V9FVMzxxuik1+s81ptPnOE10yXWbJjMb36WGGw6HnSnsild9FfU1pUrdptvdF8D1LXJ9EIvvIBYPIU7fK2quzUkCTxV3SlPYt1VWBUX6r+0iTC6UYqhjsEW5QraDf/Ig69jT5tKXkrcHr9nhoVz8fpviYBuaUObye2/o61yODt5Q54pLyevStcnbAwDAfcrNLkrIV4PrpmHwt3HqDpGnOZ5OO712H4dIRqFKTUzs2LtT3enzfJbd31NkkqHe2OZV1d/at0/9ADZ1f1/jOAGXlnodX+/6IBa33U4sHkKcvg8Urs1JTnLbuaLWTrNnqpyItqBIq9hqx/3LNGWcJNP+4NxniU7hmvRO1eaT4dDeiFAbb6/lUVbd9HOgpl7Ksi4h2p6ti1qjtgcAgCcUMl2S5pmS70mdzhuq3R466J5F3UXHIwv9A0uKZ//tKIWYvL8vd5yA+zPn9UEsfnzE6dtG4dqMqmaEWjttZwvS6kKigzns2h3335bQ9FQunuPL9JRcy5ysah/UTShDLbDIecu6hNxsXNXncv9N1nF4ewAAeGqvmUvs97+mvzNxnjRdlLkaSEeEpkNzPxQbSruEWu6yaQ/zeD91f1/5OAE3baHrg1hcechYPIQ4fSsoXJuNr6aqpciultNNqmuX6dXkw039xGJvOgrBT2o0pdzXTSj917FzlzULCRIdt5YgdISp63hiewAAeGrZq6nu7H1dTtQPqRqJ88TpQpqj763i8dvkpt64e9IHJ5cpQi33O00v1OvfzJCm7u9FjxNw5xa5PojF1r3H4iHE6dtG4dps6pLfstBXFUdvFfEd9a+3Zu9LfhdTvdXEL6uxtFJ+W/k3nLT6f4v7i/sq43SsprbtrqdvkYutmps2pXQXffiu5dxlnSM8mdFCQLdg3U/tdQgdYco62lcfi77tAQDgqdU1vu3Linw6QEnaYytpINttRjvtkTpdSEfoZCtJ+IepbPphtXL37YG3yR05lT5oLbP5tjbXwXS1srJY/+bx21JuV5ImXdv91Uz3yPrLb379j/Zb6v5e4jgBjyL5+tB44/OY22qcgFis3916LK7Ws/sYEqfv3MdE/84crjbMZZebD910k+/cNz12eTWeyT6KxuIPH3IS2t+as6i/12myrBqqv+sha8ysb161Q+HmcWp9rd2HnPeN5R0PWc+yZNqw/tV41TbE3+UyVrewX920zX3WlrKs0/uqMjRefIzqoXlMKmG/2+HU9gAA8My676/10Jf2SJzuUHxIfqBjfDdk/emVbiPSB6eWKUM2nECZTTONMjBE6zNqmr79lrq/Zz9OwANJuj7ivF7X78RiHW45Fg8dQ+L0faPm2pz2/oUG2lH/wRwO1SD72f69k0ihymI7f42sIDc7fVVvkZvM923myd8SaOw6+TeNNOm0up46rf6tJeZVqbnOKy902v43pNQdLIosN19ai286b1npMrN5k/1TLbQi65p3rGy2iZ52nNweAACemdxfG/d1T9Me1UudutMeidNlG3PQtFXuazk4yWmIEekDv8yudZVxdV0P3Rt5E7KNpktlG3WfNdZffpP1L3bV792HKXF/z36cgAeSdH28amOaioznGk5FiMW3HouHjiFx+r69aAmb+zzKv3+pqwpe2r/UMtWbpc0xtRmjXNC9r+j142SmkIv+6m8OxQllqAadFRLIOGAAAAAAAKCFmmtz0Y783cde5ftgJ/q4MeFNM1lnzTYAAAAAAAAK1+YSdb4YOvSPaWeQX32HgDQxvAf7LccLAAAAAAAMo1nojI7eWJK5AjftS8x+IWw7cNot3z7fhFcOGU1CAQAAAABAj8mFaximr6zVmmvvcYGa0A4I883GfGl3FIjbtF+bl7UWrQ31oQcAAAAAAJ4dhWsAAAAAAABAIvpcAwAAAAAAABJRuAYAAAAAAAAkonANAAAAAAAASPSwfa69vLy4TwAAAAAAAMB0Y4rNeKEBAAAAAAAAkIhmoQAAAAAAAEAiCtcAAAAAAACARBSuAQAAAAAAAIkoXAMAAAAAAAASUbgGAAAAAAAAJKJwDQAAAAAAAEhE4RoAAAAAAACQiMI1AAAAAAAAIBGFawAAAAAAAEAiCtcAAAAAAACARBSuAQAAAAAAAIkoXAMAAAAAAAASUbgGAAAAAAAAJDHm/wensUSdq+MovgAAAABJRU5ErkJggg==)

# In[ ]:


# this code takes the above function (remapDNBR) where the dNBR threshold has been applied to the image'
# and applies a color coded map to each threshold as shown in the image above'


def showDNBR(dnbr):
    cmap = matplotlib.colors.ListedColormap(
        [
            "blue",
            "teal",
            "green",
            "yellow",
            "orange",
            "red",
            "purple",
        ]
    )
    plt.imshow(remapDNBR(dnbr), cmap=cmap)


showDNBR(dnbr_remapped)


# # Further Reading
# 
# 
# *   [Forest ecosystems, disturbance, and climate change in Washington State, USA | US Forest Service Research and Development Fire Ecology and Monitoring at Yosemite](https://www.fs.usda.gov/research/treesearch/38936)
# *   [Fire Ecology and Monitoring at Yosemite](https://www.nps.gov/yose/learn/nature/fireecology.htm)
# *   [A Project for Monitoring Trends in Burn Severity | Fire Ecology | Full Text](https://fireecology.springeropen.com/articles/10.4996/fireecology.0301003)
# *   [The unequal vulnerability of communities of color to wildfire | PLOS ONE ](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0205825)
# *   [Fire Frequency, Area Burned, and Severity: A Quantitative Approach to Defining a Normal Fire Year](https://fireecology.springeropen.com/articles/10.4996/fireecology.0702051)
# *   [Identifying Key Drivers of Wildfires in the Contiguous US Using Machine Learning and Game Theory Interpretation - Wang - 2021 - Earth's Future - Wiley Online Library](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020EF001910)
# *   [Science, technology, and human factors in fire danger rating: the Canadian experience](https://www.researchgate.net/publication/237505534_Science_technology_and_human_factors_in_fire_danger_rating_the_Canadian_experience)
# *   [Wildfire Selectivity for Land Cover Type: Does Size Matter?](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0084760)
# *   [Vegetation, topography and daily weather influenced burn severity in central Idaho and western Montana forests](https://esajournals.onlinelibrary.wiley.com/doi/full/10.1890/ES14-00213.1)
# 
# 
# Socio-economic effects of wildfires
# 
# * Zhao, J. et al. (2020). Quantifying the Effects of Vegetation Restorations on the Soil Erosion Export and Nutrient Loss on the Loess Plateau. Front. Plant Sci. 11 [https://doi.org/10.3389/fpls.2020.573126](https://www.frontiersin.org/articles/10.3389/fpls.2020.573126/full)
# * Amanda K. Hohner, Charles C. Rhoades, Paul Wilkerson, Fernando L. Rosario-Ortiz (2019). Wildfires alter forest watersheds and threaten drinking water quality. Accounts of Chemical Research. 52: 1234-1244. [https://doi.org/10.1021/acs.accounts.8b00670](https://doi.org/10.1021/acs.accounts.8b00670)
# * Alan Buis (2021). The Climate Connections of a Record Fire Year in the U.S. West. [Link](https://climate.nasa.gov/explore/ask-nasa-climate/3066/the-climate-connections-of-a-record-fire-year-in-the-us-west/)
# * Ian P. Davies ,Ryan D. Haugo,James C. Robertson,Phillip S. Levin (2018). The unequal vulnerability of communities of color to wildfire.PLoS ONE 13(11): e0205825. [https://doi.org/10.1371/journal.pone.0205825](https://doi.org/10.1371/journal.pone.0205825)
# 
# 
# Wildfires and forest ecosystems
# *   [Controlled fires](https://smokeybear.com/es/about-wildland-fire/benefits-of-fire/prescribed-fires)
# *   [Argentina on fire: what the fire left us | Spanish (pdf)](https://farn.org.ar/wp-content/uploads/2020/12/DOC_ARGENTINA-INCENDIADA_links.pdf)
# *   [Forest fires and biological diversity](https://www.fao.org/3/y3582s/y3582s08.htm)
# 
# 
