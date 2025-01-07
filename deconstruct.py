import argparse
from extract import slice_image
import os
from helper import Helper, DEFAULT_PATH
from tqdm import tqdm

def extract_all_parts(helper, file, atlas_info, output_dir, resize, compress_level):
    # Create a subdirectory within the output directory based on the parent file name
    parent_file_name = os.path.splitext(os.path.basename(file))[0]
    output_subdir = os.path.join(output_dir, parent_file_name)
    os.makedirs(output_subdir, exist_ok=True)
    
    # Print the number of assets and their names
    asset_names = list(atlas_info.keys())
    print(f"Number of assets to extract: {len(asset_names)}")
    print("Assets to extract:")
    for name in asset_names:
        print(f" - {name}")
    
    # Use tqdm to display a progress bar
    with tqdm(total=len(asset_names), desc="Extracting parts", unit="part") as pbar:
        for part_name, coords in atlas_info.items():
            left, right, top, bottom = coords[3], coords[4], coords[5], coords[6]
            input_file = os.path.join(DEFAULT_PATH, file)
            if not input_file.endswith(".blp"):
                input_file += ".blp"
            output_file = os.path.join(output_subdir, f"{part_name}.png")
            if not os.path.exists(output_file):
                slice_image(input_file, output_file, left, right, top, bottom, resize, compress_level, silent=True)
                pbar.set_postfix_str(f"Processed {part_name}")
            else:
                pbar.set_postfix_str(f"Skipped {part_name}")
            pbar.update(1)

def main():
    parser = argparse.ArgumentParser(description="Deconstruct an asset from a BLP image using coordinates from a Lua table.")
    parser.add_argument("identifier", help="Atlas name or file path to look up in the Lua table.")
    parser.add_argument("--info", help="Path to the Lua file containing the atlas info. If not provided, it will be downloaded and cached.")
    parser.add_argument("--download", action="store_true", help="Force redownload of the AtlasInfo.lua file.")
    parser.add_argument("--resize", action="store_true", help="Resize the output images to the nearest power of 2.")
    parser.add_argument("--path", help="Directory where the exported art files are located.", default=DEFAULT_PATH)
    parser.add_argument("--output-dir", help="Directory to save the extracted parts.", default="output")
    parser.add_argument("--compress-level", type=int, default=9, help="Compression level for saving PNG files (0-9).")

    args = parser.parse_args()

    helper = Helper(lua_file=args.info, download=args.download)

    if os.path.isfile(args.identifier):
        file = os.path.relpath(args.identifier, args.path)
        print(f"Looking for file: {file}")
        atlas_info = helper.find_file_by_name(file)
        if atlas_info:
            extract_all_parts(helper, file, atlas_info, args.output_dir, args.resize, args.compress_level)
        else:
            print(f'File {args.identifier} not found in the Lua table')
    else:
        file = helper.find_file_by_atlas_name(args.identifier)
        if file:
            print(f'Found atlas {args.identifier} in file {file}')
            atlas_info = helper.find_file_by_name(file)
            if atlas_info:
                extract_all_parts(helper, file, atlas_info, args.output_dir, args.resize, args.compress_level)
            else:
                print(f'File {file} not found in the Lua table')
        else:
            print(f'Atlas name {args.identifier} not found in the Lua table')

if __name__ == "__main__":
    main()