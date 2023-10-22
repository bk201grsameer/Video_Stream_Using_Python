import cv2
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()  # Read a frame from the source
    if not ret:
        break  # Break the loop if there are no more frames
    # Process the frame here
    cv2.imshow('Frame', frame)  # Display the frame
    if cv2.waitKey(1) & 0xFF == 27:  # Exit when the 'Esc' key is pressed
        break

cap.release()  # Release the video capture object
cv2.destroyAllWindows()  # Close any OpenCV windows





