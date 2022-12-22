import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import cm
import numpy as np

class ImageFromGrid:
    """Creates images from FractalGrid objects
    
    fractalgrid: A FractalGrid object to be plotted
    cmap (optional): A colormap to use. Can be set later
    Idea is to allow for easy adjustment between different
    setting to lead up to a final image. Then to save that image.
    Going to make it stateful on the different options"""

    def __init__(self, fractalgrid, cmap=None):
        self.fractalgrid = fractalgrid
        self.cmap_start = cmap
        self.cmap = cmap

    def set_colormap(self, cmap):
        self.cmap_start = cmap
        self.cmap = cmap

    def colormap_add_black(self):
        """Changes the zero value on the colormap to black"""

        # Note: this only works for predefined color maps
        colormap = cm.get_cmap(self.cmap_start, 6000)
        map_vals = colormap(range(0,6001))
        map_vals[0] = np.array([0.0,0.0,0.0,1.0])
        self.cmap = ListedColormap(map_vals)

    def colormap_reverse_add_black(self):
        """Changes the zero value on the reversed colormap to black"""

        colormap = cm.get_cmap(self.cmap_start, 6000)
        map_vals = colormap(range(0,6001))[::-1]
        map_vals[0] = np.array([0.0,0.0,0.0,1.0])
        self.cmap = ListedColormap(map_vals)

    def reset_colormap(self):
        self.cmap = self.cmap_start

    def plot(self, smoothed=False, scaled=True, dpi=None, filename=None):
        """Creates an image
        
        smoothed: if remainders should be used to smooth (see FractalGrid)
        scaled: if values should be rescaled (see FractalGrid)
        dpi: If set, sets figure size to fractalgrid.shape/dpi in inches
        filename: If None, don't save to a file
            if a filename with an extension, save to that file
            if just 'jpg', '.png', or similar, filename generated using fractalgrid info:
            {name}_{shape[0]}x{shape[1]}.extension
            if dpi set: {name}_{shape_inches[0]}x{shape_inches[1]}_{dpi}dpi.extension"""

        to_plot = self.fractalgrid.plottable(smoothed=smoothed, scaled=scaled)

        fig = plt.figure(frameon=False)
        if dpi:
            width = self.fractalgrid.shape[0]/dpi
            height = self.fractalgrid.shape[1]/dpi
            fig.set_size_inches(width, height)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(to_plot, cmap=self.cmap)

        if filename:
            filename = self.make_filename(filename, dpi)

            if dpi:
                fig.savefig(filename, dpi=dpi)
            else:
                fig.savefig(filename)

        return fig

    def make_filename(self, filename, dpi):
        if '.' not in filename:
                filename = '.' + filename
        if filename[0] == '.':
            tempname = self.fractalgrid.name + "_"
            shape = self.fractalgrid.shape
            if dpi:
                shape[0] = shape[0]/dpi
                shape[1] = shape[1]/dpi
                if shape[0].is_integer():
                    shape[0] = int(shape[0])
                if shape[1].is_integer():
                    shape[1] = int(shape[1])
                tempname += '{}x{}_{}dpi'.format(*shape, dpi)
            else:
                tempname += '{}x{}'.format(*shape)
            filename = tempname + filename

        return filename
