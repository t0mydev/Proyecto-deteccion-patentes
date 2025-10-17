import cv2

# Initialize global variables
points = []  # List to store points

# Mouse callback function
def select_points(event, x, y, flags, param):
    global img_temp, points
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        cv2.circle(img_temp, (x, y), 5, (0, 255, 0), -1)  # Mark the point
        points.append((x, y))

        if len(points) > 1:
            # Draw line to the next point
            cv2.line(img_temp, points[-2], points[-1], (0, 255, 0), 2)

        if len(points) == 4:
            # Draw line to close the polygon
            cv2.line(img_temp, points[3], points[0], (0, 255, 0), 2)
            print("Coordinates of selected points:")  # Print when polygon completes
            for point in points:
                print(point)
            points = []  # Reset points after printing

        cv2.imshow('frame', img_temp)

# Read a frame from a video
video_path = 'videos/entree_4s.mp4'
cap = cv2.VideoCapture(video_path)

ret, img = cap.read()  # Read the first frame
if not ret:
    print("Failed to grab a frame from the video")
    exit()

# Store the original frame to reset later
img_original = img.copy()
img_temp = img.copy()

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', select_points)

while True:
    cv2.imshow('frame', img_temp)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):  # Quit program
        break
    elif k == ord('r'):  # Reset drawing
        if points:  # Check if there are points selected before resetting
            print("Resetting, last points selected were:")
            for point in points:
                print(point)
        img_temp = img_original.copy()  # Reset to the original image
        points = []  # Clear the points
        cv2.imshow('frame', img_temp)

cap.release()
cv2.destroyAllWindows()
