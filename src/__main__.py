from argparse import ArgumentParser
from time import strftime

from file.csv_file import CsvFile
from utils.url import is_valid_url
from utils.aws_s3 import upload_to_s3
from core.extraction_data import ExtractionData
from config.config import config
from utils.file import remove

def validate_args(args) -> None:
    if not args.urls:
        raise SystemExit('Please specify an URL as data source')

    if not args.out:
        raise SystemExit('Please specify an path to export a file')

    for url in args.urls:
        if is_valid_url(url) is False:
            raise SystemExit('Data source should be a URL format')

def get_args():
    parser = ArgumentParser(description='Data extraction args')
    parser.add_argument(
        '-i',
        '--urls',
        help='URLs as data source',
        type=str,
        nargs='+',
        required=True
    )
    parser.add_argument('-o', '--out', help='Output path', required=True)
    parser.add_argument('-e', '--ext', default='csv', help='File extension')

    return parser.parse_args()

def generate_file_name_include_ext(ext: str = 'csv'):
    return f'{strftime("%Y%m%d")}.{ext}'

def main():
    # Step 1: Args
    args = get_args()
    validate_args(args)

    # Step 2: Process
    out_file_path: str = f'{args.out}/{generate_file_name_include_ext()}'
    process = ExtractionData(args.urls[0], out_file_path)
    data: str = process.execute()

    # Step 3: Write file
    file = CsvFile(
        file_name = out_file_path,
        headers = config.CSV_HEADER.split(','),
        data = data
    )
    file.create_file()

    # Step 4: Upload file to s3
    upload_to_s3(out_file_path, args.out, generate_file_name_include_ext())

    # Step 5: Done
    remove(out_file_path)
    SystemExit()

if __name__ == "__main__":
    main()
