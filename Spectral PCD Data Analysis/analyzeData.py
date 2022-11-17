import hxtV3Read
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import math


def analyzeData(binStart, binEnd, binWidth, energyWindow, backgroundFilePath, sampleFilePath):
    mat = scipy.io.loadmat('test_mask.mat')

    # caffeine, empty syringe
    [data0, bins0] = hxtV3Read.hxtV3Read(backgroundFilePath)
    [data1, bins1] = hxtV3Read.hxtV3Read(sampleFilePath)

    energy_bins = bins1
    N_ang = 50
    xData = []
    yData = []
    zData = []

    nTimes = math.ceil((binEnd - binStart + 1) / energyWindow)
    # See if it's a perfect square, so it can put the separated graphs in the neatest fashion
    #Subplot orgnization, getting the plt.subplot axes to fit the correct number of plots based on # of energy windows
    if math.floor(math.sqrt(nTimes)) == math.ceil(math.sqrt(nTimes)):
        xlen = int(math.sqrt(nTimes))
        # Changing Size depending on how many graphs are going to be made
        if xlen >= 3:
            fig, axs = plt.subplots(xlen, xlen, figsize=(xlen * 2 + 1, xlen * 2), sharex='all', squeeze=False)
        elif xlen >= 5:
            fig, axs = plt.subplots(xlen, xlen, figsize=(xlen + 1, xlen), sharex='all', squeeze=False)
        else:
            fig, axs = plt.subplots(xlen, xlen, figsize=(7, 6), sharex='all', squeeze=False)
    else:
        xlen = int(math.sqrt(nTimes)) + 1
        # Delete row if completely unused
        if 1 + (xlen - 1) * xlen > nTimes:
            if xlen >= 3:
                fig, axs = plt.subplots(xlen - 1, xlen, figsize=(xlen * 2 + 1, (xlen - 1) * 2), sharex='all',
                                        squeeze=False)
            elif xlen >= 5:
                fig, axs = plt.subplots(xlen - 1, xlen, figsize=(xlen + 1, xlen - 1), sharex='all', squeeze=False)
            else:
                fig, axs = plt.subplots(xlen - 1, xlen, figsize=(7, 6), sharex='all', squeeze=False)
        else:
            if xlen >= 3:
                fig, axs = plt.subplots(xlen, xlen, figsize=(xlen * 2 + 1, xlen * 2), sharex='all', squeeze=False)
            elif xlen >= 5:
                fig, axs = plt.subplots(xlen, xlen, figsize=(xlen + 1, xlen), sharex='all', squeeze=False)
            else:
                fig, axs = plt.subplots(xlen, xlen, figsize=(7, 6), sharex='all', squeeze=False)
        # Delete blank axes where there are no graphs and break out of the for loop if the row was deleted
        for k in range(0, xlen):
            try:
                if (k + 1) + (xlen - 2) * xlen > nTimes:
                    axs[xlen - 2][k].set_axis_off()
                if (k + 1) + (xlen - 1) * xlen > nTimes:
                    axs[xlen - 1][k].set_axis_off()
            except:
                break
    fig.suptitle('Raw Data', fontsize=18)
    yPosition = 0
    #loop needs to iterate for each subplt,  plots the 2D spetra for each of the defined windows
    #windows are still weird, the do not end at the binEnd
    for x in range(0, nTimes):

        try:
            Ei = np.arange(binStart + x * energyWindow, binStart + (x + 1) * energyWindow, binWidth)
            kkk = []

            for k in range(0, Ei.size):
                kkk.append(bins0[Ei[k] - 1])

            data11 = np.take(data1, Ei, axis=0)
            data00 = np.take(data0, Ei, axis=0)

            # direct subtraction of 2D data from open beam for Ei interval giving total counts
            data_correct2 = data11.sum(axis=0) - data00.sum(axis=0)
            # same as detector readout, but at each energy interval predefined by you
            # 2D plot of the detector at Ei
            # If statement to ensure you start at a new row if you reach the end of the last row
            if x >= xlen * (yPosition + 1):
                yPosition += 1
            image = axs[yPosition][x - xlen * yPosition].pcolormesh(np.flipud(data_correct2), cmap='jet', vmin=0)
            axs[yPosition][x - xlen * yPosition].set_title(str(binStart + x * energyWindow) + '-' + str(binStart + (x + 1)
                                                            * energyWindow - 1) + ' keV', fontweight="bold")
            bar = plt.colorbar(image, ax=axs[yPosition][x - xlen * yPosition])
            bar.set_label('Counts', rotation=270, fontsize=10, labelpad=15)
            axs[yPosition][x - xlen * yPosition].get_xaxis().set_visible(False)
            axs[yPosition][x - xlen * yPosition].get_yaxis().set_visible(False)

            # figure(2)
            # spectra in particular pixel
            data_sample = data11[:, ::-1, :]
            data_bg = data00[:, ::-1, :]

            # create a matrix for 80 by 80 pixels with 250 um pixel size
            px = 0.25  # pixel pitch in mm %change this based on how far is the beam from first pixel
            py = 0.25
            theta = np.empty((80, 80))
            q = np.empty((len(Ei), 80, 80))
            for jj in range(1, 81):
                for ii in range(1, 81):
                    d = math.sqrt((ii * px - .25 * 9) ** 2 + ((jj * py - .25 * 1) ** 2))  # refined AUG 31 for 1 mm pinhole
                    theta[jj - 1][ii - 1] = math.degrees(math.atan(d / 214))  # front 214,
                    for i in range(0, len(Ei)):
                        q[i][jj - 1][ii - 1] = 4 * math.pi * 1 / 1.24 * Ei[i] * math.sin(
                            math.radians(theta[jj - 1][ii - 1] / 2))

            # q binning to have same q interval for all data before summing them
            image11 = data_sample
            image22 = data_bg
            q_hist = np.linspace(0.04, 30.04, num=N_ang + 1)  # binning q - angles
            # q max is 30

            dq = q_hist[2] - q_hist[1]
            Zt = np.empty((N_ang - 1, len(Ei)))
            Ztb = np.empty((N_ang - 1, len(Ei)))
            for k in range(0, len(Ei)):
                image1 = np.take(image11, k, axis=0)  # for all pixel at one q for each pixel
                image2 = np.take(image22, k, axis=0)
                for j in range(0, N_ang - 1):  # binning
                    bins = np.logical_and(np.take(q, k, axis=0) >= q_hist[j], np.take(q, k, axis=0) < q_hist[j + 1])
                    # count the number of those locations
                    n = np.sum(np.sum(bins, axis=1), axis=0)
                    if n != 0:
                        # summed values at those binned locations
                        Zt[j][k] = np.sum(image1, where=bins)
                        Ztb[j][k] = np.sum(image2, where=bins)
                    else:
                        # special case for no bins(divide - by - zero)
                        Zt[j][k] = 0
                        Ztb[j][k] = 0
            xData.append(q_hist[:len(q_hist) - 2])
            yData.append(np.sum(Zt, axis=1) - np.sum(Ztb, axis=1))
            zData.append([binStart + x * energyWindow] * (N_ang - 1))
        except:
            break
    fig.tight_layout()
    plt.subplots_adjust(wspace=0.2)

    # 30 keV to 45 keV for 1 keV binning
    # Ei = np.arange(30, 46, 1)
    Ei = np.arange(binStart, binEnd + 1, binWidth)

    kkk = []

    for k in range(0, Ei.size):
        kk = Ei[k]
        kkk.append(bins0[Ei[k] - 1])

    data11 = np.take(data1, Ei, axis=0)
    data00 = np.take(data0, Ei, axis=0)

    # direct subtraction of 2D data from open beam for Ei interval giving total counts
    data_correct2 = data11.sum(axis=0) - data00.sum(axis=0)
    # 2D plot of the detector at Ei
    plt.figure(figsize=(7, 6))
    plt.pcolormesh(np.flipud(data_correct2), cmap='jet', vmin=0)
    bar = plt.colorbar()
    bar.set_label('Counts per Transmitted Photon', rotation=270, fontsize=16, labelpad=35)
    plt.axis('off')
    plt.title('Background Corrected (30-45 keV)', fontweight="bold")
    # figure(2)
    # spectra in particular pixel
    data_sample = data11[:, ::-1, :]
    data_bg = data00[:, ::-1, :]

    # create a matrix for 80 by 80 pixels with 250 um pixel size
    px = 0.25  # pixel pitch in mm %change this based on how far is the beam from first pixel
    py = 0.25
    theta = np.empty((80, 80))
    q = np.empty((len(Ei), 80, 80))
    for jj in range(1, 81):
        for ii in range(1, 81):
            d = math.sqrt((ii * px - .25 * 9) ** 2 + ((jj * py - .25 * 1) ** 2))  # refined AUG 31 for 1 mm pinhole
            theta[jj - 1][ii - 1] = math.degrees(math.atan(d / 214))  # front 214,
            for i in range(0, len(Ei)):
                q[i][jj - 1][ii - 1] = 4 * math.pi * 1 / 1.24 * bins1[Ei[i]] * math.sin(
                    math.radians(theta[jj - 1][ii - 1] / 2))
    # Creating Figure 4 Color Mesh
    plt.figure(figsize=(7, 6))
    plt.pcolormesh(theta, cmap='jet', vmin=0)
    bar2 = plt.colorbar()
    bar2.set_label('Scattering Angle', rotation=270, fontsize=16, labelpad=35)
    plt.axis('off')
    plt.title('Figure 3', fontweight="bold")

    # q binning to have same q interval for all data before summing them
    image11 = data_sample
    image22 = data_bg
    N_ang = 50
    q_hist = np.linspace(0.04, 30.04, num=N_ang + 1)  # binning q - angles
    # q max is 30

    dq = q_hist[2] - q_hist[1]
    Zt = np.empty((N_ang - 1, len(Ei)))
    Ztb = np.empty((N_ang - 1, len(Ei)))
    for k in range(0, len(Ei)):
        image1 = np.take(image11, k, axis=0)  # for all pixel at one q for each pixel
        image2 = np.take(image22, k, axis=0)
        for j in range(0, N_ang - 1):  # binning
            bins = np.logical_and(np.take(q, k, axis=0) >= q_hist[j], np.take(q, k, axis=0) < q_hist[j + 1])
            # count the number of those locations
            n = np.sum(np.sum(bins, axis=1), axis=0)
            if n != 0:
                # summed values at those binned locations
                Zt[j][k] = np.sum(image1, where=bins)
                Ztb[j][k] = np.sum(image2, where=bins)
            else:
                # special case for no bins(divide - by - zero)
                Zt[j][k] = 0
                Ztb[j][k] = 0

    plt.figure(figsize=(7, 6))
    ax = plt.axes(projection='3d')
    for x in range(0, nTimes):
        try:
            ax.plot3D(xData[x], zData[x], yData[x], label=str(binStart + x * energyWindow) + ' keV')
        except:
            break
    ax.legend()
    ax.grid(False)
    ax.set_title('Transmission Uncorrected Counts')
    ax.set_xlabel('${q(nm^{-1})}$')
    ax.set_ylabel('Energy(keV)')
    ax.set_zlabel('Counts')

    plt.figure(figsize=(7, 6))
    plt.plot(q_hist[:len(q_hist) - 2], np.sum(Zt, axis=1) - np.sum(Ztb, axis=1))
    plt.xlabel('${q(nm^{-1})}$', fontsize=16)
    plt.xlim(0, 30)
    plt.ylabel('Counts', fontsize=16)
    plt.ylim(0, np.max(np.sum(Zt, axis=1) - np.sum(Ztb, axis=1)))
    plt.title('Figure 5', fontweight="bold")

    plt.figure(figsize=(7, 6))
    plt.plot(q_hist[:len(q_hist) - 2], np.sum(Zt, axis=1))
    plt.plot(q_hist[:len(q_hist) - 2], np.sum(Ztb, axis=1), linestyle='dotted')
    plt.xlabel('${q(nm^{-1})}$', fontsize=16)
    plt.xlim(0, 30)
    plt.ylabel('Counts', fontsize=16)
    plt.ylim(0, np.max([np.sum(Zt, axis=1), np.sum(Ztb, axis=1)]))
    plt.legend(['Caffeine Powder', 'Syringe Background'], fontsize=14)
    plt.title('Figure 6', fontweight="bold")

    plt.show()

    # AUC calculation
    # Save this info with sample information

    q_data = q_hist[:len(q_hist) - 2]

    sSAXS_data = np.sum(Zt, axis=1) - np.sum(Ztb, axis=1)

    sSAXS_SAMPLE = np.sum(Zt, axis=1)

    sSAXS_BACKGROUND = np.sum(Ztb, axis=1)
