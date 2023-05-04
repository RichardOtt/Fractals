# Fractals

Formalizing and making reproducible the Fractal generating code I have been playing with. This is moving from the current system of Jupyter notebooks and pure functions to a more class-based and py file approach.

This code takes the basic idea of the Mandelbrot set and allows for a greater range of functional forms.

The base Mandelbrot set iterates $z = z^2  + c$, and produces an image by coloring the points $c$ by how long they take to "escape" (i.e. grow so large they diverge). The base set is those points that _don't_ diverge, traditionally colored black.
