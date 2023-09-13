import argparse
import os

from splitter import split_file

def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError("%s is not a positive integer" % value)
    return ivalue

def bool_type(value):
    if value == True:
        return True
    if value == False:
        return False
    if isinstance(value, str):
        value = value.lower()
    elif isinstance(value, (int, float)):
        value = int(value)
        return value == 1
    else:
        raise ValueError(f"Unknown value type: {type(value)}")
    
    return value in ["true", "1", "y", "yes"]

def silence_type(value):
    try:
        value = int(value)
        if value == 1:
            return True
        return positive_int(value)
    except ValueError:
        b = bool_type(value)
        return b if b else 250

def main():
    parser = argparse.ArgumentParser(description='Process audio files.')
    
    parser.add_argument('path', nargs='+', default=None, help='Path to a folder or an audio file')
    parser.add_argument('-r', '--recurse-depth', type=positive_int, default=1, help='Folder recurse depth if Path was a folder (default: No recurse)')
    parser.add_argument('-t', '--threshold', type=int, default=-25, help='Decibel threshold (default: -25)')
    parser.add_argument('-m', '--mode', choices=['large', 'small'], default='large', help='Mode (default: large)')
    parser.add_argument('-d', '--min-duration', type=positive_int, default=210000, help='Minimum duration in milliseconds (default: 21000)')
    parser.add_argument('-x', '--max-duration', type=positive_int, default=240000, help='Maximum duration in milliseconds (default: 24000)')
    parser.add_argument('-s', '--min-silence-length', type=positive_int, default=500, help='Minimum silence length in milliseconds (default: 500)')
    parser.add_argument('-k', '--keep-silence', type=silence_type, default=True, help='Keeps silence to maintain original file length.\n\tTrue/true/1/Y/yes keeps all silence.\n\tA Number in milliseconds specifies the amount to keep (useful if file is a chat dialogue)\n\t(default: True, when False, defaults to 250)')
    parser.add_argument('-o', '--output-format', choices=['mp3', 'wav', 'flac', 'ogg'], default="mp3", help='Target output format (default: mp3)')
    

    args = parser.parse_args()
    parse(args)
    
    recurse_depth = args.recurse_depth
    threshold = args.threshold
    mode = args.mode
    min_duration = args.min_duration
    max_duration = args.max_duration
    min_silence_length = args.min_silence_length
    keep_silence = args.keep_silence
    output_format = args.output_format
    files = list(args.paths)
        
    # Add your code logic here to use these variables.
    print("Files:", files)
    print("Recurse Depth:", recurse_depth)
    print("Threshold:", threshold)
    print("Mode:", mode)
    print("Minimum Duration:", min_duration)
    print("Maximum Duration:", max_duration)
    print("Minimum Silence Length:", min_silence_length)
    print("Keep Silence:", keep_silence)
    print("Output Format:", output_format)
    
    for file_path in files:
        print("Loading", file_path)
        split_file(file_path, output_format, mode, min_duration, max_duration, threshold, min_silence_length, keep_silence)

        
    
def parse(args):
    args.paths = parse_folders(args.path, args.recurse_depth)

def parse_folders(file_list, recurse_depth):
    def _parse_recursive(folder, depth):
        if depth <= 0:
            return
        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            if os.path.isfile(item_path):
                yield item_path
            elif os.path.isdir(item_path):
                yield from _parse_recursive(item_path, depth - 1)
            else:
                raise Exception(f"No such file: {item}")
    
    for item in file_list:
        if os.path.isfile(item):
            yield item
        elif os.path.isdir(item):
            yield from _parse_recursive(item, recurse_depth)
        else:
            raise Exception(f"No such file: {item}")
    
if __name__ == '__main__':
    main()
