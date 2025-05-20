import pandas as pd
import numpy as np
import pickle
import glob

# To display all the columns
pd.set_option('display.max_columns', None)

# Sampling for covariance calculations
# 2 is not a reliable amount of measurements, but it works as a proof of concept
sampling = 30

# Define bin sizes (adjust as needed)
bin_sizes = [0.3, 0.3, 0.3, 15, 15, 15]     # x,y,z,roll,pitch,yaw

# Find all measured and error CSV files
measured_files = glob.glob("ground_truth_data*.csv")
error_files = glob.glob("error_data*.csv")

# Sort both lists to maintain matching order
measured_files.sort()
error_files.sort()

# Initialize empty DataFrames
measured_df = pd.DataFrame()
error_df = pd.DataFrame()

for m_file, e_file in zip(measured_files, error_files):
    m_temp = pd.read_csv(m_file)
    e_temp = pd.read_csv(e_file)

    # Drop time columns
    # m_temp.drop(columns=["time_secs", "time_nsecs"], inplace=True)
    # e_temp.drop(columns=["time_secs", "time_nsecs"], inplace=True)

    measured_df = pd.concat([measured_df, m_temp], ignore_index=True)
    error_df = pd.concat([error_df, e_temp], ignore_index=True)

# Load CSV files
# measured_df = pd.read_csv("ground_truth_data.csv")  # Raw measured position
# error_df = pd.read_csv("error_data.csv")  # Error between measured and actual

# Drop time columns (not needed for analysis)
measured_df.drop(columns=["time_secs", "time_nsecs", "roll_meas", "pitch_meas", "yaw_meas"], inplace=True)
error_df.drop(columns=["time_secs", "time_nsecs"], inplace=True)


#pd.set_option('display.max_rows', None)

#print(error_df)

# Every "measured" (raw data from tag_detections) is being rounded to a multiple
# of the bin sizes. This way we create the identifiers in the same index for the error data
size = 0
for column in measured_df.columns:
    measured_df[column] = np.round(measured_df[column] / bin_sizes[size]) * bin_sizes[size]
    size += 1

cov_dict = {}

for index in error_df.index:
    bin = tuple(np.round(measured_df.loc[index].values,1))
    # Visualize bins 400 to 500
    # if 399 < index < 501:
    #     print(bin)

    # If bin doesn't exist, we'll create the empty matrix which will contain all
    # of the errors for this bin (in order to later obtain the covariance from it)
    if bin not in cov_dict:
        cov_dict[bin] = []

    cov_dict[bin].append(error_df.loc[index].values.tolist())

for keys in cov_dict:
    print(keys)

# We calculate the covariance for each set of error measurements (for a given sampling)
bins_to_delete = []
for bin_id in cov_dict:
    bin = cov_dict[bin_id]
    if len(bin) >= sampling:
        cov_matrix = np.cov(bin, rowvar=False).tolist()
        print(f'{bin_id} : {cov_matrix}')

        # Rewrite the cov_dictionary with the covariances
        cov_dict[bin_id] = cov_matrix

    # If there isn't enough data, we just delete that entrance
    else:
        bins_to_delete.append(bin_id)

# print(cov_dict)

for bin_id in bins_to_delete:
    del cov_dict[bin_id]

# Let's check dictionary's length and then let's look at the dictionary
# for i in cov_dict:
#     print(i, ":",cov_dict[i])
# print("\nBins number:",len(cov_dict))

# Save covariance matrices to a file
with open("covariance_matrices.pkl", "wb") as f:
    pickle.dump(cov_dict, f)

