import os
import csv
from agents import function_tool


def read_file(file_path: str) -> str:
    """
    Core file-reading implementation.
    Supports TXT, MD, and CSV files.
    """

    if not file_path:
        return "ERROR: No file path was provided."

    if not os.path.exists(file_path):
        return f"ERROR: File not found: {file_path}"

    if not os.path.isfile(file_path):
        return f"ERROR: Path is not a file: {file_path}"

    extension = os.path.splitext(file_path)[1].lower()

    try:

        # TXT / Markdown
        if extension in [".txt", ".md"]:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            if not content.strip():
                return "The file is empty."

            return (
                f"FILE: {os.path.basename(file_path)}\n"
                f"TYPE: {extension}\n\n"
                f"CONTENT:\n{content}"
            )

        # CSV
        elif extension == ".csv":

            rows = []

            with open(
                file_path,
                "r",
                encoding="utf-8-sig",
                newline=""
            ) as file:

                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    return "ERROR: CSV file does not contain headers."

                for row in reader:
                    rows.append(row)

            if not rows:
                return (
                    f"FILE: {os.path.basename(file_path)}\n"
                    "TYPE: CSV\n"
                    "The CSV file contains headers but no data."
                )

            output = []

            output.append(
                f"FILE: {os.path.basename(file_path)}"
            )

            output.append("TYPE: CSV")

            output.append(
                f"ROWS: {len(rows)}"
            )

            output.append(
                f"COLUMNS: {', '.join(reader.fieldnames)}"
            )

            output.append("\nDATA:")

            for index, row in enumerate(rows, start=1):

                output.append(
                    f"{index}. {row}"
                )

            return "\n".join(output)

        else:

            return (
                f"ERROR: Unsupported file type '{extension}'. "
                "Supported types: .txt, .md, .csv"
            )

    except UnicodeDecodeError:

        return "ERROR: Could not decode the file as UTF-8."

    except PermissionError:

        return "ERROR: Permission denied while reading the file."

    except Exception as error:

        return f"ERROR: Failed to read file: {str(error)}"


@function_tool
def file_reader(file_path: str) -> str:
    """
    Agent tool for reading TXT, MD, and CSV marketing files.
    """

    return read_file(file_path)