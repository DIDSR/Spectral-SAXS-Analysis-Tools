from enum import Enum
from typing import Dict
import numpy as np
from models import sSAXS_tools as s
import pandas as pd
from matplotlib import pyplot as plt
from utils import PlotUtils
import math
import os


class ScanReconstructionModel:
    """
    The class that holds the data and analysis relavent to the scan reconstruction portion of 
    the app. 
    """

    class Property(str, Enum):
        """
        Property strings to make sure names do not get misspelled across files
        """
        INTEGRAL_q_START = "integral_q_start"
        INTEGRAL_q_END = "integral_q_end"
        SCAN_WIDTH = "scan_width"
        ENERGY_RANGE_MIN = "energy_range_min"
        ENERGY_RANGE_MAX = "energy_range_max"
        SAMPLE_FILE_PATH = "sample_file_path"
        BACKGROUND_FILE_PATH = "background_file_path"
        FILE_EXTENSION = "file_extension"
        DETECTOR_DISTANCE_mm = "detector_distance_mm"
        q_START = "global_q_start"
        q_END = "global_q_end"
        TRANSMISSION_BEAM_X = "transmission_beam_x"
        TRANSMISSION_BEAM_Y = "transmission_beam_y"

    def __init__(self, data: Dict[Property, object]):
        """
        Initializes the class and sets all the necessary variables to perform
        the scan reconstruction.
        Parameters
        ----------
        data : Dict[Property, object]
            key value pairs of all necessary parameters for analysis.

        Returns
        -------
        None.

        """
        self.energy_range = np.arange(
            data.get(self.Property.ENERGY_RANGE_MIN),
            data.get(self.Property.ENERGY_RANGE_MAX)+1,
            dtype=int,
        )
        self.background_file_path = data.get(
            self.Property.BACKGROUND_FILE_PATH)
        self.sample_file_path = data.get(self.Property.SAMPLE_FILE_PATH)
        self.detector_distance = data.get(self.Property.DETECTOR_DISTANCE_mm)
        self.q_range = np.linspace(
            data.get(self.Property.q_START), data.get(self.Property.q_END), num=63
        )
        integral_min = np.absolute(
            self.q_range-data.get(self.Property.INTEGRAL_q_START)).argmin()
        integral_max = np.absolute(
            self.q_range-data.get(self.Property.INTEGRAL_q_END)).argmin()
        self.integral_q_range = np.arange(integral_min, integral_max)
        self.transmission_beam_x = data.get(self.Property.TRANSMISSION_BEAM_X)
        self.transmission_beam_y = data.get(self.Property.TRANSMISSION_BEAM_Y)
        self.file_extension = data.get(self.Property.FILE_EXTENSION)
        self.scan_width = data.get(self.Property.SCAN_WIDTH)
        self.theta: np.ndarray = None
        self.dataframe = pd.DataFrame()
        self.figures = {}

    def reconstruct_scan(self):
        """
        Performs the spectral analysis on each file plots them in aggregate, then
        integrates each spectrum at the region of interest and plots a map of the values.

        Returns
        -------
        None.

        """
        sample_data = s.bundle_data(
            os.path.join(self.sample_file_path, f"*{self.file_extension}"))
        background_data = s.bundle_data(self.background_file_path)
        self.data_frame = pd.concat(
            [sample_data, background_data], ignore_index=True)
        self.windows, self.theta = s.extract_spectra(
            self.data_frame,
            samp_det_dist=self.detector_distance,
            transm_beam_x_pos=self.transmission_beam_x,
            transm_beam_y_pos=self.transmission_beam_y,
            energy_range=self.energy_range,
            q_range=self.q_range)
        spectra = self.data_frame["Spectra"]
        """
        Plotting
        """
        self.figures['heatmap'] = self.__create_spectral_heatmap()
        self.figures['raster_3d'] = self.__plot_3d_spectra()
        plt.show(block=False)

    def __create_spectral_heatmap(self):
        """
        Plotting logic for the heatmap construction

        Returns
        -------
        fig : TYPE
            DESCRIPTION.

        """
        # Reconstructs a 2D scan assuming the data were collected in a right to left
        # raster pattern with rows of equal width.
        data_frame = self.data_frame[:-1]
        ret_image = np.zeros(
            [math.ceil(len(data_frame) / self.scan_width), self.scan_width])
        spectra = data_frame["Spectra"]
        aups = np.array(
            spectra.apply(lambda x: np.trapz(
                x[0, self.integral_q_range])).tolist()
        )
        image_height = math.floor(len(aups) / self.scan_width) - 1
        for i, aup in enumerate(aups):
            y = i / self.scan_width
            x = i % self.scan_width
            if y % 2 < 1:
                ret_image[image_height - math.floor(y), x] = aup
            else:
                ret_image[image_height -
                          math.floor(y), self.scan_width - 1 - x] = aup
        fig = plt.figure()
        ax = fig.add_subplot()
        mesh = ax.pcolormesh(ret_image, cmap="jet", vmin=aups.min())
        fig.colorbar(mappable=mesh, cmap="jet",
                     label="AUP", orientation="vertical")
        ax.set_aspect(1.0 / ax.get_data_ratio(), adjustable="box")
        return fig

    def __plot_3d_spectra(self):
        """
        Plotting logic for the aggregate spectra

        Returns
        -------
        fig : TYPE
            DESCRIPTION.

        """
        # open beam will be appended to the end
        spectra = self.data_frame["Spectra"]
        q_range = self.q_range[:-1]
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        bg_sub_data = spectra.apply(
            lambda x: np.subtract(x, spectra[len(spectra) - 1]))
        bg_sub_data = bg_sub_data[0:-1]
        for x in range(len(bg_sub_data)):
            ax.plot3D(
                q_range,
                [x] * len(q_range),
                np.reshape(spectra.iloc[x], (len(q_range)))
                - np.reshape(spectra.iloc[-1], (len(q_range))))
            ax.set_ylabel("Scan Number")
        ax.set_xlabel("${q(nm^{-1})}$")
        ax.set_zlabel("Counts")
        ax.grid(False)
        return fig
