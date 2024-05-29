from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import tkinter as tk


class Frame:
    def __init__(self, ctk, master, width, height, fg_color, padx = 20, process_name = 'none'):
        self.padx= padx
        self.process_name = process_name
        self.frame = ctk.CTkFrame(master=master, width=width, height=height,
                                  fg_color=fg_color, corner_radius=20)
        self.frame.pack_propagate(0)

    def get_frame(self):
        return self.frame
    
    def get_process_name(self):
        return self.process_name
    
    def set_width_frame(self, new_width):
        self.frame.configure(width= new_width)

    def show_frame(self):
        self.frame.pack_propagate(0)
        self.frame.pack()

    def hide_frame(self):
        self.frame.pack_forget()

    def show_frame_custom(self):
        self.frame.pack_propagate(0)
        self.frame.pack(side='left', padx=(self.padx, 20), pady=20)

    def show_sidebar(self):
        self.frame.pack_propagate(0)
        self.frame.pack(fill="y", anchor="w", side="left",
                        padx=(20, 0), pady=20)


class Image_Upload():
    def __init__(self, ctk, img, width, height):
        self.image = ctk.CTkImage(
            dark_image=img, light_image=img, size=(width, height))

    def get_image(self):
        return self.image


class Label_Image:
    def __init__(self, ctk, master, text, image, width, height):
        self.ctk = ctk
        self.master = master
        self.text = text
        self.image = image
        self.width = width
        self.height = height
        self.create_label()

    def create_label(self):
        self.label = self.ctk.CTkLabel(
            master=self.master, text=self.text, image=self.image, width=self.width, height=self.height)

    def get_label(self):
        return self.label

    def show_label(self):
        self.label.pack(anchor="center", padx=10, pady=10)

    def hide_label(self):
        self.label.pack_forget()


class Label_Text_Slider:
    def __init__(self, ctk, master, text, width, pady=10):
        self.ctk = ctk
        self.master = master
        self.text = text
        self.width = width
        self.pady = pady
        self.create_label()

    def create_label(self):
        self.label = self.ctk.CTkLabel(
            master=self.master, text=self.text, fg_color="#0C5EF7", text_color="#ffffff", justify="center", width=self.width, corner_radius=5)

    def get_label(self):
        return self.label

    def set_value_label(self, new_value):
        self.label.configure(text=new_value)

    def show_label(self):
        self.label.pack_propagate(0)
        self.label.pack(pady=(10, self.pady))

    def hide_label(self):
        self.label.pack_forget()

class Label_Simple:
    def __init__(self, ctk, master, text, font_size):
        self.label = ctk.CTkLabel(master, text=text, fg_color="transparent", text_color="#ffffff", justify="center", font=("Arial Bold", font_size))
    
    def get_label(self):
        return self.label
    
    def show_label(self):
        self.label.pack(fill='x', pady=20)


class Label_Canvas:
    def __init__(self, ctk, master, text, width, height):
        self.ctk = ctk
        self.master = master
        self.text = text
        self.width = width
        self.height = height
        self.create_label()

    def create_label(self):
        self.label = self.ctk.CTkLabel(
            master=self.master, text=self.text, width=self.width, height=self.height, fg_color='transparent')

    def get_label(self):
        return self.label

    def show_label(self):
        self.label.pack_propagate(0)
        self.label.pack(anchor="center", padx=10, pady=10)

    def hide_label(self):
        self.label.pack_forget()

    def modify(self, x, y, z, img, plano, deep, draw, canvas, app_status, slider):
        print("Canvas", x, y, z, plano, deep)
        global image_to_show_
        app_status.set_current_depth(deep)
        # Plano XY -> Vista coronal
        # Plano YZ -> Vista sagital
        # Plano XZ -> Vista axial
        if plano == "coronal":
            aux_range1 = y
            aux_range2 = x
            slider.configure(to=z)
            pil_image = Image.fromarray(img[:, :, deep])
        elif plano == "sagital":
            aux_range1 = z
            aux_range2 = y
            slider.configure(to=x)
            pil_image = Image.fromarray(img[deep, :, :])
        elif plano == "axial":
            aux_range1 = z
            aux_range2 = x
            slider.configure(to=y)
            pil_image = Image.fromarray(img[:, deep, :])

        if draw:
            print('Editing')
            canvas.configure(width=aux_range1*2, height=aux_range2*2)
            plt.imsave("src/img_slides/slide.jpeg", pil_image)
            image_to_show = Image.open("src/img_slides/slide.jpeg")
            image_to_show = image_to_show.resize((aux_range1*2, aux_range2*2))
            image_to_show_ = ImageTk.PhotoImage(image_to_show)
            canvas.create_image(0, 0, anchor=tk.NW, image=image_to_show_)
        else:
            print('View only')
            plt.imsave("src/img_slides/slide.jpeg", pil_image)
            image_to_show = Image.open("src/img_slides/slide.jpeg")
            image_to_show_ = self.ctk.CTkImage(
                dark_image=image_to_show, light_image=image_to_show, size=(aux_range1*2, aux_range2*2))
            self.label.configure(image=image_to_show_)


class Button:
    def __init__(self, ctk, master, text, width, func):
        self.button = ctk.CTkButton(master=master, text=text, fg_color="#0C5EF7", font=(
            "Arial Bold", 15), anchor="center", width=width, corner_radius=10, hover_color="#5992FC", command=func)

    def get_button(self):
        return self.button

    def show_button(self):
        self.button.pack(pady=10)
        
    def show_button_custom(self):
        self.button.pack(fill='x', pady=20)
        
    def hide_button(self):
        self.button.pack_forget()


class Button_Sidebar:
    def __init__(self, ctk, master, text, image, fg_color, hover_color, func, i_padx, i_pady, padx, pady):
        self.ctk = ctk
        self.master = master
        self.text = text
        self.image = image
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.func = func
        self.i_padx = i_padx
        self.i_pady = i_pady
        self.padx = padx
        self.pady = pady
        self.create_button()

    def create_button(self):
        self.button = self.ctk.CTkButton(master=self.master, image=self.image, text=self.text, fg_color=self.fg_color, font=(
            "Arial Bold", 14), anchor="w", corner_radius=10, hover_color=self.hover_color, command=self.func)

    def get_button(self):
        return self.button

    def show_button(self):
        self.button.pack(fill="x", ipadx=self.i_padx, ipady=self.i_pady, padx=(
            self.padx[0], self.padx[1]), pady=(self.pady[0], self.pady[1]))

    def hide_button(self):
        self.button.pack_forget()


class Button_Upload:
    def __init__(self, ctk, master, text, image, fg_color, hover_color, func, i_padx, i_pady, padx, pady, width, height, compound):
        self.ctk = ctk
        self.master = master
        self.text = text
        self.image = image
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.func = func
        self.i_padx = i_padx
        self.i_pady = i_pady
        self.padx = padx
        self.pady = pady
        self.width = width
        self.height = height
        self.compound = compound
        self.create_button()

    def create_button(self):
        self.button = self.ctk.CTkButton(master=self.master, image=self.image, text=self.text, fg_color=self.fg_color, font=(
            "Arial Bold", 16), anchor="w", corner_radius=10, hover_color=self.hover_color, command=self.func, width=self.width, height=self.height, compound=self.compound)

    def get_button(self):
        return self.button

    def show_button(self):
        self.button.pack(anchor="center", pady=[self.pady[0], self.pady[1]])

    def hide_button(self):
        self.button.pack_forget()


class Option_Menu:
    def __init__(self, ctk, master, list_values, variable, command):
        self.option_menu = ctk.CTkOptionMenu(
            master, values=list_values, variable=variable, command=command)

    def get_option_menu(self):
        return self.option_menu

    def show_option_menu(self):
        self.option_menu.pack_propagate(0)
        self.option_menu.pack(anchor="center", padx=10, pady=10)

    def hide_option_menu(self):
        self.option_menu.pack_forget()


class Canvas:
    def __init__(self, tk, master, width, height, option_menu, app_status, algorithm_status, color):
        self.canvas = tk.Canvas(master, width=width, height=height)
        self.app_status = app_status
        self.algorithm_status = algorithm_status
        self.option_menu = option_menu
        self.add_actions_canvas()
        self.color = color

    def get_canvas(self):
        return self.canvas
    
    def get_color(self):
        return self.color
    
    def set_color(self, newColor):
        self.color = newColor

    def show_canvas(self):
        self.canvas.pack()

    def hide_canvas(self):
        self.canvas.pack_forget()

    def add_actions_canvas(self):
        self.canvas.bind("<Button-1>", self.draw_line_canvas)
        self.canvas.bind("<B1-Motion>", self.draw_line_canvas)
        self.canvas.bind("<ButtonRelease-1>",
                         self.app_status.reset_coordinates_draw)

    def draw_line_canvas(self, event):
        # Coordenadas actuales del click
        x, y = event.x, event.y
        cord_i = int(y/2)
        cord_j = int(x/2)
        # ANOTACIÓN Y SELECCIÓN DE BOXELES QUE SE GUARDARÁN
        if self.option_menu.get() == "coronal":
            for i in range(10):
                self.algorithm_status.set_annotated_array(
                    cord_i+i, cord_j+i, int(self.app_status.get_current_depth()), self.app_status.get_app_img_main(), self.color)
            for j in range(10):
                self.algorithm_status.set_annotated_array(
                    cord_i-j, cord_j-j, int(self.app_status.get_current_depth()), self.app_status.get_app_img_main(), self.color)
        elif self.option_menu.get() == "sagital":
            for i in range(10):
                self.algorithm_status.set_annotated_array(
                    int(self.app_status.get_current_depth()), cord_i+i, cord_j+i, self.app_status.get_app_img_main(), self.color)
            for j in range(10):
                self.algorithm_status.set_annotated_array(
                    int(self.app_status.get_current_depth()), cord_i-j, cord_j-j, self.app_status.get_app_img_main(), self.color)
        elif self.option_menu.get() == "axial":
            for i in range(10):
                self.algorithm_status.set_annotated_array(
                    cord_i+i, int(self.app_status.get_current_depth()), cord_j-i, self.app_status.get_app_img_main(), self.color)
            for j in range(10):
                self.algorithm_status.set_annotated_array(
                    cord_i-j, int(self.app_status.get_current_depth()), cord_j-j, self.app_status.get_app_img_main(), self.color)

        # Dibujar una línea desde las coordenadas anteriores a las actuales
        if self.app_status.get_draw_x_prev() is not None and self.app_status.get_draw_y_prev() is not None:
            self.canvas.create_line(self.app_status.get_draw_x_prev(
            ), self.app_status.get_draw_y_prev(), x, y, fill=self.color, width=20)

        # Actualizar las coordenadas anteriores
        self.app_status.set_draw_x_prev(x)
        self.app_status.set_draw_y_prev(y)


class Slider:
    def __init__(self, ctk, master, from_, to, command, variable):
        self.slider = ctk.CTkSlider(
            master, from_=from_, to=to, command=command, variable=variable)

    def get_slider(self):
        return self.slider

    def show_slider(self):
        self.slider.set(0)
        self.slider.pack_propagate(0)
        self.slider.pack(pady=30)

    def hide_slider(self):
        self.slider.pack_forget()
