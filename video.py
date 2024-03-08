import cv2
import pytesseract

# Path to the video file
video_path = 'video.mp4'

# Initialize the video capture object
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error opening video file")

# Set frame rate for capturing
frame_rate = 60  # Change this number based on your needs
count = 0

try:
    while cap.isOpened():
        ret, frame = cap.read()  # Read the frame

        if not ret:
            break  # Break the loop if there are no frames to read

        # Process frames at the specified frame rate
        if count % frame_rate == 0:
            # Convert the frame to grayscale for better OCR accuracy
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Use Pytesseract to extract text
            text = pytesseract.image_to_string(gray, lang='eng')
            print(f"Text on frame {count}: {text}")

        count += 1

finally:
    # When everything is done, release the video capture object
    cap.release()

# Closes all the frames
cv2.destroyAllWindows()
