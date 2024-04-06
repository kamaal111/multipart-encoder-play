from dataclasses import dataclass
from typing import Literal

from requests_toolbelt import MultipartEncoder


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

    @property
    def boundary(self):
        return self.encoded.boundary

    def to_string(self):
        return self.__make_encoded_string()

    def __make_encoded_string(self):
        encoded_string = ""
        for file in self.files:
            string_file_content = self.__extract_string_from_file(file)
            encoded_string += (
                (self.__make_header())
                + f'name="{file.key}"; filename="{file.name}"{self.separator}'
                + f"Content-Type: {file.content_type}{self.separator * 2}"
                + f"{string_file_content}{self.separator * 2}"
            )
        for key, value in self.data.items():
            encoded_string += (
                f'{self.__make_header()}name="{key}"{self.separator * 2}{value}'
            )
        encoded_string += f"{self.boundary}--{self.separator}"
        return encoded_string.encode()

    def __make_header(self):
        return f"{self.boundary}{self.separator}Content-Disposition: form-data; "

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
