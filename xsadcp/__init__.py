"""Top-level package for xsadcp."""

__author__ = """Tina Odaka"""
__email__ = "Tina.Odaka@ifremer.fr"
__version__ = "0.1.0"

from .util import (
    get_range,
    load_csv,
    load_bathymetry,
    load_zarr,
    load_file,
    filter_df,
    filter_data,
    quiver_depth_filtered,
    bathy_uship_vship_bottom_depth,
    corsen_data,
    vectors_plot,
    fix_time,
    transform_netCDF,
    get_info,
    get_file_names,
    open_ds,
#    SADCP_Viewer
)

__all__ = [
    'get_range',
    'load_csv',
    'load_bathymetry',
    'load_zarr',
    'load_file',
    'filter_df',
    'filter_data',
    'quiver_depth_filtered',
    'bathy_uship_vship_bottom_depth',
    'corsen_data',
    'vectors_plot',
#    'SADCP_Viewer'
]

