from enum import Enum
from typing import Dict
import numpy as np
from models import sSAXS_tools as s
import pandas as pd
from matplotlib import pyplot as plt
from utils import PlotUtils
import math


class EnergyWindowingModel:

    class Property(str, Enum):
        ENERGY_RANGE_MIN = "energy_range_min"
        ENERGY_RANGE_MAX = "energy_range_max"
        BIN_WIDTH = "bin_width"
        ENERGY_WINDOW_WIDTH = "energy_window_width"
        SAMPLE_FILE_PATH = "sample_file_path"
        BACKGROUND_FILE_PATH = "background_file_path"
        DETECTOR_DISTANCE_mm = "detector_distance_mm"
        q_START = "global_q_start"
        q_END = "global_q_end"
        TRANSMISSION_BEAM_X = "transmission_beam_x"
        TRANSMISSION_BEAM_Y = "transmission_beam_y"

    def __init__(self, data: Dict[Property, object]):

        self.energy_range = np.arange(
            data.get(self.Property.ENERGY_RANGE_MIN),
            data.get(self.Property.ENERGY_RANGE_MAX)+1,
            data.get(self.Property.BIN_WIDTH),
            dtype=int,
        )

        self.energy_window_width = data.get(self.Property.ENERGY_WINDOW_WIDTH)
        self.background_file_path = data.get(
            self.Property.BACKGROUND_FILE_PATH)
        self.sample_file_path = data.get(self.Property.SAMPLE_FILE_PATH)

        self.detector_distance = data.get(self.Property.DETECTOR_DISTANCE_mm)
        self.q_range = np.linspace(
            data.get(self.Property.q_START), data.get(self.Property.q_END), num=51
        )
        self.transmission_beam_x = data.get(self.Property.TRANSMISSION_BEAM_X)
        self.transmission_beam_y = data.get(self.Property.TRANSMISSION_BEAM_Y)
        self.dataframe = pd.DataFrame()
        self.windows: np.ndarray = None
        self.theta: np.ndarray = None
        self.figures = {}

    def plot_windowing_figures(self):
        sample_data = s.bundle_data(self.sample_file_path)
        background_data = s.bundle_data(self.background_file_path)
        self.data_frame = pd.concat(
            [sample_data, background_data], ignore_index=True)
        self.windows, self.theta = s.extract_spectra(
            self.data_frame,
            samp_det_dist=self.detector_distance,
            transm_beam_x_pos=self.transmission_beam_x,
            transm_beam_y_pos=self.transmission_beam_y,
            energy_range=self.energy_range,
            q_range=self.q_range,
            energy_window_width=self.energy_window_width)

        spectra = pd.Series(self.data_frame["Spectra"])
        """
        Plotting
        """
        self.figures["window_3d"] = self.__plot_3d_spectra()
        self.figures["detector_images_windowed"] = self.__plot_windowed_det_images()
        self.figures["detector_image"] = self.__plot_det_image()
        self.figures["theta_map"] = self.__plot_theta()
        self.figures["bg_sub_plot"] = self.__plot_bg_sub_spectrum()
        self.figures["spectra"] = self.__plot_spectra()
        plt.show(block=False)
        print("Finish")

    def __plot_windowed_det_images(self):
        nTimes = len(self.windows)
        fig = plt.figure()
        if math.floor(math.sqrt(nTimes)) == math.ceil(math.sqrt(nTimes)):
            xlen = int(math.sqrt(nTimes))
            # Changing Size depending on how many graphs are going to be made
            if xlen >= 3:
                fig, axs = plt.subplots(
                    xlen,
                    xlen,
                    figsize=(xlen * 2 + 1, xlen * 2),
                    sharex="all",
                    squeeze=False,
                )
            elif xlen >= 5:
                fig, axs = plt.subplots(
                    xlen, xlen, figsize=(xlen + 1, xlen), sharex="all", squeeze=False
                )
            else:
                fig, axs = plt.subplots(
                    xlen, xlen, figsize=(7, 6), sharex="all", squeeze=False
                )
        else:
            xlen = int(math.sqrt(nTimes)) + 1
            # Delete row if completely unused
            if 1 + (xlen - 1) * xlen > nTimes:
                if xlen >= 3:
                    fig, axs = plt.subplots(
                        xlen - 1,
                        xlen,
                        figsize=(xlen * 2 + 1, (xlen - 1) * 2),
                        sharex="all",
                        squeeze=False,
                    )
                elif xlen >= 5:
                    fig, axs = plt.subplots(
                        xlen - 1,
                        xlen,
                        figsize=(xlen + 1, xlen - 1),
                        sharex="all",
                        squeeze=False,
                    )
                else:
                    fig, axs = plt.subplots(
                        xlen - 1, xlen, figsize=(7, 6), sharex="all", squeeze=False
                    )
            else:
                if xlen >= 3:
                    fig, axs = plt.subplots(
                        xlen,
                        xlen,
                        figsize=(xlen * 2 + 1, xlen * 2),
                        sharex="all",
                        squeeze=False,
                    )
                elif xlen >= 5:
                    fig, axs = plt.subplots(
                        xlen,
                        xlen,
                        figsize=(xlen + 1, xlen),
                        sharex="all",
                        squeeze=False,
                    )
                else:
                    fig, axs = plt.subplots(
                        xlen, xlen, figsize=(7, 6), sharex="all", squeeze=False
                    )
        # Delete blank axes where there are no graphs and break out of the for loop if the row was deleted
        yPosition = 0
        bg_corrected_data = self.data_frame.at[0,
                                               "Image"] - self.data_frame.at[1, "Image"]
        for k in range(0, xlen):
            try:
                if (k + 1) + (xlen - 2) * xlen > nTimes:
                    axs[xlen - 2][k].set_axis_off()
                if (k + 1) + (xlen - 1) * xlen > nTimes:
                    axs[xlen - 1][k].set_axis_off()
            except:
                break
        for x, key in enumerate(self.windows):
            window = self.windows[key]
            if x >= xlen * (yPosition + 1):
                yPosition += 1
            image = axs[yPosition][x - xlen * yPosition].pcolormesh(
                np.flipud(bg_corrected_data[window].sum(axis=0)), cmap="jet", vmin=0)
            axs[yPosition][x - xlen * yPosition].set_title(
                str(window[0]) + "-" + str(window[-1]) + " keV", fontweight="bold")
            bar = plt.colorbar(image, ax=axs[yPosition][x - xlen * yPosition])
            bar.set_label("Counts", rotation=270, fontsize=10, labelpad=15)
            axs[yPosition][x - xlen * yPosition].get_xaxis().set_visible(False)
            axs[yPosition][x - xlen * yPosition].get_yaxis().set_visible(False)
        fig.tight_layout()
        return fig

    def __plot_det_image(self):
        bg_corrected_data = (
            self.data_frame.at[0, "Image"] - self.data_frame.at[1, "Image"]
        )
        bg_corrected_data = bg_corrected_data[self.energy_range, :, :]
        bg_corrected_data = np.flipud(bg_corrected_data.sum(axis=0))
        fig = plt.figure()
        ax = fig.add_subplot()
        mesh = ax.pcolormesh(bg_corrected_data, cmap="jet", vmin=0)
        fig.colorbar(mappable=mesh, cmap="jet",
                     label="Counts", orientation="vertical")
        ax.set_aspect(1.0 / ax.get_data_ratio(), adjustable="box")
        # plt.title(
        #     "Background Corrected ("
        #     + str(self.energy_range[0])
        #     + "-"
        #     + str(self.energy_range[-1])
        #     + "keV)",
        #     fontweight="bold",
        # )
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        return fig

    def __plot_theta(self):
        fig = plt.figure()
        ax = fig.add_subplot()
        mesh = ax.pcolormesh(self.theta, cmap="jet", vmin=0)
        fig.colorbar(
            mappable=mesh, cmap="jet", label="Scattering Angle", orientation="vertical"
        )
        ax.set_aspect(1.0 / ax.get_data_ratio(), adjustable="box")
        return fig

    def __plot_bg_sub_spectrum(self):
        sample = self.data_frame.at[0, "Spectra"]
        background = self.data_frame.at[1, "Spectra"]
        if len(self.windows) > 1:
            sample = np.sum(sample, axis=0)
            background = np.sum(background, axis=0)
        q_range = self.q_range[:-1]
        bg_sub_data = np.reshape(sample - background, (len(q_range)))
        fig = plt.figure(figsize=(7, 6))
        plt.plot(q_range, bg_sub_data)
        plt.xlabel("${q(nm^{-1})}$", fontsize=16)
        plt.xlim(0, 30)
        plt.ylabel("Counts", fontsize=16)
        plt.ylim(0, np.max(sample - background))
        plt.yticks(fontsize=16)
        plt.xticks(fontsize=16)
        plt.title("Background Subtracted Spectrum", fontweight="bold")
        return fig

    def __plot_spectra(self):
        sample = self.data_frame.at[0, "Spectra"]
        background = self.data_frame.at[1, "Spectra"]
        if len(self.windows) > 1:
            sample = np.sum(sample, axis=0)
            background = np.sum(background, axis=0)
        q_range = self.q_range[:-1]
        fig = plt.figure(figsize=(7, 6))
        plt.plot(q_range, np.reshape(sample, (len(q_range))))
        plt.plot(q_range, np.reshape(
            background, (len(q_range))), linestyle="dotted")
        plt.xlabel("${q(nm^{-1})}$", fontsize=16)
        plt.xlim(0, 30)
        plt.ylabel("Counts", fontsize=16)
        plt.yticks(fontsize=16)
        plt.xticks(fontsize=16)
        # plt.title("Background Subtracted Spectrum", fontweight="bold")
        plt.legend(["Sample", "Background"], fontsize=16)
        return fig

    def __plot_3d_spectra(self):
        spectra = self.data_frame["Spectra"]
        q_range = self.q_range[:-1]
        fig = plt.figure(figsize=(7, 6))
        ax = fig.add_subplot(projection="3d")
        bg_sub_data = np.subtract(spectra[0], spectra[1])
        for x in range(len(bg_sub_data)):
            window = self.windows[x]
            ax.plot3D(
                q_range,
                [window[0]] * len(q_range),
                bg_sub_data[x],
                label=str(window[0]) + " keV",
            )
        ax.set_ylabel("Energy(keV)")
        ax.set_xlabel("${q(nm^{-1})}$")
        ax.set_zlabel("Counts")
        ax.grid(False)
        return fig
