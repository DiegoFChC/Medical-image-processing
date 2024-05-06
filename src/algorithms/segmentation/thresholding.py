import copy


def thresholding(tau, deltaTau, img_main):
    img = copy.deepcopy(img_main)
    tau_init = tau
    tau_t = tau_init

    if tau != 0:
        img_th = img > tau_t
        print("Umbralizacion sencilla")
    else:
        print("isodata")
        while True:
            img_th = img > tau_t
            m_foreground = img[img_th == 1].mean()
            m_background = img[img_th == 0].mean()
            tau_new = 0.5 * (m_foreground + m_background)

            if abs(tau_new - tau_t) < deltaTau:
                break
            else:
                tau_t = tau_new
    print("Fin de umbralización!!!")
    return img_th
