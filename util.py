import csv
import json
import logging
from typing import Any, List, Optional, Union

log: logging.Logger = logging.getLogger(__name__)


class Utility:
    """Class containing utilitarian functions intended to reduce duplicate code."""

    def ReadFile(
        self: Any, directory: str, filename: str, extension: str
    ) -> Optional[Union[str, dict, List[List[str]]]]:
        """Read and return the contents of the specified file."""

        try:
            with open(
                f"{directory}{filename}.{extension}", "r", encoding="utf-8"
            ) as file:
                if extension == "json":
                    return json.loads(file.read())
                elif extension == "csv":
                    rows: List[List[str]] = []
                    for row in csv.reader(file):
                        rows.append(row)

                    return rows
                else:
                    return file.read()
        except Exception as e:
            log.error(f"Failed to read file {directory}{filename}.{extension}, {e}")

    def WriteFile(
        self: Any,
        directory: str,
        filename: str,
        extension: str,
        contents: Union[str, dict, list],
    ) -> bool:
        """Write the contents of the specified file."""

        try:
            with open(
                f"{directory}{filename}.{extension}", "w+", encoding="utf-8"
            ) as file:
                if extension == "json":
                    file.write(json.dumps(contents, indent=4))
                else:
                    file.write(contents)

                return True
        except Exception as e:
            log.error(f"Failed to write file {directory}{filename}.{extension}, {e}")

            return False

    def GetRow(
        self: Any, valueA: str, tableB: List[List[str]], columnB: int
    ) -> Optional[List[str]]:
        """Return the row in Table B whose Column B matches the value in Value A."""

        for rowB in tableB:
            if rowB[columnB] == valueA:
                return rowB

    def GetColumn(self: Any, column: str) -> Optional[Union[str, int]]:
        """Return the value of a CSV's column with the correct type."""

        if column == "":
            return None

        try:
            return int(column)
        except ValueError:
            return column

    def StripColors(self: Any, input: str) -> str:
        """Remove all Call of Duty font color codes from the provided string."""

        colors: List[str] = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "*",
            "+",
            ";",
            ".",
            "/",
            "<",
            ">",
        ]
        output: str = input

        for i in colors:
            output: str = output.replace(f"^{i}", "")

        return output

    def FindBetween(self: Any, input: str, start: str, end: str) -> str:
        """Return the text found between two strings."""

        output: str = input.split(start)[1].split(end)[0]

        return output
