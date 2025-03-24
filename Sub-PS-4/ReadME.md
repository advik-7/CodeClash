# 🚗 Custom Decision-Making Agent for Autonomous Vehicle Control in CARLA Simulator

## 📄 Project Overview
This project implements an enhanced collision prevention agent for autonomous vehicle control in the **CARLA Simulator**. The system leverages **sensor fusion**, **real-time risk assessment**, and **adaptive decision-making** to enable safe navigation in both normal and adverse weather conditions.

---

## 🌐 Features
✅ **Sensor Fusion** (IMU, GNSS, LiDAR, Radar, Cameras, Collision & Lane Sensors)  
✅ **Dynamic Risk Assessment Engine**  
✅ **Hierarchical Decision-Making Agent**  
✅ **Weather Adaptation Module**  
✅ **Real-time Action Execution**  
✅ **Weather-Aware Performance Tuning**  
✅ **Modular Architecture for Future Expansion**

---

## 📊 System Components

### 1️⃣ Sensor Data Collection
- Integrated CARLA sensors: IMU, GNSS, Cameras, LiDAR, Radar, Lane, and Collision detection.

### 2️⃣ Risk Assessment Engine
Calculates a **composite risk score** based on:
- **Proximity Risk**
- **Collision History**
- **Speed**
- **Lane Deviation**
- **Vehicle Stability (Yaw Rate)**
- **Weather-specific risks** (Visibility, Traction, Sensor Reliability)

#### Risk Formula:
```python
weather_adjusted_risk_score = 
(risk_external + risk_collision + risk_speed + risk_lane + risk_yaw + 
visibility_risk + traction_risk + sensor_reliability_risk) / 8.0
```

### 3️⃣ Decision-Making Agent
- Intervenes under risk triggers:
  - Collision intensity
  - Lane invasion
  - High yaw rate
  - Speed threshold breach
- **Possible Actions:** Brake, Steer, Brake & Steer, Accelerate, Maintain

### 4️⃣ Weather Adaptation Module
- Dynamically adjusts:
  - Critical distance
  - Speed limits
  - Steering sensitivity
  - Sensor reliability weighting

### 5️⃣ Control Interface
- Translates decisions into actionable vehicle commands within CARLA.

---

## 🌦 Weather Impact Example (Testing Results)

| Weather Condition | Base Risk | Adjusted Risk | Speed Reduction | Distance Increase |
|-------------------|----------|--------------|-----------------|-------------------|
| Clear (Baseline)  | 0.35     | 0.35         | 0%              | 0%                |
| Light Rain        | 0.35     | 0.42         | 10%             | 15%               |
| Heavy Rain        | 0.35     | 0.58         | 25%             | 40%               |
| Fog               | 0.35     | 0.61         | 30%             | 50%               |
| Night             | 0.35     | 0.48         | 15%             | 25%               |
| Night + Rain      | 0.35     | 0.67         | 35%             | 60%               |

---

## 🔮 Future Enhancements
- Trajectory prediction for surrounding vehicles
- Machine learning-based scene understanding
- Extensive testing in extreme weather
- Real-world parameter tuning

---


## 🛠 Technologies Used
- **CARLA Simulator (Python API)**
- **Sensor Fusion Techniques**
- **Rule-based Decision Engine**
- **Weather API Integration**
- **Risk Scoring System**

---
