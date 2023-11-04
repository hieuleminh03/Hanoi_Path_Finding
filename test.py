import json
import os
import heapq

from utils import convert_dict_grap
from utils import algorithm_ucs


# Specify the directory where data files are stored
data_directory = "data"

# List the available data samples (1.json to 16.json)
data_samples = [os.path.join(data_directory, f"{i}.json") for i in range(1, 17)]

# Initialize variables to store the chosen data sample and algorithm
chosen_data_sample = "Chưa chọn"
chosen_algorithm = "Chưa chọn"

while True:
    print(f"Mẫu data đã chọn: {chosen_data_sample}")
    print(f"Thuật toán đang dùng: {chosen_algorithm}")

    print("Menu:")
    print("1. Chọn mẫu data")
    print("2. Xem mẫu data")
    print("3. Chọn thuật toán")
    print("4. Tìm đường")
    print("5. Thoát")

    choice = input("Chọn một tùy chọn: ")

    if choice == "1":
        print("Chọn một mẫu data:")
        for i, sample in enumerate(data_samples):
            print(f"{i + 1}. {sample}")
        try:
            sample_choice = int(input("Nhập số của mẫu data: "))
            if 1 <= sample_choice <= len(data_samples):
                chosen_data_sample = data_samples[sample_choice - 1]
        except ValueError:
            print("Lựa chọn không hợp lệ.")

    elif choice == "2":
        if chosen_data_sample == "Chưa chọn":
            print("Bạn chưa chọn mẫu data.")
        else:
            # Load and display information about the selected data sample
            with open(chosen_data_sample, 'r') as f:
                data = json.load(f)
            # Display sample information (you can customize this part)
            for point in data:
                print(f"Point {point['id']} - Name: {point['name']} - Limit: {point['point_limit']}")

    elif choice == "3":
        print("Chọn một thuật toán:")
        algorithms = ["UCS (Uniform Cost Search)", "Thuật toán khác"]
        for i, alg in enumerate(algorithms):
            print(f"{i + 1}. {alg}")
        try:
            algorithm_choice = int(input("Nhập số của thuật toán: "))
            if 1 <= algorithm_choice <= len(algorithms):
                chosen_algorithm = algorithms[algorithm_choice - 1]
        except ValueError:
            print("Lựa chọn không hợp lệ.")

    elif choice == "4":
        if chosen_data_sample == "Chưa chọn" or chosen_algorithm == "Chưa chọn":
            print("Hãy chọn mẫu data và thuật toán trước khi tìm đường.")
        else:
            # Implement the path finding logic here using the chosen algorithm
            with open(chosen_data_sample, 'r') as f:
                data = json.load(f)
            grap = convert_dict_grap(data)
            start_point = input("Nhập điểm bắt đầu: ")
            end_point = input("Nhập điểm kết thúc: ")
            path, cost = algorithm_ucs(grap, start_point, end_point)
            if path is not None:
                print(f"Đường đi từ điểm {start_point} đến điểm {end_point}: {path}")
                print(f"Chi phí của đường đi: {cost}")
            else:
                print(f"Không tìm thấy đường đi từ {start_point} đến {end_point}")

    elif choice == "5":
        break

    else:
        print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
