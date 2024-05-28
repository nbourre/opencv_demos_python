import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import morphology, measure, color
import os

# Load the image
input_dir = "data/"
output_dir = "res/"
# image_filename = "PXL_20240514_213157432.jpg"
image_filename = "justin_01.jpg"
image_path = os.path.join(input_dir, image_filename)
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Resize the image to a width of 1200 pixels while maintaining aspect ratio
scale_percent = 1200 / image.shape[1]
width = int(image.shape[1] * scale_percent)
height = int(image.shape[0] * scale_percent)
dim = (width, height)
image_resized = cv2.resize(image_rgb, dim, interpolation=cv2.INTER_AREA)

# Convert to HSL color space
image_hsl = cv2.cvtColor(image_resized, cv2.COLOR_RGB2HLS)

# Define the green color range in HSL
lower_green = np.array([25, 40, 20])
upper_green = np.array([85, 255, 255])

# Create a mask for green color
mask = cv2.inRange(image_hsl, lower_green, upper_green)

# Apply morphological operations to clean the mask
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_OPEN, kernel)

# Dilate the mask to merge close regions
mask_dilated = cv2.dilate(mask_cleaned, kernel, iterations=2)

# Remove small noise
mask_cleaned = morphology.remove_small_objects(mask_dilated.astype(bool), min_size=600)
mask_cleaned = morphology.remove_small_holes(mask_cleaned, area_threshold=600)
mask_cleaned = mask_cleaned.astype(np.uint8) * 255

# Label the connected components
labels = measure.label(mask_cleaned, connectivity=2)
regions = measure.regionprops(labels)

# Create an empty mask to store the weeds
weed_mask = np.zeros_like(mask_cleaned)

# Iterate over the regions and keep only those that have the expected size and shape of weeds
for region in regions:
    if region.area > 2000:  # Adjusted condition for region area
        for coordinates in region.coords:
            weed_mask[coordinates[0], coordinates[1]] = 255

# Dilate the final weed mask to group nearby weed regions
weed_mask_dilated = cv2.dilate(weed_mask, kernel, iterations=5)

# Label the grouped weed regions
grouped_labels = measure.label(weed_mask_dilated, connectivity=2)
grouped_regions = measure.regionprops(grouped_labels)

# Create an RGB image to visualize the grouped regions
grouped_image = color.label2rgb(grouped_labels, bg_label=0, bg_color=(0, 0, 0), image=image_resized)
grouped_image_uint8 = (grouped_image * 255).astype(np.uint8)  # Convert to uint8

# Display the results
fig, axes = plt.subplots(2, 2, figsize=(8, 8))
ax = axes.ravel()

ax[0].imshow(image_resized)
ax[0].set_title("Original Image")
ax[1].imshow(mask, cmap='gray')
ax[1].set_title("Green Mask")
ax[2].imshow(weed_mask, cmap='gray')
ax[2].set_title("Weed Mask")
ax[3].imshow(grouped_image)
ax[3].set_title("Grouped Weed Regions")

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()

# Save the results with the original filename and appropriate suffixes
base_filename = os.path.splitext(image_filename)[0]
cv2.imwrite(os.path.join(output_dir, f"{base_filename}_resized.jpg"), cv2.cvtColor(image_resized, cv2.COLOR_RGB2BGR))
cv2.imwrite(os.path.join(output_dir, f"{base_filename}_green_mask.jpg"), mask)
cv2.imwrite(os.path.join(output_dir, f"{base_filename}_weed_mask.jpg"), weed_mask)
cv2.imwrite(os.path.join(output_dir, f"{base_filename}_grouped_weed_mask.jpg"), weed_mask_dilated)
cv2.imwrite(os.path.join(output_dir, f"{base_filename}_grouped_image.jpg"), cv2.cvtColor(grouped_image_uint8, cv2.COLOR_RGB2BGR))
