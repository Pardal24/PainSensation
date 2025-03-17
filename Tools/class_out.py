import os
import numpy as np

# Path to the Data_Robot directory
data_robot_path = "Data_Robot"

# Loop through all 50 folders (0 to 49)
for folder_index in range(50):
    folder_path = os.path.join(data_robot_path, str(folder_index))
    touch_data_file = os.path.join(folder_path, "touch_data.txt")

    if os.path.exists(touch_data_file):  # Check if the file exists
        # Load the file
        data = np.loadtxt(touch_data_file, dtype=int)

        # Remove the last column
        new_data = data[:, :-1]

        # Save the modified data back, overwriting the original file
        np.savetxt(touch_data_file, new_data, fmt="%d")

print("All files updated successfully!")