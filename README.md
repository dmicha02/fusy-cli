# fusy-cli

CLI for pdf merge, split or pages extraction

## Installation

`pip install -r requirements.txt`

## Usage

For merging:
`python fusy.py -m merge -f "file1.pdf" "file2.pdf" -o "merged.pdf"`

For splitting (-s for the number of starting page and -e for the ending page):
`python fusy.py -m split -f "file.pdf" -o "splitted" -s 2 -e 4`

For page extraction (-p is for the wanted pages):
`python fusy.py -m extract -f "file.pdf" -o "extracted.pdf" -p "1,4-6,8,10"`

## TODO

[] Wizard mode

[] Improve doc

[] CI/CD

