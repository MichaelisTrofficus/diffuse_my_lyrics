import os
import logging
from tqdm import tqdm
from diffuse_my_lyrics.utils import auth_hugging_face, parse_lyrics

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


class Lyrics2Images:
    def __init__(self,
                 model_id: str = "CompVis/stable-diffusion-v1-4",
                 revision: str = "fp16",
                 torch_dtype: torch.dtype = torch.float16,
                 prompt: str = "digital art",
                 num_inference_steps: int = 50,
                 use_auth_token: bool = True,


                 ):
        self.model_id = model_id
        self.revision = revision
        self.torch_dtype = torch_dtype
        self.prompt = prompt
        self.num_inference_steps = num_inference_steps
        self.use_auth_token = use_auth_token

        if self.use_auth_token:
            auth_hugging_face()

    def load_model_pipeline(self) -> StableDiffusionPipeline:
        return StableDiffusionPipeline.from_pretrained(self.model_id,
                                                       revision=self.revision,
                                                       torch_dtype=self.torch_dtype,
                                                       use_auth_token=self.use_auth_token).to("cuda")

    def run(self, input_path: str, output_path: str):
        verses = parse_lyrics(input_path, self.prompt)
        pipe = self.load_model_pipeline()

        try:
            os.mkdir(output_path)
        except FileExistsError:
            logging.info(f"Folder {output_path} already exists. Using it to store the images ...")

        with autocast("cuda"):
            for idx, verse in enumerate(verses):
                image = pipe(verse, num_inference_steps=self.num_inference_steps)["sample"][0]
                image.save(f"{output_path}/{idx}.png")
