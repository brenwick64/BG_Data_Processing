# Initial Imports and Dataframe load
import pandas as pd
import argparse
import sys

input_csv = '../Processed_Data/bolus_events_max.csv'
output_x = '../Processed_Data/x_data.csv'
output_y = '../Processed_Data/y_data.csv'

# Argparse config
parser = argparse.ArgumentParser()
parser.add_argument("-bh", "--beforehours",
                    help="The amount of contextual hours before a bolus event", type=int)
parser.add_argument("-ah", "--afterhours",
                    help="The amount of contextual hours after a bolus event", type=int)
args = parser.parse_args()


# TODO: Split up partition and pruning logic for better separation
def split_data(df, xgap, ygap):
    # The column representing the current bolus event
    zero_index = 52

    # All data BEFORE or DURING a bolus event
    x_data = df.iloc[:, 0:zero_index]

    # All Blood Glucose (BG) readings AFTER the bolus event
    y_data = df.iloc[:, zero_index:-1]

    # Prune Y Data
    y_data = y_data.filter(regex='BG')
    y_data = y_data.iloc[:, 0:ygap]

    # Prune X Data
    x_data = x_data.iloc[:, (x_data.shape[1] - (4 * xgap)):x_data.shape[1]]

    # Write X and Y data to files
    x_data.to_csv(output_x, index=False)
    y_data.to_csv(output_y, index=False)


# __SCRIPT START__

# Cheks for required args
if(args.beforehours == None or args.afterhours == None):
    print(
        "error: arguments: [-bh ah], [--beforehours, --afterhours] requried (-h for help info)")
    sys.exit()

# Checks gap appropriate value
elif((args.beforehours > 12 or args.beforehours < 1) or (args.afterhours > 12 or args.afterhours < 1)):
    print("error: argument -g must be an integer (1-12)")
    sys.exit()

df = pd.read_csv(input_csv)
df = df.fillna(0)

split_data(df, args.beforehours, args.afterhours)
print(f'\nX file created ({args.beforehours} hour context gap)')
print(f'\nY file created ({args.afterhours} hour context gap)')
