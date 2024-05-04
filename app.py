import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
from src.components.configuration_app import Configuration_App
from src.components.app_status import App_Status
from src.components.algorithm_status import Algorithm_Status
import src.components.components as comp

# APP STATE
configuration_App = Configuration_App()
app_Status = App_Status()
algorithm_Status = Algorithm_Status()

# MAIN APP
app = ctk.CTk()

# APP CONFIGURATION
# To position the window in the center
wtotal = app.winfo_screenwidth()
htotal = app.winfo_screenheight()
pwidth = round(((wtotal-configuration_App.APP_WIDTH)/2) - 90)
pheight = round(((htotal-configuration_App.APP_HEIGHT)/2) - 65)

app.geometry(f"{configuration_App.APP_WIDTH}x{
             configuration_App.APP_HEIGHT}+{pwidth}+{pheight}")
app.resizable(0, 0)
app.title("PROCESAMIENTO DE IMÁGENES MÉDICAS")
app.configure(fg_color=configuration_App.BACKGROUND_COLOR)
app.iconbitmap("src/icons/icon.ico")

###########################################################################
#                           VARIABLES DE CONTROL                          #
###########################################################################
canvas_slider_variable = tk.IntVar(value=0)
option_menu_view_type_variable = tk.StringVar(value="coronal")
slider_umbralizacion_tau = tk.IntVar(value=0)
slider_tolerancia_regiones_var = tk.IntVar(value=0)
slider_iteraciones_regiones_var = tk.IntVar(value=0)
slider_iteraciones_k_means_var = tk.IntVar(value=0)
slider_umbralizacion_delta_tau = tk.DoubleVar(value=0)


###########################################################################
#                     FUNCIONES PARA CONTROL DE FLUJO                     #
###########################################################################


def upload_image():
    file_url = tk.filedialog.askopenfilename()

    if file_url:
        # Procesar el archivo
        x, y, z, img = algorithm_Status.upload_img_nii(file_url)
        app_Status.set_app_img_main(img)
        app_Status.set_canvas_size_x_y_z(x, y, z)
        container_img_upload_nii.hide_frame()
        main_view_edition_nii.show_frame_custom()
        algorithm_Status.reset_annotated_array()
        canvas_like_label.modify(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(
        ), app_Status.get_app_img_main(), 'coronal', 0, app_Status.get_draw(), canvas_draw.get_canvas(), app_Status, canvas_slider.get_slider())
    else:
        print("No se seleccionó ningún archivo")


def updateImageView():
    if app_Status.get_draw():
        canvas_like_label.modify(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(
        ), app_Status.get_app_img_main(), option_menu_view_type_variable.get(), int(canvas_slider_variable.get()), app_Status.get_draw(), canvas_draw.get_canvas(), app_Status, canvas_slider.get_slider())
    else:
        canvas_like_label.modify(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(), app_Status.get_app_img_main(
        ), option_menu_view_type_variable.get(), int(canvas_slider_variable.get()), app_Status.get_draw(), canvas_draw.get_canvas(), app_Status, canvas_slider.get_slider())


def draw_on_img():
    if app_Status.get_draw() == True:
        canvas_like_label.hide_label()
        canvas_label_slider.hide_label()
        canvas_slider.hide_slider()
        button_select_edition_mode.hide_button()
        button_save_annotations.hide_button()
        canvas_draw.show_canvas()
        canvas_label_slider.show_label()
        canvas_slider.show_slider()
        button_select_edition_mode.show_button()
        canvas_like_label.modify(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(), app_Status.get_app_img_main(
        ), option_menu_view_type_variable.get(), int(canvas_slider_variable.get()), app_Status.get_draw(), canvas_draw.get_canvas(), app_Status, canvas_slider.get_slider())
        button_save_annotations.show_button()
    elif app_Status.get_draw() == False:
        canvas_draw.hide_canvas()
        canvas_label_slider.hide_label()
        canvas_slider.hide_slider()
        button_select_edition_mode.hide_button()
        button_save_annotations.hide_button()
        canvas_like_label.show_label()
        canvas_label_slider.show_label()
        canvas_slider.show_slider()
        button_select_edition_mode.show_button()

# APP VIEW


###########################################################################
#                                SIDEBAR                                  #
###########################################################################
# Main container
sidebar = comp.Frame(
    ctk, app, configuration_App.SIDEBAR_WITDH, configuration_App.APP_HEIGHT, 'transparent')
sidebar.show_sidebar()

# SECTION 1: START
# Logo
logo = comp.Frame(ctk, sidebar.get_frame(), 70, 70, '#ffffff')
logo.show_frame()

# Logo image
img_logo = Image.open("src/icons/logo.png")
img_logo_upload = comp.Image_Upload(ctk, img_logo, 50, 50)
label_img_logo = comp.Label_Image(
    ctk, logo.get_frame(), "", img_logo_upload.get_image(), width=500, height=1000)
label_img_logo.show_label()

# Start button
img_btn_start = Image.open("src/icons/home.png")
img_btn_start_upload = comp.Image_Upload(ctk, img_btn_start, 20, 20)
btn_start = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Start", img_btn_start_upload.get_image(
), '#090909', '#0C5EF7', None, 0, 5, [0, 0], [60, 0])
btn_start.show_button()

# SECTION 2: SEGMENTATION
# Segmentation button
img_btn_segmentation = Image.open('src/icons/seg.png')
img_btn_segmentation_upload = comp.Image_Upload(
    ctk, img_btn_segmentation, 20, 20)
btn_segmentation = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Segmentation", img_btn_segmentation_upload.get_image(
), '#090909', '#0C5EF7', None, 0, 5, [0, 0], [20, 0])
btn_segmentation.show_button()

# SUB-SECTION
img_btn_sub_section = Image.open('src/icons/arrow.png')
img_btn_sub_section_upload = comp.Image_Upload(
    ctk, img_btn_sub_section, 12, 12)

# Thresholding button
btn_segmentation_thresholding = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Thresholding", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', None, 0, 5, [20, 0], [10, 0])
btn_segmentation_thresholding.show_button()

# Region growing button
btn_segmentation_region_growing = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Region growing", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', None, 0, 5, [20, 0], [10, 0])
btn_segmentation_region_growing.show_button()

# Region k means
btn_segmentation_k_means = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Region growing", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', None, 0, 5, [20, 0], [10, 0])
btn_segmentation_k_means.show_button()


###########################################################################
#                                MAIN VIEW                                #
###########################################################################
# Main container
main_view = comp.Frame(ctk, app, configuration_App.get_main_view_width(
), configuration_App.APP_HEIGHT, '#ffffff')
main_view.show_frame_custom()

# Upload .nii image
img_upload_nii = Image.open('src/icons/upload.png')
img_upload_nii_upload = comp.Image_Upload(ctk, img_upload_nii, 50, 50)
container_img_upload_nii = comp.Frame(ctk, main_view.get_frame(
), configuration_App.get_main_view_width(), configuration_App.APP_HEIGHT, 'transparent')
container_img_upload_nii.show_frame_custom()

# Show and edit .nii images
main_view_edition_nii = comp.Frame(ctk, main_view.get_frame(
), configuration_App.get_main_view_width(), configuration_App.APP_HEIGHT, 'transparent')

# Button that upload .nii images
btn_upload_nii = comp.Button_Upload(ctk, container_img_upload_nii.get_frame(
), "Upload image", img_upload_nii_upload.get_image(), '#0C5EF7', '#5992FC', upload_image, 0, 0, [0, 0], [390, 0], 100, 100, 'top')
btn_upload_nii.show_button()

# Options menu for view type


def select_view_type():
    updateImageView()


option_menu_view_type = comp.Option_Menu(ctk, main_view_edition_nii.get_frame(), [
                                         "coronal", "sagital", "axial"], option_menu_view_type_variable, select_view_type)
option_menu_view_type.show_option_menu()

# Canvas like a label
canvas_like_label = comp.Label_Canvas(
    ctk, main_view_edition_nii.get_frame(), "", 200, 200)
canvas_like_label.show_label()

# Slider to change frames on the canvas
canvas_label_slider = comp.Label_Text_Slider(
    ctk, main_view_edition_nii.get_frame(), '0', 40)
canvas_label_slider.show_label()


def canvas_slider_event(value):
    canvas_label_slider.set_value_label(value)
    updateImageView()


canvas_slider = comp.Slider(ctk, main_view_edition_nii.get_frame(
), 0, 100, canvas_slider_event, canvas_slider_variable)
canvas_slider.show_slider()

# Canvas to draw
canvas_draw = comp.Canvas(
    tk, main_view_edition_nii.get_frame(), 200, 200, option_menu_view_type_variable, app_Status, algorithm_Status)

# Select edition mode


def select_edition_mode():
    app_Status.set_draw(not app_Status.get_draw())
    if app_Status.get_draw():
        button_select_edition_mode.get_button().configure(text="View only")
    else:
        button_select_edition_mode.get_button().configure(text="Draw on the image")

    draw_on_img()


button_select_edition_mode = comp.Button(ctk, main_view_edition_nii.get_frame(
), 'Draw on the image', 300, select_edition_mode)
button_select_edition_mode.show_button()

button_save_annotations = comp.Button(ctk, main_view_edition_nii.get_frame(
), 'Save annotations to new .nii file', 300, algorithm_Status.export_annotations)
button_save_annotations.show_button()


###########################################################################
#                                MAIN LOOP                                #
###########################################################################
app.mainloop()
