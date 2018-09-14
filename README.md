# About

This is the software of the course [PyRat](http://formations.telecom-bretagne.eu/pyrat).

Code by Vincent Gripon

Illustrations by Lauren Lefumeur-Pasdeloup and Christina Roberts

See full credits [here](http://formations.telecom-bretagne.eu/pyrat/?page_id=264).

# Usage

1. Open a terminal and navigate to the folder containing pyrat.py

2. Run 'python3 pyrat.py --help' for a complete list of options. A good start is 'python3 pyrat.py --rat AIs/random.py'

You can play with keyboard (tested on Linux and Windows) with 'python pyrat.py --rat human --python human' (replace with 'python3' if running Ubuntu). The rat is controlled with arrows and the python with keypad.

# Install

To be able to run, one should only need python3 and pygame for python3

* On Ubuntu, a typical installation would be:

```bash
sudo apt-get install python3-setuptools
sudo easy_install3 pip
sudo pip3.5 install pygame
```

On 18.04, users reported using:

```bash
sudo apt-get install python3-pip
pip3 -V
# pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
sudo pip3 install pygame
```

Test your installation. In the pyrat directory, type:

```bash
python3 pyrat.py --rat AIs/random.py
```

* On Windows:

```bash
pip install pygame
```

With more details:

Install Python 3 from https://www.python.org/downloads/windows/: select the version for your architecture, 32 bits or
  64 bits. Download and launch the installer.

Select "Add Python 3.x to Path" in order to be able to launch the Python interpreter from any directory.

Select "Install now": the default option locally installs Python 3 for the current user.
  
Install the library "pygame". Launch "cmd" and then type:
```bash
python -m pip install -U pygame --user
```

Test your installation. In the pyrat directory, type:
```bash
python pyrat.py --rat AIs\random.py
```

* On macOS:

macOS ships with Python 2 by default. There is several ways to install Python 3, such as from [Python.org](https://www.python.org/downloads/release/python-370/) or using [Homebrew](https://brew.sh/). Here we show how to do it using Anaconda, which cleanly separates Python 3 from the system Python, and can be removed easily.

Download and install Anaconda (Python 3.x version): https://www.anaconda.com/download/#macos.  
Then, create a Conda environment and setup the dependencies:
```bash
conda create -n pyrat_env python=3.6
source activate pyrat_env
pip install pygame
```

To run PyRat:
```bash
source activate pyrat_env
python pyrat.py
```

Note that inside the Conda environment, `python` and `python3` link to Python 3, while `python2` links to the system Python 2.
```bash
python --version
# Python 3.6.5 :: Anaconda, Inc.
python3 --version
# Python 3.6.5 :: Anaconda, Inc.
python2 --version
# Python 2.7.10
```

If wanted, Anaconda can be removed by running the following:
```bash
rm -r /anaconda3 ~/.condarc ~/.conda ~/.continuum
```

# Notes

* On Windows expect numerous bugs

* On MacOS, do not expect anything
