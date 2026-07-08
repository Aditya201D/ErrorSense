import csv

ERROR_KB = {}

DEFAULT_RECORD = {
    "severity": "Medium",
    "module": "General",
    "resolution":
        "Review the error details and contact system support if the issue persists.",
    "next_step":
        "Retry the operation after verifying the request.",
    "documentation":
        "No additional documentation available."
}

with open(
    "error_solutions.csv",
    mode="r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        category = row["category"].strip()

        ERROR_KB[category] = {

            "severity":
                row.get(
                    "severity",
                    DEFAULT_RECORD["severity"]
                ).strip()
                or DEFAULT_RECORD["severity"],

            "module":
                row.get(
                    "module",
                    DEFAULT_RECORD["module"]
                ).strip()
                or DEFAULT_RECORD["module"],

            "resolution":
                row.get(
                    "resolution",
                    DEFAULT_RECORD["resolution"]
                ).strip()
                or DEFAULT_RECORD["resolution"],

            "next_step":
                row.get(
                    "next_step",
                    DEFAULT_RECORD["next_step"]
                ).strip()
                or DEFAULT_RECORD["next_step"],

            "documentation":
                row.get(
                    "documentation",
                    DEFAULT_RECORD["documentation"]
                ).strip()
                or DEFAULT_RECORD["documentation"]

        }