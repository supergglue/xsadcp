---
title: >-
  'SADCP_VIWER', Navigate and deep dive in the ocean current mesured
  by Ship Acoustic Doppler Current Profiler(SADCP)
emoji: 🌊⛴
colorFrom: pink
colorTo: blue
sdk: docker
pinned: true
license: mit
short_description: Enjoy the Research data collected by EURO-GO-SHIP!
---

DOI: 

# How to run the web-app on a docker instance
```
git clone https://huggingface.co/spaces/SADCPVIEW/Test
```
You have all you need (Dockerfile, requirements, code) in this repo



# How to run the web-app on your PC

- Download the configuration

```
git clone https://huggingface.co/spaces/SADCPVIEW/Test
```

- Download the data.tar file as shown in the Dockerfile.



- Create python enviroment and run the code

```
micromamba create -n sadcpview python=3.11
micromamba activate sadcpview
cd Test
pip install -r requirements.txt
panel serve  app.py
```

- access the web app!

Above panel command will show the web app address. Just check that with your favorite browser!