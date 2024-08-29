import json
import os

class Config:
    datatableKey: str
    fumenKey: str

    def __init__(self) -> None:
        # Define the directory and file paths
        self.appdata_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'KeifunsDatatableEditor') #type: ignore
        self.config_file_path = os.path.join(self.appdata_dir, 'config.json')

        # Create the directory if it doesn't exist
        if not os.path.exists(self.appdata_dir):
            os.makedirs(self.appdata_dir)

        # Default configuration
        default_config = {
            "datatableKey": "",
            "fumenKey": "",
        }

        # Create the config.json file if it doesn't exist
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'w') as config_file:
                json.dump(default_config, config_file, indent=4)

        # Load the configuration from the file
        with open(self.config_file_path) as f:
            d = json.load(f)
            self.datatableKey = d['datatableKey']
            self.fumenKey = d['fumenKey']

        # Load the configuration from the file
        with open(self.config_file_path) as f:
            d = json.load(f)
            self.datatableKey = d['datatableKey']
            self.fumenKey = d['fumenKey']

    def update_config(self, datatableKey: str, fumenKey: str) -> None:
        """Update the configuration and save it to the config.json file."""
        # Update the class attributes
        self.datatableKey = datatableKey
        self.fumenKey = fumenKey

        # Update the configuration dictionary
        updated_config = {
            "datatableKey": self.datatableKey,
            "fumenKey": self.fumenKey,
        }

        # Write the updated configuration back to the config.json file
        with open(self.config_file_path, 'w') as config_file:
            json.dump(updated_config, config_file, indent=4)



config: Config = Config()



