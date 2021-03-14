from argparse import ArgumentParser
import re

from PIL import Image
import pytesseract

DATE_RE = '\d{2}/\d{2}/\d{2}'
GRAND_TOTAL_RE = '(\s+total:?\s+)(\d+\.\d+)'


def grand_total_at_date(receipt):
    with Image.open(receipt) as image:
        text = pytesseract.image_to_string(image)
        print(text)
        match = re.search(DATE_RE, text)
        date = match.group() if match else 'unknow'

        match = re.search(GRAND_TOTAL_RE, text, re.IGNORECASE)
        grand_total = match.group(2) if match else 0.0

        return grand_total, date


if __name__ == '__main__':
    parser = ArgumentParser('Receipt Digitization arguments')
    parser.add_argument('--receipt', required=True, help='Receipt file path')

    args = parser.parse_args()

    grand_total, date = grand_total_at_date(args.receipt)

    print(f'Spend {grand_total} dollar on {date}')
