import flet as ft

class CustomStatsWidget(ft.Column):
    def __init__(self, text1: str, text2: str):
        super().__init__()
        self.text1 = text1
        self.text2 = text2

    def build(self):
        # Create a column with two text widgets inside
        column = ft.Column(
            [
                ft.Text(self.text1),
                ft.Text(self.text2),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        return ft.Container(
           border_radius=20,
            bgcolor='#000000',
            content=column,
            padding=ft.padding.all(10),
        )