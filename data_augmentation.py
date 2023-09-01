import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to scale an image
def img_scaling(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

# Function to rotate an image
def img_rotation(image, angle):
    (height, width) = image.shape[:2]
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (width, height))

# Function to crop an image
def img_cropping(image, start_y, start_x, height, width):
    return image[start_y:start_y+height, start_x:start_x+width]

# Function to flip an image
def img_flipping(image, flip_code):
    return cv2.flip(image, flip_code)

# Function to adjust the contrast of an image
def adjust_contrast(image, contrast_scale):
    return cv2.convertScaleAbs(image, alpha=contrast_scale)

# Function to distort an image
def img_distortion(image):
    rows,cols = image.shape[:2]
    src_points = np.float32([[0,0], [cols-1,0], [0,rows-1], [cols-1,rows-1]])
    dst_points = np.float32([[0,0], [cols-1,0], [int(0.33*cols),rows-1], [int(0.66*cols),rows-1]]) 
    projective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    return cv2.warpPerspective(image, projective_matrix, (cols,rows))

# Function to add noise to an image
def img_noise(image):
    row, col = image.shape[:2]
    # Check if image is grayscale or color
    ch = image.shape[2] if len(image.shape) > 2 else 1
    mean = 0
    var = 0.1
    sigma = var**0.5
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch) if ch > 1 else gauss.reshape(row, col)
    gauss = gauss.astype(image.dtype)  # Ensure the same data type as the image
    noisy = cv2.add(image, gauss)
    return noisy

# Function to shift the color of an image
def color_shift(image, shift_value):
    # Only apply color shift if the image is not grayscale
    if len(image.shape) > 2:
        hsvImg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsvImg[...,1] = hsvImg[...,1]*shift_value
        hsvImg[...,2] = hsvImg[...,2]*shift_value
        image = cv2.cvtColor(hsvImg, cv2.COLOR_HSV2BGR)
    return image

# Read in the image
image = cv2.imread('example.png')

# Apply each augmentation
scaled_image = img_scaling(image, 150)
rotated_image = img_rotation(image, 45)
cropped_image = img_cropping(image, 10, 10, 200, 200)
flipped_image = img_flipping(image, 1)
adjusted_contrast_image = adjust_contrast(image, 2)
distorted_image = img_distortion(image)
noisy_image = img_noise(image)
shifted_color_image = color_shift(image, 0.8)

# Plot Original Image and Augmented Images
plt.figure(figsize=(20,20))
functions = ['Original Image', 'Scaling', 'Rotation', 'Cropping', 'Flipping', 'Contrast Adjustment', 'Distortion', 'Noise Addition', 'Color Change']
images = [image, scaled_image, rotated_image, cropped_image, flipped_image, adjusted_contrast_image, distorted_image, noisy_image, shifted_color_image]

for i in range(9):
    plt.subplot(3, 3, i+1)
    plt.imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)) if len(images[i].shape) > 2 else plt.imshow(images[i], cmap='gray')
    plt.title(functions[i])
    plt.xticks([]), plt.yticks([])
plt.show()
