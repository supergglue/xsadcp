# xsadcp


<p align="center">
<a href="https://pypi.python.org/pypi/xsadcp">
    <img src="https://img.shields.io/pypi/v/xsadcp.svg"
        alt = "Release Status">
</a>

<a href="https://github.com/tinaok/xsadcp/actions">
    <img src="https://github.com/tinaok/xsadcp/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">
</a>

<a href="https://tinaok.github.io/xsadcp/">
    <img src="https://img.shields.io/website/https/tinaok.github.io/xsadcp/index.html.svg?label=docs&down_message=unavailable&up_message=available" alt="Documentation Status">
</a>

</p>


Skeleton project created by Python Project Wizard (ppw)


* Free software: MIT
* Documentation: <https://tinaok.github.io/xsadcp/>


## Installing

```
micromamba create -n xsadcp python==3.11
micromamba activate xsadcp
micromamba install --file requirements.txt
pip install -e .
python -m ipykernel install --user --name=xsadcp
```

## Creating csv and zarr

start a notebook in the notebook folder and follow the documentation.

## Start the application on your PC

Verify that you have data directory that you've made in the last step. 
```
cd notebook
panel serve ../xsadcp/app.py
```

## set up the web app,
Go to 
(https://huggingface.co/spaces/SADCPVIEW/SADCP_VIEWER)[ https://huggingface.co/spaces/SADCPVIEW/SADCP_VIEWER]


## Credits

This package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool. For more information, please visit the [project page](https://zillionare.github.io/python-project-wizard/).
