# Football Video Summarization and Page Statistics

## Description

This project aims to summarize a full EPL football match in 40 minutes, providing a summarized video of goals and page statistics containing details of events such as yellow and red cards, substitutions, player names , Time, and teams. This is achieved using object detection (YOLO v8) and OCR (EasyOCR).

## Table of Contents

1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Examples](#examples)

## Installation

### Prerequisites

- Python 3.10.11
- YOLOv8
- EasyOCR
- Google Colab
- Streamlit
- MoviePy
- Levenshtein

### Steps

1. Clone the repository:

2. Install the required packages:

3. Download and unzip the dataset(call me):

4. Train the YOLO model using the provided notebook in Google Colab:

## Usage

1. Download the match video from `match.txt` and place it next to `Generate_Highlights.py`.
2. Run the `Generate_Highlights.py` script and enter the name of the match:
   ```bash
   python Generate_Highlights.py
   ```
   This will create a summarized video of goals and save the event details in `events.txt`.

3. To display the page statistics, run `app.py`:
   ```bash
   python app.py
   ```
   This will read `events.txt` and display the statistics using Streamlit.

## Project Structure

```
.
├── app.py
├── Detector.py
├── Editor.py
├── event.pt(not exist in github)
├── Generate_Highlights.py
├── OCR.py
├── important-before-run
│   ├── dataset.zip(not exist in github)
│   ├── generat-yolo-model.ipynb
│   ├── generate_DS.py
│   ├── match.txt
│   ├── requirements.txt
│   └── short-video-for-dataset(not exist in github)
│       ├── F-LIV.mp4
│       ├── F-MUN.mp4
│       ├── F-TOT.mp4
│       ├── G-CHE.mp4
│       ├── G-LIV.mp4
│       ├── G-MCI.mp4
│       ├── G-NEW.mp4
│       ├── R-MUN.mp4
│       ├── S-CHE.mp4
│       ├── S-CRY.mp4
│       ├── S-MCI.mp4
│       ├── S-MUN.mp4
│       ├── Y-CRY.mp4
│       ├── Y-MUN.mp4
│       ├── Y-NEW.mp4
│       └── Y-TOT.mp4
```

## Examples

### Generating Highlights

1. Prepare the match video file.
2. Run the script:
   ```bash
   python Generate_Highlights.py
   ```
3. Example output:
   - Summarized video of goals.
   - `events.txt` containing event details.

### Displaying Page Statistics

1. Ensure `events.txt` is generated.
2. Run `app.py`:
   ```bash
   python app.py
   ```
3. Example output:
   - A Streamlit page displaying event statistics.