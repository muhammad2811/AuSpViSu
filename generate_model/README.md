## Steps to Generate Dataset and Train Model

### 1. Download Matches

Download the matches from the file `matches.txt` and place them in the appropriate directory. This file contains links or references to the football match videos that will be processed.

### 2. Cut Events

Cut specific events from the match videos, such as goals, yellow cards, red cards, and substitutions. Use a video editor or an automated script to segment these events.

### 3. Generate Dataset

Run the `generate_DS.py` script for each type of event. This script processes the segmented event videos and generates a dataset suitable for training a YOLO model.

```bash
python generate_DS.py
```

### 4. Train YOLO Model in Colab

Once the dataset is created, you can train the YOLO model using the provided Colab notebook. Upload the dataset to your Colab environment and run the `generate-yolo-model.ipynb` notebook.

### 5. Obtain the Model Detection File

After training, the model detection file `best.pt` will be generated. This file contains the trained YOLO model and can be used for object detection in your main code.

### Usage

- **Generate Dataset:** Follow steps 1-3 to prepare the dataset.
- **Train Model:** Use the Colab notebook to train the YOLO model and obtain `best.pt`.
- **Main Code:** Use `best.pt` in your main code for detecting events in football matches.
