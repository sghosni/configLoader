from .accessor import ConfigAccessor


class ConfigContainer:
    def __init__(self, configs: ConfigAccessor):
        self.configs = configs

    def to_dict(self):
        return self.configs.to_dict()
