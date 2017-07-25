class Settings:
    def __init__(self):
        self.cell_colors = {-1: 'white', 1: 'black'}
        self.model_colormap = 'viridis'

    def get_cell_colors(self):
        return self.cell_colors

    def get_model_colormap(self):
        return self.model_colormap

    def set_model_colormap(self, var):
        self.model_colormap = var
