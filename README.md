# WoWAtlasExtract

WoWAtlasExtract is a Python script that extracts assets from Blizzard's World of Warcraft interface art files using coordinates from a Lua table. The script downloads atlas info from townlong-yak.com, parses it, and extracts the specified asset from the BLP image. Use together with [TextureAtlasViewer](https://www.curseforge.com/wow/addons/textureatlasviewer), the in-game browser, to find the names of the atlases you want to extract.

## Features

- Download and cache the Lua table containing atlas information.
- Parse the Lua table to find the coordinates of the specified atlas.
- Extract the asset from the BLP image using the coordinates.
- Optionally resize the output image to the nearest power of 2.
- Save the output image to a specified path or the same directory as the input file.
- Use environment variables to set default paths.

## Requirements

- Python 3.8 or higher (probably)
- `requests` library
- `lupa` library
- `Pillow` library
- `python-dotenv` library
- [exported art files](https://warcraft.wiki.gg/wiki/Viewing_Blizzard%27s_interface_code)
- [TextureAtlasViewer](https://www.curseforge.com/wow/addons/textureatlasviewer) (optional addon)

## Installation

1. Clone the repository:

```sh
git clone https://github.com/seblindfors/WoWAtlasExtract.git
cd WoWAtlasExtract
```

2. Create a virtual environment and activate it:

```sh
python3 -m venv venv
source venv/bin/activate
```

3. Install the required libraries:

```sh
pip install -r requirements.txt
```

4. Optionally create a .env file in the project directory with the following content (example for WSL):

```plaintext
WOW_ART_FILES_PATH=/mnt/c/Program Files/World of Warcraft/_retail_/BlizzardInterfaceArt
ATLAS_INFO_GET_URL=https://www.townlong-yak.com/framexml/live/Helix/AtlasInfo.lua/get
```

## Usage

```sh
python3 atlas.py <atlas_name> [output_file] [--info <path_to_lua_file>] [--download] [--resize] [--path <path_to_art_files>] [--same-dir]
```

### Arguments

- `atlas_name`: Atlas name to look up in the Lua table.
- `output_file` (optional): Path to save the output image file. If not provided, the atlas name will be used with a `.png` extension in the current directory.

### Options

- `--info`: Path to the Lua file containing the atlas info. If not provided, it will be downloaded and cached.
- `--download`: Force redownload of the AtlasInfo.lua file.
- `--resize`: Resize the output image to the nearest power of 2. This may no longer be necessary.
- `--path`: Directory where the [exported art files](https://warcraft.wiki.gg/wiki/Viewing_Blizzard%27s_interface_code) are located. Defaults to the value set in the .env file (usually `/mnt/c/Program Files/World of Warcraft/_retail_/BlizzardInterfaceArt` if you're running in WSL with default installation path).
- `--same-dir`: Export the output file to the same directory where the input file came from.

### Example

```sh
python3 atlas.py UI-Achievement-Alert-Background-Mini
```

This command will extract the `UI-Achievement-Alert-Background-Mini` atlas from the specified path and save it as `UI-Achievement-Alert-Background-Mini.png` in the current directory.

## License

I don't care what you do with this.

## Acknowledgements

Thanks to Foxlit (Townlong-Yak) for the atlas info table, I hope this is OK?