#! /usr/bin/env python

"""Test script for the imageop module.  This has the side
   effect of partially testing the imgfile module as well.
   Roger E. Masse
"""

from test_support import verbose, unlink

import imageop, uu

def main(use_rgbimg=1):

    # Create binary test files
    uu.decode(get_qualified_path('testrgb.uue'), 'test.rgb')

    if use_rgbimg:
        image, width, height = getrgbimage('test.rgb')
    else:
        image, width, height = getimage('test.rgb')

    # Return the selected part of image, which should by width by height
    # in size and consist of pixels of psize bytes.
    if verbose:
        print 'crop'
    newimage = imageop.crop (image, 4, width, height, 0, 0, 1, 1)

    # Return image scaled to size newwidth by newheight. No interpolation
    # is done, scaling is done by simple-minded pixel duplication or removal.
    # Therefore, computer-generated images or dithered images will
    # not look nice after scaling.
    if verbose:
        print 'scale'
    scaleimage = imageop.scale(image, 4, width, height, 1, 1)

    # Run a vertical low-pass filter over an image. It does so by computing
    # each destination pixel as the average of two vertically-aligned source
    # pixels. The main use of this routine is to forestall excessive flicker
    # if the image two vertically-aligned source pixels,  hence the name.
    if verbose:
        print 'tovideo'
    videoimage = imageop.tovideo (image, 4, width, height)

    # Convert an rgb image to an 8 bit rgb
    if verbose:
        print 'rgb2rgb8'
    greyimage = imageop.rgb2rgb8(image, width, height)

    # Convert an 8 bit rgb image to a 24 bit rgb image
    if verbose:
        print 'rgb82rgb'
    image = imageop.rgb82rgb(greyimage, width, height)

    # Convert an rgb image to an 8 bit greyscale image
    if verbose:
        print 'rgb2grey'
    greyimage = imageop.rgb2grey(image, width, height)

    # Convert an 8 bit greyscale image to a 24 bit rgb image
    if verbose:
        print 'grey2rgb'
    image = imageop.grey2rgb(greyimage, width, height)

    # Convert a 8-bit deep greyscale image to a 1-bit deep image by
    # thresholding all the pixels. The resulting image is tightly packed
    # and is probably only useful as an argument to mono2grey.
    if verbose:
        print 'grey2mono'
    monoimage = imageop.grey2mono (greyimage, width, height, 0)

    # monoimage, width, height = getimage('monotest.rgb')
    # Convert a 1-bit monochrome image to an 8 bit greyscale or color image.
    # All pixels that are zero-valued on input get value p0 on output and
    # all one-value input pixels get value p1 on output. To convert a
    # monochrome  black-and-white image to greyscale pass the values 0 and
    # 255 respectively.
    if verbose:
        print 'mono2grey'
    greyimage = imageop.mono2grey (monoimage, width, height, 0, 255)

    # Convert an 8-bit greyscale image to a 1-bit monochrome image using a
    # (simple-minded) dithering algorithm.
    if verbose:
        print 'dither2mono'
    monoimage = imageop.dither2mono (greyimage, width, height)

    # Convert an 8-bit greyscale image to a 4-bit greyscale image without
    # dithering.
    if verbose:
        print 'grey2grey4'
    grey4image = imageop.grey2grey4 (greyimage, width, height)

    # Convert an 8-bit greyscale image to a 2-bit greyscale image without
    # dithering.
    if verbose:
        print 'grey2grey2'
    grey2image = imageop.grey2grey2 (greyimage, width, height)

    # Convert an 8-bit greyscale image to a 2-bit greyscale image with
    # dithering. As for dither2mono, the dithering algorithm is currently
    # very simple.
    if verbose:
        print 'dither2grey2'
    grey2image = imageop.dither2grey2 (greyimage, width, height)

    # Convert a 4-bit greyscale image to an 8-bit greyscale image.
    if verbose:
        print 'grey42grey'
    greyimage = imageop.grey42grey (grey4image, width, height)

    # Convert a 2-bit greyscale image to an 8-bit greyscale image.
    if verbose:
        print 'grey22grey'
    image = imageop.grey22grey (grey2image, width, height)

    # Cleanup
    unlink('test.rgb')

def getrgbimage(name):
    """return a tuple consisting of image (in 'imgfile' format but
    using rgbimg instead) width and height"""

    import rgbimg

    try:
        sizes = rgbimg.sizeofimage(name)
    except rgbimg.error:
        name = get_qualified_path(name)
        sizes = rgbimg.sizeofimage(name)
    if verbose:
        print 'rgbimg opening test image: %s, sizes: %s' % (name, str(sizes))

    image = rgbimg.longimagedata(name)
    return (image, sizes[0], sizes[1])

def getimage(name):
    """return a tuple consisting of
       image (in 'imgfile' format) width and height
    """

    import imgfile

    try:
        sizes = imgfile.getsizes(name)
    except imgfile.error:
        name = get_qualified_path(name)
        sizes = imgfile.getsizes(name)
    if verbose:
        print 'imgfile opening test image: %s, sizes: %s' % (name, str(sizes))

    image = imgfile.read(name)
    return (image, sizes[0], sizes[1])

def get_qualified_path(name):
    """ return a more qualified path to name"""
    import sys
    import os
    path = sys.path
    try:
        path = [os.path.dirname(__file__)] + path
    except NameError:
        pass
    for dir in path:
        fullname = os.path.join(dir, name)
        if os.path.exists(fullname):
            return fullname
    return name

# rgbimg (unlike imgfile) is portable to platforms other than SGI.
# So we prefer to use it.
main(use_rgbimg=1)
