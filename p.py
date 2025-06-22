import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

keymapper = {
  "0":  "nose",
  "1":  "left_eye_inner",
  "2":  "left_eye",
  "3":  "left_eye_outer",
  "4":  "right_eye_inner",
  "5":  "right_eye",
  "6":  "right_eye_outer",
  "7":  "left_ear",
  "8":  "right_ear",
  "9":  "mouth_left",
  "10": "mouth_right",
  "11": "left_shoulder",
  "12": "right_shoulder",
  "13": "left_elbow",
  "14": "right_elbow",
  "15": "left_wrist",
  "16": "right_wrist",
  "17": "left_pinky",
  "18": "right_pinky",
  "19": "left_index",
  "20": "right_index",
  "21": "left_thumb",
  "22": "right_thumb",
  "23": "left_hip",
  "24": "right_hip",
  "25": "left_knee",
  "26": "right_knee",
  "27": "left_ankle",
  "28": "right_ankle",
  "29": "left_heel",
  "30": "right_heel",
  "31": "left_foot_index",
  "32": "right_foot_index"
}


def draw_landmarks_on_image(rgb_image, detection_result):
    annotated = np.copy(rgb_image)
    h, w, _ = annotated.shape

    # draw bigger circles
    for pose_landmarks in detection_result.pose_landmarks:
        for lm in pose_landmarks:
            x_px = int(lm.x * w)
            y_px = int(lm.y * h)
            cv2.circle(annotated, (x_px, y_px), 4, (0, 255, 0), -1)

    # draw thicker connection lines
    for pose_landmarks in detection_result.pose_landmarks:
        for start_idx, end_idx in mp.solutions.pose.POSE_CONNECTIONS:
            p1 = pose_landmarks[start_idx]
            p2 = pose_landmarks[end_idx]
            x1, y1 = int(p1.x * w), int(p1.y * h)
            x2, y2 = int(p2.x * w), int(p2.y * h)
            cv2.line(annotated, (x1, y1), (x2, y2), (0, 200, 255), 4)
            cv2.putText(annotated, keymapper[str(start_idx)], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    return annotated

# initialize PoseLandmarker
base_options = python.BaseOptions(model_asset_path='pose_landmarker_heavy.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=False
)
detector = vision.PoseLandmarker.create_from_options(options)


######################################################################################
from lateral_neck_tilt import check_left_ear_shoulder_distance
from lateral_neck_tilt import check_initial_position
from lateral_neck_tilt import check_right_ear_shoulder_distance
###############################################################################################
import time


checks_order = [
    check_initial_position,
    check_left_ear_shoulder_distance,
    check_right_ear_shoulder_distance
]
# webcam loop
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame_bgr = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    result = detector.detect(mp_frame)
    annotated = draw_landmarks_on_image(frame_rgb, result)
    # put the score on the image
    # score = checker(result.pose_landmarks[0]) if result.pose_landmarks else 0
    # response = check_left_ear_shoulder_distance(result.pose_landmarks[0], keymapper) if result.pose_landmarks else 0
    response = "ok"
    checker = checks_order[0]
    # cv2.putText(annotated, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(annotated, f"result: {response}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # shoulder angle should be between -10 and 10 degrees
    # if abs(shoulder_angle) < 10 and abs(eye_angle) >
    cv2.imshow('Live PoseLandmarker', cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
    time.sleep(0.2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
