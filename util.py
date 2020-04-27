import csv
import json
import logging
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, List, Optional, Union

from PIL import Image

log: logging.Logger = logging.getLogger(__name__)


class Utility:
    """
    Class containing utilitarian functions intended to reduce duplicate
    code.
    """

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
        **kwargs,
    ) -> bool:
        """Write the contents of the specified file."""

        try:
            with open(
                f"{directory}{filename}.{extension}", "w+", encoding="utf-8"
            ) as file:
                if extension == "json":
                    if kwargs.get("compress") is True:
                        file.write(json.dumps(contents, ensure_ascii=False))
                    else:
                        file.write(json.dumps(contents, indent=4, ensure_ascii=False))
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
        """
        Remove all Call of Duty font color codes from the provided string.
        """

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

    def SortList(self: Any, array: List[dict], key: str) -> List[dict]:
        """
        Alphabetically sort the provided list of dicts by the specified key.
        Null values are placed at the end of the list.
        """

        sort: List[dict] = sorted(array, key=lambda k: (k[key] is None, k[key]))

        return sort

    def CheckExists(self: Any, directory: str, filename: str, extension: str) -> bool:
        """
        Return a boolean value indicating whether or not the specified
        file exists.
        """

        if Path(f"{directory}{filename}.{extension}").is_file():
            return True

        return False

    def AnimateSprite(
        self: Any,
        directory: str,
        filename: str,
        extension: str,
        itemType: str,
        output: bool,
    ) -> bool:
        """Animate the provided Spritesheet into a WEBM video."""

        # TODO: Move title-specific logic to its corresponding class
        if itemType == "Calling Card":
            trueWidth: int = 512
            trueHeight: int = 128
        elif itemType == "Emblem":
            trueWidth: int = 256
            trueHeight: int = 256
        else:
            return False

        with Image.open(f"{directory}/{filename}.{extension}") as file:
            width, height = file.size

            if (width == trueWidth) and (height == trueHeight):
                return False

            if output is True:
                columns: int = width // trueWidth
                rows: int = height // trueHeight

                Path("tmp/").mkdir()

                i: int = 1
                for row in range(0, rows):
                    for column in range(0, columns):
                        frame = file.crop(
                            (
                                column * trueWidth,
                                row * trueHeight,
                                (column + 1) * trueWidth,
                                (row + 1) * trueHeight,
                            )
                        )
                        frame.save(f"tmp/{i:03}.png")

                        if i == 1:
                            frame.save(f"export/Modern Warfare/Images/{filename}.png")

                        i += 1

                subprocess.call(
                    [
                        "ffmpeg",
                        "-framerate",
                        "10",
                        "-i",
                        "tmp/%03d.png",
                        "-y",
                        f"export/Modern Warfare/DB/Videos/{filename}.webm",
                    ],
                    stderr=subprocess.DEVNULL,
                )

                shutil.rmtree("tmp/")

            return True

    def Sluggify(self: Any, input: str) -> str:
        """ToDo"""

        # Compile regex patterns
        invalids: re.Pattern[str] = re.compile(r"[^a-z0-9\s-]")
        hypens: re.Pattern[str] = re.compile(r"\s")
        doubleHypens: re.Pattern[str] = re.compile(r"-{2,}")

        # Remove invalid characters, lowercase string
        output: str = re.sub(invalids, "", input.lower())

        # Replace spaces with hypens
        output: str = re.sub(hypens, "-", output)

        # Replace double hyphens with single hyphens
        output: str = re.sub(doubleHypens, "-", output)

        # Truncate slug to 45 characters
        return output[:45]
