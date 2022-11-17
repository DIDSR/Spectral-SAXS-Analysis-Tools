import numpy as np


def fread(fileID, sizeA, precision):
    data_array = None
    if precision == 'uint64':
        return np.fromfile(fileID, np.uint64, count=sizeA)
    elif precision == 'uint32':
        return np.fromfile(fileID, np.uint32, count=sizeA)
    elif precision == 'int32':
        return np.fromfile(fileID, np.int32, count=sizeA)
    elif precision == 'double':
        return np.fromfile(fileID, np.double, count=sizeA)
    elif precision == 'char':
        data_array = np.fromfile(fileID, np.int8, count=sizeA)
        return ''.join([chr(item) for item in data_array])
    else:  # This is for the dummy
        return np.fromfile(fileID, np.int8, count=sizeA)


def hxtV3Read(filePath):
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
