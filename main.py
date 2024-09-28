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
            data="datasets/rico_small/rico_small.yaml", 
            epochs=200, 
            imgsz=640, 
            #cache='disk',
            batch=8
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






