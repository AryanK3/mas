import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('capture.jpg', frame)
        print("Image captured and saved")
    else:
        print("Error: Could not capture image.")

cap.release()
cv2.destroyAllWindows()
