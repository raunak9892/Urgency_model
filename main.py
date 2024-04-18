import flet as ft

from classifier import urgency
from custom_stats_widget import CustomStatsWidget
from custom_card import CustomCard
from temp import run_model
from two import get_emails, label




def main(page: ft.Page):

  def fetching_emails(e):
    print("Fetching Emails")
    emails = get_emails()
    urgency()
    run_model()
    label()


    

  def handle_avatar_tap(e):
    print("Circle Avatar clicked")

  page.bgcolor='#ffffff'
  # Create the AppBar with Text and CircleAvatar
  app_bar = ft.AppBar(
    title=ft.Text("FilterPro"),
    bgcolor='#ffffff',
    actions=[
        
        ft.GestureDetector(
          on_tap=handle_avatar_tap,
          content=ft.Container(padding=ft.padding.only(right=20),content=ft.CircleAvatar(bgcolor='#D9D9D9')),
        )
    ]
  )

  listView = ft.ListView(
    [
      ft.Row(
        [
          CustomStatsWidget(text1='Unread important mails',text2='7'),
          CustomStatsWidget(text1='Spam Mails Detected',text2='7'),
          CustomStatsWidget(text1='Total Unread Mails',text2='7'),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
      ),
      
      ft.Row(
        [
          CustomCard(text1='Spam Mails'),
          CustomCard(text1='Important Mails'),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
      ),
      ft.GestureDetector(
          on_tap=fetching_emails,
          content=ft.Container(padding=ft.padding.only(right=20),content=ft.CircleAvatar(bgcolor=ft.colors.RED)),
        )
    ],
    spacing=20,
  )

  # Divider
  divider = ft.Divider()

  # Row to hold the 3 sections
#   row1 = ft.Row(
#     [
#       ft.Container(
#         content=ft.Text("Unread Important Mails"),
#         padding=10,
#       ),
#       ft.Container(
#         content=ft.Text("Span Mails Detected"),
#         padding=10,
#       ),
#       ft.Container(
#         content=ft.Text("Total Unread Mails"),
#         padding=10,
#       ),
#     ],
#   )

#   # Row to hold the 2 sections
#   row2 = ft.Row(

#     [
#       ft.Container(
#         content=ft.Text("Spam Mails"),
#         width=300,
#         height=200,
#         padding=10,
#       ),
#       ft.Container(
#         content=ft.Text("Important Mails"),
#         width=300,
#         height=200,
#         padding=10,
#       ),
#     ],
#   )

  # Add all the widgets to the page
  page.add(app_bar, divider,listView)

ft.app(target=main)