import ClientMenu

client_menu = ClientMenu.ClientMenu()

while True:
    client_menu.print_menu()
    choice = int(input("Enter your choice: "))
    client_menu.act_by_user_choice(choice)
