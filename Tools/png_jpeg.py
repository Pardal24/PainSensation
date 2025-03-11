import os

# Path to Data3 folder
data3_path = "Data3"

# Loop through all subfolders
for subfolder in sorted(os.listdir(data3_path), key=lambda x: int(x)):
    subfolder_path = os.path.join(data3_path, subfolder)

    if not os.path.isdir(subfolder_path):
        continue  # Skip if not a directory

    # Rename all .png files to .jpeg
    for filename in os.listdir(subfolder_path):
        if filename.endswith(".png"):
            old_file = os.path.join(subfolder_path, filename)
            new_file = os.path.join(subfolder_path, filename.replace(".png", ".jpeg"))
            os.rename(old_file, new_file)

print("✅ All .png files changed to .jpeg successfully.")
