import os
import argparse 
from PyPDF2 import PdfMerger
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(input_files, output_file):
    """Merge multiple PDF files into a single PDF file."""
    merger = PdfMerger()

    for pdf in input_files:
        merger.append(pdf)

    merger.write(output_file+".pdf")
    merger.close()
    print(f"Merged {len(input_files)} PDFs into {output_file}.")

def split_pdf(input_file, start_page, end_page, output_file):
    """Split a PDF file into pages."""

    reader = PdfReader(input_file)
    

    for page in range(start_page - 1, end_page):
        writer = PdfWriter()
        writer.add_page(reader.pages[page])

        with open(output_file+"_"+str(page)+".pdf", "wb") as f:
            writer.write(f)
        writer.close()
    print(f"Split {input_file} from page {start_page} to {end_page} into {output_file}.")

def parse_page_ranges(page_ranges):
    """Parse a string of page ranges into a list of integers."""
    pages = set()
    ranges = page_ranges.split(',')
    for r in ranges:
        if '-' in r:
            start, end = map(int, r.split('-'))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(r))
    return sorted(pages)

def extract_pages(input_file, pages, output_file):
    """Extract specific pages from a PDF file."""

    reader = PdfReader(input_file)
    writer = PdfWriter()
    
    pages = parse_page_ranges(pages)
    for page in pages:
        writer.add_page(reader.pages[page - 1])

    with open(output_file+".pdf", "wb") as f:
        writer.write(f)
        
    print(f"Extracted pages {pages} from {input_file} into {output_file}.")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Fusy: A CLI for pdf manipulation.")
    argparser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    # argparser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
    argparser.add_argument("-w", "--wizard", action="store_true", help="Run the wizard for interactive mode.")
    # argparser.add_argument("-i", "--input", help="The input file to process.", required=True)
    argparser.add_argument("-o", "--output", help="The output file to save results.")
    argparser.add_argument("-p", "--pages", help="The pages to extract.", type=str)
    argparser.add_argument("-s", "--start", help="The start page for splitting.", type=int)
    argparser.add_argument("-e", "--end", help="The end page for splitting.", type=int)
    argparser.add_argument("-f", "--files", help="The files to merge.", nargs='+')
    argparser.add_argument("-m", "--mode", help="The mode of operation.", choices=["merge", "split", "extract"])

    args = argparser.parse_args()

    # args.input = os.path.abspath(args.input) if args.input else None
    args.output = os.path.abspath(args.output) if args.output else None
    args.files = [os.path.abspath(f) for f in args.files] if args.files else None
    args.pages = args.pages if args.pages else None
    args.start = int(args.start) if args.start else None
    args.end = int(args.end) if args.end else None
    args.mode = args.mode if args.mode else None
    args.wizard = args.wizard if args.wizard else False

    # Print the arguments for debugging purposes
    print("Arguments:")
    # print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Files: {args.files}")
    print(f"Pages: {args.pages}")
    print(f"Start: {args.start}")
    print(f"End: {args.end}")
    print(f"Mode: {args.mode}")
    print(f"Wizard: {args.wizard}")
    # Call the appropriate function based on the mode
    if args.wizard:
        print("Running in wizard mode...")
        # Add your wizard code here
        pass  # Placeholder for wizard functionality
    else:
        print("CLI mode...")
        if args.mode == "merge":
            if not args.files : raise ValueError("No files provided for merging.")
            if not args.output: raise ValueError("No output file provided for merging.")
            if len(args.files) < 2: raise ValueError("At least two files are required for merging.")
            if args.output.endswith(".pdf"): args.output = args.output[:-4]
            merge_pdfs(args.files, args.output)
        elif args.mode == "split":
            if not args.files: raise ValueError("No input file provided for splitting.")
            if not args.start: raise ValueError("No start page provided for splitting.")
            if not args.end: raise ValueError("No end page provided for splitting.")
            if not args.output: raise ValueError("No output file provided for splitting.")
            if args.start > args.end: raise ValueError("Start page must be less than end page.")
            if args.start < 1: raise ValueError("Start page must be greater than 0.")
            if args.end < 1: raise ValueError("End page must be greater than 0.")
            if args.start == args.end: raise ValueError("Start page and end page must be different.")
            input_file = args.files[0]
            if args.end > len(PdfReader(input_file).pages): raise ValueError("End page exceeds the number of pages in the PDF.")
            if args.start > len(PdfReader(input_file).pages): raise ValueError("Start page exceeds the number of pages in the PDF.")
            if args.output.endswith(".pdf"): args.output = args.output[:-4]
            split_pdf(input_file, args.start, args.end, args.output)
        elif args.mode == "extract":
            if not args.files: raise ValueError("No input file provided for extraction.")
            if not args.pages: raise ValueError("No pages provided for extraction.")
            if not args.output: raise ValueError("No output file provided for extraction.")
            if args.output.endswith(".pdf"): args.output = args.output[:-4]
            input_file = args.files[0]
            extract_pages(input_file, args.pages, args.output)
        else:
            raise ValueError("Invalid mode. Use -h for help.")