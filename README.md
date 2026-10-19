
# RoadWatch: Traffic Flow Monitor

RoadWatch is a Python-based traffic monitoring project that uses computer vision to detect, track, and count vehicles in road footage.

I built this project to learn more about object detection and tracking, and to see how these technologies can be used to analyze real-world traffic.

The program uses a pretrained YOLOv8 model to detect vehicles, ByteTrack to track them across frames, and a virtual line to count vehicles moving in different directions.

## Demo

RoadWatch processes traffic footage and produces an annotated video showing:

- Bounding boxes around detected vehicles.
- Tracking IDs for individual vehicles.
- A green virtual counting line.
- Live upward and downward vehicle counts.

**Demo video:** [Watch RoadWatch in action](roadwatch-traffic-monitor/outputs/roadwatch_result.mp4)

## Features

- **Vehicle Detection:** Detects cars, motorcycles, buses, and trucks using YOLOv8.
- **Vehicle Tracking:** Uses ByteTrack to follow vehicles across video frames.
- **Virtual Line Crossing:** Counts vehicles when they cross a horizontal line.
- **Directional Counting:** Separates upward and downward crossings.
- **Video Output:** Saves an annotated video showing detected vehicles and traffic counts.

## Technologies Used

- **Python** — Main programming language.
- **Ultralytics YOLOv8** — Pretrained object detection model.
- **OpenCV** — Video processing, drawing overlays, and saving results.
- **ByteTrack** — Multi-object tracking.

## How It Works

1. OpenCV reads the traffic video frame by frame.
2. YOLOv8 detects vehicles in each frame.
3. ByteTrack assigns tracking IDs to vehicles.
4. The program calculates the center position of each vehicle's bounding box.
5. When a tracked vehicle crosses the virtual line, the corresponding counter increases.
6. Each tracking ID is counted at most once.
7. The program saves a new video containing the bounding boxes, tracking IDs, counting line, and results.

## Project Structure

```text
Roadwatch_Traffic_Monitor/
├── .gitignore
├── README.md
└── roadwatch-traffic-monitor/
    ├── main.py
    ├── requirements.txt
    ├── videos/
    │   └── traffic.mp4
    └── outputs/
        └── roadwatch_result.mp4
```

## Getting Started

### 1. Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/Nuha5/Roadwatch_Traffic_Monitor.git
cd Roadwatch_Traffic_Monitor
cd roadwatch-traffic-monitor
```

### 2. Create a virtual environment

For macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

Make sure Python is installed, then run:

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
ultralytics
opencv-python
```

### 4. Prepare the traffic video

The project uses the video located at:

`videos/traffic.mp4`

If the sample video is included in the repository, you can use it directly.

You can also test your own traffic footage by replacing `traffic.mp4` with another MP4 video using the same filename.

For more reliable results, use footage from a stationary camera where vehicles clearly cross the counting line.

### 5. Run RoadWatch

Run the following command:

```bash
python main.py
```

The pretrained YOLOv8 model will automatically download the first time the program runs.

After processing, the program saves the annotated video to:

`outputs/roadwatch_result.mp4`

The terminal also displays the total number of vehicle crossings in each direction.

## Results

I tested RoadWatch using approximately 12 seconds of traffic footage and compared the output against my own manual count.

| Direction | RoadWatch Count | Manual Count |
|---|---:|---:|
| Upward | 19 | 18 |
| Downward | 18 | 18 |
| **Total** | **37** | **36** |

The automated result differed from my manual count by one vehicle.

Since the manual count was approximate and only one short video was tested, this is an initial comparison rather than a formal accuracy evaluation.

## What I Learned

Through this project, I learned how to use a pretrained computer vision model to detect objects in a video and how to combine object detection with tracking.

I also gained experience working with OpenCV, processing video frame by frame, and implementing logic to count objects when they cross a defined line.

One thing I noticed is that tracking isn't always perfect. Vehicles can sometimes lose their tracking IDs or receive new ones, especially when there are many vehicles close together. This can affect the final count.

Testing the results manually also helped me understand why validating the output is important.

## Possible Improvements

If I continue developing RoadWatch, some improvements I would like to explore are:

- Testing the system on longer videos and different road environments.
- Improving vehicle counting when objects overlap or tracking IDs change.
- Adding separate counts for cars, motorcycles, buses, and trucks.

## Acknowledgments

This project uses Ultralytics YOLOv8 and ByteTrack. Ultralytics is distributed under the AGPL-3.0 license with commercial licensing options.

RoadWatch was developed as a personal learning and portfolio project.
