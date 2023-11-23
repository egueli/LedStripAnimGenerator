from dataclasses import dataclass

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

blobs = [
    Blob(320, 110, 25, (255, 0, 0)),
    Blob(350, 110, 25, (255, 0, 0)),
]

def saturate(rgb):
    rgb = tuple(channel if channel > 0 else 0 for channel in rgb)
    rgb = tuple(channel if channel < 255 else 255 for channel in rgb)
    return rgb

def render_blob_pixel(blob, x, y):
    n = -(((x - blob.x)**2 + (y - blob.y)**2) - blob.radius**2) / (blob.radius**2)
    n = int(n * 256)
    return saturate((n, n, n))

def render_pixel(list_of_pixels, x, y):
    offset = y * width
    index = offset + x
    blob_pixels = [render_blob_pixel(blob, x, y) for blob in blobs]
    pixel = tuple(sum(p) for p in zip(*blob_pixels))
    list_of_pixels[index] = saturate(pixel)

for y in range(height):
    for x in range(width):
        render_pixel(list_of_pixels, x, y)

img.putdata(list_of_pixels)
img.show()
