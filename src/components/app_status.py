class App_Status:
    def __init__(self):
        self.current_segmentation = "umbralización"
        self.draw = False
        self.current_depth = 0
        self.draw_x_prev = None
        self.draw_y_prev = None
        self.canvas_size_x = 0
        self.canvas_size_y = 0
        self.canvas_size_z = 0
        self.app_img_main = []

    # Getters (accessor methods)
    def get_current_segmentation(self):
        return self.current_segmentation

    def get_draw(self):
        return self.draw

    def get_current_depth(self):
        return self.current_depth

    def get_draw_x_prev(self):
        return self.draw_x_prev

    def get_draw_y_prev(self):
        return self.draw_y_prev

    def get_canvas_size_x(self):
        return self.canvas_size_x

    def get_canvas_size_y(self):
        return self.canvas_size_y

    def get_canvas_size_z(self):
        return self.canvas_size_z

    def get_app_img_main(self):
        return self.app_img_main

    # Setters (mutator methods)
    def set_current_segmentation(self, new_segmentation):
        self.current_segmentation = new_segmentation

    def set_draw(self, new_draw_state):
        self.draw = new_draw_state

    def set_current_depth(self, new_depth):
        self.current_depth = new_depth

    def set_draw_x_prev(self, new_x):
        self.draw_x_prev = new_x

    def set_draw_y_prev(self, new_y):
        self.draw_y_prev = new_y

    def set_canvas_size_x(self, new_size_x):
        self.canvas_size_x = new_size_x

    def set_canvas_size_y(self, new_size_y):
        self.canvas_size_y = new_size_y

    def set_canvas_size_z(self, new_size_z):
        self.canvas_size_z = new_size_z
    
    def set_canvas_size_x_y_z(self, new_size_x, new_size_y, new_size_z):
        self.canvas_size_x = new_size_x
        self.canvas_size_y = new_size_y
        self.canvas_size_z = new_size_z

    def set_app_img_main(self, new_image):
        self.app_img_main = new_image

    def reset_coordinates_draw(self, event):
        self.set_draw_x_prev(None)
        self.set_draw_y_prev(None)