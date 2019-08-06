# Dingocar...Donkeycar, down-under

# Install on Comuter/Laptop (Not the Pi)

Donkeycar has great documentation but we have a few convienace functions that need 
slightly different setup. Soooo I have litterally copied the docs from donkeycar and 
added the bits we need.

1. **ONLY If you dont have Conda**
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh
```

2. cd to where you want to clone the dingocar repo, and clone.
```
cd my_repos
git clone https://github.com/tall-josh/dingocar.git
cd dingocar
git checkout master
```

3. Create a dingocar environment

**For tensorflow-cpu**
```
conda env create -f install/envs/ubuntu-cpu.yml 
```

**For tensorflow-gpu**
```
conda env create -f install/envs/ubuntu-gup.yml 
```

4. Install
```
conda activate dingo
pip install -e .[pc]
```

5. Create your working dir
```
donkey createcar --path mycar
```

---



# How to Train Responsibly

These are the steps to follow from gather data (manually drive) to training to driving with an Neural Network.

## On your local machine

### Onetime setup

1. Make sure your running an ssh server on your local machine. If not intall it.

```
sudo apt-get update
sudo apt-get install openssh-server
```

2. Add your own public key to authorized keys

```
cat ~/.ssh/id_rsa.pub >> authorized_keys
```

### Shh to pi, with the right args.

1. ssh to the pi with `-AR`. `A` will forward with you're local credentials. The
`R 2050` will forward a port from the Pi back to your local machine. This will allow
our scrips on the Pi `scp` (secure copy) files back to your loacl machine once you
are done driving.

```
ssh -AR 2050:localhost:22 pi@roba1.local

# Now you're on the Pi
```

### Gather driving data

**On the Pi**

0. `cd play/roba1/mycar`

1. Fill in the `info.json`: The `info.json` is used to help keep track of when a dataset was gathers and what type of data is in the tub that is gathered. I recomend you fill this is at the start of a labelling session (or whenever your track or track  environment changes). A sample `info.json` is below:

```
{
  "count"       : SET AUTOMATICALLY,
  "date"        : SET AUTOMATICALLY,
  "tape"        : "thick yellow",
  "floor"       : "timber",
  "location"    : "bill gates' house",
  "centre line" : true,


# donkeycar: a python self driving library

[![Build Status](https://travis-ci.org/autorope/donkeycar.svg?branch=dev)](https://travis-ci.org/autorope/donkeycar)
[![CodeCov](https://codecov.io/gh/autoropoe/donkeycar/branch/dev/graph/badge.svg)](https://codecov.io/gh/autorope/donkeycar/branch/dev)
[![PyPI version](https://badge.fury.io/py/donkeycar.svg)](https://badge.fury.io/py/donkeycar)
[![Py versions](https://img.shields.io/pypi/pyversions/donkeycar.svg)](https://img.shields.io/pypi/pyversions/donkeycar.svg)

Donkeycar is minimalist and modular self driving library for Python. It is
developed for hobbyists and students with a focus on allowing fast experimentation and easy
community contributions.

#### Quick Links
* [Donkeycar Updates & Examples](http://donkeycar.com)
* [Build instructions and Software documentation](http://docs.donkeycar.com)
* [Slack / Chat](https://donkey-slackin.herokuapp.com/)

![donkeycar](./docs/assets/build_hardware/donkey2.PNG)

#### Use Donkey if you want to:
* Make an RC car drive its self.
* Compete in self driving races like [DIY Robocars](http://diyrobocars.com)
* Experiment with autopilots, mapping computer vision and neural networks.
* Log sensor data. (images, user inputs, sensor readings)
* Drive your car via a web or game controller.
* Leverage community contributed driving data.
* Use existing CAD models for design upgrades.

### Get driving.
After building a Donkey2 you can turn on your car and go to http://localhost:8887 to drive.

### Modify your cars behavior.
The donkey car is controlled by running a sequence of events

```python
#Define a vehicle to take and record pictures 10 times per second.

import time
from donkeycar import Vehicle
from donkeycar.parts.cv import CvCam
from donkeycar.parts.datastore import TubWriter
V = Vehicle()

IMAGE_W = 160
IMAGE_H = 120
IMAGE_DEPTH = 3

#Add a camera part
cam = CvCam(image_w=IMAGE_W, image_h=IMAGE_H, image_d=IMAGE_DEPTH)
V.add(cam, outputs=['image'], threaded=True)

#warmup camera
while cam.run() is None:
    time.sleep(1)

#add tub part to record images
tub = TubWriter(path='./dat',
          inputs=['image'],
          types=['image_array'])
V.add(tub, inputs=['image'], outputs=['num_records'])

#start the drive loop at 10 Hz
V.start(rate_hz=10)
```

See [home page](http://donkeycar.com), [docs](http://docs.donkeycar.com)
or join the [Slack channel](http://www.donkeycar.com/community.html) to learn more.
