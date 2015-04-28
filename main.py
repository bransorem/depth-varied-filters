## Final Project
# Brannen Sorem

import sys
import os
import numpy as np
import cv2

# [0]main.py [1]filename [2]depth [3]num_layers
if len(sys.argv) < 3:
  print "You need to include a source image and depth-map image. See README.md"
  exit()

file_name = sys.argv[1]
depth_map = sys.argv[2]
NUM_LAYERS = int(sys.argv[3]) if len(sys.argv) > 3 else 15

img = cv2.imread(file_name)
row,col,a = img.shape
roi = img[0:row, 0:col]
depth = cv2.imread(depth_map)
out = np.zeros(img.shape)

min_depth = np.min(np.unique(depth))
max_depth = np.max(np.unique(depth))

s = (max_depth - min_depth) // NUM_LAYERS
layers = np.array(range(min_depth, max_depth, s))


###############################################
### Get layer mask (slice)
###############################################

# Create mask layer between values (s)tart <-> (e)nd
def layer_mask(img, s, e):
  # create mask in single, grayscale channel
  dm = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  # copy image dimensions, but fill with zeros
  m = np.zeros(dm.shape)
  # set values above start threshold to white
  m[dm > s] = 255
  # set values above end threshold to black
  m[dm > e] = 0
  # set mask to 3 channels
  cp = np.zeros(img.shape)
  cp[:,:,0] = m[:,:]
  cp[:,:,1] = m[:,:]
  cp[:,:,2] = m[:,:]
  # messy way to get correct format for OpenCV
  cv2.imwrite('tmp.jpg', cp)
  o = cv2.imread('tmp.jpg')
  os.remove('tmp.jpg')
  return o


###############################################
### Filters
###############################################

# Change blur by epsilon value (a)
def blur_filter(img, a):
  # increase kernel effect slowly, must be odd
  k = (a / 10) + 1 if (a / 10) % 2 == 0 else (a / 10) + 2
  # can't exceed 255
  k = k if k < 255 else 255
  kernel = (k, k)
  # blur filter
  o = cv2.GaussianBlur(img, kernel, 5)
  return o

# Change hue by epsilon value (a)
def hue_filter(img, a):
  tmp = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  o = tmp
  o[:,:,0] = tmp[:,:,0] + a
  o = cv2.cvtColor(o, cv2.COLOR_HSV2BGR)
  return o

# Change saturation by epsilon value (a)
def saturation_filter(img, a):
  tmp = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  o = tmp
  # normalize 180->0 by layer sizes
  v = int(180 - (float(a.item()) / max_depth) * (180+min_depth))
  o[:,:,1] = float(tmp[500,500,1]) * (float(v) / 180)
  o = cv2.cvtColor(o, cv2.COLOR_HSV2BGR)
  return o

# Change edge amount by epsilon value (a)
def edge_filter(img, a):
  lap = cv2.Laplacian(img, 8)
  b = float(a.item())
  k = (255-b+20) / 255
  j = 1 - k
  o = cv2.addWeighted(img, k, lap, j, 0, dtype=0)
  return o

# Change darkness by epsilon value (a)
def night_filter(img, a):
  o = np.zeros(img.shape)
  b = float(a.item())
  k = (255-b+20) / 255
  j = 1 - k
  o = cv2.addWeighted(img, k, o, j, 0, dtype=0)
  return o

# Change lightness by epsilon value (a)
def fog_filter(img, a):
  o = np.zeros(img.shape)
  o[o == 0] = 255
  b = float(a.item())
  k = (255-b+20) / 255
  j = 1 - k
  o = cv2.addWeighted(img, k, o, j, 0, dtype=0)
  return o

###############################################
### Filters
###############################################

# Get layer slice in correct format
def get_layer(slice, l_mask):
  ret, mask = cv2.threshold(l_mask, 100, 255, cv2.THRESH_BINARY)
  mask_inv = cv2.bitwise_not(mask)
  layer = cv2.bitwise_and(slice, slice, mask = mask[:,:,0])
  return layer, mask, mask_inv


###############################################
### For each slice of the image
###############################################

# Run mask on all layers and combine into output (out)
for a in layers:
  l_mask = layer_mask(depth, a, a+s)
  # res = blur_filter(img, a - min_depth)
  # res = hue_filter(img, a - min_depth)
  # res = saturation_filter(img, a - min_depth)
  # res = edge_filter(img, a)
  res = fog_filter(img, a)
  # res = night_filter(img, a)

  layer, mask, mask_inv = get_layer(res, l_mask)
  out = cv2.add(out, layer, dtype=0)



###############################################
### Display
###############################################

# rescale image for display
h,w,c = out.shape
ha = h*2 // 3
wa = w*2 // 3

# show results in window
out = cv2.resize(out, (wa,ha))
cv2.imshow('Depth Filters', out)
cv2.waitKey(0)

# cv2.imwrite("output.jpg", out)


