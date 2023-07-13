#!/usr/bin/env python
# coding: utf-8

# # **Tutorial 2: Exploring Satellite Climate Data Records**
# 
# **Week 1, Day 3, Remote Sensing**
# 
# **Content creators:** Douglas Rao
# 
# **Content reviewers:** Katrina Dobson, Younkap Nina Duplex, Maria Gonzalez, Will Gregory, Nahid Hasan, Sherry Mi, Beatriz Cosenza Muralles, Jenna Pearson, Agustina Pesce, Chi Zhang, Ohad Zivan
# 
# **Content editors:** Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Production editors:** Wesley Banfield, Jenna Pearson, Chi Zhang, Ohad Zivan
# 
# **Our 2023 Sponsors:** NASA TOPS and Google DeepMind

# # **Tutorial Objectives**
# 
# In this tutorial, you will enhance your understanding of several key concepts and tools crucial in the field of satellite remote sensing for climate applications. Specifically, by the end of this session, you should be able to:
# 
# - Grasp the principle of inter-satellite calibration, a critical step in creating reliable climate data records.
# - Familiarize yourself with an array of long-term satellite remote sensing datasets that are tailored for climate applications, brought to you by three leading data providers: NOAA, NASA, and ESA.
# - Navigate and utilize these datasets in your own climate-related studies or projects.
# 

# ##  Video 1: Video 1 Name
# 

# ###  Video 1: Video 1 Name
# 

# ####  Video 1: Video 1 Name
# 

# In[ ]:


# @title Video 1: Video 1 Name
# Tech team will add code to format and display the video


# # **Section 1: Satellite Climate Data Records**
# 
# You have already seen some examples of how satellite remote sensing data can be used for climate research and applications. But are all satellite data "created equal" for these purposes? There are a lot of considerations that need to be taken into account when using satellite data to monitor the long-term change of different components of the Earth system. In this section you will explore some of these considerations. Many of these are outlines in the definition of a climate data record given below.
# 
# **Satellite Climate Data Records**
# 
# In 2004, a committee convened by the US National Research Council defined a [***Climate Data Record (CDR)***](https://www.ncei.noaa.gov/products/climate-data-records) is "a time series of measurements of sufficient length, consistency and continuity to determine climate variability and change." Although there are no specific number to determine the "sufficient length", the typical climate length is considered to be at least 30 years. To achieve a stable, consistent, and reliable satellite CDR, we need to carefully calibrate the raw satellite data. 
# 

# ## **Section 1.1: Satellite Missions for Environmental Monitoring**
# 
# When it comes to monitoring environmental and climate changes in a region using weather stations, we have confidence in the data quality due to regular inspections and maintenance of these stations and instruments. In North America and Europe, for instance, there are numerous weather stations that have been operating for over a century, providing reliable long-term data.
# 
# In contrast, a single satellite mission has a **designed operational lifespan of 5-8 years**, and over time, the sensors on these satellites can deteriorate. While some satellites like Terra and Aqua have exceeded their designed lifespan and continue to operate successfully for more than 20 years, **relying on a single satellite for climate monitoring and applications is exceedingly challenging**, if not impossible.
# 
# Thankfully, we have a range of satellite platforms at our disposal that operate continuously and carry similar remote sensors, making it feasible to utilize multiple satellites together for climate-related purposes. Since the 1970s, dozens of satellites, including both polar-orbiting and geostationary satellites, have been designed for weather and environmental monitoring. While not originally intended for climate studies, researchers have developed methods to merge data from various satellite platforms, enabling the creation of robust long-term time series of satellite data. Moreover, future satellite missions are being carefully designed to extend these data records further.
# 
# The image below illustrates a timeline showcasing a selection of polar-orbiting satellite missions whose data are commonly employed to generate satellite Climate Data Records (CDRs). 
# 
# ![satellite_timeline](./asset/img/t2_satellite_timeline.png)
# 
# Credit: Douglas Rao

# The above figure shows the variety of satellite lifespans - some satellites only operated 3-5 years while there are a handful of satellite missions that operated for more than 15 years. Most importantly, we usually have at least two satellite missions operating during the same time period.
# 
# The overlap among satellite missions is critical for generating satellite CDRs, as we can compare the data during the overlapping time period and account for the systematic differences between satellite missions.
# 
# Meanwhile, there is significant technological advancement in remote sensors aboard different satellite missions. These different generations of remote sensors are identified by the solid grey lines in the figure. As indicated in the figure above, we have seen three major upgrades in sensor technologies. **NOTE: these sensor changes also need to be accounted for when creating satellite CDRs.**

# ## **Section 1.2: Inter-satellite Calibration**
# 
# As noted in the previous section, the change in satellite missions and remote sensors make it hard to use remotely sensed data "as it is" for climate applications. These changes often cause systematic differences in raw satellite data (see image below).
# 
# This figure is exagerating the possible systematic differences between raw data collected by different satellite missions. Nonetheless, **these systematic differences can often cause large uncertainty for climate science when not addressed properly.**
# 
# ![t2_calibration](./asset/img/t2_calibration_pt1.png)

# To address the differences that are caused by sensor and satellite changes, we often perform an **inter-satellite calibration** - which adjusts the raw data collected by different satellites to a pre-defined reference to remove or minimize the systematic difference between data. This pre-defined reference is usually determined using data during there perioud of time when the satellites overlap (see image below). But we can also use other high quality reference data like surface observations, theoretical bases, or other ancillary data. Click [here](https://www.eumetsat.int/inter-calibration) for more information on **inter-satellite calibration**.
# 
# ![t2_calibration_pt2](./asset/img/t2_calibration_pt2.png)

# A **well-calibrated multi-satellite date record** is often assessed by examining the differences between satellite data during the overlapping time period. Once we are confident that the differences are minimal or within an accepted range, the long term time series based on multiple satellites can be used for climate applications.
# 
# The inter-satellite calibration step is the key to ensure that climate signals can be accurately reflected in the satellite data and not affected by the noise caused by change in satellite platforms and sensors. Therefore, when you are choosing satellite data for climate applications, you should be asking yourself a few questions:
# 
# * Are the data that you are planning to use collected by the same sensor and satellite?
# * If the data are from multiple satellites/sensors, are there steps to ensure the data are consistent across difference satellites/sensors?
# * Can you find out how the inter-satellite calibration is done and what is the level of difference between satellites/sensors?
# 
# These questions will help you determine if the remotely sensed data is appropriate for climate applications that you are interested in.
# 
# ![t2_calibration_pt3](./asset/img/t2_calibration_pt3.png)

# ### **Questions 1.2: Climate Connection**
# 
# Assuming that you are interested in using remote sensing data to understand how the rainfall amount and frequency have changed for the region that you are in since 1990. There are three different satellite data that you can choose from:
# 
# * _Option A_: Data from the most recent satellite missions designed to monitor global precipitation. The satellite has the most accurate sensor and the satellite was launched in 2014. 
# * _Option B_: Data from three different satellite missions that carry similar sensors (first satellite: 1985-1994; second satellite: 1992-2006; third satellite: 2003-present).
# * _Option C_: Data from the three different satellite missions described in _Option B_ that has been calibrated using long term surface measurements of rainfall in your region. 
# 
# Can you choose the best data for your application? Why would you make this choice? Do you need more information to make the decision?
# 
# 

# [*Click for solution*](https://github.com/ClimateMatchAcademy/course-content/tree/main/tutorials/W1D3_RemoteSensingLandOceanandAtmosphere/solutions/W1D3_Tutorial2_Solution_1c4dc0c2.py)
# 
# 

# # **Section 2: Finding Satellite Climate Data Records**
# 
# Finding the right satellite Climate Data Records (CDRs) for your desired application can be a challenge. In this section, we will explore satellite data from three major remote sensing data providers: the **National Atmospheric and Oceanic Administration (NOAA), the National Aeronautics and Space Administration (NASA), and the European Space Agency (ESA)**. While we won't cover the code to analyze the data in this tutorial, you will learn how to do that in the upcoming tutorials.
# 

# ## **Section 2.1: NOAA Climate Data Records**
# 
# The **National Atmospheric and Oceanic Administration (NOAA)** implemented the recommendation from the US National Research Council to develop satellite-based climate data records in the 2000s, and they have maintained a suite of operational CDRs that can be used to study different aspects of the changing climate system since then.
# 
# All NOAA CDR data are available freely to the public via [NOAA National Centers for Environmental Information](https://www.ncei.noaa.gov/products/climate-data-records). Recently, the [NOAA Open Data Dissemination Program](https://www.noaa.gov/information-technology/open-data-dissemination) also made all NOAA CDRs available on three major commercial cloud service providers (i.e., Amazon Web Service, Google Cloud, and Microsoft Azure). The NOAA Climate Data Records (CDRs) are available to anyone interested in accessing the data and are typically free of charge.
# 
# NOAA CDRs have two different categories with different purposes:
# 
# * _Fundamental CDR (FCDR)_: This category consists of high-quality, low-level processed satellite sensor data, such as reflectance and brightness temperature. The FCDR datasets are carefully calibrated between satellites and sensors to ensure accuracy and consistency. These datasets are primarily used to assess and improve Earth system models (which you will learn about next week).
# * _Thematic CDR_: Thematic CDRs provide valuable information for understanding climate processes and changes in various domains.  The thematic CDRs are divided into terrestrial, atmospheric, and ocean categories to reflect the different components of the climate system.
# 
# The table below lists a selection of thematic CDRs operates by NOAA. You can find out more about all NOAA CDRs by visiting the specific webpage of each CDR categories:
# 
# * [Fundamental CDR](https://www.ncei.noaa.gov/products/climate-data-records/fundamental) - 16 datasets
# * [Thematic CDR: Terrestrial](https://www.ncei.noaa.gov/products/climate-data-records/terrestrial) - 4 datasets
# * [Thematic CDR: Atmospheric](https://www.ncei.noaa.gov/products/climate-data-records/atmospheric) - 18 datasets
# * [Thematic CDR: Oceanic](https://www.ncei.noaa.gov/products/climate-data-records/oceanic) - 5 datasets

# | Dataset | Category | Start Year | Frequency | Spatial Resolution | Example Application Areas |
# |:--|:--:|:--:|:--:|:--:|:--|
# |Leaf Area Index and FAPAR|Terrestrial|1981|Daily|0.05°| Vegetation status monitoring; Agriculture monitoring; Crop yield/food security|
# |Normalized Difference Vegetation Index (NDVI)|Terrestrial|1981|Daily|0.05°|Vegetation status monitoring; Vegetation phenology study|
# |Snow Cover Extent (Northern Hemisphere)|Terrestrial|1966|Weekly (prior 1999-06) <br><br> Daily (post 1999-06)|~190 km| Hydrology; Water resources; Snow-climate feedback|
# |Aerosol Optical Thickness|Atmospheric|1981|Daily & Monthly|0.1°|Air quality; Aerosol-climate feedback|
# |PATMOS-x Cloud Properties|Atmospheric|1979|Daily|0.1°|Cloud process; Cloud-climate feedback|
# |Precipitation - PERSIANN|Atmospheric|1982|Daily|0.25° <br><br> (60°S–60°N)|Hydrology; Water resources; Extreme events|
# |Sea Surface Temperature - Optimum Interpolation|Oceanic|1981|Daily|0.25°|Climate variability; Marine heatwave; Marine ecosystem|
# |Sea Ice Concentration|Oceanic|1978|Daily & Monthly|25 km|Crosphere study; Wildlife conservation; Ocean/climate modeling|

# ## **Section 2.2: ESA Climate Change Initiative**
# 
# The **European Space Agency (ESA)** initiated a similar effort to develop consistent satellite-based long-term records to support the mission of climate monitoring for societal benefits in late 2010s. **[ESA Climate Change Initiative (CCI)](https://climate.esa.int/en/esa-climate/esa-cci/)** has established more than 26 projects to develop satellite-based CDRs and directly engage with downstream users.
# 
# Through CCI, there is very strong emphasis on applications to support the monitoring of [**essential climate variables** (ECVs) defined by Global Climate Observing System (GCOS)](https://public.wmo.int/en/programmes/global-climate-observing-system/essential-climate-variables). An ECV is defined as "a physical, chemical or biological variable or a group of linked variables that critically contributes to the characterization of Earth’ s climate."
# 
# The table below lists a selection of ESA CCI datasets and their example application areas.

# | Dataset | Category | Duration | Frequency | Spatial Resolution | Example Application Areas |
# |:--|:--:|:--:|:--:|:--:|:--|
# |Sea Level|Oceanic|1992-2015|Monthly|0.25°|Sea level rise; Ocean modeling|
# |Water Vapor|Atmospheric|1985-2019|Monthly|5°|Water vapor-climate feedback; Hydrology|
# |Fire|Terrestrial|1981-2020|Monthly|0.05° (pixel dataset) <br><br> 0.25° (grid dataset)|Ecosystem disturbance; Extreme events; Social impact|
# |Land Cover|Terrestrial|1992-2020|Yearly|300 m|Terrestrial modeling|
# |Soil Moisture|Terrestrial|1978-2021|Daily|0.25°|Hydrology; Ecosystem impacts; Extreme events|

# You may observe that some datasets do not span the typical duration necessary for climate studies (for instance, 30 years). This occurrence is influenced by a variety of factors such as:
# 
# - Legacy sensors were not designed or capable of accurately capturing the ECVs of interest.
# - The CCI project is executed in stages, initiating with the most recent satellite missions/sensors. However, plans are underway to incorporate older data from heritage satellite missions/sensors.
# 
# Moreover, each ESA CCI project frequently offers different versions of ECV variables, each designed for specific applications. The specifications of these ECV variables might deviate from the table above if they represent a subset of the time period, utilizing data from the latest sensors. The table primarily provides information on the longest time record for each CCI.
# 
# All ESA CCI data are openly accessible and free of charge to users without any restrictions. All these resources can be accessed via the [**ESA CCI Open Data Portal**](https://climate.esa.int/en/odp/#/dashboard).
# 
# To further assist users in accessing and analyzing the CCI data, ESA has also developed the [**CCI Analysis Toolbox (Cate)**](https://climate.esa.int/en/explore/analyse-climate-data/). It is described as a "cloud-enabled computing environment geared for scientists who need to analyze, process, and visualize ESA’s climate data and other spatiotemporal data."
# 

# ## **Section 2.3: NASA Earth System Data Records**
# 
# Similar to other two satellite data providers, the **National Aeronautics and Space Administration (NASA)** also produces and distributes long-term satellite-based data records that may be suitable for different climate applications. NASA [Earth System Data Records (ESDRs)](https://www.earthdata.nasa.gov/esds/competitive-programs/measures?page=0) are defined as "as a unified and coherent set of observations of a given parameter of the Earth system, which is optimized to meet specific requirements in addressing science questions."
# 
# While NASA's ESDR does not specifically target climate, these records are often created to monitor and study various components of the climate system. For instance, surface temperature, global forest coverage change, atmospheric compositions, and ice sheet velocity are all areas of focus.
# 
# The table below showcases a selection of NASA ESDRs datasets that nicely complement the satellite Climate Data Records (CDRs) offered by NOAA and ESA.

# | Dataset | Category | Duration | Frequency | Spatial Resolution | Example Application Areas |
# |:--|:--:|:--:|:--:|:--:|:--|
# |[Sulfur Dioxide](https://www.earthdata.nasa.gov/esds/competitive-programs/measures/multi-decadal-sulfur-dioxide)|Atmospheric|1978-2022|Daily|50 km|Atmospheric modeling; Air quality|
# |[Ozone](https://disc.gsfc.nasa.gov/datasets/MSO3L3zm5_1/summary)|Atmospheric|1970-2013|Monthly|5°|Ozone monitoring; Air quality|
# |[Sea Surface Height](https://podaac.jpl.nasa.gov/dataset/SEA_SURFACE_HEIGHT_ALT_GRIDS_L4_2SATS_5DAY_6THDEG_V_JPL2205)|Oceanic|1992-ongoing|5-Day|1/6°|Sea level rise; Ocean modeling|
# |[GPCP Satellite-Gauge Combined Precipitation Data](https://disc.gsfc.nasa.gov/datasets/GPCPMON_3.2/summary)|Atmospheric|1983-2020|Daily & Monthly|0.5°|Hydrology; Extreme events|

# If you've visited the linked NASA ESDR page above, you may have noticed that it appears less structured compared to the NOAA CDR program and the ESA CCI open data portal. This is partly because NASA operates different data centers for distinct application areas (e.g., atmosphere, snow/ice, land, etc.). However, you can always visit [**NASA's Earth Data Search**](https://search.earthdata.nasa.gov/search) – a comprehensive portal for accessing datasets provided by NASA's Earth science data system. To access the data, you'll be required to create a user account. Rest assured, registration for the NASA Earthdata system is free and open to anyone.

# ### **Questions 2.3: Climate Connection**
# Now that you have been introduced to three major sources of remote sensing data for climate applications, it's time to identify the dataset that best suits your requirements. In this exercise, you can choose one or more data providers (NASA, NOAA, ESA) and explore their satellite data to determine which one aligns best with your application needs.

# In[ ]:


### Step 1: Describe your application interest. Be as specific as you can, this
### will help you narrow down your search for the data
"""

"""
### Step 2: Identify an ideal spatial and temporal resolution for your application
### (e.g., daiyl/weekly/monthly, 500 m/5 km/25 km/...?)
"""

"""
### Step 3: Explore the data from one of the data providers to see if there is
### any data that can fit your application need and explain why
"""

"""


# # **Summary**
# 
# In this tutorial, we learned about 
# 
# *   how **Inter-satellite calibration** is a critical step to produce a consistent remote sensing dataset for climate applications and allows us to use data from different satellites and sensors over different but overlappign time-periods.
# *   **major collections of satellite-based datasets** for climate applications, including NOAA Climate Data Records, ESA Climate Change Initiative, and NASA Earth System Data Records.
# 
# In the upcoming tutorial, we will be transitioning towards exploring how to utilize computational tools to access publicly available remote sensing data for climate applications.
# 
