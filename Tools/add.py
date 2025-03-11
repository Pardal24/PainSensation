import os
import shutil

# Path to Data3 folder
data3_path = "Data3"

# Minimum number of frames required
min_frames = 30

# Process each subfolder
for subfolder in sorted(os.listdir(data3_path), key=lambda x: int(x)):
    subfolder_path = os.path.join(data3_path, subfolder)
    
    if not os.path.isdir(subfolder_path):
        continue  # Skip if not a directory

    # Get sorted list of frames
    frames = sorted(
        [f for f in os.listdir(subfolder_path) if f.startswith("frame_")],
        key=lambda x: int(x.split("_")[1].split(".")[0])
    )

    num_frames = len(frames)

    # Skip folders that already have enough frames
    if num_frames >= min_frames:
        continue

    # Define text file paths
    touch_file = os.path.join(subfolder_path, "touch_data.txt")
    class_file = os.path.join(subfolder_path, "classification.txt")

    # Read touch_data.txt and classification.txt
    with open(touch_file, "r") as f:
        touch_lines = f.readlines()
    with open(class_file, "r") as f:
        class_lines = f.readlines()

    # Calculate how many frames to add
    frames_needed = min_frames - num_frames

    # Select frames from the middle
    middle_indices = list(range(num_frames // 3, (2 * num_frames) // 3))
    selected_indices = middle_indices[:frames_needed]  # Take only needed amount

    # Create copies of selected frames
    new_frames = []
    new_touch_lines = []
    new_class_lines = []

    for idx in selected_indices:
        original_frame = frames[idx]
        original_index = int(original_frame.split("_")[1].split(".")[0])

        # New frame name (insert just before the original)
        new_index = original_index  # Keep the original index to insert before
        new_frame_name = f"frame_{new_index}_copy.jpeg"

        # Copy frame
        old_frame_path = os.path.join(subfolder_path, original_frame)
        new_frame_path = os.path.join(subfolder_path, new_frame_name)
        shutil.copy(old_frame_path, new_frame_path)

        # Store new frame info
        new_frames.append((new_index, new_frame_name))

        # Copy corresponding touch and class data
        new_touch_lines.append(touch_lines[original_index])
        new_class_lines.append(class_lines[original_index])

    # Insert copied text data in the right position
    for (insert_index, _) in new_frames:
        touch_lines.insert(insert_index, new_touch_lines.pop(0))
        class_lines.insert(insert_index, new_class_lines.pop(0))

    # Write updated text files
    with open(touch_file, "w") as f:
        f.writelines(touch_lines)
    with open(class_file, "w") as f:
        f.writelines(class_lines)

    # Get updated list of frames after adding copies
    updated_frames = sorted(
        [f for f in os.listdir(subfolder_path) if f.startswith("frame_")],
        key=lambda x: int(x.split("_")[1].split(".")[0].replace("_copy", ""))
    )

    # Rename everything sequentially
    for new_index, frame in enumerate(updated_frames):
        old_frame_path = os.path.join(subfolder_path, frame)
        new_frame_name = f"frame_{new_index}.jpeg"
        new_frame_path = os.path.join(subfolder_path, new_frame_name)
        os.rename(old_frame_path, new_frame_path)

print("✅ Processing complete: Frames duplicated, text files updated, and everything reordered.")
