class FileBase:
    def __init__(self, file_name: str = '') -> None:
        self.file_name = file_name

    def validate_data(self) -> None:
        pass

    def create_file(self) -> None:
        pass
