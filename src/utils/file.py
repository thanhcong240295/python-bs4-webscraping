import os

def remove(file_path: str) -> None:
    os.unlink(file_path)