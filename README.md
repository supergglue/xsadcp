# xsadcp


## Installing

Install on your PC micromamba following description [here](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html#automatic-install) 

Then create a micromamba enviroment using following commands. 
```
micromamba create -n xsadcp python==3.11
micromamba activate xsadcp
micromamba install git
git clone https://github.com/SADCPVIEW/xsadcp.git
cd xsadcp
micromamba install --file requirements.txt
pip install -e .
python -m ipykernel install --user --name=xsadcp
```


## Creating csv and zarr
You have installed the all eviroment you need to start jupyter lab.  Type following command to start jupyter lab on your PC.

```
jupyter lab
```

Navigate to notebooks folder and star the create_csv_zarr.ipynb.  Then jhust follow the instruction in the notebook!  


## Start the application on your PC

Verify that you have data directory that you've made in the last step then type following command to start the web-ap on your PC.
```
panel serve xsadcp/app.py
```

## Try the web app,
Go to 
[https://huggingface.co/spaces/SADCPVIEW/SADCP_VIEWER](https://huggingface.co/spaces/SADCPVIEW/SADCP_VIEWER)

