import cv2
import numpy as np


def analyze_video(video_path: str):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {"error": "Could not open video file"}

    frame_count = 0
    face_detected_frames = 0
    total_movement = 0

    prev_center = None

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_eye.xml"
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_detected_frames += 1

            # Compute face center
            center_x = x + w // 2
            center_y = y + h // 2
            current_center = np.array([center_x, center_y])

            if prev_center is not None:
                movement = np.linalg.norm(current_center - prev_center)
                total_movement += movement

            prev_center = current_center

            # Detect eyes inside face
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            break  # Only analyze first detected face

    cap.release()

    if frame_count == 0:
        return {"error": "No frames processed"}

    face_presence_ratio = face_detected_frames / frame_count

    avg_movement = total_movement / frame_count if frame_count > 0 else 0

    # Normalize movement score (simple scaling)
    movement_score = min(avg_movement / 50, 1.0)

    return {
        "total_frames": frame_count,
        "face_presence_ratio": round(face_presence_ratio, 2),
        "head_movement_score": round(movement_score, 2)
    }
