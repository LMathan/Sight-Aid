import cv2
import torch

# Load YOLOv5 model (downloads model if not available)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def detect_objects(item_name, stream_url="http://10.42.0.188:5000/video_feed"):
    """
    Detects objects in a video stream and checks if the specified item is present.

    Parameters:
    item_name (str): The name of the item to check for in the detected objects.
    stream_url (str): The URL of the video stream (default: Raspberry Pi stream).
    """
    
    # Open video stream
    cap = cv2.VideoCapture(stream_url)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Run YOLOv5 object detection
        results = model(frame)

        # Convert results to OpenCV format
        df = results.pandas().xyxy[0]  # Get bounding box data as Pandas DataFrame

        # Get unique detected objects
        detected_objects = df['name'].unique()
        print("Detected objects:", detected_objects)

        # Check if the input item is detected
        found = any(item_name.lower() in obj.lower() for obj in detected_objects)
        if found:
            print(f"✅ '{item_name}' detected!")
            break
        else:
            print(f"❌ '{item_name}' not found.")

        for _, row in df.iterrows():
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            label = f"{row['name']} {row['confidence']:.2f}"

            # Draw bounding boxes and labels
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Show the processed frame
        cv2.imshow("YOLO Stream", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage
detect_objects("cell phone")  # Call the function with the item you want to detect
