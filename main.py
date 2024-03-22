from tkinter import *

class Character:
    def __init__(self, root) -> None:
        self.root = root
        character_name_label = Label(self.root, text='Name')
        character_name_entry = Entry(self.root)

        character_class_label = Label(self.root, text='Class')
        character_class_entry = Entry(self.root)

        character_level_label = Label(self.root, text='Level')
        character_level_entry = Entry(self.root)

        character_race_label = Label(self.root, text='Race')
        character_race_entry = Entry(self.root)

        character_name_label.pack()
        character_name_entry.pack()
        character_name_entry.insert(0, 'Hero')
        character_name_entry.config(state='disabled')
        
        character_class_label.pack()
        character_class_entry.pack()

if __name__ == '__main__':
    root = Tk()
    root.title('Character Smith')
    root.geometry('800x1000')
    root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

    character = Character(root)

    root.mainloop()