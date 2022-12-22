import numpy as np
import time
from numba import jit

class FractalGrid:
    """The data points associated with a fractal
    
    Effectively a "concrete" fractal, this is the grid of points needed 
    to generate an image. Contains all the information needed:
    name: an identifier string, used for filename generation
    escape: iteration when value exceeded threshold for being in the set
    remain: value when it escaped, helps smooth coloring
    shape: dimension pixels/points
    niters: number of iterations used in generation, for tracking
    desc: description, include things like function used
    """
    def __init__(self, name, escape, remain, shape, niters, desc):
        self.name = name
        self.escape = escape
        self.remain = remain
        self.shape = shape
        self.niters = niters
        self.desc = desc

    def plottable(self, smoothed=False, scaled=True):
        """Converts the raw iterations to something more plot friendly
        
        smoothed: whether to use remainders to smooth color transitions
        scaled: applies scale_for_plot, converting to log(escape) behavior
        
        Returns a grid suitable for plotting"""
        if smoothed:
            offset = np.log(self.remain)
            minimum = np.min(offset[offset > 0])
            maximum = np.max(offset[offset > 0])
            offset = np.maximum((offset - minimum) / (maximum - minimum), 0)
            to_plot = self.escape - offset
        else:
            to_plot = self.escape

        if scaled:
            to_plot = self.scale_for_plot(to_plot)

        return to_plot

    @staticmethod
    def scale_for_plot(z):
        """Takes raw iterations to something more plot-friendly

        Applies a transformation of z -> max(z) - log(z)
        and sets infinities (i.e. z = 0) to 0"""
        #separating as a function in case I want to adjust later
        #or add multiple options
        
        plot = -np.log(z) + np.log(np.max(z))
        plot[np.isinf(plot)] = 0
        return plot

    def save(self):
        # should this be one jumbo file or three smaller ones?
        # i.e. an npy for escape, an npy for r, and a text file
        pass


class FractalGenerator:
    """Generates fractals
    
    This is the main class. Takes a function to iterate over and
    generates FractalGrid for given sets of coordinates. It will
    check on optimized numba based implementations if available.
    
    name: used to track files and such. Make it unique for a function
    function: if a string, look for the corresponding numba implementation
              if a function, use that function to iterate"""

    def __init__(self, fractal_name, function):
        self.fractal_name = fractal_name
        self.function = function

    def create_grid(self, name, boundaries, niters, shape, dpi=None):
        """Creates a concrete fractal grid
        
        name: identfies this particular image (including boundaries). Make it unique
        boundaries: the complex coordinates of the region to image, values of c
                    four element list, in order: [re_min, re_max, im_min, im_max]
        niters: how many iterations to run. May influence fine details of plot
        shape: two tuple of number of (real_points, imaginary_points)
               if dpi is not None, shape = shape * dpi
               So can do 8 x 10 image, 300 dpi more easily
        dpi: points per inch, if set shape is interpreted as inches instead of points
        
        Returns the FractalGrid corresponding to this image"""

        # todo: add caching
        #       optimized functions

        if dpi:
            shape = [x*dpi for x in shape]
        c = self.make_c(*boundaries, *shape)

        escape, remain = self.iterate(c, niters)

        return FractalGrid(name, escape, remain, shape, niters)
    
    @staticmethod
    def make_c(re_min, re_max, im_min, im_max, re_points, im_points):
        """Creates the grid of complex values to iterate
        
        Turns boundaries and number of points to c"""
        x = np.linspace(re_min, re_max, re_points)
        y = np.linspace(im_max, im_min, im_points)
        re_grid, im_grid = np.meshgrid(x, y)
        c = re_grid + complex(0,1)*im_grid

        return c

    def iterate(self, c, niters):
        z = np.zeros_like(c)
        mask = np.ones_like(c, dtype=np.int32)
        solution = np.zeros_like(c,dtype=np.int32)
        remains = np.zeros_like(c,dtype=np.float32)

        maxp = niters
        for i in range(1,maxp):
            z = self.function(z) + c*mask
            status = np.abs(z) < 100
            mask = mask * status
            solution += np.logical_not(status)*i
            remains += np.logical_not(status)*np.abs(z)
            z = z*mask
            
        return (solution, remains)
