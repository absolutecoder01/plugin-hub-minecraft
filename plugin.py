class Plugin:
    unique_id = 0

    def __init__(self, name, description):
        self.id = Plugin.unique_id
        self.name = name
        self.description = description
        Plugin.unique_id += 1

    def editPlugin(self, new_name, new_description):
        self.name = new_name
        self.description = new_description
