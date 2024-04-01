from tkinter import *
from tkinter import ttk

class Character:
    def __init__(self, root) -> None:
        self.root = root
        option = StringVar(root)
        class_file = open('ASSETS\CLASSES.txt', 'r')
        class_options = [line for line in class_file.readlines()]
        race_file = open('ASSETS\RACES.txt', 'r')
        race_options = [line for line in race_file.readlines()]

        # create main frame
        frame = Frame(self.root)
        frame.pack()
        
        # create frame for character info
        character_info_frame = LabelFrame(frame, text="Character Information")
        character_info_frame.grid(row=0, column=0, columnspan=3)

        character_name_label = Label(character_info_frame, text='Name')
        character_name_entry = Entry(character_info_frame)

        character_class_label = Label(character_info_frame, text='Class')
        character_class_menu = OptionMenu(character_info_frame, option, *class_options)

        character_level_label = Label(character_info_frame, text='Level')
        character_level_entry = Entry(character_info_frame, width=3)

        character_race_label = Label(character_info_frame, text='Race')
        character_race_entry = Entry(character_info_frame)

        character_name_label.grid(row=0, column=0, sticky=W)
        character_name_entry.grid(row=1, column=0)
        character_name_entry.insert(0, 'Hero')
        # character_name_entry.config(state='disabled')
        character_name_button = Button(character_info_frame, text='Lock', command=lambda: self.lock_button(character_name_entry, character_name_button))
        character_name_button.grid(row=1, column=1)
        
        character_class_label.grid(row=0, column=2, sticky=W)
        character_class_menu.grid(row=1, column=2)

        character_race_label.grid(row=0, column=3, sticky=W)
        character_race_entry.grid(row=1, column=3)

        character_level_label.grid(row=0, column=4)
        character_level_entry.grid(row=1, column=4)

        # create frame for attributes
        attributes_frame = LabelFrame(frame, text='Attributes')
        attributes_frame.grid(row=1, column=0, columnspan=3)
        
        strength_box_label = Label(attributes_frame, text='Strength')
        strength_box = Entry(attributes_frame, width=5)
        strength_box_label.grid(row=0, column=0)
        strength_box.grid(row=1, column=0)

        dexterity_box_label = Label(attributes_frame, text='Dexterity')
        dexterity_box = Entry(attributes_frame, width=5)
        dexterity_box_label.grid(row=0, column=1)
        dexterity_box.grid(row=1, column=1)

        constitution_box_label = Label(attributes_frame, text='Constitution')
        constitution_box = Entry(attributes_frame, width=5)
        constitution_box_label.grid(row=0, column=2)
        constitution_box.grid(row=1, column=2)

        intelligence_box_label = Label(attributes_frame, text='Intelligence')
        intelligence_box = Entry(attributes_frame, width=5)
        intelligence_box_label.grid(row=0, column=3)
        intelligence_box.grid(row=1, column=3)

        wisdom_box_label = Label(attributes_frame, text='Wisdom')
        wisdom_box = Entry(attributes_frame, width=5)
        wisdom_box_label.grid(row=0, column=4)
        wisdom_box.grid(row=1, column=4)

        charisma_box_label = Label(attributes_frame, text='Charisma')
        charisma_box = Entry(attributes_frame, width=5)
        charisma_box_label.grid(row=0, column=5)
        charisma_box.grid(row=1, column=5)
        
        # create health frame
        health_frame = Frame(frame)
        health_frame.grid(row=2, column=0)
        
        hitpoints_label = Label(health_frame, text='Hit Points')
        hitpoints_label.grid(row=0, column=0)

        # create weapon frame
        attack_frame = LabelFrame(frame, text='Attacks & Spellcasting')
        attack_frame.grid(row=2, column=1)
        attack_box = Text(attack_frame, width=50)
        attack_box.grid(row=0, column=0)

        # create skills frame
        skills_frame = LabelFrame(frame, text='Skills')
        skills_frame.grid(row=2, column=2)

        acrobatics_check = Checkbutton(skills_frame, text='Acrobatics')
        acrobatics_check.grid(row=0, column=0, sticky='w')
        animalhandling_check = Checkbutton(skills_frame, text='Animal Handling')
        animalhandling_check.grid(row=1, column=0, sticky='w')
        arcana_check = Checkbutton(skills_frame, text='Arcana')
        arcana_check.grid(row=2, column=0, sticky='w')
        athletics_check = Checkbutton(skills_frame, text='Athletics')
        athletics_check.grid(row=3, column=0, sticky='w')
        deception_check = Checkbutton(skills_frame, text='Deception')
        deception_check.grid(row=4, column=0, sticky='w')
        history_check = Checkbutton(skills_frame, text='History')
        history_check.grid(row=5, column=0, sticky='w')
        insight_check = Checkbutton(skills_frame, text='Insight')
        insight_check.grid(row=6, column=0, sticky='w')
        intimidation_check = Checkbutton(skills_frame, text='Intimidation')
        intimidation_check.grid(row=7, column=0, sticky='w')
        investigation_check = Checkbutton(skills_frame, text='Investigation')
        investigation_check.grid(row=8, column=0, sticky='w')
        medicine_check = Checkbutton(skills_frame, text='Medicine')
        medicine_check.grid(row=9, column=0, sticky='w')
        nature_check = Checkbutton(skills_frame, text='Nature')
        nature_check.grid(row=10, column=0, sticky='w')
        perception_check = Checkbutton(skills_frame, text='Perception')
        perception_check.grid(row=11, column=0, sticky='w')
        performance_check = Checkbutton(skills_frame, text='Performance')
        performance_check.grid(row=12, column=0, sticky='w')
        persuasion_check = Checkbutton(skills_frame, text='Persuasion')
        persuasion_check.grid(row=13, column=0, sticky='w')
        religion_check = Checkbutton(skills_frame, text='Religion')
        religion_check.grid(row=14, column=0, sticky='w')
        sleight_check = Checkbutton(skills_frame, text='Sleight of Hand')
        sleight_check.grid(row=15, column=0, sticky='w')
        stealth_check = Checkbutton(skills_frame, text='Stealth')
        stealth_check.grid(row=16, column=0, sticky='w')
        survival_check = Checkbutton(skills_frame, text='Survival')
        survival_check.grid(row=17, column=0, sticky='w')

        for widget in character_info_frame.winfo_children():
            widget.grid_configure(padx=3)
        
        for widget in attributes_frame.winfo_children():
            widget.grid_configure(padx=3)

    def lock_button(self, entry, button):
        # if button is enabled, disabled it and recess it. otherwise do the opposite
        if entry.cget('state') == 'normal':
            entry.config(state='disabled')
            button.config(relief=SUNKEN)
        else:
            entry.config(state='normal')
            button.config(relief=RAISED)
    
    def determine_modifier(self, score):
        if score % 2 != 0:
            score -= 1
        
        modifier = (score - 10) / 2

        if modifier >= 0:
            return '+' + str(modifier)
        return str(modifier)

if __name__ == '__main__':
    root = Tk()
    root.title('Character Smith')
    root.geometry('800x1000')
    # root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

    character = Character(root)

    root.mainloop()
