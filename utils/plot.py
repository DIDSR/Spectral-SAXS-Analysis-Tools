from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


class PlotUtils:

    def plot_3d_spectra(
        spectra: pd.Series, q_range: np.ndarray, plot_type: str, windows: np.ndarray
    ):
        q_range = q_range[:-1]
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        if plot_type == "windowing":
            bg_sub_data = np.subtract(spectra[0], spectra[1])
            for x in range(len(bg_sub_data)):
                print(windows[x, 0])
                print(len(q_range))
                ax.plot3D(
                    q_range,
                    [windows[x, 0]] * len(q_range),
                    bg_sub_data[x],
                    label=str(windows[x, 0]) + " keV",
                )
            ax.set_ylabel("Energy(keV)")
        else:
            # open beam will be appended to the end
            bg_sub_data = spectra.apply(
                lambda x: np.subtract(x, spectra[len(spectra) - 1])
            )
            """
            Testing w/o bg sub in plotting function
            """
            # bg_sub_data = spectra
            bg_sub_data = bg_sub_data[0:-1]
            for x in range(len(bg_sub_data)):
                ax.plot3D(
                    q_range,
                    [x] * len(q_range),
                    np.reshape(spectra.iloc[x], (len(q_range)))
                    - np.reshape(spectra.iloc[-1], (len(q_range))),
                )
                ax.set_ylabel("Scan Number")
        ax.set_xlabel("${q(nm^{-1})}$")
        ax.set_zlabel("Counts")
        ax.grid(False)
        return fig
