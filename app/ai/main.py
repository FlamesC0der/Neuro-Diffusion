from app.ai.models.cetus import CetusDiffusion
from app.misc import ROOT_DIR
import os
import torch


class DiffusionManager:
    def __init__(self):
        print("✨ Loading diffusion models...")
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        print(f"✨ Using device: {self.device}")

        self.CetusDiffusion = CetusDiffusion(os.path.join(ROOT_DIR, "assets/models/cetusMix_Version35.safetensors"),
                                             device=self.device)
        print("✨ Diffusion models loaded!")

    async def generate_image(self, model_name: str, prompt: str):
        if model_name == "CetusMix":
            return self.CetusDiffusion.generate_image(prompt=prompt)


# diffusion_manager = DiffusionManager()
