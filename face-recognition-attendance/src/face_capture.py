import cv2
import os


def capture_faces(student_id, student_name, number_of_images=20):

    student_folder = os.path.join(
        "dataset",
        f"{student_id}_{student_name}"
    )

    os.makedirs(student_folder, exist_ok=True)

    # Load face detection model
    model_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

    face_detector = cv2.CascadeClassifier(model_path)

    if face_detector.empty():
        print("Error: Could not load face detection model.")
        return False

    # Open webcam
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not access the webcam.")
        return False

    count = 0

    print("Starting camera...")
    print("Look directly at the camera.")
    print("Press Q to stop.")

    while True:

        ret, frame = camera.read()

        if not ret:
            print("Error: Could not read camera frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(100, 100)
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            if count < number_of_images:

                face_image = frame[y:y + h, x:x + w]

                filename = os.path.join(
                    student_folder,
                    f"{student_id}_{count + 1}.jpg"
                )

                cv2.imwrite(filename, face_image)

                count += 1

                print(
                    f"Captured image {count}/{number_of_images}"
                )

        cv2.putText(
            frame,
            f"Images: {count}/{number_of_images}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Face Capture - Press Q to Exit",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if count >= number_of_images:
            break

    camera.release()
    cv2.destroyAllWindows()

    if count >= number_of_images:
        print("Face capture completed successfully.")
        return True

    print("Face capture stopped before completion.")
    return False