# Fractals

Formalizing and making reproducible the Fractal generating code I have been playing with. This is moving from the current system of Jupyter notebooks and pure functions to a more class-based and py file approach.

This code takes the basic idea of the Mandelbrot set and allows for a greater range of functional forms.

The base Mandelbrot set iterates $z = z^2  + c$, and produces an image by coloring the points $c$ by how long they take to "escape" (i.e. grow so large they diverge). The base set is those points that _don't_ diverge, traditionally colored black.

## Basic usage
To make a basic fractal, the steps are:

```python
man_gen = grid.FractalGenerator("Mandelbrot", lambda z: z**2)
man_grid = man_gen.create_grid("man", [-0.35, 0.1, 0.8, 1.15], niters=400, shape=(500,500))
man_img_grid = plot.ImageFromGrid(man_grid, 'rainbow_r')
img = man_img_grid.plot(filename='man_zoom.png')
```

The most important things that drive the process are the function (the `z**2` is for the Mandelbrot set), and the `niters` and `shape` drive the resolution and runtime.

## Future work
Eventually going to make a GUI to make this easier to explore.