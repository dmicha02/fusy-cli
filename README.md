# fusy-cli

Tool for pdf merge, split or pages extraction

## Installation

`pip install -r requirements.txt`

## Usage

**_Vanilla Way :_**

For merging:
`python fusy.py -m merge -f "file1.pdf" "file2.pdf" -o "merged.pdf"`

For splitting (-s for the number of starting page and -e for the ending page):
`python fusy.py -m split -f "file.pdf" -o "splitted" -s 2 -e 4`

For page extraction (-p is for the wanted pages):
`python fusy.py -m extract -f "file.pdf" -o "extracted.pdf" -p "1,4-6,8,10"`

**_Wizard Way :_**

The wizard is not implemented yet but it will permit to assist you to use the cli by asking you questions step by step.

**_GUI :_**

`python fusy_gui.py`

## TODO

[] Wizard mode

[] Improve doc

[] CI/CD

[x] GUI

## Miscellaneous

This tool is constructed on top of PyPDF2 python package.

I use some AI model to construct quickly the GUI (mainly by Claude 3.7 Sonnet).
I made this choice because I prefer to use CLI but I would like to offer the feature for others without spend a lot of time on cosmetic details.
