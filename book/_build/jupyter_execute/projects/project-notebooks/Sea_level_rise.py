#!/usr/bin/env python
# coding: utf-8

# # **Sea Level Rise**
# 
# **Content creators:** Aakash Sane, Karsten Haustein
# 
# **Content reviewers:** Brodie Pearson, Abigail Bodner, Jenna Pearson, Chi Zhang, Ohad Zivan 
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


# Sea level, or Sea Surface Height [SSH], describes the vertical position of the interface between the atmosphere and the ocean. It varies at numerous timescales attributable to different physical factors, such as hourly tides, daily to monthly perturbations caused by currents and storms, and alterations spanning several decades to centuries due to thermal expansion of seawater and the reduction of mass resulting from glaciers and ice sheets. Read more: [NOAA 2022 Sea level rise technical report](https://oceanservice.noaa.gov/hazards/sealevelrise/sealevelrise-tech-report.html).
# 
# **In this project**, you will work on sea level rise data from ECCO model (recall W1D2 tutorial 4 outputs) and tidal gauge datasets.

# # Project Template
# ![Project Template](https://raw.githubusercontent.com/ClimateMatchAcademy/course-content/main/projects/template-images/sea_level_rise_template_map.svg)
# 
# *Note: The dashed boxes are socio-economic questions.*

# # Data Exploration Notebook
# ## Project Setup
# 

# In[ ]:


# imports
import random
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import os
import pooch


# ## ECCO Sea Surface Height (SSH)
# 
# In this project, you will analyse sea surface height (SSH) data using the ECCO reanalysis product which combines simulations and observations. ECCO stands for Estimating the Circulation and Climate of the Ocean and integrates observations with coupled ocean/sea-ice models. The netCDF data file contains SSH stored as monthly means from the year 1992 to 2017 on a 0.5 x 0.5 degree grid. Using the ECCO product, global and regional sea level obtained due to physical effects (such as thermal expansion of sea water, etc.) can be estimated. Further details about the dataset can be obtained [here](https://ecco-group.org/).
# 
# The sea surface height variable is called 'SSH' in the data. It is a variable with three gridded dimensions: time, latitude, and longitude. The code below shows how to load the SSH dataset and provides plotting examples. One example plots the time-series at a particular latitude and longitude while another example plots a colormap on the global grid. Those examples should equip you to tackle many of the questions on the template, so go ahead and explore! 
# 
# Further resources about the dataset:
# 
# - ECCO Consortium, Fukumori, I., Wang, O., Fenty, I., Forget, G., Heimbach, P., & Ponte, R. M. (DATE ACCESSED). ECCO Central Estimate (Version 4 Release 4). Retrieved from https://podaac.jpl.nasa.gov/dataset/ECCO_L4_GMSL_TIME_SERIES_MONTHLY_V4R4.
# 
# - ECCO Consortium, Fukumori, I., Wang, O., Fenty, I., Forget, G., Heimbach, P., & Ponte, R. M. (2021, February 10). Synopsis of the ECCO Central Production Global Ocean and Sea-Ice State Estimate (Version 4 Release 4). https://doi.org/10.5281/zenodo.4533349
# 
# - Forget, G., J.-M. Campin, P. Heimbach, C. N. Hill, R. M. Ponte, and C. Wunsch, 2015: ECCO version 4: An integrated framework for non-linear inverse modeling and global ocean state estimation. Geoscientific Model Development, 8. https://www.geosci-model-dev.net/8/3071/2015/
# 

# In[ ]:


# data source:   https://pangeo-forge.org/dashboard/feedstock/7
# CMIP6.CMIP.CCCma.CanESM5.historical.r1i1p1f1.Omon.zos.gn.v20190429.zarr
url_ECCO = "~/shared/Data/Projects/Sea_Level/SEA_SURFACE_HEIGHT_mon_mean_1992-01-2017-12_ECCO_V4r4_latlon_0p50deg.nc"
ds = xr.open_dataset(url_ECCO)
ds


# In[ ]:


ds["SSH"][:, 200, 134].plot()


# In[ ]:


ds["SSH"][100, :, :].plot.pcolormesh()


# ## Observations Dataset: Tidal Gauges
# 
# Students can download any tidal gauge data of their choice from this **[website](https://uhslc.soest.hawaii.edu/data/)**
# 
# It is recommended to download the NetCDF **'daily'** data for a particular location and it can be compared to the nearest latitude-longitude from the ECCO dataset. When you download the tidal gauge data, you can select a location, right click on the NetCDF of the data you want, copy link address and paste as the url below.
# 
# The file will have the sea level stored as a variable called **'sea_level'**, which is a function of time. It can be fun to explore how close the tidal gauge data agree (or disagree) with the ECCO data!

# In[ ]:


# students can download any tidal gauge data of their choice from this website:
# https://uhslc.soest.hawaii.edu/data/
# instructions: select a location, right click on the netcdf of the data you want, copy link address and paste as the url below


# In[ ]:


# data source-specific functions
url_choosen = "https://uhslc.soest.hawaii.edu/data/netcdf/fast/daily/d825.nc"  # this is the link for "Cuxhaven Germany", change to your location
# example code after downloading tidal gauge data:
ds = xr.open_dataset(
    pooch.retrieve(url_choosen, known_hash=None)
)  # this is just an example, tidal gauge NetCDF file needs to be downloaded in order to load this.
ds


# # Further Reading
# 
# - 2022 Sea Level Rise Technical Report
# https://oceanservice.noaa.gov/hazards/sealevelrise/sealevelrise-tech-report-sections.html
# 
# - Oppenheimer, M., B.C. Glavovic , J. Hinkel, R. van de Wal, A.K. Magnan, A. Abd-Elgawad, R. Cai, M. Cifuentes-Jara, R.M. DeConto, T. Ghosh, J. Hay, F. Isla, B. Marzeion, B. Meyssignac, and Z. Sebesvari, 2019: Sea Level Rise and Implications for Low-Lying Islands, Coasts and Communities. In: IPCC Special Report on the Ocean and Cryosphere in a Changing Climate [H.-O. Pörtner, D.C. Roberts, V. Masson-Delmotte, P. Zhai, M. Tignor, E. Poloczanska, K. Mintenbeck, A. Alegría, M. Nicolai, A. Okem, J. Petzold, B. Rama, N.M. Weyer (eds.)]. Cambridge University Press, Cambridge, UK and New York, NY, USA, pp. 321-445. https://doi.org/10.1017/9781009157964.006. 
# 
# - Domingues, R., Goni, G., Baringer, M., &Volkov, D. (2018). What caused theaccelerated sea level changes along theU.S. East Coast during 2010–2015?Geophysical Research Letters,45,13,367–13,376. https://doi.org/10.1029/2018GL081183Received 
# 
# - Church, J.A., P.U. Clark, A. Cazenave, J.M. Gregory, S. Jevrejeva, A. Levermann, M.A. Merrifield, G.A. Milne, R.S. Nerem, P.D. Nunn, A.J. Payne, W.T. Pfeffer, D. Stammer and A.S. Unnikrishnan, 2013: Sea Level Change. In: Climate Change 2013: The Physical Science Basis. Contribution of Working Group I to the Fifth Assessment Report of the Intergovernmental Panel on Climate Change 
# [Stocker, T.F., D. Qin, G.-K. Plattner, M. Tignor, S.K. Allen, J. Boschung,
# A. Nauels, Y. Xia, V. Bex and P.M. Midgley (eds.)]. Cambridge University Press, Cambridge, United Kingdom and New York, NY, USA. https://www.ipcc.ch/site/assets/uploads/2018/02/WG1AR5_Chapter13_FINAL.pdf 
# 
# - Gregory, J.M., Griffies, S.M., Hughes, C.W. et al. Concepts and Terminology for Sea Level: Mean, Variability and Change, Both Local and Global. Surv Geophys 40, 1251–1289 (2019). https://doi.org/10.1007/s10712-019-09525-z
# 
# - Wang, J., Church, J. A., Zhang, X., Gregory, J. M., Zanna, L., & Chen, X. (2021). Evaluation of the Local Sea‐Level Budget at Tide Gauges Since 1958. Geophysical Research Letters, 48(20), e2021GL094502.  https://doi.org/10.1029/2021GL094502 
# 
# - Cazenave, A. and Cozannet, G.L. (2014), Sea level rise and its coastal impacts. Earth's Future, 2: 15-34. https://doi-org.ezproxy.princeton.edu/10.1002/2013EF000188
# 
# - Mimura N. Sea-level rise caused by climate change and its implications for society. Proc Jpn Acad Ser B Phys Biol Sci. 2013;89(7):281-301. doi: 10.2183/pjab.89.281. PMID: 23883609; PMCID: PMC3758961. doi: [10.2183/pjab.89.281](https://www.jstage.jst.go.jp/article/pjab/89/7/89_PJA8907B-01/_article)
# 
# 
