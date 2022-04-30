import sys
import argparse
import subprocess
import pathlib
PATH = str(pathlib.Path(__file__).parent.resolve())

# Argparse config
parser = argparse.ArgumentParser()
parser.add_argument("-bh", "--beforehours",
                    help="The amount of contextual hours before a bolus event", type=int)
parser.add_argument("-ah", "--afterhours",
                    help="The amount of contextual hours after a bolus event", type=int)
args = parser.parse_args()


# Runs processes with gap args
def process_data(beforehours, afterhours):
    subprocess.run(
        ["python", "create_bolus_events.py", "-bh", str(beforehours), "-ah", str(afterhours)], cwd=PATH+"/Scripts")
    subprocess.run(["python", "prep_bolus_events.py", "-bh", str(beforehours), "-ah", str(afterhours)],
                   cwd=PATH+"/Scripts")


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


process_data(args.beforehours, args.afterhours)
