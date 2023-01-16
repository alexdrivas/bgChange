## bgChange Version 0.7: satisfies to all color communication methods, determines most common color to change 
## to run make sure to install packages using, 'pip3 install opencv-python numpy webcolors counter' 
## download 'proc_overlay_img_1_604ae7.png' from google drive and place into same folder as this script.

import cv2
import numpy as np
from webcolors import name_to_rgb, hex_to_rgb
from collections import Counter

def get_color(color_input):
    # Check if input is a common color name
    try:
        return name_to_rgb(color_input)
    except ValueError:
        pass

    # Check if input is a hex code
    if color_input.startswith('#'):
        return hex_to_rgb(color_input)

    # Check if input is an RGB value
    try:
        r, g, b = map(int, color_input.split(','))
        return (r, g, b)
    except ValueError:
        pass

    # If input is none of the above, raise an error
    raise ValueError("Invalid color input")

# Ask user to choose colors
bgcolor = input("Enter background color (e.g. '#0000ff', '255,0,0', 'blue'): ")
#tolerance = int(input("Enter tolerance value (e.g. '10'): "))

# Convert color input to RGB values
bgcolor = get_color(bgcolor)

# Convert RGB values to BGR values
bgcolor = (bgcolor[2], bgcolor[1], bgcolor[0])
print('bgcolor: ', bgcolor)

# Load image
img = cv2.imread('proc_overlay_img_1_604ae7.png')
img_original = img.copy()

# Flatten image to one-dimensional array
img_flat = img.reshape((img.shape[0] * img.shape[1], 3))

# Count the occurrences of each color
color_count = Counter(tuple(color) for color in img_flat)
#print(color_count)

# Get the most common color
changecolor = color_count.most_common(1)[0][0]
print('changecolor_rgb: ', changecolor)

# Create mask
tolerance = 50
lower_color = np.array([changecolor[0] - tolerance, changecolor[1] - tolerance, changecolor[2] - tolerance])
upper_color = np.array([changecolor[0] + tolerance, changecolor[1] + tolerance, changecolor[2] + tolerance])
mask = cv2.inRange(img, lower_color, upper_color)

# Replace the background color with user-specified color
img[np.where(mask != 0)] = bgcolor

# Print statements for debugging 
print('mask sum: ',np.sum(mask))
print('bgcolor: ', bgcolor)
print('changecolor: ', changecolor)


# Display the original and modified images
cv2.imshow('Original Image', img_original)
cv2.imshow('Modified Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Examples used 
# img: proc_overlay_img_1_604ae7.png
# changecolor: 604ae7 rgb (96, 74, 231)

# Future Implementations ##
# Optimize threshold for the photo using k-means/ML methods
# Ask the user to upload a photo, first need to make the background solid