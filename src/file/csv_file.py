import typing
import csv
import os

from file.file_base import FileBase

class CsvFile(FileBase):
    def __init__(self,
                file_name: str = '',
                headers: typing.List[str] = None,
        data: typing.List[typing.List[str]] = None
    ) -> None:
        FileBase.__init__(self,
                          file_name)
        self.headers = headers
        self.data = data

    def validate_data(self) -> None:
        is_valid = True

        is_valid = len(self.headers) == len(self.data)

        if is_valid is False:
            raise SystemExit('Header does not match with data')

    def create_file(self) -> None:
        path: str = os.path.dirname(self.file_name)
        isExist: bool = os.path.exists(path)

        if not isExist:
            os.makedirs(path)

        with open(self.file_name,
            'w',
            encoding="UTF8",
            newline='',
        ) as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.headers)
            csv_writer.writerows(self.data)

    def read_file(self) -> dict:
        with open(self.file_name, 'r', encoding = 'UTF8') as csvfile:
            csv_reader = csv.reader(csvfile)
            self.headers = next(csv_reader)
            for row in csv_reader:
                self.data .append(row)

        result = {}
        result['header'] = self.headers
        result['rows'] = self.data

        return result
