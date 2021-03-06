def interpolate(inp, fi):
    i, f = int(fi // 1), fi % 1 
    j = i+1 if f > 0 else i 
    return (1-f) * inp[i] + f * inp[j]

def Render():
    import os
    import numpy as np
    import matplotlib.pyplot as plt  
    from scipy.signal import savgol_filter
    import cv2
    import peakutils.peak
    from PIL import Image

    val=[]
    indecies = [i for i in range(100,2000,200)]
    for i in indecies:
        for j in indecies:
            val.append([i,j]) 

    harvest_dates = []
    cycles = []

    for v in val:
        pix_2017 = []
        for filename in os.listdir(os.getcwd()):
            if filename.endswith("2_clipped.tif"):
                im = Image.open(filename)
                imarray = np.array(im)
                imarray =  imarray/255
                if filename.startswith("awifs_ndvi_2017"):
                    pix_2017.append(imarray[v[0]][v[1]])
            inp = pix_2017
        new_len = 48
        delta = (len(inp)-1) / (new_len-1)
        outp = [interpolate(inp, i*delta) for i in range(new_len)]
        res = savgol_filter(outp, 5, 3)
        indexes = peakutils.peak.indexes(np.array(res), min_dist=10)
        indexes_mod = [i//4 for i in indexes]
        harvest_dates.append(indexes_mod)
        cycles.append(len(indexes))

    image = cv2.imread('awifs_ndvi_201701_15_2_clipped.tif') 

    for i in range(len(val)):
        if cycles[i] == 1:
            colour = (0,255,0)
        elif cycles[i] == 2:
            colour = (255,0,0)
        else:
            colour = (0,255,0)
        image = cv2.circle(image,(val[i][0], val[i][1]), 16, colour, -3)
    cv2.imwrite('final_image.tif', image)  