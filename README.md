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


## running xsadcp on PANGEO@EOSC

To set up and run `sadcp_viewer` on the PANGEO@EOSC jupyter hub, we need to:
1. Only for first time, follow the registration process as indicated at [https://github.com/pangeo-data/pangeo-eosc/blob/main/users/users-getting-started.md](https://github.com/pangeo-data/pangeo-eosc/blob/main/users/users-getting-started.md).  Please request access as pangeo application on euro-goship with Tina Odaka.
2. [launch a server on EOSC](https://pangeo-eosc.vm.fedcloud.eu/). 
3. Start a termal in the jupyterlab and set up enviroments(click 'File -> New -> Terminal')
4. (only for the first time / until pangeo-fish is public create an SSH key)
  - type `ssh-keygen -t ed25519 -f ~/.ssh/github` in the terminal
  - you will be asked passphrase, you do not need to write anything. Thus hit enter key twice
  - type `cat /home/jovyan/.ssh/github.pub`
  - copy the output. It would look like `ssh-ed25519 XXXXX(very long) `
  - Go [https://github.com/settings/keys](https://github.com/settings/keys) to activate it by following descriptive here [https://docs.github.com/en/enterprise-cloud@latest/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account#adding-a-new-ssh-key-to-your-account](https://docs.github.com/en/enterprise-cloud@latest/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account#adding-a-new-ssh-key-to-your-account) from step 4. (you've already done untill step 3) 
4. (Only the first time:  clone the repository in the terminal)
  - type `git clone git@github.com:SADCPVIEW/sadcp_viewer.git`
5.  - Click the folder icon and go to /sadcp_viewer/notebooks
  - double click 'web-app.ipynb'
  - click 'Run -> Run All cells' to run the notebook.  

