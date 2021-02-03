
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from PIL import Image 
from scipy.misc import *
import colorsys
	
def shift_brightness_contrast(image, brightness=-100, contrast=300):
  def vect(a):
    c = contrast
    b = 100 * brightness
    res = ((a - 127.5) * c + 127.5) + b
    if res <0 :
      return 0
    if res > 255:
      return 255
    return res
  transform = np.vectorize(vect)
  data = transform(np.asarray(image)).astype(np.uint8)
  return Image.fromarray(data)
  
  
def get_red(source, brightness=-150, contrast = 500):
	image        = source.convert("YCbCr")
	layer        = image.split()[2];
	layer        = shift_brightness_contrast(layer,brightness,contrast)
	return layer
  
def shift_hue_saturation(image, hue = -90, saturation = 0.65):
	""" Rotate hue and set the contrast""" 
	copy = image.copy()
	ld = copy.load()
	width, height = copy.size
	for y in range(height):
		for x in range(width):
			pixel = ld[x,y]
			r = pixel[0]
			g = pixel[1]
			b = pixel[2]
			
			h,s,v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
			h = (h + hue/360.0) % 1.0
			s = s**saturation
			r,g,b = colorsys.hsv_to_rgb(h, s, v)
			ld[x,y] = (int(r * 255.9999), int(g * 255.9999), int(b * 255.9999))
	return copy
	
def get_brown(source, brightness=-100, contrast = 500, hue=-90, saturation=0.65):
	image        = shift_hue_saturation(source)
	image        = image.convert("YCbCr")
	layer        = image.split()[2];
	layer 		 = shift_brightness_contrast(layer,brightness,contrast)
	return layer
  
def get_white_pixels(source):
	return source.histogram()[-1]