'''
22 colors which can be easily distinguished by human eyes
Red, Green, Yellow, Blue, Orange, Purple, Cyan, Magenta, Lime, Pink, teal, lavender, brown, beige, maroon, mint, olive, apricot, navy, grey, white, black
'''
# COLORS = [[230, 25, 75], [60, 180, 75], [255, 225, 25], [67, 99, 216], [245, 130, 49], [145, 30, 180], [66, 212, 244],
#           [240, 50, 230], [191, 239, 69], [250, 190, 212], [70, 153, 144], [220, 190, 255], [154, 99, 36],
#           [255, 250, 200], [128, 0, 0], [170, 255, 195], [128, 128, 0], [255, 216, 177], [0, 0, 117], [169, 169, 169],
#           [255, 255, 255], [0, 0, 0]]
# print(COLORS[0][0])
# import math
#
# import numpy as np
# import colorsys
#
# def _get_colors(num_colors):
#     colors=[]
#     for i in np.arange(0., 360., 360. / num_colors):
#         hue = i/360.
#         lightness = (50 + np.random.rand() * 10)/100.
#         saturation = (90 + np.random.rand() * 10)/100.
#         colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
#     return colors
#
# if __name__ == "__main__":
#     colors = _get_colors(10)
#     for i in range(1, 9):
#         print(math.sqrt((colors[i][0]-colors[0][0])**2+(colors[i][1]-colors[0][1])**2+(colors[i][2]-colors[0][2])**2))
#     print(_get_colors(10))