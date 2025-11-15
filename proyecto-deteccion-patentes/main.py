import cv2
import easyocr
from ultralytics import YOLO
import csv


# Load the YOLOv8 model
model = YOLO('models/license_plate_detector.pt')
# to know the frame loop is on
frame_count = 0
# to grab the best read on plate and timestamp
data = []
# variable to store the best plate text
best_plate_text = ""
known_plate_length = 7  # Assuming standard license plates have 7 characters
best_confidence = 0.0

# Open the video file
video_path = "videos/entree.mp4"
cap = cv2.VideoCapture(video_path)
reader = easyocr.Reader(['en'])

with open('output.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(["Recognized Text"])

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        if success:
            frame_count += 1
            print("Processing frame: ", frame_count)

            # Run YOLOv8 inference on the frame
            results = model(frame)

            #choose result with highest confidence
            if len(results[0].boxes) > 0:
                # 1. Get the confidence score of the first box (assuming one license plate)
                current_confidence_tensor = results[0].boxes.conf[0]

                # 2. Convert the tensor containing one value to a standard Python float (.item())
                current_confidence = current_confidence_tensor.item()

                # 3. Perform the comparison using the float value
                if current_confidence > best_confidence:
                    # Update the best confidence with the float value
                    best_confidence = current_confidence
                    # Store the current results object as the best result
                    best_result = results[0]

            # Visualize the results on the frame
            annotated_frame = best_result.plot()

            if best_result.boxes is not None and len(best_result.boxes) > 0:
                # Get the bounding boxes of the detected objects
                # for this example just pick the first one
                box = best_result.boxes.xyxy.cpu()[0]
                # --- NEW CODE: Define padding and limits ---
                # Define a padding because a very tight crop does not allow for good OCR
                padding = 20  # Can be adjusted based on requirements
                h, w, _ = frame.shape # obtain original frame dimensions
                # adjust box coordinates with padding and ensure they are within image bounds
                y1 = max(0, int(box[1]) - padding)
                y2 = min(h, int(box[3]) + padding)
                x1 = max(0, int(box[0]) - padding)
                x2 = min(w, int(box[2]) + padding)
                
                # crop the detected license plate with padding
                crop = frame[y1:y2, x1:x2]
                # --- END OF NEW CODE ---

                #black and white to make text on crop clearer for OCR
                best_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                # Apply Gaussian blur to reduce noise and improve OCR accuracy
                best_crop = cv2.GaussianBlur(best_crop, (5, 5), 0)
                # --- END OF NEW CODE ---
                cv2.imwrite("crop.jpg", best_crop) #Save crop for debugging
                
                
                # OCR the cropped image
                result = reader.readtext(best_crop)
                
                #logic to obtain "text" from ocr results and filter best reading
                for detection in result:
                    text = detection[1]
                    # filter to keep only valid characters (letters and digits)
                    valid_chars = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                    text = ''.join([char for char in text if char in valid_chars])
                    # Update best_plate_text if current text is longer and matches known plate length
                    if len(text) > len(best_plate_text) or len(text) == known_plate_length:
                        best_plate_text = text
            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                # If we have a best plate text, write it to the CSV
                if best_plate_text:
                    writer.writerow([best_plate_text])
                    print(f"Written to CSV: {best_plate_text}")
                break
            cv2.waitKey(10)
        else:
            # If we have a best plate text, write it to the CSV
            if best_plate_text:
                writer.writerow([best_plate_text])
                print(f"Written to CSV: {best_plate_text}")
            # Break the loop if the end of the video is reached
            break
# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()