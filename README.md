# Invisibility Cloak Project

A Python-based implementation of a Harry Potter style invisibility cloak using OpenCV and computer vision techniques.

## 🎯 Features

- **Real-time invisibility effect**: Makes bright red objects appear transparent
- **Background capture**: Automatically captures and stores background for replacement
- **Color detection**: Uses HSV color space for robust red color detection
- **Morphological operations**: Cleans up the mask for smoother invisibility effect
- **Mirror mode**: Flips the video for a more natural user experience
- **Camera testing**: Built-in camera test functionality

## 🛠️ Requirements

- Python 3.7 or higher
- Webcam/Camera
- Bright red colored cloth or object (to act as the invisibility cloak)

## 📦 Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd invisibility-cloak
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install opencv-python numpy
   ```

## 🚀 Usage

### Running the Application

```bash
python invisibility_cloak.py
```

### Menu Options

When you run the script, you'll see a menu:
- **Option 1**: Test Camera - Verify your camera is working properly
- **Option 2**: Start Invisibility Cloak - Begin the main application

### Step-by-Step Instructions

1. **Start the application** and choose option 2
2. **Move out of camera view** when prompted (you have 3 seconds)
3. **Stay out of frame** for about 6 seconds while background is captured
4. **Put on something bright red** (shirt, cloth, scarf, etc.)
5. **Move back into the camera view** - you should now be invisible!
6. **Press 'q'** to quit the application

## 🎨 How It Works

### Technical Overview

1. **Background Capture**: The script captures 60 frames of the background to allow camera adjustment
2. **Color Detection**: Uses HSV color space to detect bright red colors (handles red's wrap-around in HSV)
3. **Mask Creation**: Creates binary masks to isolate red regions
4. **Morphological Operations**: Cleans and refines the mask using opening and dilation
5. **Image Segmentation**: Separates the frame into cloak and non-cloak regions
6. **Replacement**: Replaces cloak pixels with corresponding background pixels

### Color Ranges Used

The script detects red using two HSV ranges:
- **Range 1**: Hue 0-10°, Saturation 120-255, Value 70-255
- **Range 2**: Hue 170-180°, Saturation 120-255, Value 70-255

## 🎯 Tips for Best Results

### Lighting Conditions
- Use **good, consistent lighting**
- Avoid shadows and harsh lighting changes
- Natural daylight works best

### Cloak Material
- Use **bright, solid red** fabric or clothing
- Avoid patterns or mixed colors
- Larger surface area works better than small objects

### Camera Setup
- Keep the camera **stable** (use a tripod if possible)
- Ensure the **background is stationary**
- Position yourself at an appropriate distance from the camera

### Troubleshooting
- If the effect isn't working, try adjusting the lighting
- Make sure your red object is bright enough
- Ensure minimal background movement
- Check that your camera drivers are up to date

## 🔧 Customization

### Changing the Target Color

To detect a different color, modify the HSV ranges in the `create_invisibility_cloak()` function:

```python
# For green color detection
lower_green = np.array([40, 40, 40])
upper_green = np.array([80, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)
```

### Adjusting Mask Refinement

You can modify the morphological operations:

```python
# Change kernel size for different smoothing effects
kernel = np.ones((5, 5), np.uint8)  # Larger kernel = more smoothing

# Adjust iterations for stronger effects
mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=2)
```

## 🎥 Demo

The invisibility cloak creates a magical effect where anything bright red becomes transparent, revealing the background behind it. Perfect for creating Harry Potter-style magic effects!

## ⚠️ Known Limitations

- Works best with solid, bright red colors
- Requires stable lighting conditions
- Background must remain stationary
- Performance depends on camera quality and computer specs

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Inspired by the Harry Potter invisibility cloak
- Built using OpenCV computer vision library
- Thanks to the open-source community for the amazing tools