import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
        "--slot",
        default=None,
    )
args = parser.parse_args()
print(args.slot)