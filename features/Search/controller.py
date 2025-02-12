from flask import Blueprint, jsonify, request
import cv2
import torch
import time
import threading
import queue
import os

from flask import Blueprint, jsonify, request

user_bpSearch = Blueprint('user_bpSearch', __name__)




@user_bpSearch.route('/search', methods=['POST'])
def add_user():
    data = request.json
    item_name = data['searchItem']
    RPI_IP=os.getenv("RPI_IP")
    
    stream_url = f"http://{RPI_IP}:5000/video_feed"  

    result_queue = queue.Queue()
    thread = threading.Thread(target=search_frames_thread, args=(item_name, stream_url, result_queue))
    thread.start()
    thread.join()  

    is_found = result_queue.get() 
    return jsonify({'found': is_found}), 201




def search_frames_thread(item_name, stream_url, result_queue):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # Load model only once
    cap = cv2.VideoCapture(stream_url)
    found = False  # Initialize found outside the loop

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break  # Exit loop if no frame

        results = model(frame)
        df = results.pandas().xyxy[0]
        detected_objects = df['name'].unique()
        found = any(item_name.lower() in obj.lower() for obj in detected_objects)
        
        if found:
            print(f"✅ '{item_name}' detected!")
            break  # Exit loop once found

        for _, row in df.iterrows():
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            label = f"{row['name']} {row['confidence']:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    cap.release()
    result_queue.put(found)  # Put the result in the queue






        # (Optional) For debugging, you can still draw bounding boxes here
        # but avoid cv2.imshow in the thread
        # for _, row in df.iterrows():
        #     x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        #     label = f"{row['name']} {row['confidence']:.2f}"
        #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #     cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
