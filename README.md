# Spectral SAXS PCD data Analysis
https://github.com/DIDSR/Spectral-SAXS-Analysis-Tools/blob/main/Windowing%20UI.PNG 
![The User Interface of the Program]((https://github.com/DIDSR/Spectral-SAXS-Analysis-Tools/blob/main/Windowing%20UI.PNG)raw=true)

## Overview:
This is an open-access data analysis tool to analyze spectroscopic photon counting detector data for spectral small angle x-ray scattering (sSAXS) application.

### Data Input:
This application assumes that the input files a 3D array of detector counts at each energy level. In order to work properly the data should be formatted as [energyDetected,xPixel,yPixel]

Each functions requires some experimental parameters as well:
| Parameter                   | Units           | Description                                                             |
|-----------------------------|-----------------|-------------------------------------------------------------------------|
| Sample to Detector Distance | mm              | The distance between the scanned sample and the surface of the detector |
| q Range                     | nm<sup>-1</sup> | The region of momentum transfer values to analyze across                |
| Transmission Beam Location  | pixels          | The approximate location where the incident beam strikes the detector   |


This application allows two primary functions:

### 1D Spectral Analysis and Energy Windowing
Users have the options to plot spectra from thier collected x-ray scattering data and separate into energy windows of interest.

| Parameter           | Units | Description                                    |
|---------------------|-------|------------------------------------------------|
| Energy Range        | keV   | Total range of energies you wish to analyze    |
| Bin Width           | keV   | The size of the steps between energy values    |
| Energy Window Width | keV   | The size of the sub-ranges you wish to analyze |

#### Output:
-Plots of the individual spectra
-A single plot of the background subtracted spectrum
-A plot of the angles corresponding to each detector pixel
-A heatmap of the background subtracted detector data across the whole energy range
-Heatmaps of the background subtrated detector data in each energy window
-A 3D plot of the background subtracted spectra in each energy window

### 2D scanning analysis to generate spatially resolved scattering map
Users can map the relative intensity of scattering signals across multiple data set from 2D scanning sSAXS experiments to generate a planar image.
| Parameter        | Units           | Description                                                                                                          |
|------------------|-----------------|----------------------------------------------------------------------------------------------------------------------|
| Energy Range     | keV             | Total range of energies you wish to analyze                                                                          |
| Integral q Range | nm<sup>-1</sup> | The start and end of the q-peak of interest                                                                   |
| Scans Per Row    | pixels          | The width of the final map you wish to create, if this is a 2D scan it is the number of collections you took per row |

#### Output:
-A 3D plot of the background subtracted spectra for each file
-A heatmap of each file's intensity at the specified q region of interest


## Installation:
- Clone this repository: `https://github.com/<REPO>` and navigate to its root directory
- Install [python 3.9.19](https://www.python.org/downloads/release/python-3919/) (or any version greater than 3.9)
- Create a virtual environtment named `pcd` (or any name of your choosing) 
	- `python -m venv <chosen_env_name>`

- Activate the environment (Ensure you replace `<chosen_env_name>` with your chosen venv name)
	- **Windows:** `<chosen_env_name>\Scripts\activate`
	- **Unix:** `source <chosen_env_name>/bin/activate`

- Install the required dependencies: `pip install -r requirements.txt`


## Usage
From your activated virtual environment run: `python main.py`

## Credits:
