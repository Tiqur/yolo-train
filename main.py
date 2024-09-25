import argparse
from ultralytics import YOLO
import os


def main(mode):
    if mode == 'train':
        print("Training the model...")

        # Load a model
        model = YOLO("yolov10n.yaml")  # build a new model from YAML
        model = YOLO("yolov10n.pt")  # load a pretrained model (recommended for training)
        model = YOLO("yolov10n.yaml").load("yolov10n.pt")  # build from YAML and transfer weights

        results = model.train(
            data="datasets/custom/custom.yaml", 
            epochs=1000, 
            imgsz=640, 
            cache=True,
            hsv_h=0.015,        # Introduces hue variability for different lighting conditions
            hsv_s=0.7,          # Adjusts saturation to handle different color intensities
            hsv_v=0.4,          # Modifies brightness for varying lighting conditions
            degrees=5.0,        # Small rotation to recognize objects at slightly different angles
            translate=0.1,      # Translate images slightly to simulate partial views
            scale=0.5,          # Scales objects to simulate different distances
            shear=2.0,          # Small shearing to simulate slight perspective distortions
            perspective=0.0005, # Minor perspective change for 3D understanding
            flipud=0.0,         # No vertical flip, as it’s not typically useful for UI elements
            fliplr=0.5,         # Horizontal flip to learn from symmetrical layouts
            bgr=0.0,            # No BGR flip since RGB is standard for UI screenshots
            mosaic=1.0,         # Combines four images into one, very effective for complex scenes
            mixup=0.1,          # Small mixup to introduce variability without overwhelming the model
            copy_paste=0.0,     # No copy-paste, as it’s less applicable to UI screenshots
            auto_augment='randaugment', # Automatically applies diverse augmentations
            erasing=0.4,        # Erases portions to make the model focus on critical features
            crop_fraction=1.0   # Full image cropping for standard object detection
        )

    elif mode == 'test':
        print("Testing the model...")

        model = YOLO("runs/detect/train73/weights/best.pt")  # load a pretrained model (recommended for training)
        directory_path = 'evaluation_images'

        images = [f"{directory_path}/{filename}" for filename in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, filename))]
        results = model.predict(images)

        for i, result in enumerate(results):
            print(result.path)
            print(result.boxes)

            im = result.plot()
            filename = f"result{i+1}.jpg"
            result.save(filename=filename, conf=False)
    else:
        print("Invalid mode. Please choose 'train' or 'test'.")

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Train or test the model.")
    
    # Add the mode argument
    parser.add_argument('mode', choices=['train', 'test'], 
                        help="Choose 'train' to train the model or 'test' to test the model.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the main function with the specified mode
    main(args.mode)






