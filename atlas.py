import argparse
from lupa import LuaRuntime
from extract import slice_image
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CACHE_DIR    = os.path.join(os.path.dirname(__file__), ".cache")
CACHE_FILE   = os.path.join(CACHE_DIR, "AtlasInfo.lua")
ATLAS_URL    = os.getenv("ATLAS_INFO_GET_URL", "https://www.townlong-yak.com/framexml/live/Helix/AtlasInfo.lua/get")
DEFAULT_PATH = os.getenv("WOW_ART_FILES_PATH", "/mnt/c/Program Files/World of Warcraft/_retail_/BlizzardInterfaceArt")

def download_atlas_info(url, destination):
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, 'wb') as file:
        file.write(response.content)

def parse_lua_table(lua_file):
    lua = LuaRuntime(unpack_returned_tuples=True)
    with open(lua_file, 'r') as file:
        lua_content = file.read()
    lua_table = lua.execute(lua_content)
    return lua_table

def find_atlas_info(lua_table, atlas_name):
    for file, full_atlas_info in lua_table.items():
        if atlas_name in full_atlas_info:
            return file, full_atlas_info[atlas_name]
    return None, None

def main():
    parser = argparse.ArgumentParser(description="Extract an asset from a BLP image using coordinates from a Lua table.")
    parser.add_argument("atlas_name", help="Atlas name to look up in the Lua table.")
    parser.add_argument("output_file", nargs='?', help="Path to save the output image file. If not provided, the atlas name will be used with a .png extension.")
    parser.add_argument("--info", help="Path to the Lua file containing the atlas info. If not provided, it will be downloaded and cached.")
    parser.add_argument("--download", action="store_true", help="Force redownload of the AtlasInfo.lua file.")
    parser.add_argument("--resize", action="store_true", help="Resize the output image to the nearest power of 2.")
    parser.add_argument("--path", help="Directory where the exported art files are located (usually /mnt/c/Program Files/World of Warcraft/).", default=DEFAULT_PATH)
    parser.add_argument("--same-dir", action="store_true", help="Export the output file to the same directory where the input file came from.")

    args = parser.parse_args()

    lua_file = args.info
    if not lua_file:
        lua_file = CACHE_FILE
        if not os.path.exists(lua_file) or args.download:
            download_url = ATLAS_URL
            print(f"Downloading AtlasInfo.lua from {download_url}...")
            download_atlas_info(download_url, lua_file)
            print("Download complete.")

    lua_table = parse_lua_table(lua_file)
    file, coords = find_atlas_info(lua_table, args.atlas_name)

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