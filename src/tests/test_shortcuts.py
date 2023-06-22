import pytest
# from .climatePy import shortcuts

from src.climatePy import shortcuts
from src.climatePy import dap
from src.climatePy import climatepy_filter
from src.climatePy import utils

import pandas as pd
import geopandas as gpd
import xarray as xr
import matplotlib.pyplot as plt
import re
from datetime import datetime

# AOI    = gpd.read_file('src/data/boulder_county.gpkg')
# AOI    = gpd.read_file('src/data/san_luis_obispo_county.gpkg')

# @pytest.fixture(params=['miami_dade_county', 'san_luis_obispo_county', 
#                         'litchfield_county', 'tuscaloosa_county', 
#                         'boulder_county', 'king_county'])

@pytest.fixture(params=['san_luis_obispo_county', 'boulder_county'])

def AOI(request): 
    filepath = f'src/data/{request.param}.gpkg'
    AOI = gpd.read_file(filepath)
    yield AOI

def test_getTerraClim_case1(AOI):

    varname = ["ppt", "tmax"]
    startDate = "2018-01-01"
    endDate   = "2018-03-02"
    verbose   = True

    # Call function to get output
    output = shortcuts.getTerraClim( AOI, varname, startDate, endDate, verbose)

    # Assert that the output is a dictionary
    assert type(output) == dict

    # Assert that the output dictionary has the correct keys
    assert set(output.keys()) == {"ppt", "tmax"}

    # Assert that the values of the output dictionary are xarray DataArrays
    assert isinstance(output["ppt"], xr.DataArray)
    assert isinstance(output["tmax"], xr.DataArray)

    # Assert that the dimensions of the output DataArrays are correct
    assert output["ppt"].dims == ("y", "x", "time")
    assert output["tmax"].dims == ("y", "x", "time")   

    dates1 = [datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["ppt"].time.values]
    dates2 = [datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["tmax"].time.values]
    
    start_date1 = min(dates1)
    end_date1   = max(dates1)
    start_date2 = min(dates2)
    end_date2   = max(dates2)

    assert end_date1 - start_date1 == pd.Timedelta("59D")
    assert end_date2 - start_date2 == pd.Timedelta("59D")
    assert start_date1 - start_date2 == pd.Timedelta("0D")
    assert end_date1 - end_date2 == pd.Timedelta("0D")

    assert "ppt" in output["ppt"].time[0].values.item()
    assert "tmax" in output["tmax"].time[0].values.item()
    
def test_getGridMET_case1():
    # ---- Case 1 ----
    verbose   = True
    varname = "pr"
    startDate="2000-01-01"
    endDate="2000-01-01"
    
    # Call function to get output
    output = shortcuts.getGridMET( AOI, varname, startDate, endDate, verbose)
    
    # Assert that the output is a dictionary
    assert type(output) == dict

    # Assert that the output dictionary has the correct keys
    assert set(output.keys()) == {"pr"}

    # Assert that the values of the output dictionary are xarray DataArrays
    assert isinstance(output["pr"], xr.DataArray)

    # Assert that the dimensions of the output DataArrays are correct
    assert output["pr"].dims == ("y", "x", "time")

    # Assert dates are correct
    start_date1 = min([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["pr"].time.values])
    end_date1   = max([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["pr"].time.values])
    
    assert end_date1 - start_date1 == pd.Timedelta("0D")

    assert "pr" in output["pr"].time[0].values.item()
    assert len(output["pr"].time.values) == 1git a

def test_getGridMET_case2():    
    # ---- Case 2 ----
    verbose   = True
    varname = ["pr", "tmmx"]
    startDate = "2018-01-01"
    endDate   = "2018-01-02"

    # Call function to get output
    output = shortcuts.getGridMET( AOI, varname, startDate, endDate, verbose)

    # Assert that the output is a dictionary
    assert type(output) == dict

    # Assert that the output dictionary has the correct keys
    assert set(output.keys()) == {"tmmx", "pr"}

    # Assert that the values of the output dictionary are xarray DataArrays
    assert isinstance(output["pr"], xr.DataArray)
    assert isinstance(output["tmmx"], xr.DataArray)

    # Assert that the dimensions of the output DataArrays are correct
    assert output["pr"].dims == ("y", "x", "time")
    assert output["tmmx"].dims == ("y", "x", "time")

    # Assert dates are correct
    start_date1 = min([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["pr"].time.values])
    end_date1   = max([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["pr"].time.values])
    start_date2 = min([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["tmmx"].time.values])
    end_date2   = max([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["tmmx"].time.values])
    
    assert end_date1 - start_date1 == pd.Timedelta("1D")
    assert end_date2 - start_date2 == pd.Timedelta("1D")
    assert start_date1 - start_date2 == pd.Timedelta("0D")
    assert end_date1 - end_date2 == pd.Timedelta("0D")

    assert "pr" in output["pr"].time[0].values.item()
    assert "tmmx" in output["tmmx"].time[0].values.item()
    assert len(output["pr"].time.values) == 2
    assert len(output["tmmx"].time.values) == 2

def test_getGridMET_case3():
    # ---- Case 3 ----
    verbose = True
    varname = ["pr", "tmmx", "rmin"]
    startDate = "2015-01-01"
    endDate   = "2016-02-05"

    # Call function to get output
    output = shortcuts.getGridMET( AOI, varname, startDate, endDate, verbose)

    # Assert that the output is a dictionary
    assert type(output) == dict

    # Assert that the output dictionary has the correct keys
    assert set(output.keys()) == {"tmmx", "pr", "rmin"}

    # Assert that the values of the output dictionary are xarray DataArrays
    assert isinstance(output["pr"], xr.DataArray)
    assert isinstance(output["tmmx"], xr.DataArray)
    assert isinstance(output["rmin"], xr.DataArray)

    # Assert that the dimensions of the output DataArrays are correct
    assert output["pr"].dims == ("y", "x", "time")
    assert output["tmmx"].dims == ("y", "x", "time")
    assert output["rmin"].dims == ("y", "x", "time")

    # Assert dates are correct
    start_date1 = min([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["pr"].time.values])
    end_date1   = max([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["pr"].time.values])
    start_date2 = min([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["tmmx"].time.values])
    end_date2   = max([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["tmmx"].time.values])
    start_date3 = min([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["rmin"].time.values])
    end_date3   = max([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["rmin"].time.values])

    assert end_date1 - start_date1 == pd.Timedelta("400D")
    assert end_date2 - start_date2 == pd.Timedelta("400D")
    assert end_date3 - start_date3 == pd.Timedelta("400D")
    assert start_date1 - start_date2 == pd.Timedelta("0D")
    assert end_date1 - end_date2 == pd.Timedelta("0D")
    assert end_date3 - end_date2 == pd.Timedelta("0D")

    assert "pr" in output["pr"].time[0].values.item()
    assert "tmmx" in output["tmmx"].time[0].values.item()
    assert "rmin" in output["rmin"].time[0].values.item()

    assert len(output["pr"].time.values) == 401
    assert len(output["tmmx"].time.values) == 401
    assert len(output["rmin"].time.values) == 401
    
def test_getGridMET_case4():
    # ---- Case 4 ----
    verbose = True
    varname = ["rmin"]
    startDate = "2005-01-01"
    endDate   = "2010-01-01"

    # Call function to get output
    output = shortcuts.getGridMET(AOI, varname, startDate, endDate, verbose)

    # Assert that the output is a dictionary
    assert type(output) == dict

    # Assert that the output dictionary has the correct keys
    assert set(output.keys()) == {"rmin"}

    # Assert that the values of the output dictionary are xarray DataArrays
    assert isinstance(output["rmin"], xr.DataArray)

    # Assert that the dimensions of the output DataArrays are correct
    assert output["rmin"].dims == ("y", "x", "time")

    # Assert dates are correct
    start_date1 = min([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["rmin"].time.values])
    end_date1   = max([datetime.strptime(re.search(r'\d{4}-\d{2}-\d{2}', i).group(0), "%Y-%m-%d") for i in output["rmin"].time.values])

    assert end_date1 - start_date1 == pd.Timedelta("1826D")

    assert "rmin" in output["rmin"].time[0].values.item()
    assert len(output["rmin"].time.values) == 1827