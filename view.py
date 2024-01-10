from controller import Daytime

class Menu:

    def menu(self, daytime: Daytime) -> None:
        while True:
            try:
                print(f'\033[1;42m{"MAIN MENU":^79}\033[m')
                opt = int(input('[1] INSERT HOURS\n[2] READ WHOLE DATABASE\n[3] READ ONE WEEK\n[4] DELETE DATA\n[5] EXIT\nChoose your option: '))
                assert opt >= 1 and opt <= 5
            except:
                print('\033[31mINVALID OPTION\033[m')
            else:
                if opt == 1:
                    daytime.hours()
                elif opt == 2:
                    daytime.read_db()
                elif opt == 3:
                    daytime.read_week()
                elif opt == 4:
                    daytime.deleting_values()
                elif opt == 5:
                    print('See you soon...')
                    break


daytime = Daytime()
menu = Menu()
menu.menu(daytime)
