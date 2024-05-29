import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import morphology, measure, color
import os

# Define input and output directories
input_dir = "data/"
output_dir = "res/"
video_filename = "20231202_135817.mp4"  # Replace with your video filename
video_path = os.path.join(input_dir, video_filename)

# Open the video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Define output video writer
#output_video_path = os.path.join(output_dir, "output_video.mp4")
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

scale_percent = 320 / width

new_width = int(width * scale_percent)
new_height = int(height * scale_percent)

print (width, height)
print (scale_percent, new_width, new_height)

# Loop through each frame of the video
frame_num = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize the frame to a width of 1200 pixels while maintaining aspect ratio
    #scale_percent = 640 / frame.shape[1]
    # scale_percent = 640 / frame.shape[1]
    # new_width = int(frame.shape[1] * scale_percent)
    # new_height = int(frame.shape[0] * scale_percent)
    
    dim = ( new_width, new_height)    
    frame_resized = cv2.resize(frame_rgb, dim, interpolation=cv2.INTER_AREA)

    # Convert to HSL color space
    frame_hsl = cv2.cvtColor(frame_resized, cv2.COLOR_RGB2HLS)

    # Define the green color range in HSL
    lower_green = np.array([25, 40, 20])
    upper_green = np.array([85, 255, 255])

    # Create a mask for green color
    mask = cv2.inRange(frame_hsl, lower_green, upper_green)

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

    # # Label the grouped weed regions
    # grouped_labels = measure.label(weed_mask_dilated, connectivity=2)
    # grouped_regions = measure.regionprops(grouped_labels)

    # # Create an RGB image to visualize the grouped regions
    # grouped_image = color.label2rgb(grouped_labels, bg_label=0, bg_color=(0, 0, 0), image=frame_resized)
    # grouped_image_uint8 = (grouped_image * 255).astype(np.uint8)  # Convert to uint8

    # # Convert back to BGR for writing to video file
    # frame_output = cv2.cvtColor(grouped_image_uint8, cv2.COLOR_RGB2BGR)
    
    # cv2.imshow("Frame", frame_output)
    
    #out.write(frame_output)
    
    cv2.imshow("Original", frame_resized)
    cv2.imshow("Mask", mask)
    cv2.imshow("Mask cleaned", mask_cleaned)
    cv2.imshow("Weed Mask", weed_mask)
    cv2.imshow("Weed Mask Dilated", weed_mask_dilated)
    
    
    frame_num += 1
    print(f"Processed frame {frame_num}/{frame_count}")
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == ord('p'):
        # Pause the video
        cv2.waitKey(-1)


# Release video objects
cap.release()
#out.release()

#print(f"Output video saved to {output_video_path}")
