from dataclasses import dataclass
from random import random, randint

@dataclass
class Blob:
    x: int
    y: int
    radius: int
    color: tuple

from PIL import Image  

width = 900
height = 300

img = Image.new( mode = "RGB", size = (width, height) )
list_of_pixels = list(img.getdata())

num_blobs = 20

def create_blob():
    return Blob(x = random() * width, 
                y = random() * height, 
                radius = 50 + random() * 100, 
                color = (255 * random(), 
                         255 * random(), 
                         255 * random()))

blobs = [create_blob() for _ in range(num_blobs)]

def saturate(rgb):
    rgb = tuple(channel if channel > 0 else 0 for channel in rgb)
    rgb = tuple(channel if channel < 255 else 255 for channel in rgb)
    return rgb

def saturate_0to1(n):
    n = n if n > 0 else 0
    n = n if n < 1 else 1
    return n

def render_blob_pixel(blob, x, y):
    n = -(((x - blob.x)**2 + (y - blob.y)**2) - blob.radius**2) / (blob.radius**2)
    n = saturate_0to1(n)
    return tuple(n * channel for channel in blob.color)

def render_pixel(list_of_pixels, x, y):
    offset = y * width
    index = offset + x
    blob_pixels = [render_blob_pixel(blob, x, y) for blob in blobs]
    pixel = tuple(int(sum(p)) for p in zip(*blob_pixels))
    list_of_pixels[index] = saturate(pixel)

for y in range(height):
    for x in range(width):
        render_pixel(list_of_pixels, x, y)

img.putdata(list_of_pixels)
img.show()
