# Inpainting

class Inpaint:
    def __init__(self, inpainting_prompt):
        self.inpainting_prompt = inpainting_prompt

    def inpaint_image(self):
        inpainting_prompt_values = "".join(self.inpainting_prompt)

        print("---------- inpainting_prompt ----------")
        print(inpainting_prompt_values)