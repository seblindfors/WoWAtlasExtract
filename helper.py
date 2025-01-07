from lupa import LuaRuntime
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CACHE_DIR    = os.path.join(os.path.dirname(__file__), ".cache")
CACHE_FILE   = os.path.join(CACHE_DIR, "AtlasInfo.lua")
ATLAS_URL    = os.getenv("ATLAS_INFO_GET_URL", "https://www.townlong-yak.com/framexml/live/Helix/AtlasInfo.lua/get")
DEFAULT_PATH = os.getenv("WOW_ART_FILES_PATH", "/mnt/c/Program Files/World of Warcraft/_retail_/BlizzardInterfaceArt")

class Helper:
    def __init__(self, lua_file=None, download=False):
        self.lua_file = lua_file or CACHE_FILE
        if not os.path.exists(self.lua_file) or download:
            self.download_atlas_info(ATLAS_URL, self.lua_file)
        self.lua_table = self.parse_lua_table(self.lua_file)
        if self.lua_table is None:
            print("Failed to load Lua table.")
        else:
            print("Lua table loaded successfully.")

    def download_atlas_info(self, url, destination):
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, 'wb') as file:
            file.write(response.content)

    def parse_lua_table(self, lua_file):
        lua = LuaRuntime(unpack_returned_tuples=True)
        with open(lua_file, 'r') as file:
            lua_content = file.read()
        try:
            lua_table = lua.execute(lua_content)
            return lua_table
        except Exception as e:
            print(f"Error parsing Lua table: {e}")
            return None

    def find_atlas_info(self, atlas_name):
        for file, full_atlas_info in self.lua_table.items():
            if atlas_name in full_atlas_info:
                return file, full_atlas_info[atlas_name]
        return None, None
    
    def find_atlas_by_file_name(self, file_name):
        for file, full_atlas_info in self.lua_table.items():
            if file_name in file:
                return full_atlas_info
        return None

    def find_file_by_name(self, file_name):
        for file in self.lua_table.keys():
            if file_name in file:
                return file
        return None

    def find_file_by_atlas_name(self, atlas_name):
        for file, full_atlas_info in self.lua_table.items():
            if atlas_name in full_atlas_info:
                return file
        return None