import flet as ft

class CustomCard(ft.Column):
    def __init__(self, text1: str):
        super().__init__()
        self.text1 = text1

    def build(self):
        # Create a column with two text widgets inside
        text = ft.Text(self.text1)
        return ft.Container(
           border_radius=20,
           width=500,
           height=350,
            bgcolor='#000000',
            content=text,
            padding=ft.padding.all(10),
        )