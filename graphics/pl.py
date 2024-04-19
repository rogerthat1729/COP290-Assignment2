from PIL import Image
import os

def crop_to_bottom_left(image_path, target_width=1920, target_height=1080):
    # Open the image
    img = Image.open(image_path)
    print(f"Opened {image_path} with size {img.size}")
    # Get image dimensions
    width, height = img.size
    
    # Calculate crop box
    left = 0
    upper = height - target_height
    right = target_width
    lower = height
    
    # Crop image
    cropped_img = img.crop((left, upper, right, lower))
    
    # Resize image if necessary
    if cropped_img.size != (target_width, target_height):
        print(f"Resizing {image_path} from {cropped_img.size} to ({target_width}, {target_height})")
        cropped_img = cropped_img.resize((target_width, target_height), Image.ANTIALIAS)
    
    return cropped_img

def crop_images_in_folder(folder_path):
    # Get list of files in the folder
    files = os.listdir(folder_path)
    
    # Create a new folder for the cropped images
    output_folder = os.path.join(folder_path, 'cropped_images')
    os.makedirs(output_folder, exist_ok=True)
    
    # Crop and save each image
    for file in files:
        if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.gif'):
            image_path = os.path.join(folder_path, file)
            cropped_img = crop_to_bottom_left(image_path)
            output_path = os.path.join(output_folder, file)
            cropped_img.save(output_path)
            print(f"{file} cropped and saved as {output_path}")

# Replace 'folder_path' with the path to your folder containing the images
folder_path = 'girlrain'
crop_images_in_folder(folder_path)
