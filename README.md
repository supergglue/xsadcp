# xsadcp


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
panel serve xsadcp/app.py
```

## Try the web app,
Go to 
[https://huggingface.co/spaces/SADCPVIEW/SADCP_VIEWER](https://huggingface.co/spaces/SADCPVIEW/SADCP_VIEWER)

