# 🎨 AirCanvas – Draw in the Air with Hand Gestures

<p align="center">
  <strong>Turn your hand movements into digital art! 🖐️✨</strong>
</p>

<p align="center">
  A real-time computer vision drawing application that lets you create beautiful digital artwork using nothing but your hand gestures and a webcam.
</p>

<p align="center">
  <a href="https://github.com/chinnikavya123/Aircanvas/releases/latest">📥 Download for Windows</a> •
  <a href="https://github.com/chinnikavya123/Aircanvas">⭐ GitHub Repository</a>
</p>

---

## 🌟 About the Project

**AirCanvas** is an interactive, gesture-controlled digital drawing application built using Python, OpenCV, MediaPipe and CustomTkinter.

It transforms your webcam into a virtual canvas, allowing you to draw, erase, pause, and create artwork by moving your fingers in the air.

Using real-time hand landmark detection, AirCanvas recognizes specific hand gestures and translates them into drawing actions. No physical mouse, touchscreen, or drawing tablet is required!

Whether you want to sketch something creative, experiment with colours, or explore computer vision, AirCanvas makes digital drawing more interactive and fun. 💜

## ✨ Key Features

🎨 **Gesture-Based Drawing**
- Draw naturally by raising your index finger.
- Real-time hand tracking through your webcam.
- Smooth drawing experience.

🌈 **24+ Vibrant Colours**
- Explore a wide collection of colours.
- Open the expandable colour palette whenever needed.
- Choose your favourite colours.

🖌️ **Customizable Brushes**
- Marker, Pencil and Neon brush styles.
- Adjustable brush thickness.
- Customizable eraser size.

🧹 **Smart Eraser**
- Erase artwork using a simple fist gesture.
- Switch to eraser mode for precise editing.

↩️ **Undo and Redo**
- Undo previous drawing actions.
- Restore actions using redo.
- Maintain control over your artwork.

🖼️ **Custom Backgrounds**
- Transparent background.
- White, black and other available background options.
- Choose a background when exporting your artwork.

💾 **Save Your Artwork**
- Export drawings as PNG images.
- Save transparent artwork.
- Access your saved creations through the gallery.

💜 **Interactive User Interface**
- Modern dark-themed desktop interface.
- Dedicated gesture guide.
- Live webcam preview and drawing feedback.

## 🖐️ Gesture Controls

AirCanvas uses hand gestures to interact with the drawing canvas.

| Hand Gesture | Action |
|---|---|
| ☝️ Index finger raised | Draw |
| ✊ Fist / fingers folded | Erase |
| ✋ Four fingers raised | Pause drawing |
| ✌️ Index and middle fingers raised | Ready / reposition |

**Tip:** Keep your hand visible to the webcam and use clear gestures for better recognition.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| OpenCV | Webcam access and image processing |
| MediaPipe | Real-time hand landmark detection |
| NumPy | Drawing canvas and image operations |
| CustomTkinter | Modern desktop user interface |
| Pillow (PIL) | Image processing and PNG export |

## 🚀 Getting Started

### Option 1: Download the Windows Application

The easiest way to use AirCanvas is to download the pre-built Windows release.

1. Visit the [AirCanvas Releases](https://github.com/chinnikavya123/Aircanvas/releases/latest) page.
2. Download `AirCanvas-Windows.zip`.
3. Extract the ZIP file.
4. Open the extracted `AirCanvas` folder.
5. Double-click `AirCanvas.exe`.
6. Allow webcam access if prompted.
7. Start creating your artwork!

**Requirements:**
- Windows 10 or Windows 11.
- A working webcam.
- A compatible 64-bit Windows system.

No separate Python installation is required when using the packaged application.

### Option 2: Run from Source Code

If you want to explore or modify the source code, follow these steps.

**1. Clone the repository**

```bash
git clone https://github.com/chinnikavya123/Aircanvas.git
```

**2. Navigate to the project folder**

```bash
cd Aircanvas
```

**3. Create a virtual environment**

```bash
python -m venv .venv
```

**4. Activate the virtual environment**

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

**5. Install the dependencies**

```bash
python -m pip install -r requirements.txt
```

**6. Run the application**

```bash
python app.py
```

Make sure your webcam is connected and available before launching the application.

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + Z` | Undo |
| `Ctrl + Y` | Redo |
| `Ctrl + S` | Save artwork |
| `Esc` | Close active popup / exit the relevant interaction |

## 📁 Project Structure

```text
AirCanvas/
│
├── app.py
│   └── Main application and gesture recognition logic
│
├── requirements.txt
│   └── Python dependencies
│
└── README.md
    └── Project documentation
```

The application creates an `AirCanvas_Gallery` folder when needed to store saved artwork.

## 🔍 How It Works

AirCanvas combines computer vision and hand landmark detection to make gesture-based drawing possible.

1. **Webcam Input:** OpenCV captures live video from the webcam.
2. **Hand Detection:** MediaPipe detects the hand and identifies its landmarks.
3. **Gesture Recognition:** The application analyses finger positions to identify the user's gesture.
4. **Action Mapping:** Recognized gestures are translated into drawing, erasing, pausing or repositioning actions.
5. **Canvas Rendering:** NumPy and OpenCV process the drawing strokes and display the artwork.
6. **Image Export:** Pillow and image-processing operations help save the final artwork as a PNG.

## 🔐 Privacy

- Webcam frames are processed locally by the application.
- No cloud-based image processing is required.
- Your drawings are saved locally on your computer.

## 🎯 Project Goals

AirCanvas was developed to explore practical applications of computer vision and human-computer interaction.

The project helped me gain hands-on experience with:

- Real-time computer vision.
- Hand landmark detection.
- Gesture recognition.
- Image processing using OpenCV.
- Interactive desktop application development.
- Building a complete Python application and packaging it for Windows.

## 🚀 Future Enhancements

Some ideas for future improvements include:

- ✨ More drawing tools and creative effects.
- 🖐️ Multi-hand gesture interactions.
- 🎨 More canvas customization options.
- 📐 Shape recognition and drawing assistance.
- 🎥 Drawing session recording and playback.

## 👩‍💻 Author

**Chinni Kavya Sri**

B.Tech – Computer Science and Engineering (AI & ML)

[![GitHub](https://img.shields.io/badge/GitHub-chinnikavya123-black?style=for-the-badge&logo=github)](https://github.com/chinnikavya123)

---

<p align="center">
  Made with 💜, Python and Computer Vision.
</p>

<p align="center">
  ⭐ If you like AirCanvas, consider giving this repository a star!
</p>
