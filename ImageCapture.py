import cv2
import time

# Format current time to use in the image filename
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
savetime = f"{formatted_time}.png"

# Initialize the camera
cam_port = 0
cam = cv2.VideoCapture(cam_port)

# Check if the camera opened successfully
if not cam.isOpened():
    print("Error: Camera could not be opened.")
else:
    # Read input from the camera
    result, image = cam.read()

    # If an image is detected without any error, show the result
    if result:
        # Show the captured image
        cv2.imshow("Captured Image", image)

        # Save the image in local storage
        cv2.imwrite(savetime, image)
        print("Image captured and saved as " + savetime)

        # Wait for a key press to close the window
        cv2.waitKey(0)
        cv2.destroyAllWindows()  # Destroys all windows created by OpenCV

    else:
        print("No image detected. Please try again.")

    # Release the camera to free up resources
    cam.release()
