import math

def angle_between_points(p1: tuple[float, float], p2: tuple[float, float], *, degrees: bool = True) -> float:
    """
    Returns the angle between the vector p1→p2 and the positive x-axis.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    θ = math.atan2(dy, dx)  # radians in range (−π, π]
    return math.degrees(θ) if degrees else θ

def check_initial_position(landmarks, keymapper,
                           shoulder_tol=7, head_tol=7):
    # helper to fetch (x,y) by landmark name
    def xy(name):
        idx = int(next(k for k,v in keymapper.items() if v==name))
        lm = landmarks[idx]
        return lm.x, lm.y

    # trunk angles
    ls, rs = xy("left_shoulder"), xy("right_shoulder")
    # find the angle between the line connecting the shoulders and the x-axis
    shoulder_angle = angle_between_points(rs, ls, degrees=True)
    print(f"Shoulder angle: {shoulder_angle:.2f} degrees")

    # trunk angles
    ls, rs = xy("left_eye"), xy("right_eye")
    # find the angle between the line connecting the shoulders and the x-axis
    eye_angle = angle_between_points(rs, ls, degrees=True)
    print(f"Eye angle: {eye_angle:.2f} degrees")
    
    
    # rule-checking --------------------------------------------------------
    issues = []
    if abs(shoulder_angle) > shoulder_tol:
        issues.append("shoulders_not_level")
    if abs(eye_angle) > head_tol:
        issues.append("head_not_level")

    # *** STANDARD RETURN ***
    return {
        "ok": not issues,
        "issues": issues,                     # [] if all good
        "metrics": {
            "shoulder_angle": {
                "value": shoulder_angle,     # what we measured
                "rule": f"abs <= {shoulder_tol}" # the pass/fail threshold
            },
            "eye_angle": {
                "value": eye_angle,           # what we measured
                "rule": f"abs <= {head_tol}"      # the pass/fail threshold
            }
        }
    }

def check_left_ear_shoulder_distance(landmarks, keymapper,
                                  min_distance=0.6, shoulder_tol=7):
    """
    Check if the distance between the left ear and left shoulder is within the specified range.
    """
    # need the distance between the left ear and left shoulder be at least min_distance that of the right ear and right shoulder
    def xy(name):
        idx = int(next(k for k,v in keymapper.items() if v==name))
        lm = landmarks[idx]
        return lm.x, lm.y
    left_ear = xy("left_ear")
    left_shoulder = xy("left_shoulder")
    right_ear = xy("right_ear")
    right_shoulder = xy("right_shoulder")

    left_distance = math.sqrt((left_ear[0] - left_shoulder[0]) ** 2 + (left_ear[1] - left_shoulder[1]) ** 2)
    right_distance = math.sqrt((right_ear[0] - right_shoulder[0]) ** 2 + (right_ear[1] - right_shoulder[1]) ** 2)
    issues = []
    if left_distance > min_distance * right_distance:
        print(f"Left ear-shoulder distance {left_distance:.2f} is too large compared to right ear-shoulder distance {right_distance:.2f}")
        issues.append("left_ear_shoulder_distance_too_large")
        print(f"Ratio is {left_distance / right_distance:.2f}, which is > {min_distance}")
    else:
        print(f"Left ear-shoulder distance {left_distance:.2f} is within the acceptable range of right ear-shoulder distance {right_distance:.2f}")
        print(f"Ratio is {left_distance / right_distance:.2f}, which is <= {min_distance}")

    # now get the shoulders horizontal distance
    # trunk angles
    ls, rs = xy("left_shoulder"), xy("right_shoulder")
    # find the angle between the line connecting the shoulders and the x-axis
    shoulder_angle = angle_between_points(rs, ls, degrees=True)
    print(f"Shoulder angle: {shoulder_angle:.2f} degrees")
    if abs(shoulder_angle) > 10:
        issues.append("shoulders_not_level")

    return {
        "ok": not issues,
        "issues": issues,                     # [] if all good
        "metrics": {
            "left_ear_shoulder_distance": {
                "value": left_distance,     # what we measured
                "rule": f"<= {min_distance} * right_ear_shoulder_distance" # the pass/fail threshold
            },
            "shoulder_angle": {
                "value": shoulder_angle,     # what we measured
                "rule": f"abs <= {shoulder_tol}" # the pass/fail threshold
            }
        }
    }

def check_right_ear_shoulder_distance(landmarks, keymapper,
                                   min_distance=0.6, shoulder_tol=7):
    """
    Check if the distance between the right ear and right shoulder is within the specified range.
    """
    # need the distance between the right ear and right shoulder be at least min_distance that of the left ear and left shoulder
    def xy(name):
        idx = int(next(k for k,v in keymapper.items() if v==name))
        lm = landmarks[idx]
        return lm.x, lm.y
    right_ear = xy("right_ear")
    right_shoulder = xy("right_shoulder")
    left_ear = xy("left_ear")
    left_shoulder = xy("left_shoulder")

    right_distance = math.sqrt((right_ear[0] - right_shoulder[0]) ** 2 + (right_ear[1] - right_shoulder[1]) ** 2)
    left_distance = math.sqrt((left_ear[0] - left_shoulder[0]) ** 2 + (left_ear[1] - left_shoulder[1]) ** 2)
    issues = []
    if right_distance > min_distance * left_distance:
        print(f"Right ear-shoulder distance {right_distance:.2f} is too large compared to left ear-shoulder distance {left_distance:.2f}")
        issues.append("right_ear_shoulder_distance_too_large")
        print(f"Ratio is {right_distance / left_distance:.2f}, which is > {min_distance}")
    else:
        print(f"Right ear-shoulder distance {right_distance:.2f} is within the acceptable range of left ear-shoulder distance {left_distance:.2f}")
        print(f"Ratio is {right_distance / left_distance:.2f}, which is <= {min_distance}")

    # now get the shoulders horizontal distance
    # trunk angles
    ls, rs = xy("left_shoulder"), xy("right_shoulder")
    # find the angle between the line connecting the shoulders and the x-axis
    shoulder_angle = angle_between_points(rs, ls, degrees=True)
    print(f"Shoulder angle: {shoulder_angle:.2f} degrees")
    if abs(shoulder_angle) > 10:
        issues.append("shoulders_not_level")

    return {
        "ok": not issues,
        "issues": issues,                     # [] if all good
        "metrics": {
            "right_ear_shoulder_distance": {
                "value": right_distance,     # what we measured
                "rule": f"<= {min_distance} * left_ear_shoulder_distance" # the pass/fail threshold
            },
            "shoulder_angle": {
                "value": shoulder_angle,     # what we measured
                "rule": f"abs <= {shoulder_tol}" # the pass/fail threshold
            }
        }
    }