from fontTools.pens.basePen import BasePen
import numpy as np

class BitmapPen(BasePen):
    """This class draws a bitmap to a numpy array using horizontal scanlines"""
    def __init__(self, glyphSet, xmin, ymin, xmax, ymax):
        super().__init__(glyphSet)
        self.offset = np.array([xmin-1,ymin-1])
        self.size = np.array([xmax+2,ymax+2])-self.offset
        self.resetBitmap()
        
    def resetBitmap(self):
        self.bitmap = np.zeros(self.size[::-1], dtype=np.uint8)
        
    def getBitmap(self):
        return self.bitmap!=0
        
    def _moveTo(self, pt):
        pass

    def _lineTo(self, pt):
        x1, y1 = self._transform(self._getCurrentPoint())
        x2, y2 = self._transform(pt)
		
		# Ignore horizontal lines
        if y1 == y2:
            return
		    
        m = (x2-x1)/(y2-y1)
        c = x1 - m*y1
		    
        goingUp = y2 > y1
            
        start = (int(y1) if goingUp else int(y2))+1
        stop = (int(y2) if goingUp else int(y1))+1
        for y in range(start,stop):
            x = int(round(m*y + c))
            self.bitmap[y,x:] += 1 if goingUp else -1

    def _curveToOne(self, pt1, pt2, pt3):
        x1, y1 = self._transform(self._getCurrentPoint())
        x2, y2 = self._transform(pt1)
        x3, y3 = self._transform(pt2)
        x4, y4 = self._transform(pt3)
		
        start = int(min([y1,y2,y3,y4]))+1
        stop = int(max([y1,y2,y3,y4]))+1
		
        dy = y1
        cy = (y2 - dy) * 3.0
        by = (y3 - y2) * 3.0 - cy
        ay = y4 - dy - cy - by
		
        dx = x1
        cx = (x2 - dx) * 3.0
        bx = (x3 - x2) * 3.0 - cx
        ax = x4 - dx - cx - bx
		
        for y in range(start,stop):
            roots = np.roots([ay,by,cy,dy-y])
            roots = roots[np.isreal(roots)]
            roots = roots[np.logical_and(-1e-10 <= roots, roots <= 1+1e-10)]
            roots = np.sort(roots)
            if not len(roots):
                continue
		        
            lastT = None
            for t in roots:
                if t==lastT:
                    continue
                lastT = t
                t2 = t * t
                t3 = t2 * t

                direction = 3*ay*t2 + 2*by*t + cy
                if direction == 0.0:
                    direction = 6*ay*t + 2*by
                    if direction == 0.0:
                        direction = ay
                        if direction == 0.0:
                            # Ignore horizontal lines
                            continue
                    else:
                        # We have a turning point. Ignore it
                        continue
                goingUp = direction > 0.0
                
                xt = int(round(ax*t3 + bx*t2 + cx*t + dx))
                delta = 0
                
                # Double check against endpoints incase rounding errors have
                # given false positives (extremely unlikely but possible).
                if t <= 0.0 and y == y1 and not goingUp:
                    delta = -1
                elif t >= 1.0 and y == y4 and goingUp:
                    delta = 1
                elif 0.0 < t < 1.0:
                    delta = 1 if goingUp else -1
                else:
                    continue
                    
                self.bitmap[y,xt:] += delta
		
    def _transform(self, pt):
        return (pt[0]-self.offset[0], pt[1]-self.offset[1])
        

    def addComponent(self, glyphName, transformation):
        """This default implementation simply transforms the points
        of the base glyph and draws it onto self.
        """
        from fontTools.pens.transformPen import TransformPen
        try:
            glyph = self.glyphSet[glyphName]
        except KeyError:
            pass
        else:
            tPen = TransformPen(self, transformation)
            #Monkey patched to add second argument
            glyph.draw(tPen, self.glyphSet)
