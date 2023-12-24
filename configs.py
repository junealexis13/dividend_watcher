import toml, os, re, glob

class TOML:
    def __init__(self) -> None:
        self.working_path = os.getcwd()
        self.conf_toml = glob.glob(os.path.join(self.working_path,"conf.toml"))

    def config_load(self) -> dict:
        config_data = toml.load(self.conf_toml)
        return config_data
    
    def get_stockpicks(self) -> str:
        return self.config_load()['stockPicks']