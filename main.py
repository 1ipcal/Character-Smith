from tkinter import *
from tkinter import ttk, filedialog, messagebox
from random import randint
import jsonschema
from jsonschema import validate
from schemas import character_model_schema
from model_to_gui import convert_model_to_gui
from gui_to_model import convert_gui_to_model
import character_model
import json
import csv


class Character:
    def __init__(self, root) -> None:
        """
        Initialize the character sheet creator GUI
        """
        self.root = root
        self.character_model = character_model.Character_Model()

        # File path for character race and class options
        self.character_class_option = StringVar(root)
        self.character_race_option = StringVar(root)

        class_file = open('./ASSETS/CLASSES.txt', 'r')
        class_options = [line.strip() for line in class_file.readlines()]
        race_file = open('./ASSETS/RACES.txt', 'r')
        race_options = [line.strip() for line in race_file.readlines()]

        self.race_default_dict = self.parse_race_default_csv(
            './ASSETS/RACES_DEFAULT.csv')
        self.class_default_dict = self.parse_class_default_csv(
            './ASSETS/CLASSES_DEFAULT.csv')

        # create variables for all checkboxes
        # saving throws
        self.st_strength_var = BooleanVar()
        self.st_dexterity_var = BooleanVar()
        self.st_constitution_var = BooleanVar()
        self.st_intelligence_var = BooleanVar()
        self.st_wisdom_var = BooleanVar()
        self.st_charisma_var = BooleanVar()

        # success and fail
        self.success_var_1 = BooleanVar()
        self.success_var_2 = BooleanVar()
        self.success_var_3 = BooleanVar()
        self.fail_var_1 = BooleanVar()
        self.fail_var_2 = BooleanVar()
        self.fail_var_3 = BooleanVar()

        # skills
        self.acrobatics_var = BooleanVar()
        self.animal_handling_var = BooleanVar()
        self.arcana_var = BooleanVar()
        self.athletics_var = BooleanVar()
        self.deception_var = BooleanVar()
        self.history_var = BooleanVar()
        self.insight_var = BooleanVar()
        self.intimidation_var = BooleanVar()
        self.investigation_var = BooleanVar()
        self.medicine_var = BooleanVar()
        self.nature_var = BooleanVar()
        self.perception_var = BooleanVar()
        self.performance_var = BooleanVar()
        self.persuasion_var = BooleanVar()
        self.religion_var = BooleanVar()
        self.sleight_var = BooleanVar()
        self.stealth_var = BooleanVar()
        self.survival_var = BooleanVar()

        """The following scrollbar code is adapted from Codemy: 
        https://www.youtube.com/watch?v=0WafQCaok6g
        """
        # create root frame (this is to house the canvas
        # and the frame within the canvas)
        root_frame = Frame(self.root)
        root_frame.pack(fill=BOTH, expand=1)

        # create canvas to house scrollbar
        main_canvas = Canvas(root_frame)
        main_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # create vertical scrollbar
        vertical_scroll = Scrollbar(
            root_frame, orient=VERTICAL, command=main_canvas.yview)
        vertical_scroll.pack(side=RIGHT, fill=Y)

        # configure canvas with scrollbars
        main_canvas.configure(yscrollcommand=vertical_scroll.set)
        main_canvas.bind('<Configure>', lambda e: main_canvas.configure(
            scrollregion=main_canvas.bbox("all")))

        # create main frame
        main_frame = Frame(main_canvas)
        main_canvas.create_window(
            (0, 0), window=main_frame, anchor="center", tags="main_frame")
        """End of Codemy code"""

        # create menu bar
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        clear_menu = Menu(file_menu, tearoff=0)
        clear_menu.add_command(label='Clear all', command=self.clear_all)
        file_menu.add_cascade(label='Clear', menu=clear_menu)
        file_menu.add_separator()
        file_menu.add_command(label='Import', command=self.import_character)
        file_menu.add_command(label='Save as...', command=self.save_character)
        menu_bar.add_cascade(label='File', menu=file_menu)

        # create frame for character info
        character_info_frame = LabelFrame(
            main_frame, text="Character Information")
        character_info_frame.grid(row=0, column=0, columnspan=3)

        character_name_label = Label(character_info_frame, text='Name')
        self.character_name_entry = Entry(character_info_frame)

        character_class_label = Label(character_info_frame, text='Class')
        character_class_menu = OptionMenu(
            character_info_frame, self.character_class_option, *class_options, command=self.load_default_class_values)
        character_class_menu.config(width=10)

        character_level_label = Label(character_info_frame, text='Level')
        self.character_level_entry = Entry(character_info_frame, width=3,
                                 validatecommand=lambda: self.validate_hit_points(
                                     self.character_level_entry),
                                 validate='focusout')
        self.character_level_entry.insert(0, '1')

        character_race_label = Label(character_info_frame, text='Race')
        character_race_menu = OptionMenu(
            character_info_frame, self.character_race_option, *race_options, command=self.load_default_race_values)
        character_race_menu.config(width=10)

        character_name_label.grid(row=0, column=0, sticky=W)
        self.character_name_entry.grid(row=1, column=0)
        self.character_name_entry.insert(0, '')

        character_class_label.grid(row=0, column=2, sticky=W)
        character_class_menu.grid(row=1, column=2)

        character_race_label.grid(row=0, column=3, sticky=W)
        character_race_menu.grid(row=1, column=3)

        character_level_label.grid(row=0, column=4)
        self.character_level_entry.grid(row=1, column=4)

        # create frame for attributes
        attributes_frame = LabelFrame(main_frame, text='Attributes')
        attributes_frame.grid(row=1, column=0, columnspan=3)

        strength_box_label = Label(attributes_frame, text='Strength')
        self.strength_box = Entry(attributes_frame, width=5,
                                  validatecommand=lambda: self.validate_attribute(
                                      self.strength_box, self.strength_modifier),
                                  validate='focusout')
        self.strength_modifier = Label(attributes_frame, text='+0')
        strength_box_label.grid(row=0, column=0)
        self.strength_box.grid(row=1, column=0)
        self.strength_modifier.grid(row=2, column=0)

        dexterity_box_label = Label(attributes_frame, text='Dexterity')
        self.dexterity_box = Entry(attributes_frame, width=5,
                                   validatecommand=lambda: self.validate_attribute(
                                       self.dexterity_box, self.dexterity_modifier),
                                   validate='focusout')
        self.dexterity_modifier = Label(attributes_frame, text='+0')
        dexterity_box_label.grid(row=0, column=1)
        self.dexterity_box.grid(row=1, column=1)
        self.dexterity_modifier.grid(row=2, column=1)

        constitution_box_label = Label(attributes_frame, text='Constitution')
        self.constitution_box = Entry(attributes_frame, width=5,
                                      validatecommand=lambda: self.validate_attribute(
                                          self.constitution_box, self.constitution_modifier),
                                      validate='focusout')
        self.constitution_modifier = Label(attributes_frame, text='+0')
        constitution_box_label.grid(row=0, column=2)
        self.constitution_box.grid(row=1, column=2)
        self.constitution_modifier.grid(row=2, column=2)

        intelligence_box_label = Label(attributes_frame, text='Intelligence')
        self.intelligence_box = Entry(attributes_frame, width=5,
                                      validatecommand=lambda: self.validate_attribute(
                                          self.intelligence_box, self.intelligence_modifier),
                                      validate='focusout')
        self.intelligence_modifier = Label(attributes_frame, text='+0')
        intelligence_box_label.grid(row=0, column=3)
        self.intelligence_box.grid(row=1, column=3)
        self.intelligence_modifier.grid(row=2, column=3)

        wisdom_box_label = Label(attributes_frame, text='Wisdom')
        self.wisdom_box = Entry(attributes_frame, width=5,
                                validatecommand=lambda: self.validate_attribute(
                                    self.wisdom_box, self.wisdom_modifier),
                                validate='focusout')
        self.wisdom_modifier = Label(attributes_frame, text='+0')
        wisdom_box_label.grid(row=0, column=4)
        self.wisdom_box.grid(row=1, column=4)
        self.wisdom_modifier.grid(row=2, column=4)

        charisma_box_label = Label(attributes_frame, text='Charisma')
        self.charisma_box = Entry(attributes_frame, width=5,
                                  validatecommand=lambda: self.validate_attribute(
                                      self.charisma_box, self.charisma_modifier),
                                  validate='focusout')
        self.charisma_modifier = Label(attributes_frame, text='+0')
        charisma_box_label.grid(row=0, column=5)
        self.charisma_box.grid(row=1, column=5)
        self.charisma_modifier.grid(row=2, column=5)

        genereate_attributes_button = Button(
            attributes_frame, text='Generate Attributes', command=self.generate_attributes)
        genereate_attributes_button.grid(row=3, column=2, columnspan=2)

        # create list of attributes for use in generate values
        self.attributes_list = [self.strength_box, self.dexterity_box, self.constitution_box,
                                self.intelligence_box, self.wisdom_box, self.charisma_box]

        # create list of modifiers for use in generative values
        self.modifiers_list = [self.strength_modifier, self.dexterity_modifier, self.constitution_modifier,
                               self.intelligence_modifier, self.wisdom_modifier, self.charisma_modifier]

        # create health frame
        health_frame = Frame(main_frame)
        health_frame.grid(row=2, column=0, sticky='n')

        # Hitpoints Subframe
        hitpoints_frame = LabelFrame(health_frame, text='Hit Points')
        hitpoints_frame.grid(row=0, column=0, sticky='ew')

        max_hp_label = Label(hitpoints_frame, text='Max HP')
        self.max_hp_text = Entry(hitpoints_frame, width=10,
                                 validatecommand=lambda: self.validate_hit_points(
                                     self.max_hp_text),
                                 validate='focusout')
        self.max_hp_text.insert(0, '0')  # Default value
        current_hp_label = Label(hitpoints_frame, text='Current HP')
        self.current_hp_text = Entry(hitpoints_frame, width=20,
                                     validatecommand=lambda: self.validate_hit_points(
                                         self.current_hp_text),
                                     validate='focusout')
        self.current_hp_text.insert(0, '0')  # Default value
        max_hp_label.grid(row=0, column=0)
        self.max_hp_text.grid(row=1, column=0)
        current_hp_label.grid(row=0, column=1, columnspan=2)
        self.current_hp_text.grid(row=1, column=1, columnspan=2)

        # Armor Class, Speed, Initiative Subframe
        armour_class_label = Label(hitpoints_frame, text='Armor Class')
        self.armour_class_text = Entry(hitpoints_frame, width=10,
                                       validatecommand=lambda: self.validate_hit_points(
                                           self.armour_class_text),
                                       validate='focusout')
        self.armour_class_text.insert(0, '0')  # Default value
        initiative_label = Label(hitpoints_frame, text='Initiative')
        self.initiative_text = Entry(hitpoints_frame, width=10,
                                     validatecommand=lambda: self.validate_hit_points(
                                         self.initiative_text),
                                     validate='focusout')
        self.initiative_text.insert(0, '0')  # Default value
        speed_label = Label(hitpoints_frame, text='Speed')
        self.speed_text = Entry(hitpoints_frame, width=10,
                                validatecommand=lambda: self.validate_hit_points(
                                    self.speed_text),
                                validate='focusout')
        self.speed_text.insert(0, '0')  # Default value

        armour_class_label.grid(row=2, column=0)
        self.armour_class_text.grid(row=3, column=0)
        initiative_label.grid(row=2, column=1)
        self.initiative_text.grid(row=3, column=1)
        speed_label.grid(row=2, column=2)
        self.speed_text.grid(row=3, column=2)

        # create list for all non-negative integer values
        # this will be used for error-checking on save
        self.all_pos_int_entries = [self.max_hp_text, self.current_hp_text, self.armour_class_text,
                                    self.initiative_text, self.speed_text]

        # Saving Throws Subframe
        saving_throws_subframe = LabelFrame(health_frame, text='Saving Throws')
        saving_throws_subframe.grid(row=1, column=0, sticky='ew')

        self.saving_throws_strength_checkbox = Checkbutton(
            saving_throws_subframe, text='Strength', variable=self.st_strength_var)
        self.saving_throws_dexterity_checkbox = Checkbutton(
            saving_throws_subframe, text='Dexterity', variable=self.st_dexterity_var)
        self.saving_throws_constitution_checkbox = Checkbutton(
            saving_throws_subframe, text='Constitution', variable=self.st_constitution_var)
        self.saving_throws_intelligence_checkbox = Checkbutton(
            saving_throws_subframe, text='Intelligence', variable=self.st_intelligence_var)
        self.saving_throws_wisdom_checkbox = Checkbutton(
            saving_throws_subframe, text='Wisdom', variable=self.st_wisdom_var)
        self.saving_throws_charisma_checkbox = Checkbutton(
            saving_throws_subframe, text='Charisma', variable=self.st_charisma_var)

        self.saving_throws_strength_checkbox.grid(row=0, column=0, sticky='w')
        self.saving_throws_dexterity_checkbox.grid(row=1, column=0, sticky='w')
        self.saving_throws_constitution_checkbox.grid(
            row=2, column=0, sticky='w')
        self.saving_throws_intelligence_checkbox.grid(
            row=3, column=0, sticky='w')
        self.saving_throws_wisdom_checkbox.grid(row=4, column=0, sticky='w')
        self.saving_throws_charisma_checkbox.grid(row=5, column=0, sticky='w')

        # saving throws list
        self.saving_throws_list = [('Strength', self.st_strength_var),
                                   ('Dexterity', self.st_dexterity_var),
                                   ('Constitution', self.st_constitution_var),
                                   ('Intelligence', self.st_intelligence_var),
                                   ('Wisdom', self.st_wisdom_var),
                                   ('Charisma', self.st_charisma_var)]

        # Hit Dice Subframe
        hit_dice_subframe = LabelFrame(health_frame, text='Hit Dice')
        hit_dice_subframe.grid(row=2, column=0, sticky='ew')

        hit_dice_label = Label(hit_dice_subframe, text='Hit Dice')
        self.hit_dice_text = Entry(hit_dice_subframe, width=16)
        self.hit_dice_text.insert(0, 'd1')  # Default value
        hit_dice_total_label = Label(hit_dice_subframe, text='Total')
        self.hit_dice_total_text = Entry(hit_dice_subframe, width=16)
        self.hit_dice_total_text.insert(0, '0')  # Default value
        hit_dice_label.grid(row=0, column=0)
        self.hit_dice_text.grid(row=1, column=0)
        hit_dice_total_label.grid(row=0, column=1)
        self.hit_dice_total_text.grid(row=1, column=1)

        # Death Saves Subframe
        death_saves_subframe = LabelFrame(health_frame, text='Death Saves')
        death_saves_subframe.grid(row=3, column=0, sticky='ew')

        success_label = Label(death_saves_subframe, text='Successes')
        failure_label = Label(death_saves_subframe, text='Failures')
        success_label.grid(row=0, column=0, sticky='w')
        failure_label.grid(row=1, column=0, sticky='w')

        self.successes_checkboxes_value = []  # Variable to store the success checkboxes
        for i in range(3):
            var = BooleanVar()
            self.successes_checkboxes_value.append(var)

            success = Checkbutton(death_saves_subframe, variable=var)
            success.grid(row=0, column=i+1)

        self.failure_checkboxes_value = []  # Variable to store the failures checkboxes
        for i in range(3):
            var = BooleanVar()
            self.failure_checkboxes_value.append(var)

            failure = Checkbutton(death_saves_subframe, variable=var)
            failure.grid(row=1, column=i+1)

        # create spell button that will open a new window
        spell_button = Button(health_frame, text='Spells',
                              bg='azure2', command=lambda: self.open_spell_window())
        spell_button.grid(row=4, column=0, sticky='ew')

        # End of Health Frame

        # Create Weapon Attacks & Abilities Subframe
        weapon_attacks_subframe = LabelFrame(
            main_frame, text='Weapon Attacks & Abilities')
        weapon_attacks_subframe.grid(row=2, column=1, sticky='ns')

        # Create weapon frame
        attack_frame = LabelFrame(
            weapon_attacks_subframe, text='Weapon Attacks & Abilities')
        attack_frame.grid(row=0, column=0)

        # Create table headers
        headers = ["Name", "Bonus to Hit", "Damage"]
        for i, header in enumerate(headers):
            label = Label(weapon_attacks_subframe, text=header)
            label.grid(row=0, column=i)

        # Create table rows
        table_rows = 5
        self.weapon_entries = []  # This list will hold all the entry fields
        for i in range(1, table_rows + 1):
            row_entries = []  # This list will hold the entries for a single row
            for j in range(3):
                entry = Entry(weapon_attacks_subframe, width=17)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
            self.weapon_entries.append(row_entries)

        self.abilities_box = Text(weapon_attacks_subframe, width=40, height=20)
        self.abilities_box.grid(row=table_rows + 1, column=0, columnspan=3)

        # End of Weapon Attacks & Abilities Subframe

        # create inventory frame
        inventory_frame = LabelFrame(main_frame, text='Inventory')
        inventory_frame.grid(row=3, column=1, sticky='n')

        # create inventory box
        # Set wrap to 'none' to enable horizontal scrolling
        self.inventory_box = Text(
            inventory_frame, width=40, height=15, wrap='none')
        self.inventory_box.grid(row=0, column=0, sticky='ew')

        # create horizontal scrollbar
        xscrollbar = Scrollbar(
            inventory_frame, orient='horizontal', command=self.inventory_box.xview)
        xscrollbar.grid(row=1, column=0, sticky='ew')
        self.inventory_box['xscrollcommand'] = xscrollbar.set

        # end of inventory subframe

        # create skills frame
        skills_frame = LabelFrame(main_frame, text='Skills')
        skills_frame.grid(row=2, column=2, sticky='new')

        self.acrobatics_check = Checkbutton(
            skills_frame, text='Acrobatics', variable=self.acrobatics_var)
        self.animalhandling_check = Checkbutton(
            skills_frame, text='Animal Handling', variable=self.animal_handling_var)
        self.arcana_check = Checkbutton(
            skills_frame, text='Arcana', variable=self.arcana_var)
        self.athletics_check = Checkbutton(
            skills_frame, text='Athletics', variable=self.athletics_var)
        self.deception_check = Checkbutton(
            skills_frame, text='Deception', variable=self.deception_var)
        self.history_check = Checkbutton(
            skills_frame, text='History', variable=self.history_var)
        self.insight_check = Checkbutton(
            skills_frame, text='Insight', variable=self.insight_var)
        self.intimidation_check = Checkbutton(
            skills_frame, text='Intimidation', variable=self.intimidation_var)
        self.investigation_check = Checkbutton(
            skills_frame, text='Investigation', variable=self.investigation_var)
        self.medicine_check = Checkbutton(
            skills_frame, text='Medicine', variable=self.medicine_var)
        self.nature_check = Checkbutton(
            skills_frame, text='Nature', variable=self.nature_var)
        self.perception_check = Checkbutton(
            skills_frame, text='Perception', variable=self.perception_var)
        self.performance_check = Checkbutton(
            skills_frame, text='Performance', variable=self.performance_var)
        self.persuasion_check = Checkbutton(
            skills_frame, text='Persuasion', variable=self.persuasion_var)
        self.religion_check = Checkbutton(
            skills_frame, text='Religion', variable=self.religion_var)
        self.sleight_check = Checkbutton(
            skills_frame, text='Sleight of Hand', variable=self.sleight_var)
        self.stealth_check = Checkbutton(
            skills_frame, text='Stealth', variable=self.stealth_var)
        self.survival_check = Checkbutton(
            skills_frame, text='Survival', variable=self.survival_var)

        self.acrobatics_check.grid(row=0, column=0, sticky='w')
        self.animalhandling_check.grid(row=1, column=0, sticky='w')
        self.arcana_check.grid(row=2, column=0, sticky='w')
        self.athletics_check.grid(row=3, column=0, sticky='w')
        self.deception_check.grid(row=4, column=0, sticky='w')
        self.history_check.grid(row=5, column=0, sticky='w')
        self.insight_check.grid(row=6, column=0, sticky='w')
        self.intimidation_check.grid(row=7, column=0, sticky='w')
        self.investigation_check.grid(row=8, column=0, sticky='w')
        self.medicine_check.grid(row=9, column=0, sticky='w')
        self.nature_check.grid(row=10, column=0, sticky='w')
        self.perception_check.grid(row=11, column=0, sticky='w')
        self.performance_check.grid(row=12, column=0, sticky='w')
        self.persuasion_check.grid(row=13, column=0, sticky='w')
        self.religion_check.grid(row=14, column=0, sticky='w')
        self.sleight_check.grid(row=15, column=0, sticky='w')
        self.stealth_check.grid(row=16, column=0, sticky='w')
        self.survival_check.grid(row=17, column=0, sticky='w')

        # create skills list
        self.skills_list = [('Acrobats', self.acrobatics_var),
                            ('Animal Handling', self.animal_handling_var),
                            ('Arcana', self.arcana_var),
                            ('Athletics', self.athletics_var),
                            ('Deception', self.deception_var),
                            ('History', self.history_var),
                            ('Insight', self.insight_var),
                            ('Intimidation', self.intimidation_var),
                            ('Investigation', self.investigation_var),
                            ('Medicine', self.medicine_var),
                            ('Nature', self.nature_var),
                            ('Perception', self.perception_var),
                            ('Performance', self.performance_var),
                            ('Persuasion', self.persuasion_var),
                            ('Religion', self.religion_var),
                            ('Sleight of Hand', self.sleight_var),
                            ('Stealth', self.stealth_var),
                            ('Survival', self.survival_var)]

        # create proficiencies frame
        proficiencies_frame = LabelFrame(
            main_frame, text='Other Proficiencies')
        proficiencies_frame.grid(row=3, column=2)

        # create a subframe inside the proficiencies frame
        proficiencies_subframe = Frame(proficiencies_frame)
        proficiencies_subframe.grid(row=0, column=0)
        prof_xscroll = Scrollbar(proficiencies_subframe, orient='horizontal')
        prof_xscroll.grid(row=1, column=0, sticky='nsew')

        # text box
        self.proficiencies_box = Text(
            proficiencies_subframe, width=30, height=15, xscrollcommand=prof_xscroll.set)
        prof_xscroll.config(command=self.proficiencies_box.xview)
        self.proficiencies_box.config(undo=True, wrap=NONE)
        self.proficiencies_box.grid(row=0, column=0)

        # end of proficiencies frame

        for widget in character_info_frame.winfo_children():
            widget.grid_configure(padx=3)

        for widget in attributes_frame.winfo_children():
            widget.grid_configure(padx=3)

    def validate_hit_points(self, entry)->bool:
        """
        Validates the hit point entries to ensure it is a non-negative integer

        :param entry: the entry widget to validate
        :return: True if the entry is valid, False otherwise
        """
        number = entry.get()
        if number:
            if number.isdigit() and int(number) >= 0:
                entry.config(fg='black')
                return True
            else:
                entry.config(fg='red')
                return False
        return False

    def validate_attribute(self, entry, modifier)->bool:
        """
        Validates the attribute entries to ensure it is a number between 1 and 30

        :param entry: the entry widget to validate
        :param modifier: the label widget to update the modifier
        :return: True if the entry is valid, False otherwise
        """
        attribute = entry.get()
        # checks if attribute is empty or not
        if attribute:
            # checks if atribute is in between 1 and 30 inclusive
            if attribute.isdigit() and int(attribute) in range(1, 31):
                entry.config(fg='black')
                # run modifier code
                temp_modifier = self.determine_modifier(int(entry.get()))
                modifier.config(text=temp_modifier)
                return True
            else:
                # error
                entry.config(fg='red')
                modifier.config(text='+0')
                return False
        else:
            modifier.config(text='+0')
        return True

    def parse_race_default_csv(self, filename)->dict:
        """
        Parses the csv file containing the default values for races into a dictionary

        :param filename: the name of the file to parse
        :return: a dictionary containing the default values for races
        """
        races_default_dict = {}
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                key = row[0]
                value = row[1:]
                races_default_dict[key] = value

        return races_default_dict

    def parse_class_default_csv(self, filename)->dict:
        """
        Parses the csv file containing the default values for classes into a dictionary

        :param filename: the name of the file to parse
        :return: a dictionary containing the default values for classes
        """
        class_default_dict = {}
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                key = row[0]
                value = row[1:]
                class_default_dict[key] = value

        return class_default_dict

    def load_default_race_values(self, race)->None:
        """
        Loads the default values for the selected race and updates the GUI

        :param race: the dictionary containing the default values for the selected
        :return: None
        """
        race_options = self.race_default_dict[race]
        attributes_list = [self.strength_box, self.dexterity_box, self.constitution_box,
                           self.intelligence_box, self.wisdom_box, self.charisma_box]
        race_attributes = race_options[1:-1]

        # have message box appear to determine if code should run
        message = (
            "Do you want to change the character's race values? "
            "This will replace all attributes, speed, and hitpoints to the default "
            "values of the selected race. "
            "'No' will change the race but leave all values as is."
        )

        race_change = messagebox.askyesno(title='None', message=message)

        if race_change:
            # change speed
            self.speed_text.delete(0, END)
            self.speed_text.insert(END, str(race_options[0]))

            # change attributes
            for i, option in enumerate(race_attributes):
                # attributes_list[i].config(text=str(option))
                attributes_list[i].delete(0, END)
                if option != 0:
                    attributes_list[i].insert(END, str(option))

            # change proficiencies
            self.proficiencies_box.delete('1.0', END)
            self.proficiencies_box.insert(
                END, race_options[-1].replace('\\n', '\n'))

    def load_default_class_values(self, user_class)->None:
        """
        Loads the default values for the selected class and updates the GUI

        :param user_class: the dictionary containing the default values for the selected class
        :return: None
        """
        class_options = self.class_default_dict[user_class]

        # have message box appear to determine if code should run
        error_message = (
            "Do you want to change the character's class values? "
            "This will replace all skills, the hit die, the saving throws, "
            "and the max HP to the default values of the selected class. "
            "'No' will change the class but leave all values as is."
        )

        class_change = messagebox.askyesno(title='None', message=error_message)

        if class_change:
           # change hit die
            self.hit_dice_text.delete(0, END)
            self.hit_dice_text.insert(END, str(class_options[0]))

            # change max hp
            max_hp = int(class_options[1]) + \
                int(self.constitution_modifier.cget('text'))
            self.max_hp_text.delete(0, END)
            self.max_hp_text.insert(END, max_hp)

            # change saving throws
            temp_st = list(class_options[2].split('-'))
            for st in self.saving_throws_list:
                if temp_st[0] == st[0] or temp_st[1] == st[0]:
                    st[1].set(True)
                else:
                    st[1].set(False)
            # change skills
            class_skills = list(class_options[4].split('-'))
            num_of_skills = int(class_options[3])
            num_of_checked = 0
            skills_to_change = []

            # randomly get skills
            while num_of_checked < num_of_skills:
                temp_index = randint(0, len(class_skills)-1)
                temporary_skill = class_skills[temp_index]
                if temporary_skill not in skills_to_change:
                    skills_to_change.append(temporary_skill)
                    num_of_checked += 1

            for skill in self.skills_list:
                if skill[0] in skills_to_change:
                    skill[1].set(True)
                else:
                    skill[1].set(False)

    def determine_modifier(self, score)->str:
        """
        determines the modifier for the given score.
        The equation is as follows:
            (score - 10) / 2

        :param score: the score to determine the modifier for
        :return: the modifier as a string
        """
        if score % 2 != 0:
            score -= 1

        modifier = int((score - 10) / 2)

        if modifier >= 0:
            return '+' + str(modifier)
        return str(modifier)

    def generate_attributes(self)->None:
        """
        Generates random attributes for the character

        :return: None
        """
        # run 6 times, one for each box. skip box if it is disabled
        for index, attribute in enumerate(self.attributes_list):
            if attribute.cget('state') == 'normal':
                # roll 4 dice, save 3 highest
                temp_dice = []
                for i in range(4):
                    temp_dice.append(randint(1, 6))
                # remove the lowest value
                temp_dice.remove(min(temp_dice))

                # get total sum of dice
                total = sum(temp_dice)

                attribute.delete(0, END)
                attribute.insert(0, str(total))

                # update modifier
                self.modifiers_list[index].config(
                    text=str(self.determine_modifier(total)))

    def save_and_close_spells(self, window, textbox)->None:
        """
        Saves the contents of the spell text box to the character model and
        closes the window

        :param window: the window to close
        :param textbox: the text box to save the contents of
        :return: None
        """
        # Save the contents of the text box to the character model
        self.character_model.spells = textbox.get("1.0", 'end-1c')

        # Close the window
        window.destroy()

    def open_spell_window(self)->None:
        """
        Opens a new window to manage the character's spells

        :return: None
        """
        add_spell_window = Toplevel(self.root)
        add_spell_window.title('Manage Spells')
        add_spell_window.geometry('400x400')

        spell_name_label = Label(add_spell_window, text='Spell Name')
        spell_name_label.grid(row=0, column=0)

        # Create a frame to hold the text box and scrollbars
        frame = Frame(add_spell_window)
        frame.grid(row=1, column=0)

        # Create the vertical scrollbar
        y_scrollbar = Scrollbar(frame)
        y_scrollbar.pack(side=RIGHT, fill=Y)

        # Create the horizontal scrollbar
        x_scrollbar = Scrollbar(frame, orient=HORIZONTAL)
        x_scrollbar.pack(side=BOTTOM, fill=X)

        # Create the text box with scrollbars
        spell_name_textbox = Text(
            frame, height=20, width=40, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        spell_name_textbox.pack(side=LEFT, fill=BOTH, expand=True)

        # Configure the scrollbars to move with the text box
        y_scrollbar.config(command=spell_name_textbox.yview)
        x_scrollbar.config(command=spell_name_textbox.xview)

        # Load the spells from the character model into the text box
        spell_name_textbox.insert(END, self.character_model.spells)

        # Bind the WM_DELETE_WINDOW protocol to a method that saves the
        # contents of the text box to the character model
        add_spell_window.protocol("WM_DELETE_WINDOW", lambda: self.save_and_close_spells(
            add_spell_window, spell_name_textbox))

    def save_character(self)->None:
        """
        Saves the character to a JSON file.
        This function will validate the character data before saving and will
        prompt the user to select a file to save to.
        Any errors will be displayed in a messagebox,
        warning the user of the error.

        :return: None
        """
        try:
            # check level
            level = self.character_level_entry.get()
            if level:
                if not level.lstrip('-').isdigit():
                    print(level.isdigit())
                    raise TypeError('Level must be a positive integer.')
                if int(level) <= 0:
                    raise Exception('Level must be 1 or above.')
            else:
                raise Exception('Level must be filled in.')

            # check attributes
            for entry in self.attributes_list:
                attribute = entry.get()
                if attribute:
                    if not attribute.lstrip('-').isdigit():
                        raise TypeError('Attributes must be integers.')

                    if int(attribute) <= 0 or int(attribute) > 30:
                        raise Exception(
                            'Attributes must be between 1 and 30 inclusive.')
                else:
                    raise Exception('All attributes must be filled in.')
            # check hitpoints
            for entry in self.all_pos_int_entries:
                text = entry.get()
                if text:
                    valid_test = self.validate_hit_points(entry)
                    if not valid_test:
                        raise TypeError(
                            'Hit Points must be positive integers.')

            convert_gui_to_model(self, self.character_model)

            filename = filedialog.asksaveasfilename(
                initialdir="./EXPORTED_CHARACTERS", defaultextension=".json", filetypes=[("JSON files", "*.json")])

            if filename:
                with open(filename, 'w') as f:
                    f.write(character.character_model.to_json())

                print("File Created")
            else:
                Exception("No file selected")
        except Exception as e:
            messagebox.showerror(
                title='Error', message=f"An error occurred: {e}")

    def import_character(self)->None:
        """
        Imports a character from a JSON file. This function will validate the
        character data before importing it and will prompt the user to select
        a file to import from.
        If the imported file is invalid, an error message will be displayed in
        a messagebox.

        :return: None
        """
        try:
            filename = filedialog.askopenfilename(
                initialdir="./EXPORTED_CHARACTERS", filetypes=[("JSON files", "*.json")])

            if filename:
                with open(filename, 'r') as f:
                    json_str = f.read()
                    data = json.loads(json_str)

                    # Validate the JSON data against the schema
                    validate(instance=data, schema=character_model_schema)

                    # If the JSON data is valid, ask the user if they want to import the character
                    if messagebox.askyesno("Import Character", "The character file is valid. Do you want to import the character and replace all fields?"):
                        self.character_model = character.character_model.from_json(
                            json_str)

                        print("Character Model Loaded")

                        # Fill in the GUI with the character model
                        convert_model_to_gui(self, self.character_model)

        except jsonschema.exceptions.ValidationError as ve:
            messagebox.showerror(
                "Error", "Invalid JSON File! Please import a valid character")
        except Exception as e:
            messagebox.showerror("An error occurred", str(e))

    def clear_all(self)->None:
        """
        This will import a blank character and clear the GUI

        :return: None
        """
        filename = "./ASSETS/blank_character.json"

        # Prompt the user to confirm that they want to clear the GUI
        if not messagebox.askyesno("Clear Character", "Are you sure you want to clear the character sheet? Everything will be lost."):
            print("GUI Not Cleared")
            return

        with open(filename, 'r') as f:
            json_str = f.read()
            self.character_model = character.character_model.from_json(json_str)
            convert_model_to_gui(self, self.character_model)

        print("GUI Cleared")


if __name__ == '__main__':
    root = Tk()
    root.title('Character Smith')
    root.geometry('800x950')
    root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

    character = Character(root)

    print('Running...')

    root.mainloop()
