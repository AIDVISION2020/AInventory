import json
import os

def convert_coco_to_yolo(coco_json_path, output_dir, images_dir):
    # Load the COCO JSON file
    with open(coco_json_path) as f:
        coco_data = json.load(f)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Map image IDs to their filenames and sizes
    image_info = {img['id']: (img['file_name'], img['width'], img['height']) for img in coco_data['images']}

    # Process each annotation
    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        category_id = ann['category_id'] - 1  # Adjust to YOLO format by subtracting 1

        if image_id not in image_info:
            print(f"Warning: Image ID {image_id} not found in images!")
            continue

        filename, img_width, img_height = image_info[image_id]

        # Extract the bounding box (COCO: [x_min, y_min, width, height])
        x_min, y_min, box_width, box_height = ann['bbox']

        # Convert to YOLO format (normalize coordinates)
        center_x = (x_min + box_width / 2) / img_width
        center_y = (y_min + box_height / 2) / img_height
        norm_width = box_width / img_width
        norm_height = box_height / img_height

        # Create the corresponding .txt file for the image
        txt_filename = os.path.join(output_dir, filename.replace(".jpg", ".txt"))

        with open(txt_filename, "a") as f:
            f.write(f"{category_id} {center_x:.6f} {center_y:.6f} {norm_width:.6f} {norm_height:.6f}\n")

    print("Conversion completed!")

# Example usage
convert_coco_to_yolo(
    coco_json_path="",
    output_dir="",
    images_dir=""
)
