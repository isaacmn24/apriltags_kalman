import pandas as pd
import glob
import numpy as np

filter_files = glob.glob("filter_data_*.csv")
ground_truth_files  = glob.glob("ground_truth_data_*.csv")

filter_files.sort()
ground_truth_files.sort()

for file in range(len(filter_files)):
    filter_data = pd.read_csv(filter_files[file])
    ground_truth_data  = pd.read_csv(ground_truth_files[file])

    mean_filter       = filter_data.mean()
    mean_ground_truth = ground_truth_data.mean()

    print(f"\n-----------------------------\nARCHIVO {filter_files[file]}   ") #\n\nDATOS FILTRO
    print(np.abs(mean_ground_truth - mean_filter) * 100)
    # print("\nDATOS GROUND TRUTH")
    # print(ground_truth_data.mean(np.abs(mean_ground_truth - mean_filter)))


