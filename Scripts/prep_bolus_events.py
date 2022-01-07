# Initial Imports and Dataframe load
import pandas as pd

input_csv = '../Processed_Data/bolus_events_dirty.csv'
output_x = '../Processed_Data/x_data.csv'
output_y = '../Processed_Data/y_data.csv'


def split_data(df, gap):
    # The column representing the current bolus event
    zero_index = (gap + 1) * 4

    # All data BEFORE or DURING a bolus event
    x_data = df.iloc[:, 0:zero_index]

    # All Blood Glucose (BG) readings AFTER the bolus event
    y_data = df.iloc[:, zero_index: 99]
    for i in range(gap):
        y_data = y_data.drop('carb_'+str(i+1), axis=1)
        y_data = y_data.drop('bolus_'+str(i+1), axis=1)
        y_data = y_data.drop('basal_'+str(i+1), axis=1)

    # Write X and Y data to files
    x_data.to_csv(output_x, index=False)
    y_data.to_csv(output_y, index=False)


# __SCRIPT START__

df = pd.read_csv(input_csv)
df = df.fillna(0)

# Compute hour gap from column count of bolus events
hour_gap = int(((df.shape[1] - 4) / 8))
split_data(df, hour_gap)
print(f'\nX and Y files created ({hour_gap} hour context gap)')
