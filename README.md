# Depth-Varied Filters

Apply filters to image using depth map to vary intensity.

## Requirements

* Python 2.7+
* OpenCV 2.4+ with Python support
* Numpy

## Inspiration

This originated as a project for the [Computational Photography](https://compphotography.wordpress.com/2015-oms/) Spring '15 at Georgia Tech. I was inspired by the [Google Camera](https://play.google.com/store/apps/details?id=com.google.android.GoogleCamera) for Android [Lens Blur](http://googleresearch.blogspot.com/2014/04/lens-blur-in-new-google-camera-app.html) feature and thought: "Blur is pretty cool. What would other filters look like?"

## Run

`$> python main.py INPUT.JPG DEPTHMAP.JPG LAYERS`

LAYERS is optional (default=15). LAYERS must be an integer.

Example:

`$> python main.py Flowers-alternative.jpg Flowers-depthmap.jpg 20`

^ The flower images used are from: [Depthy.me](http://depthy.me/) [[github](https://github.com/panrafal/depthy)]

## Create Your Own

You can use Google Camera Lens Blur to create an image and then pull out the source image and depth map using depthy.me.

## Future Ideas

- apply multiple filters
- smooth blending between layers (Gaussian blending)
- add plane selector for z-origin
- additional filters

## Author

Bran Sorem <[bransorem@gmail.com](mailto:bransorem@gmail.com)>