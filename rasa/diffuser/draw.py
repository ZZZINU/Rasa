# Drawing

class Draw:
    def __init__(self, drawing_object, drawing_prompt):
        self.drawing_object = drawing_object
        self.drawing_prompt = drawing_prompt

    def draw_image(self):
        drawing_object_values = "".join(self.drawing_object)
        drawing_prompt_values = "".join(self.drawing_prompt)

        print("---------- drawing_object ----------")
        print(drawing_object_values)
        print("---------- drawing_prompt ----------")
        print(drawing_prompt_values)