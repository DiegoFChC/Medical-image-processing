def modify_canvas(x, y, z, img, plano, deep):
    """ x: tamaño de la imagen en el eje x
        y: tamaño de la imagen en el eje y
        z: tamaño de la imagen en el eje z
        img: array generado por nibabel al leer la imagen .nii
        plano: vista de la imagen (coronal, sagital, axial)
        deep: profundidad que quiero ver del plano que será fijo
    """
    print(x, y, z, plano, deep)
    # canvas_view.pack_forget()
    # canvas_main.pack_forget()
    # print("Segmentacion", x, y, z)
    # canvas_main.pack_forget()
    canvas_main.config(width=x*2, height=y*2)

    # Plano XY -> Vista coronal
    # Plano YZ -> Vista sagital
    # Plano XZ -> Vista axial
    aux_range1 = 0
    aux_range2 = 0
    if plano == "coronal":
        aux_range1 = x
        aux_range2 = y
        slider.configure(to=z)
    elif plano == "sagital":
        aux_range1 = y
        aux_range2 = z
        slider.configure(to=x)
    else:
        aux_range1 = x
        aux_range2 = z
        slider.configure(to=y)
    # Dibujado
    for i in range(aux_range1):
        for j in range(aux_range2):
            if plano == "coronal":
                matrix_value = img[i, j, deep]
            elif plano == "sagital":
                matrix_value = img[deep, i, j]
            else:
                matrix_value = img[i, deep, j]

            # Colorear
            color = int(255 * matrix_value)
            color = f"#{color:02x}{color:02x}{color:02x}"
            # print("Color a usar:",color, "valor original:", matrix_value)
            # canvas_main.create_line(i, j, (i+1), (j+1), fill=color)
            canvas_main.create_rectangle(
                i*2, j*2, (i+1)*2, (j+1)*2, fill=color)

    # canvas_view.pack()
    # canvas_main.config(width=x, height=y)
    # canvas_main.pack()
    # option_menu_view.pack()