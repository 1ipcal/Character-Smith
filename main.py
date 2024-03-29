from tkinter import *

class Character:
    def __init__(self, root) -> None:
        self.root = root
        option = StringVar(root)
        class_file = open('ASSETS\CLASSES.txt', 'r')
        class_options = [line for line in class_file.readlines()]
        race_file = open('ASSETS\RACES.txt', 'r')
        race_options = [line for line in race_file.readlines()]

        character_name_label = Label(self.root, text='Name')
        character_name_entry = Entry(self.root)

        character_class_label = Label(self.root, text='Class')
        character_class_menu = OptionMenu(self.root, option, *class_options)

        character_level_label = Label(self.root, text='Level')
        character_level_entry = Entry(self.root)

        character_race_label = Label(self.root, text='Race')
        character_race_entry = Entry(self.root)

        character_name_label.pack()
        character_name_entry.pack()
        character_name_entry.insert(0, 'Hero')
        # character_name_entry.config(state='disabled')
        character_name_button = Button(self.root, text='Lock', command=lambda: self.lock_button(character_name_entry, character_name_button))
        character_name_button.pack()
        
        character_class_label.pack()
        character_class_menu.pack()

    def lock_button(self, entry, button):
        # if button is enabled, disabled it and recess it. otherwise do the opposite
        if entry.cget('state') == 'normal':
            entry.config(state='disabled')
            button.config(relief=SUNKEN)
        else:
            entry.config(state='normal')
            button.config(relief=RAISED)

if __name__ == '__main__':
    root = Tk()
    root.title('Character Smith')
    root.geometry('800x1000')
    root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

    character = Character(root)

    root.mainloop()
