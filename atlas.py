import argparse
from extract import slice_image
import os
from helper import Helper, DEFAULT_PATH

def main():
    parser = argparse.ArgumentParser(description="Extract an asset from a BLP image using coordinates from a Lua table.")
    parser.add_argument("atlas_name", help="Atlas name to look up in the Lua table.")
    parser.add_argument("output_file", nargs='?', help="Path to save the output image file. If not provided, the atlas name will be used with a .png extension.")
    parser.add_argument("--info", help="Path to the Lua file containing the atlas info. If not provided, it will be downloaded and cached.")
    parser.add_argument("--download", action="store_true", help="Force redownload of the AtlasInfo.lua file.")
    parser.add_argument("--resize", action="store_true", help="Resize the output image to the nearest power of 2.")
    parser.add_argument("--path", help="Directory where the exported art files are located.", default=DEFAULT_PATH)
    parser.add_argument("--same-dir", action="store_true", help="Export the output file to the same directory where the input file came from.")

    args = parser.parse_args()

    helper = Helper(lua_file=args.info, download=args.download)
    file, coords = helper.find_atlas_info(args.atlas_name)

    if file and coords:
        left, right, top, bottom = coords[3], coords[4], coords[5], coords[6]
        print(f'Found atlas {args.atlas_name} in file {file} with coordinates: {left}, {right}, {top}, {bottom}')
        input_file = os.path.join(args.path, file)  # Use the actual file path from the Lua table with optional prefix
        if not input_file.endswith(".blp"):
            input_file += ".blp"
        if args.same_dir:
            output_file = os.path.join(os.path.dirname(input_file), f"{args.atlas_name}.png")
        else:
            output_file = args.output_file if args.output_file else f"{args.atlas_name}.png"
        slice_image(input_file, output_file, left, right, top, bottom, args.resize)
        print(f'Asset {args.atlas_name} extracted to {output_file}')
    else:
        print(f'Atlas name {args.atlas_name} not found in the Lua table')

if __name__ == "__main__":
    main()