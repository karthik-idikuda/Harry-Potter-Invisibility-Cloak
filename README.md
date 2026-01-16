# Harry Potter Invisibility Cloak

## Overview
A fun computer vision application that simulates the famous Invisibility Cloak from Harry Potter using color segmentation and image processing.

## Features
-   **Real-time Processing**: Hides the user instantly in the live video feed.
-   **Color Detection**: uses HSV color space to identify the cloak color (e.g., red or blue).
-   **Background Replacement**: Seamlessly patches the masked area with a static background frame.

## Technology Stack
-   **Library**: OpenCV.
-   **Language**: Python.
-   **Data**: NumPy for array manipulation.

## Usage Flow
1.  **Capture**: System records a few seconds of the background without the user.
2.  **Enter**: User steps into the frame with the "cloak".
3.  **Mask**: Algorithm detects the cloak color and creates a mask.
4.  **Invisibilize**: The masked area is replaced with the pre-recorded background.

## Quick Start
```bash
# Clone the repository
git clone "https://github.com/Nytrynox/Harry-Potter-Invisibility-Cloak.git"

# Install dependencies
pip install opencv-python numpy

# Run the simulation
python main.py
```

## License
MIT License

## Author
**Karthik Idikuda**
