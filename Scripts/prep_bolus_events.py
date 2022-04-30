# Initial Imports and Dataframe load
import pandas as pd
import argparse

input_csv = '../Processed_Data/bolus_events_dirty.csv'
output_x = '../Processed_Data/x_data.csv'
output_y = '../Processed_Data/y_data.csv'

# Argparse config
parser = argparse.ArgumentParser()
parser.add_argument("-bh", "--beforehours",
                    help="The amount of contextual hours before a bolus event", type=int)
parser.add_argument("-ah", "--afterhours",
                    help="The amount of contextual hours after a bolus event", type=int)
args = parser.parse_args()


def split_data(df, xgap, ygap):
    # The column representing the current bolus event
    x_zero_index = (xgap + 1) * 4

    # All data BEFORE or DURING a bolus event
    x_data = df.iloc[:, 0:x_zero_index]

    # All Blood Glucose (BG) readings AFTER the bolus event
    y_data = df.iloc[:, x_zero_index: 99]
    for i in range(xgap):
        y_data = y_data.drop('carb_'+str(i+1), axis=1)
        y_data = y_data.drop('bolus_'+str(i+1), axis=1)
        y_data = y_data.drop('basal_'+str(i+1), axis=1)
    # Drops columns based on ygap value
    y_data = y_data.iloc[:, ygap-1]

    # Write X and Y data to files
    x_data.to_csv(output_x, index=False)
    y_data.to_csv(output_y, index=False)


# __SCRIPT START__

df = pd.read_csv(input_csv)
df = df.fillna(0)

split_data(df, args.beforehours, args.afterhours)
print(f'\nX file created ({args.beforehours} hour context gap)')
print(f'\nY file created ({args.afterhours} hour context gap)')
