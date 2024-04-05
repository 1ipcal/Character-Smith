from tkinter import *
from tkinter import ttk
from random import randint
import json

class Character:
    def __init__(self, root) -> None:
        self.root = root
        self.character_model = Character_Model()

        character_class_option = StringVar(root)
        character_race_option = StringVar(root)
        class_file = open('ASSETS\\CLASSES.txt', 'r')
        class_options = [line.strip() for line in class_file.readlines()]
        race_file = open('ASSETS\\RACES.txt', 'r')
        race_options = [line.strip() for line in race_file.readlines()]
        
        all_not_num_entry = []

        # create main frame
        main_frame = Frame(self.root)
        main_frame.pack()
        
        # create menu bar
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        
        file_menu = Menu(menu_bar, tearoff=0)
        clear_menu = Menu(file_menu, tearoff=0)
        clear_menu.add_command(label='Clear', command=self.nothing)
        clear_menu.add_command(label='Clear all', command=self.nothing)
        file_menu.add_cascade(label='Clear', menu=clear_menu)
        file_menu.add_separator()
        file_menu.add_command(label='Import', command=self.nothing)
        file_menu.add_command(label='Save as...', command=self.nothing)
        menu_bar.add_cascade(label='File', menu=file_menu)
        
        # create frame for character info
        character_info_frame = LabelFrame(main_frame, text="Character Information")
        character_info_frame.grid(row=0, column=0, columnspan=3)

        character_name_label = Label(character_info_frame, text='Name')
        character_name_entry = Entry(character_info_frame)

        character_class_label = Label(character_info_frame, text='Class')
        character_class_menu = OptionMenu(character_info_frame, character_class_option, *class_options)
        character_class_menu.config(width=10)

        character_level_label = Label(character_info_frame, text='Level')
        character_level_entry = Entry(character_info_frame, width=3)

        character_race_label = Label(character_info_frame, text='Race')
        character_race_menu = OptionMenu(character_info_frame, character_race_option, *race_options)
        character_race_menu.config(width=10)

        character_name_label.grid(row=0, column=0, sticky=W)
        character_name_entry.grid(row=1, column=0)
        character_name_entry.insert(0, 'Hero')
        # character_name_entry.config(state='disabled')
        character_name_button = Button(character_info_frame, text='Lock', command=lambda: self.lock_button(character_name_entry, character_name_button))
        character_name_button.grid(row=1, column=1)
        
        character_class_label.grid(row=0, column=2, sticky=W)
        character_class_menu.grid(row=1, column=2)

        character_race_label.grid(row=0, column=3, sticky=W)
        character_race_menu.grid(row=1, column=3)

        character_level_label.grid(row=0, column=4)
        character_level_entry.grid(row=1, column=4)

        # create frame for attributes
        attributes_frame = LabelFrame(main_frame, text='Attributes')
        attributes_frame.grid(row=1, column=0, columnspan=3)
        
        strength_box_label = Label(attributes_frame, text='Strength')
        self.strength_box = Entry(attributes_frame, width=5)
        strength_modifier = Label(attributes_frame, text='+0')
        strength_box_label.grid(row=0, column=0)
        self.strength_box.grid(row=1, column=0)
        strength_modifier.grid(row=2, column=0)

        dexterity_box_label = Label(attributes_frame, text='Dexterity')
        self.dexterity_box = Entry(attributes_frame, width=5)
        dexterity_modifier = Label(attributes_frame, text='+0')
        dexterity_box_label.grid(row=0, column=1)
        self.dexterity_box.grid(row=1, column=1)
        dexterity_modifier.grid(row=2, column=1)

        constitution_box_label = Label(attributes_frame, text='Constitution')
        self.constitution_box = Entry(attributes_frame, width=5)
        constitution_modifier = Label(attributes_frame, text='+0')
        constitution_box_label.grid(row=0, column=2)
        self.constitution_box.grid(row=1, column=2)
        constitution_modifier.grid(row=2, column=2)

        intelligence_box_label = Label(attributes_frame, text='Intelligence')
        self.intelligence_box = Entry(attributes_frame, width=5)
        intelligence_modifier = Label(attributes_frame, text='+0')
        intelligence_box_label.grid(row=0, column=3)
        self.intelligence_box.grid(row=1, column=3)
        intelligence_modifier.grid(row=2, column=3)

        wisdom_box_label = Label(attributes_frame, text='Wisdom')
        self.wisdom_box = Entry(attributes_frame, width=5)
        wisdom_modifier = Label(attributes_frame, text='+0')
        wisdom_box_label.grid(row=0, column=4)
        self.wisdom_box.grid(row=1, column=4)
        wisdom_modifier.grid(row=2, column=4)

        charisma_box_label = Label(attributes_frame, text='Charisma')
        self.charisma_box = Entry(attributes_frame, width=5)
        charisma_modifier = Label(attributes_frame, text='+0')
        charisma_box_label.grid(row=0, column=5)
        self.charisma_box.grid(row=1, column=5)
        charisma_modifier.grid(row=2, column=5)
        
        # create list of attributes for use in generate values
        self.attributes_list = [self.strength_box, self.dexterity_box, self.constitution_box,
                                self.intelligence_box, self.wisdom_box, self.charisma_box]

        # create health frame
        health_frame = Frame(main_frame)
        health_frame.grid(row=2, column=0, sticky='n')
        
        # Hitpoints Subframe
        hitpoints_frame = LabelFrame(health_frame, text='Hit Points')
        hitpoints_frame.grid(row=0, column=0, sticky='ew')
        
        max_hp_label = Label(hitpoints_frame, text='Max HP')
        max_hp_text = Entry(hitpoints_frame, width=10)
        max_hp_text.insert(0, '0')  # Default value
        current_hp_label = Label(hitpoints_frame, text='Current HP')
        current_hp_text = Entry(hitpoints_frame, width=20)
        current_hp_text.insert(0, '0')  # Default value
        max_hp_label.grid(row=0, column=0)
        max_hp_text.grid(row=1, column=0)
        current_hp_label.grid(row=0, column=1, columnspan=2)
        current_hp_text.grid(row=1, column=1, columnspan=2)

        # Armor Class, Speed, Initiative Subframe
        armour_class_label = Label(hitpoints_frame, text='Armor Class')
        armour_class_text = Entry(hitpoints_frame, width=10)
        armour_class_text.insert(0, '0')  # Default value
        initiative_label = Label(hitpoints_frame, text='Initiative')
        initiative_text = Entry(hitpoints_frame, width=10)
        initiative_text.insert(0, '0')  # Default value
        speed_label = Label(hitpoints_frame, text='Speed')
        speed_text = Entry(hitpoints_frame, width=10)
        speed_text.insert(0, '0')  # Default value
        armour_class_label.grid(row=2, column=0)
        armour_class_text.grid(row=3, column=0)
        initiative_label.grid(row=2, column=1)
        initiative_text.grid(row=3, column=1)
        speed_label.grid(row=2, column=2)
        speed_text.grid(row=3, column=2)

        # Saving Throws Subframe
        saving_throws_subframe = LabelFrame(health_frame, text='Saving Throws')
        saving_throws_subframe.grid(row=1, column=0, sticky='ew')

        saving_throws_strength = Checkbutton(saving_throws_subframe, text='Strength')
        saving_throws_dexterity = Checkbutton(saving_throws_subframe, text='Dexterity')
        saving_throws_constitution = Checkbutton(saving_throws_subframe, text='Constitution')
        saving_throws_intelligence = Checkbutton(saving_throws_subframe, text='Intelligence')
        saving_throws_wisdom = Checkbutton(saving_throws_subframe, text='Wisdom')
        saving_throws_charisma = Checkbutton(saving_throws_subframe, text='Charisma')
        saving_throws_strength.grid(row=0, column=0, sticky='w')
        saving_throws_dexterity.grid(row=1, column=0, sticky='w')
        saving_throws_constitution.grid(row=2, column=0, sticky='w')
        saving_throws_intelligence.grid(row=3, column=0, sticky='w')
        saving_throws_wisdom.grid(row=4, column=0, sticky='w')
        saving_throws_charisma.grid(row=5, column=0, sticky='w')

        # Hit Dice Subframe
        hit_dice_subframe = LabelFrame(health_frame, text='Hit Dice')
        hit_dice_subframe.grid(row=2, column=0, sticky='ew')

        hit_dice_label = Label(hit_dice_subframe, text='Hit Dice')
        hit_dice_text = Entry(hit_dice_subframe, width=16)
        hit_dice_text.insert(0, '0')  # Default value
        hit_dice_total_label = Label(hit_dice_subframe, text='Total')
        hit_dice_total_text = Entry(hit_dice_subframe, width=16)
        hit_dice_total_text.insert(0, '0')  # Default value
        hit_dice_label.grid(row=0, column=0)
        hit_dice_text.grid(row=1, column=0)
        hit_dice_total_label.grid(row=0, column=1)
        hit_dice_total_text.grid(row=1, column=1)

        # Death Saves Subframe
        death_saves_subframe = LabelFrame(health_frame, text='Death Saves')
        death_saves_subframe.grid(row=3, column=0, sticky='ew')

        success_label = Label(death_saves_subframe, text='Successes')
        failure_label = Label(death_saves_subframe, text='Failures')
        success_label.grid(row=0, column=0, sticky='w')
        failure_label.grid(row=1, column=0, sticky='w')

        successes_checkboxes = []  # Variable to store the success checkboxes
        for i in range(3):
            success = Checkbutton(death_saves_subframe)
            success.grid(row=0, column=i+1)
            successes_checkboxes.append(success)

        failure_checkboxes = [] # Variable to store the failures checkboxes
        for i in range(3):
            failure = Checkbutton(death_saves_subframe)
            failure.grid(row=1, column=i+1)
            failure_checkboxes.append(failure)

        # create spell button that will open a new window
        spell_button = Button(health_frame, text='Spells', bg='azure2', command=lambda: self.open_spell_window())
        spell_button.grid(row=4, column=0, sticky='ew')

        # End of Health Frame
        
        # Create Weapon Attacks & Abilities Subframe
        weapon_attacks_subframe = LabelFrame(main_frame, text='Weapon Attacks & Abilities')
        weapon_attacks_subframe.grid(row=2, column=1, sticky='ns')

        # Create weapon frame
        attack_frame = LabelFrame(weapon_attacks_subframe, text='Weapon Attacks & Abilities')
        attack_frame.grid(row=0, column=0)

        # Create table headers
        headers = ["Name", "Bonus to Hit", "Damage"]
        for i, header in enumerate(headers):
            label = Label(weapon_attacks_subframe, text=header)
            label.grid(row=0, column=i)

        # Create table rows
        table_rows = 5
        entries = []  # This list will hold all the entry fields
        for i in range(1, table_rows + 1):
            row_entries = []  # This list will hold the entries for a single row
            for j in range(3):
                entry = Entry(weapon_attacks_subframe, width=17)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
                all_not_num_entry.append(entry)
            entries.append(row_entries)

        abilities_box = Text(weapon_attacks_subframe, width=40, height=20)
        abilities_box.grid(row=table_rows + 1, column=0, columnspan=3)

        # End of Weapon Attacks & Abilities Subframe

        # create inventory frame
        inventory_frame = LabelFrame(main_frame, text='Inventory')
        inventory_frame.grid(row=3, column=1, sticky='n')

        # create inventory box
        inventory_box = Text(inventory_frame, width=40, height=15, wrap='none')  # Set wrap to 'none' to enable horizontal scrolling
        inventory_box.grid(row=0, column=0, sticky='ew')

        # create horizontal scrollbar
        xscrollbar = Scrollbar(inventory_frame, orient='horizontal', command=inventory_box.xview)
        xscrollbar.grid(row=1, column=0, sticky='ew')
        inventory_box['xscrollcommand'] = xscrollbar.set
        
        # end of inventory subframe

        # create skills frame
        skills_frame = LabelFrame(main_frame, text='Skills')
        skills_frame.grid(row=2, column=2, sticky='new')

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
        
        # create proficiencies frame
        proficiencies_frame = LabelFrame(main_frame, text='Other Proficiencies')
        proficiencies_frame.grid(row=3, column=2)

        # create a subframe inside the proficiencies frame
        proficiencies_subframe = Frame(proficiencies_frame)
        proficiencies_subframe.grid(row=0, column=0)
        prof_xscroll = Scrollbar(proficiencies_subframe, orient='horizontal')
        prof_xscroll.grid(row=1, column=0, sticky='nsew')

        # text box
        proficiencies_box = Text(proficiencies_subframe, width=30, height=15, xscrollcommand=prof_xscroll.set)
        prof_xscroll.config(command=proficiencies_box.xview)
        proficiencies_box.config(undo=True, wrap=NONE)
        proficiencies_box.grid(row=0, column=0)

        # end of proficiencies frame

        for widget in character_info_frame.winfo_children():
            widget.grid_configure(padx=3)
        
        for widget in attributes_frame.winfo_children():
            widget.grid_configure(padx=3)    

    def nothing(self):
        pass

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
    
    def generate_attributes(self):
        # run 6 times, one for each box. skip box if it is disabled
        for attribute in self.attributes_list:
            if attribute.cget('state') == 'normal':
                # roll 4 dice, save 3 highest
                temp_dice = []
                for i in range(4):
                    temp_dice.append(randint(1, 6))
                # remove the lowest value
                temp_dice.remove(min(temp_dice))
                
                # get total sum of dice
                total = sum(temp_dice)
                # we need to do a check for the race so that it gets added properly
                # possibly have a variable for each attribute so that we can add it
                # to the race modifier and then update the total
                attribute.config(text=str(total))
                
                # also need to run the modifier

    def open_spell_window(self):
        add_spell_window = Toplevel(self.root)
        add_spell_window.title('Add Spell')
        add_spell_window.geometry('400x400')

        spell_name_label = Label(add_spell_window, text='Spell Name')
        spell_name_textbox = Text(add_spell_window, height=20, width=40)  # Adjust height and width as needed
        spell_name_label.grid(row=0, column=0)
        spell_name_textbox.grid(row=1, column=0)
        

class Character_Model:
    def __init__(self) -> None:
        self.character_name = ""
        self.character_class = ""
        self.race = ""
        self.level = 0
        self.attributes = {
            'strength': 0,
            'dexterity': 0,
            'constitution': 0,
            'intelligence': 0,
            'wisdom': 0,
            'charisma': 0
        }
        self.hitpoints = {
            'max': 0,
            'current': 0
        }
        self.armor_class = 0
        self.initiative = 0
        self.speed = 0
        self.saving_throws = {
            'strength': False,
            'dexterity': False,
            'constitution': False,
            'intelligence': False,
            'wisdom': False,
            'charisma': False
        }
        self.hit_dice = {
            'total': 0,
            'current': 0
        }
        self.death_saves = {
            'successes': 0,
            'failures': 0
        }
        # Weapon attacks will be in a form of a list of dictionaries
        # Example: [{'name': 'Sword', 'bonus_to_hit': 5, 'damage': '1d6 + 3'}, ...]
        self.weapon_attacks = []
        self.abilities = ""
        self.skills = {
            'acrobatics': False,
            'animal_handling': False,
            'arcana': False,
            'athletics': False,
            'deception': False,
            'history': False,
            'insight': False,
            'intimidation': False,
            'investigation': False,
            'medicine': False,
            'nature': False,
            'perception': False,
            'performance': False,
            'persuation': False,
            'religion': False,
            'sleight_of_hand': False,
            'stealth': False,
            'survival': False
        }
        self.other_proficiencies = ""
        self.inventory = ""

    # Saving Data (instance attributes) to a JSON file. 
    # This will be used to save the Character Model
    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        instance = cls()
        instance.__dict__ = json.loads(json_str)
        return instance

if __name__ == '__main__':
    root = Tk()
    root.title('Character Smith')
    root.geometry('800x1000')
    # root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

    character = Character(root)

    # JSON FILE TEST
    # with open('character.json', 'w') as f:
    #     f.write(character.character_model.to_json())
    # 
    # with open('character.json', 'r') as f:
    #     json_str = f.read()
    #     loaded_character = character.character_model.from_json(json_str)
    #     character.character_model = loaded_character
    # 
    # print("Level: " + str(character.character_model.level))

    print('Running...')

    root.mainloop()
