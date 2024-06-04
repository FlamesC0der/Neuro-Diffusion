from io import BytesIO
from diffusers import StableDiffusionPipeline
from app.exceptions import *


class CetusDiffusion:
    def __init__(self, file_path: str, device: str) -> None:
        print("✨ Loading CetusDiffusion model")
        self.pipeline = StableDiffusionPipeline.from_single_file(
            file_path
        )
        self.pipeline.to(device)

    def generate_image(
            self,
            prompt: str,
            num_inference_steps: int = 50,
            num_images: int = 1
    ) -> BytesIO:
        try:
            image = self.pipeline(
                prompt,
                num_inference_steps=num_inference_steps,
                num_images_per_prompt=num_images,
                width=1024,
                height=1024
            ).images[0]
            bio = BytesIO()
            image.save(bio, 'PNG')
            bio.seek(0)

            return bio
        except Exception:
            raise GenerationErrorException()
