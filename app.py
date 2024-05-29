import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import math
from src.components.configuration_app import Configuration_App
from src.components.app_status import App_Status
from src.components.algorithm_status import Algorithm_Status
import src.components.components as comp
# Algorithms
## Segmentation
from src.algorithms.segmentation.thresholding import thresholding
from src.algorithms.segmentation.region_growing import region_growing
from src.algorithms.segmentation.k_means import k_means
## Intensity standarization
from src.algorithms.intensity_standardization.z_score import z_score
from src.algorithms.intensity_standardization.intensity_rescaling import intensity_rescaling
from src.algorithms.intensity_standardization.white_stripe import white_stripe
from src.algorithms.intensity_standardization.histogram_matching import histogram_matching
## Noise remove
from src.algorithms.noise_removal.mean_filter import mean_filter
from src.algorithms.noise_removal.mean_filter import mean_filter_kernel
from src.algorithms.noise_removal.median_filter import median_filter
## Edges
from src.algorithms.edges.finite_differences import finite_differences
from src.algorithms.edges.centered_differences import centered_differences
## Registration
from src.algorithms.registration.registration import registration
## Laplacian coordinates
from src.algorithms.laplacian_coordinates.laplacian_coordinates import run_laplacian_coordinates

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
# pwidth = round(((wtotal-configuration_App.APP_WIDTH)/2) - 90)
pwidth = round(((wtotal-configuration_App.APP_WIDTH)/2))
# pheight = round(((htotal-configuration_App.APP_HEIGHT)/2) - 65)
pheight = round(((htotal-configuration_App.APP_HEIGHT)/2))

# app.geometry(f"{configuration_App.APP_WIDTH}x{configuration_App.APP_HEIGHT}+{pwidth}+{pheight}")
app.geometry(f"{configuration_App.APP_WIDTH}x{configuration_App.APP_HEIGHT}+{0}+{0}")
app.resizable(0, 0)
app.title("MEDICAL IMAGE PROCESSING")
app.configure(fg_color=configuration_App.BACKGROUND_COLOR)
app.iconbitmap("src/icons/icon.ico")

###########################################################################
#                             CONTROL VARIABLES                           #
###########################################################################
# Canvas
canvas_slider_variable = tk.IntVar(value=0)
option_menu_view_type_variable = tk.StringVar(value="coronal")
option_menu_color_variable = tk.StringVar(value='red')
# Thresholding
var_thresholding_slider_tau = tk.IntVar(value=0)
var_thresholding_slider_delta_tau = tk.DoubleVar(value=0)
# Region Growing
var_region_growing_slider_tolerance = tk.IntVar(value=0)
var_region_growing_slider_iterations = tk.IntVar(value=0)
# K-means
var_k_means_slider_iterations = tk.IntVar(value=0)
# Z-Score
var_z_score_slider_background_intensity = tk.IntVar(value=0)
# White stripe
var_white_stripe_slider_threshold = tk.IntVar(value=0)
# Histogram matching
var_histogram_matching_slider_k = tk.IntVar(value=0)


###########################################################################
#                          FLOW CONTROL FUNCTIONS                         #
###########################################################################

def updateImageView():
    if app_Status.get_draw():
        canvas_like_label.modify(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(
        ), app_Status.get_app_img_main(), option_menu_view_type_variable.get(), int(canvas_slider_variable.get()), app_Status.get_draw(), canvas_draw.get_canvas(), app_Status, canvas_slider.get_slider())
    else:
        canvas_like_label.modify(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(), app_Status.get_app_img_main(
        ), option_menu_view_type_variable.get(), int(canvas_slider_variable.get()), app_Status.get_draw(), canvas_draw.get_canvas(), app_Status, canvas_slider.get_slider())


def upload_image(is_main):
    file_url = tk.filedialog.askopenfilename()

    if file_url:
        if is_main:
            # Procesar el archivo
            x, y, z, img = algorithm_Status.upload_img_nii(file_url)
            app_Status.set_app_img_main(img)
            app_Status.set_canvas_size_x_y_z(x, y, z)
            container_img_upload_nii.hide_frame()
            main_view_edition_nii.show_frame_custom()
            algorithm_Status.reset_annotated_array()
            canvas_like_label.modify(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(), app_Status.get_app_img_main(), 'coronal', 0, app_Status.get_draw(), canvas_draw.get_canvas(), app_Status, canvas_slider.get_slider())
            updateImageView()
            algorithm_Status.set_url_img_main(file_url)
            print('Imagen principal cargada!!!')
        else:
            img = nib.load(file_url)
            img = img.get_fdata()
            algorithm_Status.set_img_secondary(img)
            algorithm_Status.set_url_img_secondary(file_url)
            print('Imagen secundaria cargada!!!')
    else:
        print("No se seleccionó ningún archivo")


def draw_on_img():
    if app_Status.get_draw() == True:
        canvas_like_label.hide_label()
        canvas_label_slider.hide_label()
        canvas_slider.hide_slider()
        button_select_edition_mode.hide_button()
        button_save_annotations.hide_button()
        canvas_draw.show_canvas()
        option_menu_color.show_option_menu()
        canvas_label_slider.show_label()
        canvas_slider.show_slider()
        button_select_edition_mode.show_button()
        canvas_like_label.modify(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(), app_Status.get_app_img_main(
        ), option_menu_view_type_variable.get(), int(canvas_slider_variable.get()), app_Status.get_draw(), canvas_draw.get_canvas(), app_Status, canvas_slider.get_slider())
        button_save_annotations.show_button()
    elif app_Status.get_draw() == False:
        canvas_draw.hide_canvas()
        option_menu_color.hide_option_menu()
        canvas_label_slider.hide_label()
        canvas_slider.hide_slider()
        button_select_edition_mode.hide_button()
        button_save_annotations.hide_button()
        canvas_like_label.show_label()
        canvas_label_slider.show_label()
        canvas_slider.show_slider()
        button_select_edition_mode.show_button()

def activate_upload():

    for process in app_Status.get_process_views():
        process.hide_frame()

    configuration_App.set_main_view_width(1350)
    main_view.set_width_frame(configuration_App.get_main_view_width())
    container_img_upload_nii.set_width_frame(configuration_App.get_main_view_width())
    container_img_upload_nii.show_frame_custom()
    main_view_edition_nii.hide_frame()

def change_page(process_name):
    configuration_App.set_main_view_width(1000)
    main_view.set_width_frame(configuration_App.get_main_view_width())
    container_img_upload_nii.hide_frame()
    main_view.show_frame_custom()

    for process in app_Status.get_process_views():
        if process.get_process_name() == process_name:
            process.show_frame_custom()
        else:
            process.hide_frame()


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
), '#090909', '#0C5EF7', activate_upload, 0, 5, [0, 0], [30, 0])
btn_start.show_button()




# SECTION 2: SEGMENTATION
# Segmentation button
img_btn_segmentation = Image.open('src/icons/split.png')
img_btn_segmentation_upload = comp.Image_Upload(
    ctk, img_btn_segmentation, 20, 20)
btn_segmentation = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Segmentation", img_btn_segmentation_upload.get_image(
), '#090909', '#0C5EF7', lambda: change_page('thresholding'), 0, 5, [0, 0], [20, 0])
btn_segmentation.show_button()

# SUB-SECTION
img_btn_sub_section = Image.open('src/icons/arrow.png')
img_btn_sub_section_upload = comp.Image_Upload(
    ctk, img_btn_sub_section, 12, 12)

# Thresholding button
btn_segmentation_thresholding = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Thresholding", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', lambda: change_page('thresholding'), 0, 5, [20, 0], [10, 0])
btn_segmentation_thresholding.show_button()

# Region growing button
btn_segmentation_region_growing = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Region growing", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', lambda: change_page('region_growing'), 0, 5, [20, 0], [10, 0])
btn_segmentation_region_growing.show_button()

# Region k means
btn_segmentation_k_means = comp.Button_Sidebar(ctk, sidebar.get_frame(), "K-means", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', lambda: change_page('k_means'), 0, 5, [20, 0], [10, 0])
btn_segmentation_k_means.show_button()




# SECTION 3: INTENSITY STANDARIZATION
# Intensity standardization button
img_btn_intensity_standardization = Image.open('src/icons/stand.png')
img_btn_intensity_standardization_upload = comp.Image_Upload(
    ctk, img_btn_intensity_standardization, 20, 20)
btn_intensity_standardization = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Intensity Standardization", img_btn_intensity_standardization_upload.get_image(
), '#090909', '#0C5EF7', lambda: change_page('z_score'), 0, 5, [0, 0], [20, 0])
btn_intensity_standardization.show_button()

# SUB-SECTION

# Z-score button
btn_intensity_standarization_z_score = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Z-Score", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', lambda: change_page('z_score'), 0, 5, [20, 0], [10, 0])
btn_intensity_standarization_z_score.show_button()

# Intensity rescaling button
btn_intensity_standarization_intensity_rescaling = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Intensity Rescaling", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', lambda: change_page('intensity_rescaling'), 0, 5, [20, 0], [10, 0])
btn_intensity_standarization_intensity_rescaling.show_button()

# White stripe button
btn_intensity_standarization_white_stripe = comp.Button_Sidebar(ctk, sidebar.get_frame(), "White Stripe", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', lambda: change_page('white_stripe'), 0, 5, [20, 0], [10, 0])
btn_intensity_standarization_white_stripe.show_button()

# Histogram Matching button
btn_intensity_standarization_histogram_matching = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Histogram Matching", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', lambda: change_page('histogram_matching'), 0, 5, [20, 0], [10, 0])
btn_intensity_standarization_histogram_matching.show_button()




# SECTION 4: NOISE REMOVAL
# Noise removal button
img_btn_noise_removal = Image.open('src/icons/noise.png')
img_btn_noise_removal_upload = comp.Image_Upload(
    ctk, img_btn_noise_removal, 20, 20)
btn_noise_removal = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Noise Removal", img_btn_noise_removal_upload.get_image(
), '#090909', '#0C5EF7', lambda: change_page('mean_filter'), 0, 5, [0, 0], [20, 0])
btn_noise_removal.show_button()

# SUB-SECTION

# Mean filter button
btn_noise_removal_mean_filter = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Mean Filter", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', lambda: change_page('mean_filter'), 0, 5, [20, 0], [10, 0])
btn_noise_removal_mean_filter.show_button()

# Median filter button
btn_noise_removal_median_filter = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Median Filter", img_btn_sub_section_upload.get_image(
), '#090909', '#5992FC', lambda: change_page('median_filter'), 0, 5, [20, 0], [10, 0])
btn_noise_removal_median_filter.show_button()



# SECTION 5: EDGES
# Noise removal button
img_btn_edges = Image.open('src/icons/edges.png')
img_btn_noise_edges = comp.Image_Upload(
    ctk, img_btn_edges, 20, 20)
btn_edges = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Edges", img_btn_noise_edges.get_image(
), '#090909', '#0C5EF7', lambda: change_page('edges'), 0, 5, [0, 0], [20, 0])
btn_edges.show_button()



# SECTION 6: REGISTRATION
# Registration button
img_btn_registration = Image.open('src/icons/registro.png')
img_btn_registration_upload = comp.Image_Upload(
    ctk, img_btn_registration, 20, 20)
btn_registration = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Registration", img_btn_registration_upload.get_image(
), '#090909', '#0C5EF7', lambda: change_page('registration'), 0, 5, [0, 0], [20, 0])
btn_registration.show_button()




# SECTION 7: REGISTRATION
# Laplacian button
img_btn_laplacian = Image.open('src/icons/coordenada.png')
img_btn_laplacian_upload = comp.Image_Upload(
    ctk, img_btn_laplacian, 20, 20)
btn_laplacian = comp.Button_Sidebar(ctk, sidebar.get_frame(), "Laplacian coordinates", img_btn_laplacian_upload.get_image(
), '#090909', '#0C5EF7', lambda: change_page('laplacian_coordinates'), 0, 5, [0, 0], [20, 0])
btn_laplacian.show_button()

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
), "Upload image", img_upload_nii_upload.get_image(), '#0C5EF7', '#5992FC', lambda: upload_image(True), 0, 0, [0, 0], [390, 0], 100, 100, 'top')
btn_upload_nii.show_button()

# Options menu for view type

option_menu_view_type = comp.Option_Menu(ctk, main_view_edition_nii.get_frame(), [
                                         "coronal", "sagital", "axial"], option_menu_view_type_variable, lambda x: updateImageView())
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
    canvas_label_slider.set_value_label(math.floor(value))
    updateImageView()


canvas_slider = comp.Slider(ctk, main_view_edition_nii.get_frame(
), 0, 100, canvas_slider_event, canvas_slider_variable)
canvas_slider.show_slider()

# Canvas to draw
canvas_draw = comp.Canvas(
    tk, main_view_edition_nii.get_frame(), 200, 200, option_menu_view_type_variable, app_Status, algorithm_Status, 'red')

def canvas_change_color():
    print('Cambio de color a:', option_menu_color_variable.get())
    canvas_draw.set_color(option_menu_color_variable.get())

option_menu_color = comp.Option_Menu(ctk, main_view_edition_nii.get_frame(), [
                                         "red", "white"], option_menu_color_variable, lambda x: canvas_change_color())

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
), 'Save annotations to new .nii file', 300, lambda: algorithm_Status.export_annotations(app_Status.get_current_process()))
# button_save_annotations.show_button()




###########################################################################
#                               SIDES VIEWS                               #
###########################################################################

# ------------------------------ Thresholding ------------------------------
side_view_thresholding = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'thresholding')
side_view_thresholding.show_frame_custom()
app_Status.add_process_view(side_view_thresholding)


def segmentation_thresholding():
    tau = int(var_thresholding_slider_tau.get())
    delta_tau = round(var_thresholding_slider_delta_tau.get(), 1)
    new_img = thresholding(tau, delta_tau, algorithm_Status.get_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
thresholding_label_title = comp.Label_Simple(
    ctk, side_view_thresholding.get_frame(), 'THRESHOLDING', 20)
thresholding_label_title.show_label()

# Label initial tau
thresholding_label_tau = comp.Label_Simple(
    ctk, side_view_thresholding.get_frame(), 'Initial Tau', 15)
thresholding_label_tau.show_label()

# Label and slider initial tau
thresholding_label_slider_tau = comp.Label_Text_Slider(
    ctk, side_view_thresholding.get_frame(), '0', 40, 5)
thresholding_label_slider_tau.show_label()

thresholding_slider_tau = comp.Slider(ctk, side_view_thresholding.get_frame(
), 0, 100, lambda value: thresholding_label_slider_tau.set_value_label(int(value)), var_thresholding_slider_tau)
thresholding_slider_tau.show_slider()

# Label tau delta
thresholding_label_tau_delta = comp.Label_Simple(
    ctk, side_view_thresholding.get_frame(), 'Tau Delta', 15)
thresholding_label_tau_delta.show_label()

# Label and slider tau delta
thresholding_label_slider_tau_delta = comp.Label_Text_Slider(
    ctk, side_view_thresholding.get_frame(), '0', 40, 5)
thresholding_label_slider_tau_delta.show_label()

thresholding_slider_tau_delta = comp.Slider(ctk, side_view_thresholding.get_frame(
), 0, 2, lambda value: thresholding_label_slider_tau_delta.set_value_label(round(value, 1)), var_thresholding_slider_delta_tau)
thresholding_slider_tau_delta.show_slider()

# Buttons
thresholding_button_run = comp.Button(ctk, side_view_thresholding.get_frame(), 'Run algorithm', 100, segmentation_thresholding)
thresholding_button_run.show_button_custom()

thresholding_button_save = comp.Button(ctk, side_view_thresholding.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('thresholding'))
thresholding_button_save.show_button_custom()




# -------------------------- Region Growing ------------------------------
side_view_region_growing = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'region_growing')
side_view_region_growing.show_frame_custom()
app_Status.add_process_view(side_view_region_growing)


def segmentation_region_growing():
    tolerance = var_region_growing_slider_tolerance.get()
    starting_point = (100, 25, 125)
    iterations = var_region_growing_slider_iterations.get()
    new_img = region_growing(tolerance, starting_point, iterations, algorithm_Status.get_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
region_growing_label_title = comp.Label_Simple(
    ctk, side_view_region_growing.get_frame(), 'REGION GROWING', 20)
region_growing_label_title.show_label()

# Label tolerance
region_growing_label_tolerance = comp.Label_Simple(
    ctk, side_view_region_growing.get_frame(), 'Tolerance', 15)
region_growing_label_tolerance.show_label()

# Label and slider tolerance
region_growing_label_slider_tolerance = comp.Label_Text_Slider(
    ctk, side_view_region_growing.get_frame(), '0', 40, 5)
region_growing_label_slider_tolerance.show_label()

region_growing_slider_tolerance = comp.Slider(ctk, side_view_region_growing.get_frame(
), 0, 200, lambda value: region_growing_label_slider_tolerance.set_value_label(int(value)), var_region_growing_slider_tolerance)
region_growing_slider_tolerance.show_slider()

# Label iterations
region_growing_label_iterations = comp.Label_Simple(
    ctk, side_view_region_growing.get_frame(), 'Iterations', 15)
region_growing_label_iterations.show_label()

# Label and slider tolerance
region_growing_label_slider_iterations = comp.Label_Text_Slider(
    ctk, side_view_region_growing.get_frame(), '0', 40, 5)
region_growing_label_slider_iterations.show_label()

region_growing_slider_iterations = comp.Slider(ctk, side_view_region_growing.get_frame(
), 0, 20000, lambda value: region_growing_label_slider_iterations.set_value_label(int(value)), var_region_growing_slider_iterations)
region_growing_slider_iterations.show_slider()

# Buttons
region_growing_button_run = comp.Button(ctk, side_view_region_growing.get_frame(), 'Run algorithm', 100, segmentation_region_growing)
region_growing_button_run.show_button_custom()

region_growing_button_save = comp.Button(ctk, side_view_region_growing.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('region_growing'))
region_growing_button_save.show_button_custom()




# ---------------------------- K-means ------------------------------
side_view_k_means = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'k_means')
side_view_k_means.show_frame_custom()
app_Status.add_process_view(side_view_k_means)


def segmentation_k_means():
    centroids = [(110, 75, 125), (80, 12, 125), (110, 100, 125)]
    iterations = var_k_means_slider_iterations.get()
    new_img = k_means(iterations, centroids, algorithm_Status.get_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
k_means_label_title = comp.Label_Simple(
    ctk, side_view_k_means.get_frame(), 'K-MEANS', 20)
k_means_label_title.show_label()

# Label iterations
k_means_label_iterations = comp.Label_Simple(
    ctk, side_view_k_means.get_frame(), 'Iterations', 15)
k_means_label_iterations.show_label()

# Label and slider tolerance
k_means_label_slider_iterations = comp.Label_Text_Slider(
    ctk, side_view_k_means.get_frame(), '0', 40, 5)
k_means_label_slider_iterations.show_label()

k_means_slider_iterations = comp.Slider(ctk, side_view_k_means.get_frame(
), 0, 100, lambda value: k_means_label_slider_iterations.set_value_label(int(value)), var_k_means_slider_iterations)
k_means_slider_iterations.show_slider()

# Buttons
k_means_button_run = comp.Button(ctk, side_view_k_means.get_frame(), 'Run algorithm', 100, segmentation_k_means)
k_means_button_run.show_button_custom()

k_means_button_save = comp.Button(ctk, side_view_k_means.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('k_means'))
k_means_button_save.show_button_custom()




# ------------------------------ Z-Score ------------------------------
side_view_z_score = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'z_score')
side_view_z_score.show_frame_custom()
app_Status.add_process_view(side_view_z_score)


def intensity_standarization_z_score():
    background_intensity = int(var_z_score_slider_background_intensity.get())
    new_img = z_score(background_intensity, algorithm_Status.get_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
z_score_label_title = comp.Label_Simple(
    ctk, side_view_z_score.get_frame(), 'Z-SCORE', 20)
z_score_label_title.show_label()

# Label background intensity
z_score_label_background_intensity = comp.Label_Simple(
    ctk, side_view_z_score.get_frame(), 'Background intensity', 15)
z_score_label_background_intensity.show_label()

# Label and slider background intensity
z_score_label_slider_background_intensity = comp.Label_Text_Slider(
    ctk, side_view_z_score.get_frame(), '0', 40, 5)
z_score_label_slider_background_intensity.show_label()

z_score_slider_background_intensity = comp.Slider(ctk, side_view_z_score.get_frame(
), 0, 100, lambda value: z_score_label_slider_background_intensity.set_value_label(int(value)), var_z_score_slider_background_intensity)
z_score_slider_background_intensity.show_slider()

# Buttons
z_score_button_run = comp.Button(ctk, side_view_z_score.get_frame(), 'Run algorithm', 100, intensity_standarization_z_score)
z_score_button_run.show_button_custom()

z_score_button_save = comp.Button(ctk, side_view_z_score.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('z_score'))
z_score_button_save.show_button_custom()




# ------------------------------ Intensity rescaling ------------------------------
side_view_intensity_rescaling = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'intensity_rescaling')
side_view_intensity_rescaling.show_frame_custom()
app_Status.add_process_view(side_view_intensity_rescaling)


def intensity_standarization_intensity_rescaling():
    new_img = intensity_rescaling(algorithm_Status.get_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
intensity_rescaling_label_title = comp.Label_Simple(
    ctk, side_view_intensity_rescaling.get_frame(), 'INTENSITY RESCALING', 20)
intensity_rescaling_label_title.show_label()

# Buttons
intensity_rescaling_button_run = comp.Button(ctk, side_view_intensity_rescaling.get_frame(), 'Run algorithm', 100, intensity_standarization_intensity_rescaling)
intensity_rescaling_button_run.show_button_custom()

intensity_rescaling_button_save = comp.Button(ctk, side_view_intensity_rescaling.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('intensity_rescaling'))
intensity_rescaling_button_save.show_button_custom()




# ------------------------------ White stripe ------------------------------
side_view_white_stripe = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'white_stripe')
side_view_white_stripe.show_frame_custom()
app_Status.add_process_view(side_view_white_stripe)


def intensity_standarization_white_stripe():
    threshold = int(var_white_stripe_slider_threshold.get())
    new_img = white_stripe(threshold, algorithm_Status.get_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
white_stripe_label_title = comp.Label_Simple(
    ctk, side_view_white_stripe.get_frame(), 'WHITE STRIPE', 20)
white_stripe_label_title.show_label()

# Label threshold
white_stripe_label_threshold = comp.Label_Simple(
    ctk, side_view_white_stripe.get_frame(), 'Threshold', 15)
white_stripe_label_threshold.show_label()

# Label and slider background intensity
white_stripe_label_slider_threshold = comp.Label_Text_Slider(
    ctk, side_view_white_stripe.get_frame(), '0', 40, 5)
white_stripe_label_slider_threshold.show_label()

white_stripe_slider_threshold = comp.Slider(ctk, side_view_white_stripe.get_frame(
), 0, 200, lambda value: white_stripe_label_slider_threshold.set_value_label(int(value)), var_white_stripe_slider_threshold)
white_stripe_slider_threshold.show_slider()

# Buttons
white_stripe_button_run = comp.Button(ctk, side_view_white_stripe.get_frame(), 'Run algorithm', 100, intensity_standarization_white_stripe)
white_stripe_button_run.show_button_custom()

white_stripe_button_save = comp.Button(ctk, side_view_white_stripe.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('white_stripe'))
white_stripe_button_save.show_button_custom()




# ------------------------------ Histogram matching ------------------------------
side_view_histogram_matching = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'histogram_matching')
side_view_histogram_matching.show_frame_custom()
app_Status.add_process_view(side_view_histogram_matching)


def intensity_standarization_histogram_matching():
    k = var_histogram_matching_slider_k.get()
    print("k:", k)
    new_img = histogram_matching(algorithm_Status.get_img_secondary(), algorithm_Status.get_img_main(), k)
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
histogram_matching_label_title = comp.Label_Simple(
    ctk, side_view_histogram_matching.get_frame(), 'HISTOGRAM MATCHING', 20)
histogram_matching_label_title.show_label()

# Button that upload .nii images
btn_upload_nii_histogram_matching = comp.Button_Upload(ctk, side_view_histogram_matching.get_frame(
), "Upload training image", img_upload_nii_upload.get_image(), '#0C5EF7', '#5992FC', lambda: upload_image(False), 0, 0, [0, 0], [0, 0], 100, 100, 'top')
btn_upload_nii_histogram_matching.show_button()

# Label k
histogram_matching_label_k = comp.Label_Simple(
    ctk, side_view_histogram_matching.get_frame(), 'K', 15)
histogram_matching_label_k.show_label()

# Label and slider background intensity
histogram_matching_label_slider_k = comp.Label_Text_Slider(
    ctk, side_view_histogram_matching.get_frame(), '0', 40, 5)
histogram_matching_label_slider_k.show_label()

histogram_matching_slider_k = comp.Slider(ctk, side_view_histogram_matching.get_frame(
), 0, 10, lambda value: histogram_matching_label_slider_k.set_value_label(int(value)), var_histogram_matching_slider_k)
histogram_matching_slider_k.show_slider()

# Buttons
histogram_matching_button_run = comp.Button(ctk, side_view_histogram_matching.get_frame(), 'Run algorithm', 100, intensity_standarization_histogram_matching)
histogram_matching_button_run.show_button_custom()

histogram_matching_button_save = comp.Button(ctk, side_view_histogram_matching.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('histogram_matching'))
histogram_matching_button_save.show_button_custom()




# ------------------------------ Mean filter ------------------------------
side_view_mean_filter = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'mean_filter')
side_view_mean_filter.show_frame_custom()
app_Status.add_process_view(side_view_mean_filter)


def intensity_standarization_mean_filter():
    new_img = mean_filter_kernel(algorithm_Status.get_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
mean_filter_label_title = comp.Label_Simple(
    ctk, side_view_mean_filter.get_frame(), 'MEAN FILTER', 20)
mean_filter_label_title.show_label()

# Buttons
mean_filter_button_run = comp.Button(ctk, side_view_mean_filter.get_frame(), 'Run algorithm', 100, intensity_standarization_mean_filter)
mean_filter_button_run.show_button_custom()

mean_filter_button_save = comp.Button(ctk, side_view_mean_filter.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('mean_filter'))
mean_filter_button_save.show_button_custom()


# ------------------------------ Median filter ------------------------------
side_view_median_filter = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'median_filter')
side_view_median_filter.show_frame_custom()
app_Status.add_process_view(side_view_median_filter)


def intensity_standarization_median_filter():
    new_img = median_filter(3, algorithm_Status.get_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
median_filter_label_title = comp.Label_Simple(
    ctk, side_view_median_filter.get_frame(), 'MEDIAN FILTER', 20)
median_filter_label_title.show_label()

# Buttons
median_filter_button_run = comp.Button(ctk, side_view_median_filter.get_frame(), 'Run algorithm', 100, intensity_standarization_median_filter)
median_filter_button_run.show_button_custom()

median_filter_button_save = comp.Button(ctk, side_view_median_filter.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('median_filter'))
median_filter_button_save.show_button_custom()




# ------------------------------ Edges ------------------------------
side_view_edges = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'edges')
side_view_edges.show_frame_custom()
app_Status.add_process_view(side_view_edges)


def edges_finite_differences():
    new_img = finite_differences(algorithm_Status.get_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

def edges_centered_differences():
    new_img = centered_differences(algorithm_Status.get_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
edges_label_title = comp.Label_Simple(
    ctk, side_view_edges.get_frame(), 'EDGES', 20)
edges_label_title.show_label()

# Buttons
edges_finite_differences_button_run = comp.Button(ctk, side_view_edges.get_frame(), 'Run finite differences', 100, edges_finite_differences)
edges_finite_differences_button_run.show_button_custom()

edges_centered_differences_button_run = comp.Button(ctk, side_view_edges.get_frame(), 'Run centered differences', 100, edges_centered_differences)
edges_centered_differences_button_run.show_button_custom()

edges_button_save = comp.Button(ctk, side_view_edges.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('edges'))
edges_button_save.show_button_custom()





# ------------------------------ Registration ------------------------------
side_view_registration = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'registration')
side_view_registration.show_frame_custom()
app_Status.add_process_view(side_view_registration)


def registration_image():
    new_img = registration(algorithm_Status.get_url_img_secondary(), algorithm_Status.get_url_img_main())
    app_Status.set_app_img_main(new_img)
    updateImageView()

# Title
registration_label_title = comp.Label_Simple(
    ctk, side_view_registration.get_frame(), 'REGISTRATION', 20)
registration_label_title.show_label()

# Button that upload .nii images
btn_upload_nii_registration = comp.Button_Upload(ctk, side_view_registration.get_frame(
), "Upload fixed image", img_upload_nii_upload.get_image(), '#0C5EF7', '#5992FC', lambda: upload_image(False), 0, 0, [0, 0], [0, 0], 100, 100, 'top')
btn_upload_nii_registration.show_button()

# Buttons
registration_button_run = comp.Button(ctk, side_view_registration.get_frame(), 'Run algorithm', 100, registration_image)
registration_button_run.show_button_custom()

registration_button_save = comp.Button(ctk, side_view_registration.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('registration'))
registration_button_save.show_button_custom()







# ------------------------------ Laplacian coordinates ------------------------------
side_view_laplacian_coordinates = comp.Frame(ctk, app, configuration_App.get_help_view_width(
), configuration_App.APP_HEIGHT, 'transparent', 0, 'laplacian_coordinates')
side_view_laplacian_coordinates.show_frame_custom()
app_Status.add_process_view(side_view_laplacian_coordinates)


def laplacian_coordinates():
    new_img = run_laplacian_coordinates(algorithm_Status.get_img_main(), algorithm_Status.get_annotated_array(), app_Status.get_current_depth(), option_menu_view_type_variable.get())
    
    
    img_laplacian = app_Status.get_app_img_main()
    if option_menu_view_type_variable.get() == 'coronal':
        img_laplacian[:, :, app_Status.get_current_depth()] = new_img
    elif option_menu_view_type_variable.get() == 'sagital':
        img_laplacian[app_Status.get_current_depth(), :, :] = new_img
    elif option_menu_view_type_variable.get() == 'axial':
        img_laplacian[:, app_Status.get_current_depth(), :] = new_img
    
    
    app_Status.set_app_img_main(img_laplacian)
    updateImageView()

# Title
laplacian_label_title = comp.Label_Simple(
    ctk, side_view_laplacian_coordinates.get_frame(), 'LAPLACIAN COORDINATES', 20)
laplacian_label_title.show_label()

# Buttons
laplacian_button_run = comp.Button(ctk, side_view_laplacian_coordinates.get_frame(), 'Run algorithm', 100, laplacian_coordinates)
laplacian_button_run.show_button_custom()

laplacian_button_save = comp.Button(ctk, side_view_laplacian_coordinates.get_frame(), 'Save segmentation', 100, lambda: app_Status.save_image_nii('laplacian_coordinates'))
laplacian_button_save.show_button_custom()



###########################################################################
#                                MAIN LOOP                                #
###########################################################################
app.mainloop()
