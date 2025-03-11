import os

# Path to Data3/1 folder

start = 3
end = 3
folder = 44

subfolder_path = f"Data3/{folder}"

# Define paths to text files
touch_file = os.path.join(subfolder_path, "touch_data.txt")
class_file = os.path.join(subfolder_path, "classification.txt")

# Process touch_data.txt
if os.path.exists(touch_file):
    with open(touch_file, "r") as f:
        lines = f.readlines()
    if len(lines) > 6:
        with open(touch_file, "w") as f:
            f.writelines(lines[start:-end])  # Remove first 3 and last 3 rows

# Process classification.txt
if os.path.exists(class_file):
    with open(class_file, "r") as f:
        lines = f.readlines()
    if len(lines) > 6:
        with open(class_file, "w") as f:
            f.writelines(lines[start:-end])  # Remove first 3 and last 3 rows

# Rename and reorder frames
frames = sorted(
    [f for f in os.listdir(subfolder_path) if f.startswith("frame_")],
    key=lambda x: int(x.split("_")[1].split(".")[0])  # Sort numerically
)

frames_to_delete = frames[:start] + frames[-end:]  # First 3 and last 3
for frame in frames_to_delete:
    os.remove(os.path.join(subfolder_path, frame))

# Get remaining frames after deletion
remaining_frames = sorted(
    [f for f in os.listdir(subfolder_path) if f.startswith("frame_")],
    key=lambda x: int(x.split("_")[1].split(".")[0])
)

# Rename remaining frames sequentially
for new_index, frame in enumerate(remaining_frames):
    old_frame_path = os.path.join(subfolder_path, frame)
    new_frame_name = f"frame_{new_index}.png"  # Adjust extension if needed
    new_frame_path = os.path.join(subfolder_path, new_frame_name)
    os.rename(old_frame_path, new_frame_path)

print("✅ Processing complete: Text files updated, frames deleted, and reordered.")