"""
@authors: Sabri.Amer, Andrew.Xu
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import glob


def fread(filenergy_rangeD: str, sizeA: int, precision: str):
    """


    Parameters
    ----------
    filenergy_rangeD : TYPE
        DESCRIPTION.
    sizeA : TYPE
        DESCRIPTION.
    precision : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    data_array = None
    if precision == 'uint64':
        return np.fromfile(filenergy_rangeD, np.uint64, count=sizeA)
    elif precision == 'uint32':
        return np.fromfile(filenergy_rangeD, np.uint32, count=sizeA)
    elif precision == 'int32':
        return np.fromfile(filenergy_rangeD, np.int32, count=sizeA)
    elif precision == 'double':
        return np.fromfile(filenergy_rangeD, np.double, count=sizeA)
    elif precision == 'char':
        data_array = np.fromfile(filenergy_rangeD, np.int8, count=sizeA)
        return ''.join([chr(item) for item in data_array])
    else:
        return np.fromfile(filenergy_rangeD, np.int8, count=sizeA)


def hxtV3Read(filePath: str):
    """
     Method to parse the header of the .hxt file format, you will need to write
     your own version for any other file type you wish to use.

     Parameters
     ----------
     filePath : str

     Returns
     -------
     list [M,bins]
         Returns a list of the file's detector images and the energy bins represented
         in M's axis0.

     """
    #
    fid = open(filePath, 'rb')
    # read first 8 characters to distinguish file type
    label = "%s" % fread(fid, 8, 'char')
    M = 0
    bins = 0
    if label.lower() == 'hexitech':
        version = fread(fid, 1, 'uint64')
        if version == 3:
            mssX = fread(fid, 1, 'uint32')
            mssY = fread(fid, 1, 'uint32')
            mssZ = fread(fid, 1, 'uint32')
            MssRot = fread(fid, 1, 'uint32')
            GalX = fread(fid, 1, 'uint32')
            GalY = fread(fid, 1, 'uint32')
            GalZ = fread(fid, 1, 'uint32')
            GalRot = fread(fid, 1, 'uint32')
            GalRot2 = fread(fid, 1, 'uint32')
            nCharFPreFix = fread(fid, 1, 'int32')
            filePreFix = fread(fid, nCharFPreFix[0], 'char')

            # The next two lines are used to skip some unnecessary parts of the binary file
            dummy = fread(fid, 100 - nCharFPreFix[0], 'dummy')
            timestamp = fread(fid, 16, 'timestamp')

            nRows = fread(fid, 1, 'uint32')
            nCols = fread(fid, 1, 'uint32')
            nBins = fread(fid, 1, 'uint32')
            bins = fread(fid, nBins[0], 'double')
            d = fread(fid, nBins[0] * nRows[0] * nCols[0], 'double')
            M = np.reshape(d, [nRows[0], nCols[0], nBins[0]])
            M = np.swapaxes(M, 0, 2)
        else:
            print("Not Version 3 of HXT File - Zeros Returned")
    fid.close()
    return [M, bins]


def extract_spectra(data_frame: pd.DataFrame, **kwargs):
    """
    Calculates the momentum transfer spectra from the raw detector images.
    Spectra are appended to the data frame at the same row of their corresponding
    detector data.

    Parameters
    ----------
    data_frame : pd.DataFrame
        Data frame of the extraced detector data from bundle_data().
    **kwargs : np.ndarray, int
        Experimental and analysis parameters for calculation.

        samp_det_dist: int
            Distance in mm from the sample to the detector.
        transm_beam_x: int
            Location of the incident beam in pixels.
        transm_beam_y: int
            Location of the incident beam in pixels.
        energy_range: np.ndarray(numerical)
            List of the energy values in keV the user is interested in analyzing
        q_range: np.ndarray(numerical)
            List of the momentum transfer values the user is interested in analyzing
        energy_window_width: int
            The width in keV of the subranges the user would like to divide thier
            energy range into.

    Returns
    -------
    windows : np.ndarray(numerical)
        List containing all of the energy windows and their values for later plotting.
    theta : np.ndarray
        Each pixel's angular distance from the incident beam

    """
    # Default Values For Testing With Included Caffiene Data
    samp_det_dist = kwargs.get(
        'samp_det_dist') if 'samp_det_dist' in kwargs else 244
    transm_beam_x_pos = kwargs.get(
        'transm_beam_x_pos') if 'transm_beam_x_pos' in kwargs else 9
    transm_beam_y_pos = kwargs.get(
        'transm_beam_y_pos') if 'transm_beam_y_pos' in kwargs else 1
    energy_range = kwargs.get(
        'energy_range') if 'energy_range' in kwargs else np.arange(30, 80)
    q_range = kwargs.get('q_range') if 'q_range' in kwargs else np.linspace(
        0.04, 30.04, num=63)
    energy_window_width = kwargs.get(
        'energy_window_width') if 'energy_window_width' in kwargs else len(energy_range)
    num_q_bins = len(q_range)-1
    # Determine detector shape
    data_dimensions = np.shape(data_frame.loc[0, 'Image'])
    theta = np.zeros([data_dimensions[1], data_dimensions[2]])
    q_image = np.zeros(
        [data_dimensions[0], data_dimensions[1], data_dimensions[2]])

    split_indicies = np.arange(0, len(energy_range)-1, energy_window_width)
    # The first index returns an empty list since the first split index matches
    # the first energy index
    energy_windows = np.split(energy_range, split_indicies)[1:]
    data_frame['Spectra'] = None
    # For each pixel in the detector, find it's angular distance from the incident
    # beam and the q values it corresponds to across the total energy range collected
    for x in range(data_dimensions[1]):
        for y in range(data_dimensions[2]):
            d = math.sqrt(((x+1)*.25-.25*transm_beam_x_pos) **
                          2 + ((y+1)*.25-.25*transm_beam_y_pos)**2)
            theta[y, x] = math.atan(d/samp_det_dist)
            # TODO alter this to be agnostic of the det file's energy values
            for e in range(data_dimensions[0]):
                q_image[e, y, x] = (
                    4*math.pi*(e+1)*math.sin(theta[y, x]/2))/1.24

    # For each detector file, find the pixels that fall within the q range of
    # interest and count the number of photons that they encountered.
    # Repeat for each energy range of interest.
    for i, detector_image in enumerate(data_frame['Image']):
        q_counts = np.zeros([len(energy_windows), num_q_bins])
        for j, window in enumerate(energy_windows):
            # .hxt files are read in upside down
            processed_image = detector_image[window, ::-1, :]
            for k in range(0, num_q_bins):
                # Find the pixels that fall within this q bin.
                greater_than_lower_bound = q_image[window] >= q_range[k]
                lower_than_upper_bound = q_image[window] < q_range[k+1]
                mask = np.logical_and(greater_than_lower_bound,
                                      lower_than_upper_bound)
                if np.sum(mask) != 0:
                    # Count the number of occurances
                    q_counts[j, k] = processed_image[mask].sum()
                else:
                    q_counts[j, k] = 0
        print("Files Completed:", i+1)
        data_frame.at[i, 'Spectra'] = q_counts
    # Energy windows are returned as a dictionary in case they are of uneven length
    windows = {}
    for i, x in enumerate(energy_windows):
        windows[i] = x
    # Return values for plotting, spectral data is appended to the data frame
    return windows, theta


def bundle_data(folder_path: str):
    """
    Constructs a data frame containing the data from each indi
    Parameters
    ----------
    folder_path : str
        Path to the folder containing the .

    Returns
    -------
    ret_frame : pd.DataFrame
        Pandas data frame.

    """
    raw_files = glob.glob(folder_path)
    temp = []
    for i, file in enumerate(raw_files):
        # Edit this line for alternative file types: V
        image, bins = hxtV3Read(file)
        temp.append({"Image": image, "Energy_Bins_Sampled_By_Detector": bins})
    ret_frame = pd.DataFrame(temp)
    return ret_frame


def create_spectral_heatmap(data_frame: pd.DataFrame, region_to_analyze: list, scans_per_row: int):
    """  
    Reconstructs a 2D scan assuming the data were collected in a right to left
    raster scan pattern with rows of equal width. The color values for the image
    are the magnitude of the integral of a specified spectral region.

    region_to_analyze must be a list of indicies where the spectra should be 
    analyzed, not a list of q values. To convert between the two consider
    something like this:

    q_range = np.linspace(0.04, 30.04, num=63)
    integral_q_start = 7 #(nm-1)
    integral_q_end = 9 #(nm-1)
    integral_min_index = np.absolute(q_range-integral_q_start).argmin()
    integral_max_index = np.absolute(q_range-integral_q_end).argmin()
    integral_index_range = np.arange(integral_min, integral_max)
    """
    image_width = scans_per_row
    ret_image = np.zeros([math.ceil(
        len(data_frame)/image_width), image_width])
    aups = np.array(data_frame.apply(
        lambda x: np.trapz(x[region_to_analyze])).tolist())
    image_height = math.floor(len(aups)/image_width)-1
    for i, aup in enumerate(aups):
        y = i/image_width
        x = i % image_width
        if y % 2 < 1:
            ret_image[image_height-math.floor(y), x] = aup
        else:
            ret_image[image_height -
                      math.floor(y), image_width-1-x] = aup
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.pcolormesh(ret_image, cmap='jet', vmin=aups.min())
    plt.colorbar(mappable=fig, cmap='jet', label="AUP", orientation="vertical")
    ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
    plt.show()
    return fig


def plot_3d_spectra(spectra: pd.Series, q_range: np.ndarray, plot_type: str, windows):
    """
    Parameters
    ----------
    spectra : pd.Series
        DESCRIPTION.
    q_range : np.ndarray
        DESCRIPTION.
    plot_type : str
        DESCRIPTION.
    windows : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    if plot_type == "windowing":
        bg_sub_data = np.subtract(spectra[0], spectra[1])
        for x in range(len(bg_sub_data)):
            ax.plot3D(q_range, [windows[x, 0]]*len(q_range), bg_sub_data[x],
                      label=str(windows[x, 0]) + ' keV')
        ax.set_ylabel('Energy(keV)')
    else:
        # open beam will be appended to the end
        bg_sub_data = spectra.apply(
            lambda x: np.subtract(x-spectra[len(spectra)-1]))
        bg_sub_data = bg_sub_data[0:-1]
        for x in range(len(bg_sub_data)):
            ax.plot3D(q_range, [x]*len(q_range), spectra[x])
            ax.set_ylabel('Scan Number')
    ax.set_xlabel('${q(nm^{-1})}$')
    ax.set_zlabel('Counts')
    ax.grid(False)
    plt.show()
