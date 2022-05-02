import pandas as pd
import glob
import argparse
import sys

output_csv = '../Processed_Data/bolus_events_max.csv'
path = '../Clean_Batches/'
filenames = glob.glob(path + "/*.csv")

# __DATA CONSTANTS__

# How many rows each table consists of
batch_size = 5
# For each table, the index of the bolus(u) data
bolus_row_index = 2
# The length of all table rows
table_row_length = 25
# The maximum context span for X and Y data
max_hour_span = 12


# __HELPER FUNCTIONS__

# Converts a column into a list and trims the initial null column
def get_column_info_as_list(table, index):
    my_list = table.iloc[:, index].tolist()
    my_list.pop(0)
    return my_list


# Extracts tables from CSV file based on batch size
def get_tables(filename, batch_size):
    tables = []
    total_rows = sum(1 for row in (open(filename)))
    for i in range(0, total_rows-1, batch_size):
        df = pd.read_csv(filename,
                         nrows=batch_size, skiprows=i)
        tables.append(df.iloc[:, :-2])
    return tables


# Grabs the indicies of a table's bolus event columns
def get_bolus_indices(table, bolus_row_index):
    bolus_indices = []
    # Returns bolus row as a list
    bolus_row = table.iloc[bolus_row_index].tolist()

    for i in range(len(bolus_row)):
        bolus_data = bolus_row[i]
        # Checks to make sure numerical value is gained
        if (pd.isna(bolus_data) == False and type(bolus_data) != str):
            bolus_indices.append(i)
    return bolus_indices


# Removes row "labels" to avoid shifting issues
def trim_tables(tables):
    trimmed_tables = []
    for table in tables:
        trimmed_tables.append(table.iloc[:, 1:])
    return trimmed_tables


# Takes a table and index and provides a record of a bolus event with context
def index_to_bolus_event(table, bolus_index):
    bolus_index = bolus_index
    df = pd.DataFrame(columns=df_columns)
    bolus_event = []

    # Gets current event and surrounding context
    for i in range((-1 * hour_gap), (hour_gap + 1)):
        bolus_event.extend(get_column_info_as_list(
            table, (bolus_index + i) % 24))
    full_bolus_event = pd.Series(bolus_event, index=df.columns)
    df = df.append(full_bolus_event, ignore_index=True)

    return df


# __SCRIPT START__
hour_gap = max_hour_span
df_columns = []

# Allocates 4 distinct columns for each hourly context slice within the time gap
for i in range((-1 * hour_gap), (hour_gap + 1)):
    df_columns.append('carb_' + str(i))
    df_columns.append('bolus_' + str(i))
    df_columns.append('basal_' + str(i))
    df_columns.append('BG_' + str(i))

dfs = []

for filename in filenames:
    print(filename)
    main_df = pd.DataFrame(columns=df_columns)
    tables = get_tables(filename=filename, batch_size=batch_size)
    trimmed_tables = trim_tables(tables)

    for table in trimmed_tables:
        indices = get_bolus_indices(table, bolus_row_index)
        for index in indices:
            row = index_to_bolus_event(table, index)
            main_df = main_df.append(row, ignore_index=True)

    dfs.append(main_df)

# Concatenate all data into one DataFrame
big_frame = pd.concat(dfs, ignore_index=True)
big_frame.to_csv(output_csv, index=False)
