# 🌫️ AI-Based Object Detection in Foggy and Rainy Conditions

## 🚀 Project Overview
This project focuses on developing an **AI-based object detection system** that works reliably in challenging weather conditions like **fog, rain, and low visibility**. The goal is to enhance **road safety** by improving detection accuracy during adverse weather, where traditional methods often fail.

---

## 📌 Problem Statement
Visibility on roads decreases drastically during foggy or rainy conditions, leading to challenges in object detection for autonomous vehicles and surveillance systems.

Our AI system is designed to:
- ✅ Detect objects like vehicles, pedestrians, and road signs
- ✅ Perform better under synthetic fog, blurring, and low contrast
- ✅ Enhance images using AI-based preprocessing for clearer detection

---

## 🗂 Dataset & Augmentation

### 📚 Datasets Used
- **BDD100K** - General driving dataset
- **Foggy Cityscapes** - Dataset with synthetic fog

### 🛠 Data Augmentation Techniques
- Synthetic Fog Addition
- Blurring
- Contrast Reduction/Enhancement

> **Why?**  
> To simulate real-world harsh conditions and make the model robust for low-visibility scenarios.

---

## 🧠 Model & Methods

### ⚙ Model Used
- **YOLO (You Only Look Once)** - Known for speed and real-time object detection capabilities

### ✨ Preprocessing & Enhancement
- AI-based **Dehazing**
- **Rain Removal** using Deep Learning
- **Noise Reduction**
- **CLAHE (Histogram Equalization)** for traditional comparison

---

## 📊 Performance Evaluation

| Condition            | mAP (YOLO) | IoU  |
|----------------------|-----------|------|
| **Normal Weather**   | 82%       | 0.75 |
| **Foggy/Blurred**    | 68%       | 0.63 |
| **After Enhancement**| **76%**   | **0.70** |

✅ **Result:** Enhanced images improved detection accuracy significantly.

---

## 🌟 Unique Features / USPs
- ✅ Synthetic fog, blurring, and low contrast generation for **realistic dataset augmentation**
- ✅ **AI-based dehazing and rain removal models** for image clarity
- ✅ YOLO optimized for **better detection in degraded conditions**
- ✅ Comparative analysis of **AI-enhancement vs. traditional methods (CLAHE)**

---

## 📈 Future Improvements
- Testing on **real-world foggy/rainy video data**
- Implementing **depth estimation** for distance measurement
- Further optimization for **mobile/embedded systems**

---

## 🛠 Tech Stack
- Python
- TensorFlow / Keras
- OpenCV
- YOLOv5
- Matplotlib, NumPy, Pandas

---

## 🤝 Acknowledgments
- **BDD100K Dataset**
- **Foggy Cityscapes Dataset**
- **YOLOv5 Community**

---
