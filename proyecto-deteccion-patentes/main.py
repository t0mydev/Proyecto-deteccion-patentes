import cv2
import easyocr
from ultralytics import YOLO
from time_helpers import draw_timestamp
import re
from datetime import datetime
import csv


# Load the YOLOv8 model
model = YOLO('models/best.pt')
# to know the frame loop is on
frame_count = 0
# to grab the best read on plate and timestamp
data = []


# This is one of the default models which will detect the car, not the plate
#model = YOLO('models/yolov8n.pt')

# Open the video file
video_path = "videos/entree_4s.mp4"
cap = cv2.VideoCapture(video_path)
reader = easyocr.Reader(['en'])

with open('output.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(["Recognized Text", "Timestamp"])

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            frame_count += 1
            # Run YOLOv8 inference on the frame
            results = model(frame)
            

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Define the coordinates and dimensions for the timestamp area
            x, y, width, height = 0, 101, 712, 100

            # Draw the rectangle around the timestamp area
            color = (255, 0, 0)  # Red color in BGR
            thickness = 2
            cv2.rectangle(annotated_frame, (x, y), (x + width, y + height), color, thickness)

            # Use the same coordinates to OCR the timestamp
            #TODO: Clean OCR to do date operations
            timestamp_text = draw_timestamp(frame, x, y, width, height, reader)
            
            # timestamp without the seconds for consistency, seconds weren't being read correctly
            new_timestamp_text = timestamp_text[0:14]+timestamp_text[-3:]
            
            # define pattern for the timestamp
            date_pattern = r'(\d{1,2})/(\d{1,2})/(\d{4}) (\d{1,2})\.(\d{1,2})'

            
            # match the timestamp to the pattern
            match = re.search(date_pattern, new_timestamp_text)
            
            if match:
                # parse the timestamp into datetime object
                month, day, year, hour, minute = match.groups()
                timestamp_str = f"{month}/{day}/{year} {hour}:{minute}"
                timestamp_dt = datetime.strptime(timestamp_str, "%m/%d/%Y %I:%M")
                print("Timestamp (datetime object):", timestamp_dt)
                
                # now it's ready to do date operations
                # example: take date and time separately
                date = timestamp_dt.date()
                time = timestamp_dt.time()
                print("Date:", date)
                print("Time:", time)
                
            else:
                print("No valid timestamp found.")
                
            
            

            if results[0].boxes is not None and len(results[0].boxes) > 0:
                # Get the bounding boxes of the detected objects
                # for this example just picked the first one
                box = results[0].boxes.xyxy.cpu()[0]

                # Crop the frame to only select the detected object
                crop = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                # Preprocess the cropped image, commenting because results were not good.
                #crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                #crop = cv2.equalizeHist(crop)
                #crop = cv2.GaussianBlur(crop, (5, 5), 0)
                
                #crop = cv2.adaptiveThreshold(crop, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
                
                

                #Optionally save the image for debugging
                cv2.imwrite("crop.jpg", crop)

                


                # OCR the cropped image
                result = reader.readtext(crop)
                

                # Print the OCR result
                for detection in result:
                    text = detection[1]
                    # take the frame with correct reading for the plate
                    if frame_count == 6:
                        data.append(text)
                    print("Detected plate: ",text)
                
                  
                # Create a datetime object with the specified date and time
                datetime_obj = datetime(2024, 2, 15, 9, 6, 0)
                # take the frame with correct reading for the timestamp
                if frame_count == 7:
                    data.append(timestamp_dt)
                    writer.writerow([data[0], data[1]])
                

                #TODO Register plate and entree/exit timestamp

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()