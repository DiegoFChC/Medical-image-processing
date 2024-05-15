import SimpleITK as sitk
import numpy as np


def convert_to_float32(image_path):
    """
    Reads an image using SimpleITK and casts it to float32 data type.

    Args:
        image_path (str): Path to the medical image file.

    Returns:
        sitk.Image: The image loaded and converted to float32.
    """

    image = sitk.ReadImage(image_path)
    image_type = image.GetPixelIDValue()
    if image_type != sitk.sitkFloat32:
        image = sitk.Cast(image, sitk.sitkFloat32)
    return image


def register_images(fixed_image_path, moving_image_path):
    """
    Performs medical image registration using SimpleITK.

    Args:
        fixed_image_path (str): Path to the fixed image file.
        moving_image_path (str): Path to the moving image file.

    Returns:
            - "fixed_image_array": The fixed image as a numpy array.
            - "registered_moving_image_array": The registered moving image as a numpy array.
    """

    # Load images and convert to float32
    fixed_image = convert_to_float32(fixed_image_path)
    moving_image = convert_to_float32(moving_image_path)

    # Check the data types of the images
    fixed_image_type = fixed_image.GetPixelIDValue()
    moving_image_type = moving_image.GetPixelIDValue()

    if fixed_image_type == sitk.sitkFloat32:
      target_type = sitk.sitkFloat32
    elif moving_image_type == sitk.sitkUInt8:
      target_type = sitk.sitkUInt8
    else:
      target_type = sitk.sitkFloat32  # Consider float for wider intensity range

    if fixed_image_type != target_type:
      fixed_image = sitk.Cast(fixed_image, target_type)
    if moving_image_type != target_type:
      moving_image = sitk.Cast(fixed_image, target_type)


    # Create registration method
    registration_method = sitk.ImageRegistrationMethod()
    registration_method.SetMetricAsMeanSquares()

    registration_method.SetOptimizerAsRegularStepGradientDescent(learningRate=4.0,
                                                                minimumStepLength=0.01,
                                                                numberOfIterations=200)

    registration_method.SetInitialTransform(sitk.TranslationTransform(fixed_image.GetDimension()))

    registration_method.SetInterpolator(sitk.sitkLinear)

    outTx = registration_method.Execute(fixed_image, moving_image)

    # Resample registered moving image to fixed image space
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed_image)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(100)
    resampler.SetTransform(outTx)

    result = resampler.Execute(moving_image)

    # Convert images to NumPy arrays
    fixed_image_array = sitk.GetArrayFromImage(fixed_image)
    registered_moving_image_array = sitk.GetArrayFromImage(result)

    return fixed_image_array, registered_moving_image_array