#!/bin/bash

### Install python libraries (as of 2022-02-09 use Python 3.2 for open3d compatibility)
# python3.6 -m ensurepip --upgrade; python3.6 -m pip install ...
pip install numpy pandas matplotlib pyntcloud open3d-python --user

### Install CloudCompare for visualising the 3D scans
### For other installation routes: https://www.danielgm.net/cc/
snap install cloudcompare
