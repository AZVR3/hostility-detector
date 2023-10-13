import cv2
import mediapipe as mp

# Create an object detector object
mp_object_detector = mp.solutions.objectron
object_detector = mp_object_detector.Objectron(static_image_mode=False,
                                               max_num_objects=5,
                                               min_detection_confidence=0.5,
                                               model_name='Shoe')

# Open the laptop camera
cap = cv2.VideoCapture(0)

# Loop until the user presses 'q' key
while cap.isOpened():
  # Read a frame from the camera
  success, image = cap.read()
  if not success:
    break

  # Convert the image to RGB format
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  # Run inference on the image
  results = object_detector.process(image)

  # Draw the detected objects on the image
  if results.detected_objects:
    for detected_object in results.detected_objects:
      mp_object_detector.draw_landmarks(
          image, detected_object.landmarks_2d, mp_object_detector.BOX_CONNECTIONS)
      mp_object_detector.draw_axis(image, detected_object.rotation,
                                   detected_object.translation)

  # Convert the image back to BGR format
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

  # Display the image
  cv2.imshow('Object Detection', image)
  
  # Check if the user pressed 'q' key
  if cv2.waitKey(5) & 0xFF == ord('q'):
    break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
