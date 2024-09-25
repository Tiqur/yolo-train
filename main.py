from ultralytics import YOLO

# Load a model
model = YOLO("yolov10n.yaml")  # build a new model from YAML
model = YOLO("yolov10n.pt")  # load a pretrained model (recommended for training)
model = YOLO("yolov10n.yaml").load("yolov10n.pt")  # build from YAML and transfer weights

# Train the model
results = model.train(data="datasets/custom/custom.yaml", epochs=256, imgsz=640)

#model = YOLO("runs/detect/train66/weights/best.pt")  # load a pretrained model (recommended for training)
#results = model.predict(['image1.jpg', 'image2.jpg', 'image3.png', 'image4.jpg', 'image5.jpg'])
#for i, result in enumerate(results):
#    print(result.boxes)
#
#    # Annotate
#    im = result.plot()
#
#    # Generate unique filenames like result1.jpg, result2.jpg, etc.
#    filename = f"result{i+1}.jpg"
#    
#    # Save each result to a different file
#    result.save(filename=filename, conf=False)
