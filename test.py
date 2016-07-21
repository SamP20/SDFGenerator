import numpy as np
import matplotlib.pyplot as plt
from fontTools.ttLib import TTFont
from bitmapPen import BitmapPen
from scale import ScaledBitmap
import png
import sys

if __name__ == '__main__':
    argv = sys.argv
    font = TTFont(argv[1])
    glyf = font['glyf']['ampersand']
    glyf.getCoordinates(font['glyf'])
    pen = BitmapPen(font['glyf'], glyf.xMin, glyf.yMin, glyf.xMax, glyf.yMax, 64, 64)
    glyf.draw(pen, font['glyf'])
    
    #scaled = ScaledBitmap(64,64)
    #scaled.loadBitmap(pen.getBitmap())
    
    #g = Grid(64,64,glyf.xMin, glyf.xMax, glyf.yMin, glyf.yMax)
    #bz = CubicBezier((0.5,0.2),(0.8,0.4), (0.7,0.9))
    #g.draw_curve(bz)
    #bz = CubicBezier((0.7,0.9),(0.5,0.4), (0.3,0.9))
    #g.draw_curve(bz)
    png.from_array(pen.getBitmap(), 'L').save("temp/export.png")
    plt.imshow(pen.getBitmap(), cmap='Greys', vmin=0, vmax=255)
    plt.colorbar()
    plt.show()
