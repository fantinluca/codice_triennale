from PIL import Image
import numpy as np
import os

# apriamo immagine originale
script_dir = os.path.dirname(os.path.abspath(__file__))
image = Image.open(os.path.join(script_dir, 'img.jpg'))

# convertiamo immagine da spazio RGB a spazio YCbCr
image_ycbcr = image.convert('YCbCr')

# associamo indice a componenti YCbCr
Y, Cb, Cr = 0, 1, 2
C = [Y, Cb, Cr]

# oggetto PIL.Image diventa array numpy con componenti YCbCr espressi per righe e colonne (range 0-255)
np_ycbcr = list(image_ycbcr.getdata())
np_ycbcr = np.reshape(np_ycbcr, (image.size[1], image.size[0], 3))
np_ycbcr = np.uint8(np_ycbcr)

print("Immagine completa:")
print(np_ycbcr)
print("-------\n", np.shape(np_ycbcr), "\n-------")

# prendo sezione di immagine
c = np.array((300,300))
i = 75
sub = np_ycbcr[c[0]-i:c[0]+i,c[1]-i:c[1]+i]

print("Sezione immagine:")
print(sub)
print("-------\n", np.shape(sub), "\n-------")