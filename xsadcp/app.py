import numpy as np
import pandas as pd
import panel as pn
import xarray as xr
import param

import hvplot.xarray
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datatree import open_datatree
from xsadcp import get_range, load_csv, load_bathymetry, load_zarr, load_file, filter_df, filter_data, quiver_depth_filtered, bathy_uship_vship_bottom_depth, corsen_data, vectors_plot, fix_time, transform_netCDF, get_info, get_file_names, open_ds



class SADCP_Viewer(param.Parameterized):
    """
    A parameterized class for viewing SADCP data.
    
    This class provides widgets for selecting data parameters, updating data based on selections,
    and generating plots to visualize the SADCP data.
    
    Available functions:
        - update_name_options: Update dropdown options and slider ranges based on selected years and file.
        - update_plots: Update plots based on selected data and parameters.
    """

    # Load data and initialize widgets
    df = load_csv()
    bathy = load_bathymetry()
    tree=load_zarr()
    file_names = df["file_name"].tolist()
    years = sorted(df["year"].unique())

    # Widgets for selecting data parameters
    year_slider = pn.widgets.IntRangeSlider(name="Year Range", start=df["year"].min(), end=df["year"].max())
    file_dropdown = pn.widgets.Select(name="File Selector")
    longitude_slider = pn.widgets.RangeSlider(name="Longitude Range", start=-180, end=180, step=1)
    latitude_slider = pn.widgets.RangeSlider(name="Latitude Range", start=-90, end=90, step=1)
    depth_range_slider = pn.widgets.IntRangeSlider(start=100, end=300, value=(100, 300), step=1, name="Depth Range")
    depth_2_checkbox = pn.widgets.Checkbox(value=False, name="Depth 2 Checkbox")
    depth_3_checkbox = pn.widgets.Checkbox(value=False, name="Depth 3 Checkbox")
    depth_2_range_slider = pn.widgets.IntRangeSlider(start=100, end=300, value=(100, 300), step=1, name="Depth 2 Range")
    depth_3_range_slider = pn.widgets.IntRangeSlider(start=100, end=300, value=(100, 300), step=1, name="Depth 3 Range")
    num_vectors_slider = pn.widgets.IntSlider(start=40, end=800, step=1, value=100, name="Number of Vectors")
    scale_factor_slider = pn.widgets.FloatSlider(start=0.1, end=1, step=0.1, value=0.5, name="Scale Factor")
    bathy_checkbox = pn.widgets.Checkbox(value=False, name="Bathy Checkbox")

 
    data_table = pn.widgets.Tabulator(width=400, height=200)
    metadata_table = pn.widgets.Tabulator(width=600, height=800)
    # Download button is not working : TODO
    download_button = pn.widgets.Button(name="Download", button_type="primary")

    def __init__(self, **params):
        """
        Initialize the SADCP_Viewer class.
        
        Parameters:
            **params: Additional parameters to be passed to the superclass.
        """

        super(SADCP_Viewer, self).__init__(**params)
        self.file_dropdown.objects = self.file_names
        self.file_dropdown.value = (
            self.file_dropdown.objects[0] if self.file_dropdown.objects else None
        )
        self.update_name_options()

    @param.depends("year_slider.value", "file_dropdown.value", watch=True)
    def update_name_options(self):
        """
        Update dropdown options and slider ranges based on selected years and file.

        This function updates the dropdown options and slider ranges based on the selected years
        and file. It also loads the selected file's data and adjusts slider ranges accordingly.

        """
        # Extract selected start and end years
        start_year, end_year = self.year_slider.value
        
        # Filter DataFrame based on selected years and sort by year
        mask = (self.df["year"] >= start_year) & (self.df["year"] <= end_year)
        sorted_df = self.df[mask].sort_values(by="year")
        
        # Get unique file names
        files = sorted_df["file_name"].unique().tolist()
        
        # Update file dropdown options
        self.file_dropdown.options = files
        
        if files:
            selected_file = self.file_dropdown.value
            
            # Set default selected file if not selected or not in options
            if not selected_file or selected_file not in files:
                selected_file = files[0]
                self.file_dropdown.value = selected_file
            
            # Update data table and metadata table based on selected file
            self.data_table.value, self.metadata_table.value = filter_df(sorted_df, selected_file)
            
            # Load selected file's data
            self.ds = load_file(self.tree,selected_file)
            
            # Update slider ranges for longitude, latitude, and depth
            for slider, coord in zip([self.longitude_slider, self.latitude_slider, self.depth_range_slider,
                          self.depth_2_range_slider, self.depth_3_range_slider],
                         [self.ds.LONGITUDE, self.ds.LATITUDE, self.ds.PROFZ,self.ds.PROFZ,self.ds.PROFZ]):
                coord_range = get_range(coord)
                slider.start, slider.end, slider.value = coord_range[0], coord_range[1], coord_range


            # Close dataset to free up resources
            # self.ds.close()

    @param.depends(
        "year_slider.value",
        "file_dropdown.value",
        "depth_range_slider.value",
        "depth_2_checkbox.value",
        "depth_3_checkbox.value",
        "depth_2_range_slider.value",
        "depth_3_range_slider.value",
        "longitude_slider.value",
        "latitude_slider.value",
        "num_vectors_slider.value",
        "scale_factor_slider.value",
        "bathy_checkbox.value",
        watch=False,)
    def update_plots(self):
        """
        This function updates the plots based on the selected data and parameters.

        The function filters the data, generates additional plots, and updates the main vector plot based on the selected parameters.

        Returns:
            pn.Row: A Panel row containing the updated map plot and additional plots.

        """
        # Filter the data
        self.ds_filtered = filter_data(self.ds,self.longitude_slider.value,self.latitude_slider.value)

        # Prepare the plots shown in left
        # Update vector plots
        vector_plot = vectors_plot(self.ds_filtered, self.bathy, 
                                   self.longitude_slider.value, self.latitude_slider.value,
                                   self.depth_range_slider.value, self.depth_2_range_slider.value, self.depth_3_range_slider.value,
                                   self.scale_factor_slider.value,self.num_vectors_slider.value,
                                   depth_2_checkbox= self.depth_2_checkbox.value,
                                   depth_3_checkbox= self.depth_3_checkbox.value,
                                   bathy_checkbox=self.bathy_checkbox.value,
                                   )


        # Generate plots which will be plotted on the left row.
        self.plot_left = pn.Column(
                              # Here adjust the style option later TODO
                              # https://panel.holoviz.org/how_to/styling/matplotlib.html
                               pn.pane.Matplotlib(vector_plot, dpi=144),
                              # Add here the hvplot block of contour TODO
                                sizing_mode="stretch_both")

        # Generate additional plots which will be plotted on the right row.
        other_plots = bathy_uship_vship_bottom_depth(self.ds_filtered)
        self.plot_right = pn.Column(
            *(pn.pane.HoloViews(plot, width=400, height=200) for plot in other_plots),
            sizing_mode="stretch_width"
        )

        # Return a Panel row containing the updated map plot and additional plots
        return pn.Row(self.plot_left, self.plot_right, sizing_mode="stretch_both")


pn.extension("tabulator")
pn.config.theme = 'dark'

explorer = SADCP_Viewer()
# Instantiate the SADCP_Viewer class and create a template
tabs = pn.Tabs(
    ("Plots", pn.Column(explorer.update_plots)),
    (
        "Metadata",
        pn.Column(
            explorer.metadata_table, explorer.download_button, height=500, margin=10
        ),
    ),
)

sidebar = [
    pn.panel('./EuroGO-SHIP_logo_wide_tagline_1.2.png',width=300 ),
    """This application, developed in the frame of Euro Go Shop, helps to interactively visualise and download ship ADCP data.""",
    explorer.year_slider,
    explorer.file_dropdown,
    explorer.longitude_slider,
    explorer.latitude_slider,
    explorer.bathy_checkbox,
    explorer.depth_range_slider,
    explorer.depth_2_checkbox,
    explorer.depth_3_checkbox,
    explorer.depth_2_range_slider,
    explorer.depth_3_range_slider,
    explorer.num_vectors_slider,
    explorer.scale_factor_slider,
    explorer.data_table,
    """You can consult detailed information on this data in the metadata tab shown on the right.
       To download full dataset, please go to https://cdi.seadatanet.org/search 
      and search with LOCAL_CDI_ID indicated above.""",
    #pn.panel('https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png', ),
#width=10)
]

template = pn.template.FastListTemplate(
    title="SADCP data Viewer", logo='https://avatars.githubusercontent.com/u/123177533?s=200&v=4',
    sidebar=sidebar, main=[tabs]
    
)
template.servable()
