import os
import json
from pathlib import Path

import urllib3

from lib.multipart_encoder import CustomMultipartEncoder, MultipartFile


file_name = "bitcoin_it.pdf"
content_type = "application/pdf"


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
    encoded_data = data.to_string()
    response = urllib3.request(
        method="POST",
        url="http://localhost:3000/file",
        headers={"Content-Type": "application/json"},
        body=json.dumps({"yes": "no"}),
    )
    print("resp", response.data)
    return "success"


if __name__ == "__main__":
    print(main())
