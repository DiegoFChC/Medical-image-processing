class Configuration_App:
    # Constants (no setters needed for constants)
    BACKGROUND_COLOR = '#000000'
    APP_WIDTH = 1600
    APP_HEIGHT = 900
    SIDEBAR_WITDH = 250

    def __init__(self):
        self.main_view_width = 1350 # 1000
        self.help_view_width = 300 # 0

    # Getters (accessor methods)
    def get_main_view_width(self):
        return self.main_view_width

    def get_help_view_width(self):
        return self.help_view_width

    # Setters (mutator methods)
    def set_main_view_width(self, new_value):
        self.main_view_width = new_value

    def set_help_view_width(self, new_value):
        self.help_view_width = new_value
