import numpy as np

class ScaledBitmap(object):
    def __init__(self, width, height, padding=2):
        self.bitmap = np.zeros((height, width), dtype=np.uint8)
        self.padding = padding
        
    def loadBitmap(self, bmp):
        origH, origW = bmp.shape
        newH, newW = self.bitmap.shape
        self.scale = np.array((origW/(newW-2*self.padding), origH/(newH-2*self.padding)))
        for y in range(self.bitmap.shape[0]):
            for x in range(self.bitmap.shape[1]):
                px = (x-self.padding)*self.scale[0]
                py = (y-self.padding)*self.scale[1]
                
                outside=True                
                if (0 <= px < origW) and (0 <= py < origH):
                    outside = not bmp[py,px]
                
                minX = max(px-130,0)
                minY = max(py-130,0)
                maxX = min(px+130,origW)
                maxY =  min(py+130,origH)
                
                searchRange = bmp[minY:maxY,minX:maxX]
                nearby = np.dstack(np.where(searchRange==outside))
                closest = 128.
                if nearby.shape[1]:
                    nearby = nearby.astype(float) + np.array((minY-py,minX-px))
                    closest = np.min(np.sqrt(nearby[...,0]**2. + nearby[...,1]**2.))
                    
                self.bitmap[y,x] = int(np.clip(closest, 0., 255.))
                
                if outside:
                    self.bitmap[y,x] = int(np.clip(128.-closest, 0., 128.))
                else:
                    self.bitmap[y,x] = int(np.clip(128.+closest, 128., 255.))
