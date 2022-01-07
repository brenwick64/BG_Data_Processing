import sys
import argparse
import subprocess
import pathlib
PATH = str(pathlib.Path(__file__).parent.resolve())

# Argparse config
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gap",
                    help="The amount of contextual hours surrounding a single bolus event", type=int)
args = parser.parse_args()


# Runs processes with gap args
def process_data(gap):
    subprocess.run(
        ["python", "create_bolus_events.py", "-g", str(gap)], cwd=PATH+"/Scripts")
    subprocess.run(["python", "prep_bolus_events.py"],
                   cwd=PATH+"/Scripts")


# __SCRIPT START__


# Cheks for required args
if(args.gap == None):
    print("error: arguments: -g, --gap requried (-h for help info)")
    sys.exit()

# Checks gap appropriate value
elif(args.gap > 12 or args.gap < 1):
    print("error: argument -g must be an integer (1-12)")
    sys.exit()


process_data(args.gap)
