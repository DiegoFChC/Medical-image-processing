import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
# import segmentacion
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
from auxFuntions.configuration_app import Configuration_App
from auxFuntions.app_status import App_Status
from auxFuntions.algorithm_status import Algorithm_Status

# # App State
# configuration_App = Configuration_App()
# app_Status = App_Status()
# algorithm_Status = Algorithm_Status()

# # App principal
# app = ctk.CTk()

# option_menu_view_var = tk.StringVar(value="coronal")
# slider_value_var = tk.IntVar(value=0)
# slider_umbralizacion_tau = tk.IntVar(value=0)
# slider_tolerancia_regiones_var = tk.IntVar(value=0)
# slider_iteraciones_regiones_var = tk.IntVar(value=0)
# slider_iteraciones_k_means_var = tk.IntVar(value=0)
# slider_umbralizacion_delta_tau = tk.DoubleVar(value=0)

# # Para posicionar la ventana en el centro
# wtotal = app.winfo_screenwidth()
# htotal = app.winfo_screenheight()
# pwidth = round((wtotal-configuration_App.APP_WIDTH)/2)
# pheight = round((htotal-configuration_App.APP_HEIGHT)/2)

# app.geometry(f"{configuration_App.APP_WIDTH}x{
#              configuration_App.APP_HEIGHT}+{pwidth}+{pheight}")
# app.resizable(0, 0)
# app.title("PROCESAMIENTO DE IMÁGENES MÉDICAS")
# app.configure(fg_color=configuration_App.BACKGROUND_COLOR)
# app.iconbitmap("images/icon.ico")

#################### FUNCTIONS #####################


# def modify_canvas(x, y, z, img, plano, deep):
#     """ x: tamaño de la imagen en el eje x
#         y: tamaño de la imagen en el eje y   
#         z: tamaño de la imagen en el eje z
#         img: array generado por nibabel al leer la imagen .nii
#         plano: vista de la imagen (coronal, sagital, axial)
#         deep: profundidad que quiero ver del plano que será fijo
#     """
#     print("Solo ver", x, y, z, plano, deep)
#     app_Status.set_current_depth(deep)
#     # Plano XY -> Vista coronal
#     # Plano YZ -> Vista sagital
#     # Plano XZ -> Vista axial
#     if plano == "coronal":
#         aux_range1 = x
#         aux_range2 = y
#         slider.configure(to=z)
#         pil_image = Image.fromarray(img[:, :, deep])
#     elif plano == "sagital":
#         aux_range1 = y
#         aux_range2 = z
#         slider.configure(to=x)
#         pil_image = Image.fromarray(img[deep, :, :])
#     elif plano == "axial":
#         aux_range1 = x
#         aux_range2 = z
#         slider.configure(to=y)
#         pil_image = Image.fromarray(img[:, deep, :])

#     plt.imsave("imagen.jpeg", pil_image)
#     image_to_show = Image.open("images/imagen.jpeg")
#     image_to_show_ = ctk.CTkImage(
#         dark_image=image_to_show, light_image=image_to_show, size=(aux_range1*2, aux_range2*2))
#     labellll.configure(image=image_to_show_)


# def draw_in_canvas(x, y, z, img, plano, deep):
#     global image_to_show_
#     print("Dibujar", x, y, z, plano, deep)
#     app_Status.set_current_depth(deep)
#     # Plano XY -> Vista coronal
#     # Plano YZ -> Vista sagital
#     # Plano XZ -> Vista axial
#     if plano == "coronal":
#         aux_range1 = x
#         aux_range2 = y
#         slider.configure(to=z)
#         pil_image = Image.fromarray(img[:, :, deep])
#     elif plano == "sagital":
#         aux_range1 = y
#         aux_range2 = z
#         slider.configure(to=x)
#         pil_image = Image.fromarray(img[deep, :, :])
#     elif plano == "axial":
#         aux_range1 = x
#         aux_range2 = z
#         slider.configure(to=y)
#         pil_image = Image.fromarray(img[:, deep, :])

#     canvas_draw.configure(width=aux_range1*2, height=aux_range2*2)
#     plt.imsave("imagen.jpeg", pil_image)
#     image_to_show = Image.open("imagen.jpeg")
#     image_to_show = image_to_show.resize((aux_range1*2, aux_range2*2))
#     image_to_show_ = ImageTk.PhotoImage(image_to_show)
#     # image_to_show_ = ctk.CTkImage(
#     #     dark_image=image_to_show, light_image=image_to_show, size=(aux_range1*2, aux_range2*2))
#     canvas_draw.create_image(0, 0, anchor=tk.NW, image=image_to_show_)


# def upload_image():
#     file_url = tk.filedialog.askopenfilename()

#     if file_url:
#         # Procesar el archivo
#         x, y, z, img = segmentacion.upload_img_nii(file_url)
#         app_Status.set_canvas_size_x(x)
#         app_Status.set_canvas_size_y(y)
#         app_Status.set_canvas_size_z(z)
#         app_Status.set_app_img_main(img)
#         temporal_upload_img.pack_forget()
#         img_view.pack(side="left", padx=20, pady=20)
#         # Sliders para umbralización
#         slider_tau.configure(to=segmentacion.max_value)
#         segmentacion.reiniciar_anotacion()
#         modify_canvas(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(
#         ), app_Status.get_canvas_size_z(), app_Status.get_app_img_main(), "coronal", 100)
#     else:
#         print("No se seleccionó ningún archivo")


# def activate_upload():
#     configuration_App.set_main_view_width(1150)
#     main_view.configure(width=configuration_App.get_main_view_width())
#     temporal_upload_img.configure(
#         width=configuration_App.get_main_view_width())
#     temporal_upload_img.pack(side="left", padx=20, pady=20)
#     img_view.pack_forget()


# def change_page():
#     configuration_App.set_main_view_width(825)
#     main_view.configure(width=configuration_App.get_main_view_width())
#     temporal_upload_img.configure(
#         width=configuration_App.get_main_view_width())
#     temporal_upload_img.pack_forget()
#     img_view.pack(side="left", padx=20, pady=20)
#     if app_Status.get_current_segmentation() == "umbralizacion":
#         lateral_view_umbralizacion.pack(side="left", padx=(0, 20), pady=20)
#         lateral_view_regiones.pack_forget()
#         lateral_view_k_means.pack_forget()
#     elif app_Status.get_current_segmentation() == "regiones":
#         lateral_view_umbralizacion.pack_forget()
#         lateral_view_regiones.pack(side="left", padx=(0, 20), pady=20)
#         lateral_view_k_means.pack_forget()
#     elif app_Status.get_current_segmentation() == "k-means":
#         lateral_view_umbralizacion.pack_forget()
#         lateral_view_regiones.pack_forget()
#         lateral_view_k_means.pack(side="left", padx=(0, 20), pady=20)


# def draw_img():
#     if app_Status.get_draw() == True:
#         labellll.pack_forget()
#         slider_number.pack_forget()
#         slider.pack_forget()
#         draw_button.pack_forget()
#         save_draw_button.pack_forget()
#         canvas_draw.pack()
#         slider_number.pack(pady=10)
#         slider.pack(pady=30)
#         draw_button.pack(pady=20)
#         draw_in_canvas(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(), app_Status.get_app_img_main(),
#                        option_menu_view_var.get(), int(slider_value_var.get()))
#         save_draw_button.pack(pady=10)
#     elif app_Status.get_draw() == False:
#         canvas_draw.pack_forget()
#         slider_number.pack_forget()
#         slider.pack_forget()
#         draw_button.pack_forget()
#         save_draw_button.pack_forget()
#         labellll.pack(anchor="center", padx=10, pady=10)
#         slider_number.pack(pady=10)
#         slider.pack(pady=30)
#         draw_button.pack(pady=20)


# def save_image_nii():
#     img_uint8 = app_Status.get_app_img_main().astype(np.uint8)
#     nii_img = nib.Nifti1Image(img_uint8, affine=np.eye(4))
#     nib.save(nii_img, "segmentaión.nii")


#################### SIDEBAR #######################
# sidebar = ctk.CTkFrame(master=app, width=configuration_App.SIDEBAR_WITDH, height=configuration_App.APP_HEIGHT,
#                        fg_color="transparent", corner_radius=20)
# sidebar.pack_propagate(0)
# sidebar.pack(fill="y", anchor="w", side="left", padx=(20, 0), pady=20)

# Logo menu
# logo = ctk.CTkFrame(master=sidebar, width=70, height=70,
#                     fg_color="#ffffff", corner_radius=20)
# logo.pack_propagate(0)
# logo.pack()

# logo_img_data = Image.open("images/logo.png")
# logo_img = ctk.CTkImage(dark_image=logo_img_data,
#                         light_image=logo_img_data, size=(50, 50))

# ctk.CTkLabel(master=logo, text="", image=logo_img).pack(
#     anchor="center", padx=10, pady=10)

# Botón de inicio
# home_img_data = Image.open("images/home.png")
# home_img = ctk.CTkImage(dark_image=home_img_data, light_image=home_img_data)
# ctk.CTkButton(master=sidebar, image=home_img, text="Inicio", fg_color="#090909", font=(
#     "Arial Bold", 16), anchor="w", corner_radius=10, hover_color="#0C5EF7", 
            #   command=activate_upload).pack(fill="x", ipady=5, pady=(60, 0))


# def segmentacion_():
#     app_Status.set_current_segmentation("umbralizacion")
#     change_page()


# Botón de segmentación
# seg_img_data = Image.open("images/seg.png")
# seg_img = ctk.CTkImage(dark_image=seg_img_data, light_image=seg_img_data)
# ctk.CTkButton(master=sidebar, image=seg_img, text="Segmentación", fg_color="#090909", font=(
#     "Arial Bold", 16), anchor="w", corner_radius=10, hover_color="#0C5EF7", 
            #   command=segmentacion_).pack(fill="x", ipady=5, pady=(20, 0))

# Sub-botones


# def segmentacion_umbralizacion():
#     app_Status.set_current_segmentation("umbralizacion")
#     change_page()


# ctk.CTkButton(master=sidebar, text="  Umbralización", fg_color="#090909", font=(
#     "Arial Bold", 15), anchor="w", corner_radius=10, hover_color="#5992FC", 
            #   command=segmentacion_umbralizacion).pack(fill="x", ipady=5, pady=(10, 0), padx=(20, 0))


# def segmentacion_regiones():
#     app_Status.set_current_segmentation("regiones")
#     change_page()


# ctk.CTkButton(master=sidebar, text="  Crecimiento de regiones", fg_color="#090909", font=(
#     "Arial Bold", 15), anchor="w", corner_radius=10, hover_color="#5992FC", 
            #   command=segmentacion_regiones).pack(fill="x", ipady=5, pady=(10, 0), padx=(20, 0))


# def segmentacion_k_means():
#     app_Status.set_current_segmentation("k-means")
#     change_page()


# ctk.CTkButton(master=sidebar, text="  K-means", fg_color="#090909", font=(
#     "Arial Bold", 15), anchor="w", corner_radius=10, hover_color="#5992FC", 
            #   command=segmentacion_k_means).pack(fill="x", ipady=5, pady=(10, 0), padx=(20, 0))

##################### VISTA PRINCIPAL #####################
# main_view = ctk.CTkFrame(master=app, width=configuration_App.get_main_view_width(),
#                          height=configuration_App.APP_HEIGHT, fg_color="#ffffff", corner_radius=20)
# main_view.pack_propagate(0)
# main_view.pack(side="left", padx=20, pady=20)

# # Cargar archivo
# upload_img_data = Image.open("images/upload.png")
# upload_img = ctk.CTkImage(dark_image=upload_img_data,
#                           light_image=upload_img_data, size=(50, 50))

# temporal_upload_img = ctk.CTkFrame(master=main_view, width=configuration_App.get_main_view_width(),
#                                    height=configuration_App.APP_HEIGHT, fg_color="transparent", corner_radius=20)
# temporal_upload_img.pack_propagate(0)
# temporal_upload_img.pack(side="left", padx=20, pady=20)

# img_view = ctk.CTkFrame(master=main_view, width=configuration_App.get_main_view_width(),
#                         height=configuration_App.APP_HEIGHT, fg_color="transparent", corner_radius=20)
# img_view.pack_propagate(0)

# btn_upload = ctk.CTkButton(master=temporal_upload_img, image=upload_img, text="Cargar imagen", fg_color="#0C5EF7", font=(
#     "Arial", 16), width=100, height=100, corner_radius=10, hover_color="#5992FC", compound="top", 
                        #    command=upload_image).pack(anchor="center", pady=(350, 0))


# def updateImageView():
#     if app_Status.get_draw():
#         draw_in_canvas(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(), app_Status.get_app_img_main(),
#                        option_menu_view_var.get(), int(slider_value_var.get()))
#     else:
#         modify_canvas(app_Status.get_canvas_size_x(), app_Status.get_canvas_size_y(), app_Status.get_canvas_size_z(), app_Status.get_app_img_main(),
#                       option_menu_view_var.get(), int(slider_value_var.get()))


# def option(option):
#     updateImageView()


# Lista de opciones de vista
# option_menu_view = ctk.CTkOptionMenu(
#     img_view, values=["coronal", "sagital", "axial"], variable=option_menu_view_var, command=option)
# option_menu_view.pack_propagate(0)
# option_menu_view.pack(pady=30)

# labellll = ctk.CTkLabel(master=img_view, text="",
#                         width=200, height=200, fg_color="transparent")
# labellll.pack_propagate(0)
# labellll.pack(
#     anchor="center", padx=10, pady=10)

# def dibujar_circulo(event):
#     # Coordenadas del clic
#     x, y = event.x, event.y

#     # Dibujar un círculo rojo de 4x4 píxeles en las coordenadas del clic
#     canvas_draw.create_oval(x-2, y-2, x+2, y+2, fill="red")


# def dibujar_linea(event):

#     # Coordenadas actuales del click
#     x, y = event.x, event.y
#     cord_i = int(y/2)
#     cord_j = int(x/2)
#     # print(x,y,cord_i,cord_j)
#     # ANOTACIÓN Y SELECCIÓN DE BOXELES QUE SE GUARDARÁN
#     if option_menu_view_var.get() == "coronal":
#         for i in range(10):
#             segmentacion.anotar_imagen(
#                 cord_i+i, cord_j+i, int(app_Status.get_current_depth()), app_Status.get_app_img_main())
#         for j in range(10):
#             segmentacion.anotar_imagen(
#                 cord_i-j, cord_j-j, int(app_Status.get_current_depth()), app_Status.get_app_img_main())
#     elif option_menu_view_var.get() == "sagital":
#         for i in range(10):
#             segmentacion.anotar_imagen(
#                 int(app_Status.get_current_depth()), cord_i+i, cord_j+i, app_Status.get_app_img_main())
#         for j in range(10):
#             segmentacion.anotar_imagen(
#                 int(app_Status.get_current_depth()), cord_i-j, cord_j-j, app_Status.get_app_img_main())
#     elif option_menu_view_var.get() == "axial":
#         for i in range(10):
#             segmentacion.anotar_imagen(
#                 cord_i+i, int(app_Status.get_current_depth()), cord_j-i, app_Status.get_app_img_main())
#         for j in range(10):
#             segmentacion.anotar_imagen(
#                 cord_i-j, int(app_Status.get_current_depth()), cord_j-j, app_Status.get_app_img_main())
    # if x%2 == 0 and y%2 == 0:
    #     cord_i = int(x/2)
    #     cord_j = int(y/2)
    #     if option_menu_view_var.get() == "coronal":
    #         segmentacion.anotar_imagen(cord_i, cord_j, int(profundidad_actual))
    #     elif option_menu_view_var.get() == "sagital":
    #         segmentacion.anotar_imagen(int(profundidad_actual), cord_i, cord_j)
    #     elif option_menu_view_var.get() == "axial":
    #         segmentacion.anotar_imagen(cord_i, int(profundidad_actual), cord_j)
        # print("mouse al dibujar",x/2,y/2)

    # Dibujar una línea desde las coordenadas anteriores a las actuales
    # if app_Status.get_draw_x_prev() is not None and app_Status.get_draw_y_prev() is not None:
    #     canvas_draw.create_line(app_Status.get_draw_x_prev(
    #     ), app_Status.get_draw_y_prev(), x, y, fill="red", width=20)

    # # Actualizar las coordenadas anteriores
    # app_Status.set_draw_x_prev(x)
    # app_Status.set_draw_y_prev(y)


# def reiniciar_coordenadas(event):
#     # Reiniciar las coordenadas anteriores al soltar el botón del ratón
#     app_Status.set_draw_x_prev(None)
#     app_Status.set_draw_y_prev(None)


# canvas_draw = tk.Canvas(img_view, width=200, height=200)
# canvas_draw.bind("<Button-1>", dibujar_linea)
# canvas_draw.bind("<B1-Motion>", dibujar_linea)
# canvas_draw.bind("<ButtonRelease-1>", reiniciar_coordenadas)

# slider_number = ctk.CTkLabel(img_view, text="0", fg_color="#0C5EF7",
#                              text_color="#ffffff", justify="center", width=40, corner_radius=5)
# slider_number.pack_propagate(0)
# slider_number.pack(pady=10)


# def slider_event(value):
#     # print("cambié de valor", value)
#     slider_number.configure(text=int(value))
#     updateImageView()


# slider = ctk.CTkSlider(img_view, from_=0, to=100,
#                        command=slider_event, variable=slider_value_var)
# slider.set(0)
# slider.pack_propagate(0)
# slider.pack(pady=30)


# def draw_buton_event():
#     app_Status.set_draw(not app_Status.get_draw())
#     if app_Status.get_draw():
#         draw_button.configure(text="Sólo visualisar")
#     else:
#         draw_button.configure(text="Dibujar sobre la imagen")
#     draw_img()


# def exportar_anotaciones():
#     img_uint8 = segmentacion.array_anotado.astype(np.uint8)
#     nii_img = nib.Nifti1Image(img_uint8, affine=np.eye(4))
#     nib.save(nii_img, "segmentaión_anotada.nii")


# draw_button = ctk.CTkButton(master=img_view, text="Dibujar sobre la imagen", fg_color="#0C5EF7", font=(
#     "Arial Bold", 15), anchor="center", width=300, corner_radius=10, hover_color="#5992FC", command=draw_buton_event)
# draw_button.pack(pady=10)

# save_draw_button = ctk.CTkButton(master=img_view, text="Guardar anotation en nuevo archivo .nii", fg_color="#0C5EF7", font=(
#     "Arial Bold", 15), anchor="center", width=300, corner_radius=10, hover_color="#5992FC", command=exportar_anotaciones)

################### VISTA LATERAL PARA SEGMENTACIONES ####################
# UMBRALIZACIÓN
# lateral_view_umbralizacion = ctk.CTkFrame(master=app, width=250,
                                        #   height=configuration_App.APP_HEIGHT, fg_color="transparent", corner_radius=20)
# lateral_view_umbralizacion.pack_propagate(0)
# lateral_view.pack(side="left", padx=(0, 20), pady=20)


# def seg_thresholding():
#     tau = int(slider_umbralizacion_tau.get())
#     # print(slider_umbralizacion_delta_tau.get())
#     delta_tau = round(slider_umbralizacion_delta_tau.get(), 1)
#     print("tau:", tau, "delta_tau", delta_tau)
#     temp_img = segmentacion.thresholding(tau, delta_tau)
#     app_Status.set_app_img_main(temp_img)
#     updateImageView()

# pack
# label_umbralización = ctk.CTkLabel(lateral_view_umbralizacion, text="UMBRALIZACIÓN",
#                                    fg_color="transparent", text_color="#ffffff", justify="center", font=("Arial Bold", 20)).pack(fill="x", pady=20)

# # Label y slider para tau
# label_umbralización_tau = ctk.CTkLabel(lateral_view_umbralizacion, text="Tau inicial",
#                                        fg_color="transparent", text_color="#ffffff", justify="left", font=("Arial Bold", 15)).pack(fill="x", pady=20)

# slider_label_umbralizacion_tau = ctk.CTkLabel(lateral_view_umbralizacion, text="0", fg_color="#0C5EF7",
#                                               text_color="#ffffff", justify="center", width=40, corner_radius=5)
# slider_label_umbralizacion_tau.pack_propagate(0)
# slider_label_umbralizacion_tau.pack(pady=(10, 5))


# def slider_event_tau(value):
#     slider_label_umbralizacion_tau.configure(text=int(value))


# slider_tau = ctk.CTkSlider(lateral_view_umbralizacion, from_=0, to=100,
#                            variable=slider_umbralizacion_tau, command=slider_event_tau)
# slider_tau.set(0)
# slider_tau.pack_propagate(0)
# slider_tau.pack(pady=(10, 30))

# # Label y slider para delta tau
# label_umbralización_delta_tau = ctk.CTkLabel(lateral_view_umbralizacion, text="Delta tau",
#                                              fg_color="transparent", text_color="#ffffff", justify="left", font=("Arial Bold", 15)).pack(fill="x", pady=20)

# slider_label_umbralizacion_delta_tau = ctk.CTkLabel(lateral_view_umbralizacion, text="0", fg_color="#0C5EF7",
#                                                     text_color="#ffffff", justify="center", width=40, corner_radius=5)
# slider_label_umbralizacion_delta_tau.pack_propagate(0)
# slider_label_umbralizacion_delta_tau.pack(pady=(10, 5))


# def slider_event_delta_tau(value):
#     slider_label_umbralizacion_delta_tau.configure(text=round(value, 1))


# slider_delta_tau = ctk.CTkSlider(lateral_view_umbralizacion, from_=0, to=10,
#                                  variable=slider_umbralizacion_delta_tau, command=slider_event_delta_tau)
# slider_delta_tau.set(0)
# slider_delta_tau.pack_propagate(0)
# slider_delta_tau.pack(pady=(10, 30))

# thresholding_button = ctk.CTkButton(master=lateral_view_umbralizacion, text="Ejecutar algoritmo", fg_color="#0C5EF7", font=(
#     "Arial Bold", 15), anchor="center", corner_radius=10, hover_color="#5992FC", command=seg_thresholding).pack(fill="x", pady=20)

# thresholding_save = ctk.CTkButton(master=lateral_view_umbralizacion, text="Guardar segmentación", fg_color="#5992FC", font=(
#     "Arial Bold", 15), anchor="center", corner_radius=10, hover_color="#0C5EF7", command=save_image_nii).pack(fill="x", pady=20)

# CRECIMIENTO DE REGIONES
lateral_view_regiones = ctk.CTkFrame(master=app, width=250,
                                     height=configuration_App.APP_HEIGHT, fg_color="transparent", corner_radius=20)
lateral_view_regiones.pack_propagate(0)


def seg_crecimiento_regiones():
    tolerancia = slider_tolerancia_regiones_var.get()
    punto_inicial = (110, 25, 125)
    iteraciones = slider_iteraciones_regiones_var.get()
    print("tolerancia:", tolerancia, "Punto inicial:",
          punto_inicial, "Iteraciones:", iteraciones)
    temp_img = segmentacion.crecimiento_regiones_3d(
        tolerancia, punto_inicial, iteraciones)
    app_Status.set_app_img_main(temp_img)
    updateImageView()


label_crecimiento = ctk.CTkLabel(lateral_view_regiones, text="CRECIMIENTO DE REGIONES",
                                 fg_color="transparent", text_color="#ffffff", justify="center", font=("Arial Bold", 20), anchor="center", wraplength=200).pack(fill="x", pady=20)


# Label y slider para tolerancia
label_regiones_tolerancia = ctk.CTkLabel(lateral_view_regiones, text="Tolerancia",
                                         fg_color="transparent", text_color="#ffffff", justify="left", font=("Arial Bold", 15)).pack(fill="x", pady=20)

slider_regiones_tolerancia = ctk.CTkLabel(lateral_view_regiones, text="0", fg_color="#0C5EF7",
                                          text_color="#ffffff", justify="center", width=40, corner_radius=5)
slider_regiones_tolerancia.pack_propagate(0)
slider_regiones_tolerancia.pack(pady=(10, 5))


def slider_event_tolerancia(value):
    slider_regiones_tolerancia.configure(text=int(value))


slider_regiones_1 = ctk.CTkSlider(lateral_view_regiones, from_=0, to=200,
                                  variable=slider_tolerancia_regiones_var, command=slider_event_tolerancia)
slider_regiones_1.set(0)
slider_regiones_1.pack_propagate(0)
slider_regiones_1.pack(pady=(10, 30))


# Label y slider para iteraciones
label_regiones_iteraciones = ctk.CTkLabel(lateral_view_regiones, text="Iteraciones",
                                          fg_color="transparent", text_color="#ffffff", justify="left", font=("Arial Bold", 15)).pack(fill="x", pady=20)

slider_regiones_iteraciones = ctk.CTkLabel(lateral_view_regiones, text="0", fg_color="#0C5EF7",
                                           text_color="#ffffff", justify="center", width=40, corner_radius=5)
slider_regiones_iteraciones.pack_propagate(0)
slider_regiones_iteraciones.pack(pady=(10, 5))


def slider_event_iteraciones(value):
    slider_regiones_iteraciones.configure(text=int(value))


slider_regiones_2 = ctk.CTkSlider(lateral_view_regiones, from_=0, to=20000,
                                  variable=slider_iteraciones_regiones_var, command=slider_event_iteraciones)
slider_regiones_2.set(0)
slider_regiones_2.pack_propagate(0)
slider_regiones_2.pack(pady=(10, 30))

crecimiento_regiones_button = ctk.CTkButton(master=lateral_view_regiones, text="Ejecutar algoritmo", fg_color="#0C5EF7", font=(
    "Arial Bold", 15), anchor="w", corner_radius=10, hover_color="#5992FC", command=seg_crecimiento_regiones).pack(fill="x", pady=20)

crecimiento_save = ctk.CTkButton(master=lateral_view_regiones, text="Guardar segmentación", fg_color="#5992FC", font=(
    "Arial Bold", 15), anchor="center", corner_radius=10, hover_color="#0C5EF7", command=save_image_nii).pack(fill="x", pady=20)

# K-MEANS
lateral_view_k_means = ctk.CTkFrame(master=app, width=250,
                                    height=configuration_App.APP_HEIGHT, fg_color="transparent", corner_radius=20)
lateral_view_k_means.pack_propagate(0)
# lateral_view.pack(side="left", padx=(0, 20), pady=20)


def seg_k_means():
    arr = [(110, 75, 125), (80, 12, 125), (110, 100, 125)]
    it = slider_iteraciones_k_means_var.get()
    print("iteraciones:", it, "centroides:", arr)
    temp_img = segmentacion.k_means(it, arr)
    app_Status.set_app_img_main(temp_img)
    updateImageView()


label_k_means = ctk.CTkLabel(lateral_view_k_means, text="K-MEANS",
                             fg_color="transparent", text_color="#ffffff", justify="center", font=("Arial Bold", 20)).pack(fill="x", pady=20)

# Label y slider para iteraciones
label_k_means_iteraciones = ctk.CTkLabel(lateral_view_k_means, text="Iteraciones",
                                         fg_color="transparent", text_color="#ffffff", justify="left", font=("Arial Bold", 15)).pack(fill="x", pady=20)

slider_k_means_iteraciones = ctk.CTkLabel(lateral_view_k_means, text="0", fg_color="#0C5EF7",
                                          text_color="#ffffff", justify="center", width=40, corner_radius=5)
slider_k_means_iteraciones.pack_propagate(0)
slider_k_means_iteraciones.pack(pady=(10, 5))


def slider_event_iteraciones_k_means(value):
    slider_k_means_iteraciones.configure(text=int(value))


slider_k_menas = ctk.CTkSlider(lateral_view_k_means, from_=0, to=100,
                               variable=slider_iteraciones_k_means_var, command=slider_event_iteraciones_k_means)
slider_k_menas.set(0)
slider_k_menas.pack_propagate(0)
slider_k_menas.pack(pady=(10, 30))

####################################
# OJO

# Label y slider para tau
# label_k_means = ctk.CTkLabel(lateral_view_k_means, text="Número de clousters - K",
#                              fg_color="transparent", text_color="#ffffff", justify="left", font=("Arial Bold", 15)).pack(fill="x", pady=20)

# slider_k_means = ctk.CTkLabel(lateral_view_k_means, text="3", fg_color="#0C5EF7",
#                               text_color="#ffffff", justify="center", width=40, corner_radius=5)
# slider_k_means.pack_propagate(0)
# slider_k_means.pack(pady=(10, 5))

# slider_k = ctk.CTkSlider(lateral_view_k_means, from_=0, to=100,
#                          variable=slider_umbralizacion_tau, command=slider_event_tau)
# slider_k.set(0)
# slider_k.pack_propagate(0)
# slider_k.pack(pady=(10, 30))


#######################################

k_means_button = ctk.CTkButton(master=lateral_view_k_means, text="Ejecutar algoritmo", fg_color="#0C5EF7", font=(
    "Arial Bold", 15), anchor="center", corner_radius=10, hover_color="#5992FC", command=seg_k_means).pack(fill="x", pady=20)

k_means_save = ctk.CTkButton(master=lateral_view_k_means, text="Guardar segmentación", fg_color="#5992FC", font=(
    "Arial Bold", 15), anchor="center", corner_radius=10, hover_color="#0C5EF7", command=save_image_nii).pack(fill="x", pady=20)

# Loop que mantiene via la app
app.mainloop()
