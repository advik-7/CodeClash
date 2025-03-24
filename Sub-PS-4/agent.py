import math

def compute_risk_score(raw_data):
    vehicle = raw_data["sensors"]["vehicle"]
    imu = raw_data["sensors"]["imu"]
    lane_inv = raw_data["sensors"]["lane_invasion"]
    collision = raw_data["sensors"]["collision"]
    env = raw_data.get("environment", {})
    nearby_vehicles = env.get("nearby_vehicles", [])
    host_location = vehicle.get("location", {"x": 0, "y": 0, "z": 0})
    host_x = host_location.get("x", 0)
    host_y = host_location.get("y", 0)
    
    speed = vehicle.get("speed_kmh", 0)
    current_throttle = vehicle.get("control", {}).get("throttle", 0)
    yaw_rate = abs(imu["gyroscope"].get("z", 0))
    collision_history = collision.get("history", [])
    avg_collision = sum(collision_history) / len(collision_history) if collision_history else 0
    lane_invasion_detected = len(lane_inv.get("crossed_lane_markings", [])) > 0
    
    CRITICAL_DISTANCE = 10.0
    ANGLE_THRESHOLD = 30.0
    min_distance = float('inf')
    
    for ext_vehicle in nearby_vehicles:
        ext_distance = ext_vehicle.get("distance", float('inf'))
        ext_location = ext_vehicle.get("location", {"x": 0, "y": 0, "z": 0})
        ext_x = ext_location.get("x", 0)
        ext_y = ext_location.get("y", 0)
        delta_x = ext_x - host_x
        delta_y = ext_y - host_y
        if ext_distance < min_distance:
            min_distance = ext_distance

    risk_external = max(0, (CRITICAL_DISTANCE - min_distance) / CRITICAL_DISTANCE) if min_distance < CRITICAL_DISTANCE else 0
    risk_collision = min(avg_collision / 0.15, 1)
    risk_speed = 0 if speed <= 80.0 else min((speed - 80.0) / 20.0, 1)
    risk_lane = 0.5 if lane_invasion_detected else 0
    risk_yaw = min(yaw_rate / 0.05, 1)
    
    risk_score = (risk_external + risk_collision + risk_speed + risk_lane + risk_yaw) / 5.0
    return risk_score

def collision_prevention_agent_enhanced(raw_data):
    vehicle = raw_data["sensors"]["vehicle"]
    imu = raw_data["sensors"]["imu"]
    lane_inv = raw_data["sensors"]["lane_invasion"]
    collision = raw_data["sensors"]["collision"]
    speed = vehicle.get("speed_kmh", 0)
    control = vehicle.get("control", {})
    current_throttle = control.get("throttle", 0)
    current_steer = control.get("steer", 0)
    yaw_rate = abs(imu["gyroscope"].get("z", 0))
    collision_history = collision.get("history", [])
    avg_collision = sum(collision_history) / len(collision_history) if collision_history else 0
    lane_invasion_detected = len(lane_inv.get("crossed_lane_markings", [])) > 0

    env = raw_data.get("environment", {})
    nearby_vehicles = env.get("nearby_vehicles", [])
    host_location = vehicle.get("location", {"x": 0, "y": 0, "z": 0})
    host_x = host_location.get("x", 0)
    host_y = host_location.get("y", 0)
    
    CRITICAL_DISTANCE = 10.0
    ANGLE_THRESHOLD = 30.0
    external_risk = False
    recommended_steer_change = 0
    min_distance = float('inf')
    
    for ext_vehicle in nearby_vehicles:
        ext_distance = ext_vehicle.get("distance", float('inf'))
        ext_location = ext_vehicle.get("location", {"x": 0, "y": 0, "z": 0})
        ext_x = ext_location.get("x", 0)
        ext_y = ext_location.get("y", 0)
        delta_x = ext_x - host_x
        delta_y = ext_y - host_y
        angle = math.degrees(math.atan2(delta_y, delta_x))
        if angle > 180:
            angle -= 360
        elif angle < -180:
            angle += 360
        if ext_distance < min_distance:
            min_distance = ext_distance
        if ext_distance < CRITICAL_DISTANCE and abs(angle) < ANGLE_THRESHOLD:
            external_risk = True
            recommended_steer_change = -angle

    SPEED_LIMIT_HIGH = 80.0
    SPEED_MIN_FOR_ACCELERATION = 30.0
    YAW_RATE_THRESHOLD = 0.01
    COLLISION_INTENSITY_THRESHOLD = 0.15

    activate_agent = (
        avg_collision > COLLISION_INTENSITY_THRESHOLD or
        lane_invasion_detected or
        yaw_rate > YAW_RATE_THRESHOLD or
        external_risk or
        speed > SPEED_LIMIT_HIGH
    )
    
    if not activate_agent:
        return {
            "action": "Maintain",
            "notes": "No significant risk detected.",
            "throttle": current_throttle,
            "steer": current_steer,
            "brake": 0,
            "risk_score": compute_risk_score(raw_data)
        }
    
    recommendation = {
        "action": None,
        "notes": "",
        "throttle": current_throttle,
        "steer": current_steer,
        "brake": 0
    }
    
    if external_risk:
        if speed > SPEED_MIN_FOR_ACCELERATION:
            recommendation["action"] = "Brake"
            brake_intensity = min(1, (CRITICAL_DISTANCE - min_distance) / CRITICAL_DISTANCE)
            recommendation["brake"] = brake_intensity
            recommendation["notes"] = f"External object detected at {min_distance:.1f}m. Braking with intensity {brake_intensity:.2f}."
        else:
            recommendation["action"] = "Steer"
            steer_adjust = max(-15, min(15, recommended_steer_change))
            recommendation["steer"] += steer_adjust / 100
            recommendation["notes"] = f"Low speed but external risk detected. Changing steering by {steer_adjust:.1f}°."
    elif lane_invasion_detected or yaw_rate > YAW_RATE_THRESHOLD:
        recommendation["action"] = "Steer"
        steer_adjust = recommended_steer_change if recommended_steer_change != 0 else 5.0
        steer_adjust = max(-10, min(10, steer_adjust))
        recommendation["steer"] += steer_adjust / 100
        recommendation["notes"] = f"Internal risk (lane invasion/yaw) detected. Adjust steering by {steer_adjust:.1f}°."
        if speed > SPEED_LIMIT_HIGH:
            recommendation["action"] = "Brake & Steer"
            brake_intensity = 0.3
            recommendation["brake"] = brake_intensity
            recommendation["notes"] += f" Also braking with intensity {brake_intensity:.2f}."
    elif speed < SPEED_MIN_FOR_ACCELERATION and not external_risk:
        recommendation["action"] = "Accelerate"
        throttle_increase = 0.1
        recommendation["throttle"] = min(1.0, current_throttle + throttle_increase)
        recommendation["notes"] = "Speed below minimum threshold, accelerating."
    
    if recommendation["action"] is None:
        recommendation["action"] = "Maintain"
        recommendation["notes"] = "Maintaining current state as conditions are borderline."
    
    recommendation["risk_score"] = compute_risk_score(raw_data)
    return recommendation

raw_input = {
  "frame": 1205,
  "timestamp": "2025-03-23T14:25:36",
  "sensors": {
    "imu": {
      "compass": 178.5,
      "accelerometer": {"x": 0.01, "y": -0.02, "z": 9.81},
      "gyroscope": {"x": 0.0005, "y": -0.0002, "z": 0.02}
    },
    "gnss": {"latitude": 37.7749, "longitude": -122.4194, "altitude": 12.5},
    "collision": {"history": [0.0, 0.1, 0.0, 0.3, 0.2, 0.0, 0.0, 0.1, 0.0, 0.2]},
    "lane_invasion": {"crossed_lane_markings": ["Solid Yellow", "Dashed White"]},
    "vehicle": {
      "speed_kmh": 75.0,
      "location": {"x": 235.7, "y": 123.4, "z": 0.5},
      "control": {"throttle": 0.5, "steer": -0.1, "brake": 0.0, "reverse": False, "hand_brake": False, "manual_gear_shift": False, "gear": 3}
    },
    "camera": {
      "type": "sensor.camera.rgb",
      "transform": {"location": {"x": 1.5, "y": 0.0, "z": 1.7}, "rotation": {"pitch": 0.0, "yaw": 90.0, "roll": 0.0}}
    },
    "lidar": {
      "frame": 1205,
      "point_count": 1024,
      "channels": 32,
      "points_sample": [
        {"x": 5.1, "y": -1.2, "z": 0.3, "intensity": 0.8},
        {"x": 4.3, "y": -0.5, "z": 0.2, "intensity": 0.7},
        {"x": 6.2, "y": -1.0, "z": 0.5, "intensity": 0.9}
      ]
    },
    "radar": {
      "frame": 1205,
      "detection_count": 5,
      "detections_sample": [
        {"depth": 10.2, "azimuth": 0.3, "altitude": -0.1, "velocity": 5.0},
        {"depth": 12.5, "azimuth": -0.2, "altitude": 0.2, "velocity": 4.5}
      ]
    }
  },
  "environment": {
    "nearby_vehicles": [
      {"distance": 8.0, "type": "Tesla Model 3", "id": 305, "location": {"x": 240.0, "y": 124.0, "z": 0.5}},
      {"distance": 28.7, "type": "Ford Mustang", "id": 412, "location": {"x": 260.3, "y": 118.2, "z": 0.5}}
    ],
    "total_vehicles": 10,
    "map_name": "Town05"
  }
}

action_recommendation = collision_prevention_agent_enhanced(raw_input)
print("Detailed Recommendation:")
for key, value in action_recommendation.items():
    print(f"{key}: {value}")
