import torch
from PIL import Image

import folder_paths

remove = None
new_session = None


class ImageSegmentation:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "model": ([
                              "u2net",
                              "u2netp",
                              "u2net_human_seg",
                              "u2net_cloth_seg",
                              "silueta",
                              "isnet-general-use",
                              "isnetis",
                              "modnet-p",
                              "modnet-w"
                          ],),
                "alpha_matting": (["true", "false"],),
                "alpha_matting_foreground_threshold": ("INT", {
                    "default": 240,
                    "max": 250,
                    "step": 5
                }),
                "alpha_matting_background_threshold": ("INT", {
                    "default": 20,
                    "max": 250,
                    "step": 5
                }),
                "alpha_matting_erode_size": ("INT", {
                    "default": 10,
                    "step": 1
                }),
                "post_process_mask": (["false", "true"],),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/segmentation"

    def node(
            self,
            images,
            model,
            alpha_matting,
            alpha_matting_foreground_threshold,
            alpha_matting_background_threshold,
            alpha_matting_erode_size,
            post_process_mask,
            session=None
    ):
        from ..session.ModnetPhotographicSession import ModnetPhotographicSession
        from ..session.ModnetWebcamSession import ModnetWebcamSession
        global remove, new_session
        if new_session is None:
            from rembg import remove, new_session
        if session is None:
            if model == "isnetis":
                session = new_session("isnet-anime")
            elif model == "modnet-p":
                session = ModnetPhotographicSession(model)
            elif model == "modnet-w":
                session = ModnetWebcamSession(model)
            else:
                session = new_session(model)

        def verst(image):
            img: Image = image.tensor_to_image()
            global remove, new_session
            if remove is None:
                from rembg import remove, new_session

            return remove(
                img, alpha_matting == "true",
                alpha_matting_foreground_threshold,
                alpha_matting_background_threshold,
                alpha_matting_erode_size, session,
                False, post_process_mask == "true"
            ).image_to_tensor()

        return (torch.stack([
            verst(images[i]) for i in range(len(images))
        ]),)


class ImageSegmentationCustom:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "model": (folder_paths.get_filename_list("onnx"),),
                "alpha_matting": (["true", "false"],),
                "alpha_matting_foreground_threshold": ("INT", {
                    "default": 240,
                    "max": 250,
                    "step": 5
                }),
                "alpha_matting_background_threshold": ("INT", {
                    "default": 20,
                    "max": 250,
                    "step": 5
                }),
                "alpha_matting_erode_size": ("INT", {
                    "default": 10,
                    "step": 1
                }),
                "post_process_mask": (["false", "true"],),
                "mean": ("FLOAT", {
                    "default": 0.485,
                    "max": 1.0,
                    "step": 0.01
                }),
                "std": ("FLOAT", {
                    "default": 1.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "size": ("INT", {
                    "default": 1024,
                    "step": 8
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/segmentation"

    def node(
            self,
            images,
            model,
            alpha_matting,
            alpha_matting_foreground_threshold,
            alpha_matting_background_threshold,
            alpha_matting_erode_size,
            post_process_mask,
            mean,
            std,
            size
    ):
        from ..session.CustomSession import CustomAbstractSession
        from ..session.CustomSession import CustomSessionContainer
        container = CustomSessionContainer(mean, mean, mean, std, std, std, size, size)

        class CustomSession(CustomAbstractSession):
            def __init__(self):
                super().__init__(model)

            @classmethod
            def name(cls, *args, **kwargs):
                return model

        session = CustomSession().from_container(container)

        return ImageSegmentation().node(
            images,
            model,
            alpha_matting,
            alpha_matting_foreground_threshold,
            alpha_matting_background_threshold,
            alpha_matting_erode_size,
            post_process_mask,
            session
        )


class ImageSegmentationCustomAdvanced:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "model": (folder_paths.get_filename_list("onnx"),),
                "alpha_matting": (["true", "false"],),
                "alpha_matting_foreground_threshold": ("INT", {
                    "default": 240,
                    "max": 250,
                    "step": 5
                }),
                "alpha_matting_background_threshold": ("INT", {
                    "default": 20,
                    "max": 250,
                    "step": 5
                }),
                "alpha_matting_erode_size": ("INT", {
                    "default": 10,
                    "step": 1
                }),
                "post_process_mask": (["false", "true"],),
                "mean_r": ("FLOAT", {
                    "default": 0.485,
                    "max": 1.0,
                    "step": 0.01
                }),
                "mean_g": ("FLOAT", {
                    "default": 0.456,
                    "max": 1.0,
                    "step": 0.01
                }),
                "mean_b": ("FLOAT", {
                    "default": 0.406,
                    "max": 1.0,
                    "step": 0.01
                }),
                "std_r": ("FLOAT", {
                    "default": 1.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "std_g": ("FLOAT", {
                    "default": 1.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "std_b": ("FLOAT", {
                    "default": 1.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "width": ("INT", {
                    "default": 1024,
                    "step": 8
                }),
                "height": ("INT", {
                    "default": 1024,
                    "step": 8
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "node"
    CATEGORY = "image/segmentation"

    def node(
            self,
            images,
            model,
            alpha_matting,
            alpha_matting_foreground_threshold,
            alpha_matting_background_threshold,
            alpha_matting_erode_size,
            post_process_mask,
            mean_x,
            mean_y,
            mean_z,
            std_x,
            std_y,
            std_z,
            width,
            height
    ):
        from ..session.CustomSession import CustomAbstractSession
        from ..session.CustomSession import CustomSessionContainer
        container = CustomSessionContainer(mean_x, mean_y, mean_z, std_x, std_y, std_z, width, height)

        class CustomSession(CustomAbstractSession):
            def __init__(self):
                super().__init__(model)

            @classmethod
            def name(cls, *args, **kwargs):
                return model

        session = CustomSession().from_container(container)

        return ImageSegmentation().node(
            images,
            model,
            alpha_matting,
            alpha_matting_foreground_threshold,
            alpha_matting_background_threshold,
            alpha_matting_erode_size,
            post_process_mask,
            session
        )


NODE_CLASS_MAPPINGS = {
    "ImageSegmentation": ImageSegmentation,
    "ImageSegmentationCustom": ImageSegmentationCustom,
    "ImageSegmentationCustomAdvanced": ImageSegmentationCustomAdvanced,
}
