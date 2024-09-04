import json
import os

class Config:
    datatableKey: str
    fumenKey: str
    gameFilesOutDir: str

    def __init__(self) -> None:
        # Define the directory and file paths
        self.appdata_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'KeifunsDatatableEditor') # type: ignore
        self.config_file_path = os.path.join(self.appdata_dir, 'config.json')

        # Create the directory if it doesn't exist
        if not os.path.exists(self.appdata_dir):
            os.makedirs(self.appdata_dir)

        # Default configuration
        default_config = {
            "datatableKey": "",
            "fumenKey": "",
            "gameFilesOutDir": ""
        }

        # Create the config.json file if it doesn't exist
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'w') as config_file:
                json.dump(default_config, config_file, indent=4)

        # Load the configuration from the file
        with open(self.config_file_path) as f:
            d = json.load(f)

        # Check for missing keys and update with defaults if necessary
        updated = False
        if 'datatableKey' not in d:
            d['datatableKey'] = default_config['datatableKey']
            updated = True
        if 'fumenKey' not in d:
            d['fumenKey'] = default_config['fumenKey']
            updated = True
        if 'gameFilesOutDir' not in d:
            d['gameFilesOutDir'] = default_config['gameFilesOutDir']
            updated = True

        # If any updates were made, write back the updated config
        if updated:
            with open(self.config_file_path, 'w') as config_file:
                json.dump(d, config_file, indent=4)

        # Set class attributes
        self.datatableKey = d['datatableKey']
        self.fumenKey = d['fumenKey']
        self.gameFilesOutDir = d['gameFilesOutDir']

    def update_keys(self, datatableKey: str, fumenKey: str) -> None:
        """Update the configuration and save it to the config.json file."""
        # Update the class attributes
        self.datatableKey = datatableKey
        self.fumenKey = fumenKey
        self.write_back_to_json()

    def update_game_files_out_dir(self, game_files_out_dir: str):
        self.gameFilesOutDir = game_files_out_dir
        self.write_back_to_json()
        
    def write_back_to_json(self):
        # Update the configuration dictionary
        updated_config = {
            "datatableKey": self.datatableKey,
            "fumenKey": self.fumenKey,
            "gameFilesOutDir": self.gameFilesOutDir
        }

        # Write the updated configuration back to the config.json file
        with open(self.config_file_path, 'w') as config_file:
            json.dump(updated_config, config_file, indent=4)

# Instantiate and use the Config class
config: Config = Config()
