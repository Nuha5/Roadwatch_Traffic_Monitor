import cv2
from ultralytics import YOLO

# RoadWatch - Traffic Flow Monitor
VIDEO_PATH = "videos/traffic.mp4"
OUTPUT_PATH = "outputs/roadwatch_result.mp4"

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture(VIDEO_PATH)

if not video.isOpened():
    raise FileNotFoundError("Could not open traffic video.")

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

# Place the counting line at 65% of the video height
line_y = int(height * 0.65)

writer = cv2.VideoWriter(
    OUTPUT_PATH,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps if fps > 0 else 30,
    (width, height)
)

if not writer.isOpened():
    raise RuntimeError("Could not create output video.")

# Remember where each tracked vehicle was last seen
previous_positions = {}

# Prevent counting the same tracking ID twice
counted_ids = set()

down_count = 0
up_count = 0

while True:
    success, frame = video.read()

    if not success:
        break

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[2, 3, 5, 7],
        conf=0.35,
        verbose=False
    )

    # Draw YOLO's bounding boxes and tracking IDs
    annotated = results[0].plot()

    boxes = results[0].boxes

    if boxes is not None and boxes.id is not None:
        for box in boxes:
            track_id = int(box.id.item())

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Use the center of the vehicle's bounding box
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            if track_id in previous_positions:
                old_y = previous_positions[track_id]

                # Count downward crossings
                if old_y < line_y <= center_y:
                    if track_id not in counted_ids:
                        down_count += 1
                        counted_ids.add(track_id)

                # Count upward crossings
                elif old_y > line_y >= center_y:
                    if track_id not in counted_ids:
                        up_count += 1
                        counted_ids.add(track_id)

            previous_positions[track_id] = center_y

            # Draw the center point
            cv2.circle(
                annotated,
                (center_x, center_y),
                4,
                (0, 255, 255),
                -1
            )

    # Draw counting line
    cv2.line(
        annotated,
        (0, line_y),
        (width, line_y),
        (0, 255, 0),
        3
    )

    # Draw traffic statistics
    cv2.rectangle(
        annotated,
        (10, 10),
        (310, 110),
        (30, 30, 30),
        -1
    )

    cv2.putText(
        annotated,
        f"Downward: {down_count}",
        (20, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated,
        f"Upward: {up_count}",
        (20, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    writer.write(annotated)

video.release()
writer.release()

print("RoadWatch analysis complete!")
print(f"Downward crossings: {down_count}")
print(f"Upward crossings: {up_count}")
print(f"Total crossings: {down_count + up_count}")
print(f"Saved video: {OUTPUT_PATH}")