import csv

ERROR_SOLUTIONS = {}

with open(
    "error_solutions.csv",
    mode="r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        category = row["category"].strip()
        resolution = row["resolution"].strip()

        ERROR_SOLUTIONS[category] = resolution


DEFAULT_RESOLUTION = (
    "Review the error details and contact system support if the issue persists."
)