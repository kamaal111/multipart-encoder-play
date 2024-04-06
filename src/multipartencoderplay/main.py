import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from requests_toolbelt import MultipartEncoder

file_name = "bitcoin_it.pdf"
content_type = "application/pdf"


@dataclass
class MultipartFile:
    key: str
    name: str
    file_content: bytes
    content_type: Literal["application/pdf", "text/plain"]


def merge_dicts(dict1: dict, dict2: dict):
    return {**dict1, **dict2}


class CustomMultipartEncoder:
    encoded: MultipartEncoder
    files: list[MultipartFile]
    data: dict[str, str]
    separator: str

    def __init__(
        self, files: list[MultipartFile], data: dict[str, str], separator: str
    ):
        files_dict = {}
        for file in files:
            files_dict[file.key] = (file.name, file.file_content, file.content_type)
        self.encoded = MultipartEncoder(merge_dicts(files_dict, data))
        self.files = files
        self.data = data
        self.separator = separator

    def to_string(self):
        return self.__make_encoded_string()

    def __make_encoded_string(self):
        encoded_string = ""
        for file in self.files:
            string_file_content = self.__extract_string_from_file(file)
            encoded_string += (
                (f"{self.boundary}{self.separator}Content-Disposition: form-data; ")
                + f'name="{file.key}"; filename="{file.name}"{self.separator}'
                + f"Content-Type: {file.content_type}{self.separator * 2}"
                + f"{string_file_content}{self.separator * 2}"
            )
        for key, value in self.data.items():
            encoded_string += (
                f"{self.boundary}{self.separator}Content-Disposition: form-data; "
                + f'name="{key}"{self.separator * 2}{value}'
            )
        encoded_string += f"{self.boundary}--{self.separator}"
        return encoded_string.encode()

    def __extract_string_from_file(self, file: MultipartFile):
        match file.content_type:
            case "application/pdf":
                return self.__extract_string_from_pdf(file)
            case "text/plain":
                return self.__extract_string_from_plain_text(file)
            case _:
                raise Exception("Oh no")

    def __extract_string_from_plain_text(self, file: MultipartFile):
        return file.file_content.decode()

    def __extract_string_from_pdf(self, file: MultipartFile):
        return file.file_content

    @property
    def boundary(self):
        return self.encoded.boundary


def main() -> str:
    script_file_path = os.path.realpath(__file__)
    script_file_directory = os.path.dirname(script_file_path)
    file = Path(f"{script_file_directory}/{file_name}")
    data = CustomMultipartEncoder(
        files=[
            MultipartFile(
                key="file",
                name=file_name,
                file_content=file.read_bytes(),
                content_type=content_type,
            )
        ],
        data={"data": "123"},
        separator="\\r\\n",
    )
    return data.to_string()


if __name__ == "__main__":
    print(main())
