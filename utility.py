import csv
import json
import logging
import re
import shutil
import subprocess
from datetime import datetime
from glob import glob
from itertools import islice
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union

from PIL import Image

log: logging.Logger = logging.getLogger(__name__)


class Utility:
    """Utilitarian functions intended to reduce duplicate code."""

    def ReadFile(
        self: Any, path: str
    ) -> Optional[Union[Dict[str, Any], List[Any], str]]:
        """Read and return the contents of the specified file."""

        try:
            with open(path, "r", encoding="utf-8") as file:
                if path.rsplit(".")[1] == "json":
                    return json.loads(file.read())
                else:
                    return file.read()
        except Exception as e:
            log.error(f"Failed to read file {path}, {e}")

    def ReadCSV(
        self: Any, path: str, types: TypedDict, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Read and transform a comma separated values (csv) file to a list
        of dictionaries with the desired value types.
        """

        entries: List[Dict[str, Any]] = []
        fields: Dict[str, Any] = types.__annotations__

        try:
            with open(path, "r", encoding="utf-8") as file:
                if skip > 0:
                    file: List[str] = file.readlines()[skip:]

                for row in csv.DictReader(file, fieldnames=list(fields)):
                    entries.append(
                        {
                            key: None
                            if ((v := value) == "") or (v is None)
                            else fields[key](value)
                            for key, value in islice(row.items(), 0, len(list(fields)))
                        }
                    )
        except Exception as e:
            log.error(f"Failed to read file {path}, {e}")

        return entries

    def WriteFile(
        self: Any, path: str, contents: Union[str, dict, list], **kwargs
    ) -> None:
        """Write the contents of the specified file."""

        if Path(dirPath := (path.rsplit("/", 1)[0])).exists() is False:
            Path(dirPath).mkdir(parents=True, exist_ok=True)

        try:
            with open(path, "w+", encoding="utf-8") as file:
                if path.rsplit(".")[1] == "json":
                    if kwargs.get("compress") is True:
                        file.write(json.dumps(contents, ensure_ascii=False))
                    else:
                        file.write(json.dumps(contents, indent=4, ensure_ascii=False))
                else:
                    file.write(contents)
        except Exception as e:
            log.error(f"Failed to write file {path}, {e}")

    def FileExists(self: Any, path: str) -> bool:
        """
        Return a boolean value indicating whether or not the specified
        file exists.
        """

        if Path(path).is_file():
            return True

        return False

    def GetMatchingFiles(
        self: Any,
        path: str,
        fileType: str,
        start: Optional[str],
        end: Optional[str],
        recursive: bool = False,
    ) -> List[str]:
        """
        Return a list of paths to the files in the specified directory
        which match the desired filetype and filename scheme.
        """

        files: List[str] = []

        for file in glob(f"{path}*.{fileType}", recursive=recursive):
            filename: str = file.rsplit("\\")[1].split(".")[0]

            if (start is not None) and (end is None):
                if filename.startswith(start) is False:
                    continue
            elif (start is None) and (end is not None):
                if filename.endswith(end) is False:
                    continue
            elif (start is not None) and (end is not None):
                if (filename.startswith(start) is False) or (
                    filename.endswith(end) is False
                ):
                    continue

            files.append(file)

        return files

    def GetCSVArray(
        self: Any, array: str, type: Any, delimiter: str = "|"
    ) -> List[Any]:
        """
        Transform a comma separated values (csv) array to a list of
        values with the desired value types.
        """

        values: List[Any] = []

        for value in array.split(delimiter):
            values.append(type(value))

        return values

    def GetStringBool(self: Any, value: str) -> Optional[bool]:
        """Determine the proper boolean value for the given string."""

        if value == "TRUE":
            return True
        elif value == "FALSE":
            return False
        elif value == "Y":
            return True
        elif value == "N":
            return False

    def SortList(
        self: Any, array: List[Dict[str, Any]], key: str, **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Alphabetically sort the provided list of dicts by the specified key.
        Null values are placed at the end of the list.
        """

        if (key2 := kwargs.get("key2", key)) is not None:
            sort: List[Dict[str, Any]] = sorted(
                array, key=lambda k: (k[key] is None, k[key], k[key2] is None, k[key2])
            )
        else:
            sort: List[Dict[str, Any]] = sorted(
                array, key=lambda k: (k[key] is None, k[key])
            )

        return sort

    def PrettyTime(self: Any, timestamp: int) -> str:
        """Convert the provided UTC timestamp to a human-readable string."""

        return datetime.utcfromtimestamp(timestamp).strftime("%A, %B %e, %Y %I:%M %p")

    def StripColorCodes(self: Any, input: str) -> str:
        """Remove all Call of Duty color codes from the provided string."""

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

    def Sluggify(self: Any, input: str) -> str:
        """Transform the provided string into a URL-friendly slug."""

        invalids: re.Pattern[str] = re.compile(r"[^a-z0-9\s-]")
        hypens: re.Pattern[str] = re.compile(r"\s")
        doubleHypens: re.Pattern[str] = re.compile(r"-{2,}")

        output: str = re.sub(invalids, "", input.lower())
        output: str = re.sub(hypens, "-", output)
        output: str = re.sub(doubleHypens, "-", output)

        return output[:45]

    def AnimateSprite(
        self: Any, filename: str, dimensions: List[Tuple[int, int]]
    ) -> bool:
        """Animate the provided Spritesheet into a WEBM video."""

        with Image.open(f"{self.iImages}/{filename}.png") as file:
            width, height = file.size

            for dimension in dimensions:
                frameWidth: int = dimension[0]
                frameHeight: int = dimension[1]

                if (width == frameWidth) and (height == frameHeight):
                    return False

                if (width % dimension[0] != 0) or (height % frameHeight != 0):
                    continue

                columns: int = width // frameWidth
                rows: int = height // frameHeight

                if self.config.get("animateImages") is True:
                    Path(f"{self.eImages}/temp/").mkdir(exist_ok=True)

                    i: int = 1

                    for row in range(0, rows):
                        for column in range(0, columns):
                            frame = file.crop(
                                (
                                    column * frameWidth,
                                    row * frameHeight,
                                    (column + 1) * frameWidth,
                                    (row + 1) * frameHeight,
                                )
                            )

                            frame.save(f"{self.eImages}/temp/{filename}_{i:03}.png")

                            if i == 1:
                                frame.save(f"{self.eImages}/{filename}.png")

                            i += 1

                    subprocess.call(
                        [
                            "ffmpeg",
                            "-framerate",
                            "10",
                            "-i",
                            f"{self.eImages}/temp/{filename}_%03d.png",
                            "-y",
                            f"{self.eVideos}/{filename}.webm",
                        ],
                        stderr=subprocess.DEVNULL,
                    )

                    shutil.rmtree(f"{self.eImages}/temp/", ignore_errors=True)

                    return True
