import xarray as xr

def get_range(da):
    return  ( int(da.min().round() - 1), int(da.max().round() + 1),)

def load_csv(path='./data/zarr_table.csv'):
    import pandas as pd
    df = pd.read_csv(path,index_col=None)
    return df.sort_values(by="year") #inplace=True)

def load_bathymetry(path='./data/bathy6min.nc'):
    return xr.open_dataset(path, decode_times=False, use_cftime=True)

def load_zarr(path='./data/1H_file.zarr'):
    from datatree import open_datatree
    return open_datatree(path, engine='zarr')

def load_file(tree,selected_file):
    return tree[selected_file+"/"].ds

def filter_df(sorted_df,selected_file):
    # include  user_interface_url here
    dataframe = sorted_df[sorted_df["file_name"] == selected_file].drop(
                columns=[
                    "file_name",
                    "title",
                    "Conventions",
                    "featureType",
                    "date_update",
                    "ADCP_beam_angle",
                    "ADCP_ship_angle",
                    "middle_bin1_depth",
                    "heading_corr",
                    "pitch_corr",
                    "ampli_corr",
                    "pitch_roll_used",
                    "date_creation",
                    "ADCP_type",
                    "data_type",
                ]
            )
    # include  LOCAL_CDI_ID here
    dataframe2 = sorted_df[sorted_df["file_name"] == selected_file].drop(
                columns=[
                    "file_name",
                    "date_start",
                    "date_end",
                    "ADCP_frequency(kHz)",
                    "bin_length(meter)",
                    "year",
                ]
            )
    return dataframe.transpose(), dataframe2.transpose()

def filter_data(ds,longitude_range,latitude_range):
    return ds.where(
        (ds.LONGITUDE >= longitude_range[0])
        & (ds.LONGITUDE <= longitude_range[1])
        & (ds.LATITUDE >= latitude_range[0])
        & (ds.LATITUDE <= latitude_range[1]),
        drop=True,
    )


def quiver_depth_filtered(ax, ds, depth_range, scale_factor, color="blue"):
    """
    Plot quiver plot of mean current vectors filtered by depth.

    Parameters:
        ax (matplotlib.axes.Axes): The matplotlib axes object to plot on.
        ds (xarray.Dataset): The dataset containing the current data.
        depth_range (tuple): Tuple containing the minimum and maximum depth values for filtering.
        scale_factor (float): Scaling factor for the magnitude of the current vectors.
        color (str, optional): Color of the quiver arrows. Defaults to "blue".

    Returns:
        matplotlib.quiver.Quiver: The quiver plot object.
    """
    # Filter data based on depth range
    ds = ds.sel( PROFZ=slice(depth_range[1],depth_range[0]))

    # Calculate mean current vectors within the selected depth range
    u_mean = ds.UCUR.mean(dim="PROFZ", skipna=True)
    v_mean = ds.VCUR.mean(dim="PROFZ", skipna=True)

    # Extract longitude and latitude coordinates
    lon = ds.coords["LONGITUDE"].values
    lat = ds.coords["LATITUDE"].values

    # Plot quiver plot
    return ax.quiver(
        lon,
        lat,
        u_mean * scale_factor,
        v_mean * scale_factor,
        color=color,
        scale=2,
        width=0.001,
        headwidth=3,
        transform=ccrs.PlateCarree(),
    )

def bathy_uship_vship_bottom_depth(ds):
    """
    Plot maximum values of bathymetry, USHIP, VSHIP, and bottom depth over time.

    Parameters:
        ds (xarray.Dataset): Dataset containing the required variables.

    Returns:
        list: List of hvplot objects representing the plots of maximum values of bathymetry,
              USHIP, VSHIP, and bottom depth over time.
    """
    import hvplot.xarray
    return [
        ds["BATHY"].max(dim="PROFZ").hvplot(x="TIME", width=400, height=200),
        ds["USHIP"].max(dim="PROFZ").hvplot(x="TIME", width=400, height=200),
        ds["VSHIP"].max(dim="PROFZ").hvplot(x="TIME", width=400, height=200),
        ds["BOTTOM_DEPTH"].max(dim="PROFZ").hvplot(x="TIME", width=400, height=200),
    ]


def corsen_data(ds, sample):
    """
    Downsample the dataset `ds` based on the number of vectors specified by `sample`.

    Parameters:
        ds (xarray.Dataset): Dataset to be downsampled.
        sample (int): Number of vectors used for downsampling.

    Returns:
        xarray.Dataset: Downsampled dataset.
    """
    coords = ["LATITUDE", "LONGITUDE"]
    corsen = max(1, ds.TIME.size // sample)
    return (
        ds.reset_coords(coords)
        .coarsen({"TIME": corsen}, boundary="trim")
        .mean()
        .set_coords(coords)
    )



def vectors_plot(ds, bathy, longitude_range, latitude_range ,
                 depth_range, depth_2_range, depth_3_range,
                 scale_factor=0.5, sample=100,
                 depth_2_checkbox=False, depth_3_checkbox=False, bathy_checkbox=False):
    """
    Plot vectors filtered by depth on a map with specified features.

    Parameters:
        ds (xarray.Dataset): Dataset containing current data.
        bathy (xarray.Dataset): Dataset containing bathymetry data.
        longitude_range (tuple): Tuple containing the minimum and maximum longitude values.
        latitude_range  (tuple): Tuple containing the minimum and maximum latitude values.
        depth_range (tuple): Tuple containing the minimum and maximum depth values for filtering.
        depth_2_range (tuple): Tuple containing the minimum and maximum depth values for filtering depth 2.
        depth_3_range (tuple): Tuple containing the minimum and maximum depth values for filtering depth 3.
        scale_factor (float): Scaling factor for the magnitude of the current vectors.
        sample (int): Number of vectors used for downsampling.
        depth_2_checkbox (bool, optional): Whether to plot vectors for depth 2. Defaults to False.
        depth_3_checkbox (bool, optional): Whether to plot vectors for depth 3. Defaults to False.
        bathy_checkbox (bool, optional): Whether to plot bathymetry. Defaults to False.

    Returns:
        matplotlib.figure.Figure: The generated plot.
    """
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    # Create subplot with Mercator projection
    fig, ax = plt.subplots(figsize=(5, 4), subplot_kw={"projection": ccrs.Mercator()})

    # Apply data downsampling
    ds = corsen_data(ds, sample)

    # Plot vectors filtered by depth
    quiver_depth_filtered(ax, ds, depth_range, scale_factor, color="blue")
    if depth_2_checkbox:
        quiver_depth_filtered(ax, ds, depth_2_range, scale_factor, color="green")
    if depth_3_checkbox:
        quiver_depth_filtered(ax, ds, depth_3_range, scale_factor, color="red")

    # Add map features
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.add_feature(cfeature.LAND, color="lightgray")

    # Plot bathymetry if provided
    if bathy_checkbox:
        contour_levels = [-1000]
        ax.contour(bathy.longitude, bathy.latitude, bathy.z,
                   levels=contour_levels, colors="black", transform=ccrs.PlateCarree())

    # Set extent and add gridlines
    ax.set_extent([longitude_range[0], longitude_range[1],
                   latitude_range[0], latitude_range[1]])
    ax.gridlines(draw_labels=True)

    # Set labels and close plot
    plt.ylabel("Latitude", fontsize=15, labelpad=35)
    plt.xlabel("Longitude", fontsize=15, labelpad=20)
    #https://panel.holoviz.org/reference/panes/Matplotlib.html#using-the-matplotlib-pyplot-interface
    plt.close(fig) 
    return fig

def greg_0h(jourjul):
    import math
    import numpy as np

    # Julian days start and end at noon.
    # Julian day 2440000 begins at 00 hours, May 23, 1968.

    # Round the input Julian day number to avoid precision errors
    fac = 10**9
    jourjul = np.round(fac * jourjul + 0.5) / fac

    # Calculate seconds in the day
    secs = (jourjul % 1) * 24 * 3600

    # Round seconds to avoid precision errors
    secs = np.round(fac * secs + 0.5) / fac

    # Gregorian calendar conversion
    j = math.floor(jourjul) - 1721119
    in_ = 4 * j - 1
    y = math.floor(in_ / 146097)
    j = in_ - 146097 * y
    in_ = math.floor(j / 4)
    in_ = 4 * in_ + 3
    j = math.floor(in_ / 1461)
    d = math.floor(((in_ - 1461 * j) + 4) / 4)
    in_ = 5 * d - 3
    m = math.floor(in_ / 153)
    d = math.floor(((in_ - 153 * m) + 5) / 5)
    y = y * 100 + j
    if m < 10:
        mo = m + 3
        yr = y
    else:
        mo = m - 9
        yr = y + 1

    hour = math.floor(secs / 3600)
    mins = math.floor((secs % 3600) / 60)
    sec = secs % 60

    gtime = [yr, mo, d]

    return gtime

def greg_0hfull(jourjul):
    import math
    import numpy as np
    # Julian days start and end at noon.
    # Julian day 2440000 begins at 00 hours, May 23, 1968.

    # Round the input Julian day number to avoid precision errors
    fac = 10**9
    jourjul = np.round(fac * jourjul + 0.5) / fac

    # Calculate seconds in the day
    secs = (jourjul % 1) * 24 * 3600

    # Round seconds to avoid precision errors
    secs = np.round(fac * secs + 0.5) / fac

    # Gregorian calendar conversion
    j = math.floor(jourjul) - 1721119
    in_ = 4 * j - 1
    y = math.floor(in_ / 146097)
    j = in_ - 146097 * y
    in_ = math.floor(j / 4)
    in_ = 4 * in_ + 3
    j = math.floor(in_ / 1461)
    d = math.floor(((in_ - 1461 * j) + 4) / 4)
    in_ = 5 * d - 3
    m = math.floor(in_ / 153)
    d = math.floor(((in_ - 153 * m) + 5) / 5)
    y = y * 100 + j
    if m < 10:
        mo = m + 3
        yr = y
    else:
        mo = m - 9
        yr = y + 1

    hour = math.floor(secs / 3600)
    mins = math.floor((secs % 3600) / 60)
    sec = int(secs % 60)

    gtime = [yr, mo, d, hour, mins, sec]

    return gtime


def fix_time(ds):
    from datetime import datetime, timedelta

    time = ds["TIME"]
    time2 = time.dropna(dim="MAXT")
    time2 = time2.reindex_like(time, method="nearest")
    jourjul = [greg_0hfull(jourjul) for jourjul in time2.values]
    date = [
        datetime(jourjul[0], jourjul[1], jourjul[2], jourjul[3], jourjul[4], jourjul[5])
        for jourjul in jourjul
    ]
    date = xr.DataArray(date, dims="MAXT")
    return ds.assign(TIME=date)


def transform_netCDF_old(ds,selected_file):
    print(selected_file,'transforminig')

    ds = (
                ds
                .squeeze()
                .set_coords(["LONGITUDE", "LATITUDE", "TIME", "PROFZ"])
                .set_xindex("PROFZ")
                .set_xindex("TIME")
            )
    ds = ds.where(
            (ds.VCUR_SEADATANET_QC == 49)
            & (ds.UCUR_SEADATANET_QC == 49)
            #& (ds.WCUR_SEADATANET_QC == 49)
            #& (ds.ECUR_SEADATANET_QC == 49)
           # & (ds.PGOOD_SEADATANET_QC == 49)
            #& (ds.ECI_SEADATANET_QC == 49)
            #& (ds.BOTTOM_DEPTH_SEADATANET_QC == 49)
           # & (ds.BATHY_SEADATANET_QC == 49)
            & (ds.USHIP_SEADATANET_QC == 49)
            & (ds.VSHIP_SEADATANET_QC == 49),
            drop=False)
    ds = ds[
                [
                    "TIME",
                    "USHIP", "VSHIP", "BATHY", "BOTTOM_DEPTH",
                    "UCUR", "VCUR",
#                    "ROLL", "PITCH", "TR_TEMP", "HEADING", "U_BOTTOM", "V_BOTTOM",
#                    "WCUR", "ECUR", "PGOOD", "ECI", "UTIDE", "VTIDE",
                ]
            ]
    fix_time(ds).to_netcdf('transformed_netCDF/'+selected_file,mode='w')
    return 


def transform_netCDF(ds,selected_file):
    print(selected_file,'transforminig')

    ds = (
                ds
                .squeeze()
#                .set_coords(["LONGITUDE", "LATITUDE", "TIME", "PROFZ"])
#                .set_xindex("PROFZ")
                .set_xindex("TIME")
            )
    PROFZ=-(ds.PROFZ.isel(MAXT=0))
    #
    #ds.reset_coords("PROFZ")
    ds["PROFZ"]=PROFZ
    ds = ds.where(
            (ds.VCUR_SEADATANET_QC == 49)
            & (ds.UCUR_SEADATANET_QC == 49)
            #& (ds.WCUR_SEADATANET_QC == 49)
            #& (ds.ECUR_SEADATANET_QC == 49)
           # & (ds.PGOOD_SEADATANET_QC == 49)
            #& (ds.ECI_SEADATANET_QC == 49)
            #& (ds.BOTTOM_DEPTH_SEADATANET_QC == 49)
           # & (ds.BATHY_SEADATANET_QC == 49)
            & (ds.USHIP_SEADATANET_QC == 49)
            & (ds.VSHIP_SEADATANET_QC == 49),
            drop=False)
    ds = ds[
                [
                    "TIME",
                    "USHIP", "VSHIP", "BATHY", "BOTTOM_DEPTH",
                    "UCUR", "VCUR",
#                    "ROLL", "PITCH", "TR_TEMP", "HEADING", "U_BOTTOM", "V_BOTTOM",
#                    "WCUR", "ECUR", "PGOOD", "ECI", "UTIDE", "VTIDE",
                ]
            ]
    ds=fix_time(ds).swap_dims({"MAXZ":"PROFZ"}).set_xindex("TIME")
    ds.to_netcdf('transformed_netCDF/'+selected_file,mode='w')
    return ds


def get_info(file_name):
    
    from datetime import date, datetime, timedelta
    from bs4 import BeautifulSoup
#    file_path='https://data-eurogoship.ifremer.fr/copy_seadatanet/18000510_3_OVIDE2018_THALASSA_OS150_SDN2.nc'
#    if local_pc:
#        file_path = glob.glob("/Users/lfranc/Documents/octopus_ok/output/" + file_name)[0]
#    else:
#        file_path = fs.glob("https://data-eurogoship.ifremer.fr/copy_seadatanet/" + file_name)[0]
    ds=open_ds(file_name)
    transform_netCDF(ds,file_name)
    
    xml_path=BeautifulSoup(ds.SDN_XLINK.data[0][0].decode('utf-8'), 'xml').sdn_reference.get('href')
#    print(xml_path)
    user_interface_url = "/".join(xml_path.split("/")[:-1])
    print('You can consult detailed information on this data at ', user_interface_url)
    LOCAL_CDI_ID = ds.SDN_LOCAL_CDI_ID.data[0].decode('utf-8')
    print('To download full dataset, please go to https://cdi.seadatanet.org/search ' + 
          'and search with LOCAL_CDI_ID as',LOCAL_CDI_ID)

    ds = (
        ds.squeeze()
        .set_coords(["LATITUDE", "LONGITUDE", "TIME", "PROFZ"])
#        .set_xindex("PROFZ")
        .set_xindex("TIME")
    )

    time = ds["TIME"]
    time = time.dropna(dim="MAXT", how="any")
    jourjul = [greg_0h(jourjul) for jourjul in time.values]
    # a=pd.DataFrame(a)
    # c=pd.to_datetime(a)
    date = [datetime(jourjul[0], jourjul[1], jourjul[2]) for jourjul in jourjul]
    # d=[c.strftime('%Y-%m-%d') for c in c]
    date_start = date[0]
    date_end = date[-1]
    date_start_str = date_start.strftime("%Y-%m-%d")
    date_end_str = date_end.strftime("%Y-%m-%d")
    # year=(date_start.year)
    year_str = date_start.strftime("%Y")

    shipname = ds["SDN_CRUISE"].attrs["shipname"]
    shipcode = ds["SDN_CRUISE"].attrs["shipcode"]
    adcp_frequency = ds.attrs["ADCP_frequency"]
    numeric_filter = filter(str.isdigit, adcp_frequency)
    adcp_frequency = "".join(numeric_filter)
    numeric_filter = filter(str.isdigit, ds.attrs["bin_length"])
    bin_length = "".join(numeric_filter)


    if bin_length:
        bin_length = bin_length
    else:
        bin_length = None
    if "principal_investigator" in ds.attrs:
        principal_investigator = ds.attrs["principal_investigator"]
    else:
        principal_investigator = None
    if "project" in ds.attrs:
        project = ds.attrs["project"]
    else:
        project = None
    dict = {  #'download_link': f"<a href='",#{file_url}' target='_blank'>{selected_file }</a>",
        'filename': file_name,
        "shipname": shipname,
        "date_start": date_start_str,  # pd.to_datetime(date_start_str).strftime('%Y-%m-%d'), #gregorian_date[0:3]
        "date_end": date_end_str,  # pd.to_datetime(date_end_str).strftime('%Y-%m-%d'),
        "adcp_frequency(KiloHz)": adcp_frequency,
        "bin_length(meter)": bin_length,
        "year": year_str,
        "title": ds.attrs['title'],
        "Conventions": ds.attrs['Conventions'] ,
        "featureType" :ds.attrs['featureType'],
        "date_update": ds.attrs['date_update'],
        "ADCP_frequency": ds.attrs['ADCP_frequency'],
        "ADCP_beam_angle": ds.attrs['ADCP_beam_angle'],
        "ADCP_ship_angle": ds.attrs['ADCP_ship_angle'],
        "bin_length": ds.attrs['bin_length'],
        "middle_bin1_depth": ds.attrs['middle_bin1_depth'],
        "heading_corr": ds.attrs['heading_corr'],
        "pitch_corr": ds.attrs['pitch_corr'],
        "ampli_corr": ds.attrs['ampli_corr'],
        "pitch_roll_used": ds.attrs['pitch_roll_used'],
#"instr_error": ds.attrs['instr_error'],
        "date_creation": ds.attrs['date_creation'],
        "ADCP_type": ds.attrs['ADCP_type'],
#"platform_number": ds.attrs['platform_number'],
        "data_type": ds.attrs['data_type'],
         
        'user_interface_url' :  user_interface_url,
        'LOCAL_CDI_ID' : LOCAL_CDI_ID,
    }

    #    - link to the downloading file,
    # - Vessel : name of the boat (platform
    # - start and end date (this can be taken off once we have a cursor for time)
    # - ADCP Frequency (KHz)
    # - bin Length (meter )

    return dict

def get_file_names(local_pc=True,files_path="/Users/todaka/data/goship/octopus_output_newprofz/*.nc"):
    import os
    import glob

    if local_pc:
        files_path = "/Users/lfranc/Documents/octopus_ok/output/*.nc"
        files_path ="/Users/todaka/data/goship/octopus_output_newprofz/*.nc"
        files_paths = glob.glob(files_path)

    else:
        fs = fsspec.filesystem("https")
        files_path = "https://data-eurogoship.ifremer.fr/copy_seadatanet/*.nc"
        files_paths = fs.glob(files_path)

    file_names = [os.path.basename(path) for path in files_paths]
    file_names = file_names[0 : len(file_names)]
    return file_names


def open_ds(file_name,base_path="/Users/todaka/data/goship/octopus_output_newprofz/",local_pc=True):
    print("open ", file_name)
    ds = xr.open_dataset(
            base_path+file_name, decode_cf=True, decode_times=False, engine="scipy"
        )
    return ds
