# python3 pip install numpy opencv-python
import numpy as np
import cv2
import pickle
import sys

# Constants for terminal dimensions and aspect ratio
ASPECT_RATIO = 16 / 9
WIDTH = 80
HEIGHT = int(WIDTH / (2 * ASPECT_RATIO))

# Character set for ASCII art and ANSI color codes
CHARSET = " ,(S#g@@g#S(, "
BLACK = "\u001b[48;5;16;38;5;16m"  # ANSI code for black background

# Load color lookup table data and color mapping information
LUT = np.load("LUT.npy")
LERPED = pickle.load(open("colors.pkl", "rb"))

# Function to set ANSI color codes
def set_color(bg, fg):
    return "\u001b[48;5;%s;38;5;%sm" % (bg, fg)

# Convert RGB image to text with colored ASCII art
def convert_img(img):
    lines = []

    for row in img:
        line = ""
        for color in row:
            color = np.round(color).astype(int)
            b, g, r = color[0], color[1], color[2]

            # Look up the color index in the RGB lookup table
            idx = LUT[b, g, r]
            bg, fg, lerp, _ = LERPED[idx]

            # Get the corresponding character from the character set
            char = CHARSET[lerp]
            line += "%s%c" % (set_color(bg, fg), char)
        line += BLACK + "\n"  # Add a black background to avoid color fringe
        lines.append(line)

    # Move the cursor to the top left to prevent rolling effect
    lines.append("\u001b[%iD\u001b[%iA" % (WIDTH, HEIGHT + 1))
    return "".join(lines)

# Main function for video to ASCII conversion
def main():
    if len(sys.argv) == 2:
        video_path = sys.argv[1]
        cap = cv2.VideoCapture(video_path)

        with cap:
            while True:
                ret, frame = cap.read()

                # Check if the frame was successfully read
                if not ret:
                    break

                img = cv2.resize(frame, (WIDTH, HEIGHT))
                print(convert_img(img))
    else:
        print("Expected video file as an argument.")

if __name__ == "__main__":
    main()
