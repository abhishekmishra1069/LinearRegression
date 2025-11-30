# Error 1
ModuleNotFoundError                       Traceback (most recent call last)
Cell In[3], line 3
      1 # Import Libraries
      2 import pandas as pd
----> 3 from sklearn.data import fetch_california_housing
      4 from sklearn.model_selection import train_test_split

For conda based environments, please install the package using:
    conda install -c conda-forge scikit-learn
For pip based environments, please install the package using:
    pip install scikit-learn   
For more information, please refer to the official documentation: https://scikit-learn.org/stable/install.html


# Error 2
base) abhishekmishra MLR % podman build -t ghcr.io/abhishekmishra1069/mlr-california-housing:20251130 . 
STEP 1/8: FROM python:3.13-slim
STEP 2/8: RUN apt-get update &&     apt-get install -y --no-install-recommends         build-essential         gfortran         python3-dev         libatlas-base-dev &&     apt-get clean &&     rm -rf /var/lib/apt/lists/*
Hit:1 http://deb.debian.org/debian trixie InRelease
Get:2 http://deb.debian.org/debian trixie-updates InRelease [47.3 kB]
Get:3 http://deb.debian.org/debian-security trixie-security InRelease [43.4 kB]
Get:4 http://deb.debian.org/debian trixie/main arm64 Packages [9607 kB]
Get:5 http://deb.debian.org/debian trixie-updates/main arm64 Packages [5404 B]
Get:6 http://deb.debian.org/debian-security trixie-security/main arm64 Packages [76.3 kB]
Fetched 9779 kB in 1s (10.8 MB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
Package libatlas-base-dev is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source
-----------------  
E: Package 'libatlas-base-dev' has no installation candidate
Error: building at STEP "RUN apt-get update &&     apt-get install -y --no-install-recommends         build-essential         gfortran         python3-dev         libatlas-base-dev &&     apt-get clean &&     rm -rf /var/lib/apt/lists/*": while running runtime: exit status 100

(base) abhishekmishra@mishras-Mac-Studio MLR % 

The error E: Package 'libatlas-base-dev' has no installation candidate means that the specific Debian package we added in the previous step to provide optimized linear algebra libraries is not available in the repositories used by the python:3.13-slim base image (which uses a very recent version of Debian).

This is a common issue when using minimal or cutting-edge base images. To fix this, we'll swap out the unavailable package for a modern, universally available alternative that provides the same essential BLAS/LAPACK capabilities needed by NumPy and Pandas for compilation: libopenblas-dev.

I am updating the Dockerfile in the Canvas to replace libatlas-base-dev with libopenblas-dev.

This change should successfully complete the apt-get install step and allow the subsequent pip install of Pandas and NumPy to compile without errors.