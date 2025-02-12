import cv2
import torch
import time

# Load YOLO model globally (to avoid reloading on every request)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
stream_url="http://10.42.0.188:5000/video_feed"


def SearchFrames(item_name, timeOut=10):
    
    cap = cv2.VideoCapture(stream_url)

    start_time = time.time()

    if not cap.isOpened():
        print("❌ Failed to open video stream.")
        return False  # Return False if the camera stream is not accessible

    while (cap.isOpened() and (time-time()-start_time<=5) ):
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame.")
            break

        # Run YOLO object detection
        results = model(frame)

        # Convert results to Pandas DataFrame
        df = results.pandas().xyxy[0]  
        detected_objects = df['name'].unique()
        print("Detected objects:", detected_objects)

        # Check if the desired item is found
        found = any(item_name.lower() in obj.lower() for obj in detected_objects)
        if found:
            print(f"✅ '{item_name}' detected!")
            cap.release()
            cv2.destroyAllWindows()
            return True
        
        # Timeout condition
        if time.time() - start_time > timeOut:
            print("⏳ Timeout reached.")
            break

        # Show the processed frame (optional)
        for _, row in df.iterrows():
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            label = f"{row['name']} {row['confidence']:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow("YOLO Stream", frame)
        cv2.waitKey(1)  # Allow OpenCV to process UI events

    # Ensure resources are released properly
    cap.release()
    cv2.destroyAllWindows()
    return False
