
import os

count_arr = []
for i in range(50):
    path = f"Data3/{i}"
    count = 0
    if i != 32:
        for n in os.listdir(path):
            if os.path.isfile(os.path.join(path, n)):
                count += 1
        count = count-2
        count_arr.append(count)
        if count == 36:
            print(i)
print(count_arr)

# data3_path = "Data3"
# t=0
# for subfolder in sorted(os.listdir(data3_path), key=lambda x: int(x)):
#     subfolder_path = os.path.join(data3_path, subfolder)
#     t+=1
#     if t == 1:
#         print("ola")
#         print(subfolder_path)