from tkinter import *
from tkinter import ttk, filedialog, messagebox
from random import randint
import jsonschema
from jsonschema import validate
from schemas import character_model_schema
import json, csv

class Character:
    def __init__(self, root) -> None:
        self.root = root
        self.character_model = Character_Model()

        self.character_class_option = StringVar(root)
        self.character_race_option = StringVar(root)
        class_file = open('./ASSETS/CLASSES.txt', 'r')
        class_options = [line.strip() for line in class_file.readlines()]
        race_file = open('./ASSETS/RACES.txt', 'r')
        race_options = [line.strip() for line in race_file.readlines()]
        self.race_default_dict = self.parse_race_default_csv('./ASSETS/RACES_DEFAULT.csv')
        self.class_default_dict = self.parse_class_default_csv('./ASSETS/CLASSES_DEFAULT.csv')

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
        self.nature_var= BooleanVar()
        self.perception_var = BooleanVar()
        self.performance_var = BooleanVar()
        self.persuasion_var = BooleanVar()
        self.religion_var = BooleanVar()
        self.sleight_var = BooleanVar()
        self.stealth_var = BooleanVar()
        self.survival_var = BooleanVar()
        
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
        file_menu.add_command(label='Import', command=self.import_character)
        file_menu.add_command(label='Save as...', command=self.save_character)
        menu_bar.add_cascade(label='File', menu=file_menu)
        
        # create frame for character info
        character_info_frame = LabelFrame(main_frame, text="Character Information")
        character_info_frame.grid(row=0, column=0, columnspan=3)

        character_name_label = Label(character_info_frame, text='Name')
        self.character_name_entry = Entry(character_info_frame)

        character_class_label = Label(character_info_frame, text='Class')
        character_class_menu = OptionMenu(character_info_frame, self.character_class_option, *class_options, command=self.load_default_class_values)
        character_class_menu.config(width=10)

        character_level_label = Label(character_info_frame, text='Level')
        self.character_level_entry = Entry(character_info_frame, width=3)
        self.character_level_entry.insert(0, '1')

        character_race_label = Label(character_info_frame, text='Race')
        character_race_menu = OptionMenu(character_info_frame, self.character_race_option, *race_options, command=self.load_default_race_values)
        character_race_menu.config(width=10)

        character_name_label.grid(row=0, column=0, sticky=W)
        self.character_name_entry.grid(row=1, column=0)
        self.character_name_entry.insert(0, 'Hero')
        # character_name_entry.config(state='disabled')
        character_name_button = Button(character_info_frame, text='Lock', command=lambda: self.lock_button(self.character_name_entry, character_name_button))
        character_name_button.grid(row=1, column=1)
        
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
                                  validatecommand=lambda: self.validate_attribute(self.strength_box, self.strength_modifier),
                                  validate='focusout')
        self.strength_modifier = Label(attributes_frame, text='+0')
        strength_box_label.grid(row=0, column=0)
        self.strength_box.grid(row=1, column=0)
        self.strength_modifier.grid(row=2, column=0)

        dexterity_box_label = Label(attributes_frame, text='Dexterity')
        self.dexterity_box = Entry(attributes_frame, width=5,
                                  validatecommand=lambda: self.validate_attribute(self.dexterity_box, self.dexterity_modifier),
                                  validate='focusout')
        self.dexterity_modifier = Label(attributes_frame, text='+0')
        dexterity_box_label.grid(row=0, column=1)
        self.dexterity_box.grid(row=1, column=1)
        self.dexterity_modifier.grid(row=2, column=1)

        constitution_box_label = Label(attributes_frame, text='Constitution')
        self.constitution_box = Entry(attributes_frame, width=5,
                                  validatecommand=lambda: self.validate_attribute(self.constitution_box, self.constitution_modifier),
                                  validate='focusout')
        self.constitution_modifier = Label(attributes_frame, text='+0')
        constitution_box_label.grid(row=0, column=2)
        self.constitution_box.grid(row=1, column=2)
        self.constitution_modifier.grid(row=2, column=2)

        intelligence_box_label = Label(attributes_frame, text='Intelligence')
        self.intelligence_box = Entry(attributes_frame, width=5,
                                  validatecommand=lambda: self.validate_attribute(self.intelligence_box, self.intelligence_modifier),
                                  validate='focusout')
        self.intelligence_modifier = Label(attributes_frame, text='+0')
        intelligence_box_label.grid(row=0, column=3)
        self.intelligence_box.grid(row=1, column=3)
        self.intelligence_modifier.grid(row=2, column=3)

        wisdom_box_label = Label(attributes_frame, text='Wisdom')
        self.wisdom_box = Entry(attributes_frame, width=5,
                                  validatecommand=lambda: self.validate_attribute(self.wisdom_box, self.wisdom_modifier),
                                  validate='focusout')
        self.wisdom_modifier = Label(attributes_frame, text='+0')
        wisdom_box_label.grid(row=0, column=4)
        self.wisdom_box.grid(row=1, column=4)
        self.wisdom_modifier.grid(row=2, column=4)

        charisma_box_label = Label(attributes_frame, text='Charisma')
        self.charisma_box = Entry(attributes_frame, width=5,
                                  validatecommand=lambda: self.validate_attribute(self.charisma_box, self.charisma_modifier),
                                  validate='focusout')
        self.charisma_modifier = Label(attributes_frame, text='+0')
        charisma_box_label.grid(row=0, column=5)
        self.charisma_box.grid(row=1, column=5)
        self.charisma_modifier.grid(row=2, column=5)

        genereate_attributes_button = Button(attributes_frame, text='Generate Attributes', command=self.generate_attributes)
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
                            validatecommand=lambda: self.validate_hit_points(self.max_hp_text),
                            validate='focusout')
        self.max_hp_text.insert(0, '0')  # Default value
        current_hp_label = Label(hitpoints_frame, text='Current HP')
        self.current_hp_text = Entry(hitpoints_frame, width=20,
                            validatecommand=lambda: self.validate_hit_points(self.current_hp_text),
                            validate='focusout')
        self.current_hp_text.insert(0, '0')  # Default value
        max_hp_label.grid(row=0, column=0)
        self.max_hp_text.grid(row=1, column=0)
        current_hp_label.grid(row=0, column=1, columnspan=2)
        self.current_hp_text.grid(row=1, column=1, columnspan=2)

        # Armor Class, Speed, Initiative Subframe
        armour_class_label = Label(hitpoints_frame, text='Armor Class')
        self.armour_class_text = Entry(hitpoints_frame, width=10,
                            validatecommand=lambda: self.validate_hit_points(self.armour_class_text),
                            validate='focusout')
        self.armour_class_text.insert(0, '0')  # Default value
        initiative_label = Label(hitpoints_frame, text='Initiative')
        self.initiative_text = Entry(hitpoints_frame, width=10,
                            validatecommand=lambda: self.validate_hit_points(self.initiative_text),
                            validate='focusout')
        self.initiative_text.insert(0, '0')  # Default value
        speed_label = Label(hitpoints_frame, text='Speed')
        self.speed_text = Entry(hitpoints_frame, width=10,
                            validatecommand=lambda: self.validate_hit_points(self.speed_text),
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

        self.saving_throws_strength_checkbox = Checkbutton(saving_throws_subframe, text='Strength', variable=self.st_strength_var)
        self.saving_throws_dexterity_checkbox = Checkbutton(saving_throws_subframe, text='Dexterity', variable=self.st_dexterity_var)
        self.saving_throws_constitution_checkbox = Checkbutton(saving_throws_subframe, text='Constitution', variable=self.st_constitution_var)
        self.saving_throws_intelligence_checkbox = Checkbutton(saving_throws_subframe, text='Intelligence', variable=self.st_intelligence_var)
        self.saving_throws_wisdom_checkbox = Checkbutton(saving_throws_subframe, text='Wisdom', variable=self.st_wisdom_var)
        self.saving_throws_charisma_checkbox = Checkbutton(saving_throws_subframe, text='Charisma', variable=self.st_charisma_var)
        
        self.saving_throws_strength_checkbox.grid(row=0, column=0, sticky='w')
        self.saving_throws_dexterity_checkbox.grid(row=1, column=0, sticky='w')
        self.saving_throws_constitution_checkbox.grid(row=2, column=0, sticky='w')
        self.saving_throws_intelligence_checkbox.grid(row=3, column=0, sticky='w')
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
        self.hit_dice_text.insert(0, '0')  # Default value
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

        self.failure_checkboxes_value = [] # Variable to store the failures checkboxes
        for i in range(3):
            var = BooleanVar()
            self.failure_checkboxes_value.append(var)

            failure = Checkbutton(death_saves_subframe, variable=var)
            failure.grid(row=1, column=i+1)

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
        self.weapon_entries = []  # This list will hold all the entry fields
        for i in range(1, table_rows + 1):
            row_entries = []  # This list will hold the entries for a single row
            for j in range(3):
                entry = Entry(weapon_attacks_subframe, width=17)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
                all_not_num_entry.append(entry)
            self.weapon_entries.append(row_entries)

        self.abilities_box = Text(weapon_attacks_subframe, width=40, height=20)
        self.abilities_box.grid(row=table_rows + 1, column=0, columnspan=3)

        # End of Weapon Attacks & Abilities Subframe

        # create inventory frame
        inventory_frame = LabelFrame(main_frame, text='Inventory')
        inventory_frame.grid(row=3, column=1, sticky='n')

        # create inventory box
        self.inventory_box = Text(inventory_frame, width=40, height=15, wrap='none')  # Set wrap to 'none' to enable horizontal scrolling
        self.inventory_box.grid(row=0, column=0, sticky='ew')

        # create horizontal scrollbar
        xscrollbar = Scrollbar(inventory_frame, orient='horizontal', command=self.inventory_box.xview)
        xscrollbar.grid(row=1, column=0, sticky='ew')
        self.inventory_box['xscrollcommand'] = xscrollbar.set
        
        # end of inventory subframe

        # create skills frame
        skills_frame = LabelFrame(main_frame, text='Skills')
        skills_frame.grid(row=2, column=2, sticky='new')

        self.acrobatics_check = Checkbutton(skills_frame, text='Acrobatics', variable=self.acrobatics_var)
        self.animalhandling_check = Checkbutton(skills_frame, text='Animal Handling', variable=self.animal_handling_var)
        self.arcana_check = Checkbutton(skills_frame, text='Arcana', variable=self.arcana_var)
        self.athletics_check = Checkbutton(skills_frame, text='Athletics', variable=self.athletics_var)
        self.deception_check = Checkbutton(skills_frame, text='Deception', variable=self.deception_var)
        self.history_check = Checkbutton(skills_frame, text='History', variable=self.history_var)
        self.insight_check = Checkbutton(skills_frame, text='Insight', variable=self.insight_var)
        self.intimidation_check = Checkbutton(skills_frame, text='Intimidation', variable=self.intimidation_var)
        self.investigation_check = Checkbutton(skills_frame, text='Investigation', variable=self.investigation_var)
        self.medicine_check = Checkbutton(skills_frame, text='Medicine', variable=self.medicine_var)
        self.nature_check = Checkbutton(skills_frame, text='Nature', variable=self.nature_var)
        self.perception_check = Checkbutton(skills_frame, text='Perception', variable=self.perception_var)
        self.performance_check = Checkbutton(skills_frame, text='Performance', variable=self.performance_var)
        self.persuasion_check = Checkbutton(skills_frame, text='Persuasion', variable=self.persuasion_var)
        self.religion_check = Checkbutton(skills_frame, text='Religion', variable=self.religion_var)
        self.sleight_check = Checkbutton(skills_frame, text='Sleight of Hand', variable=self.sleight_var)
        self.stealth_check = Checkbutton(skills_frame, text='Stealth', variable=self.stealth_var)
        self.survival_check = Checkbutton(skills_frame, text='Survival', variable=self.survival_var)

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
        proficiencies_frame = LabelFrame(main_frame, text='Other Proficiencies')
        proficiencies_frame.grid(row=3, column=2)

        # create a subframe inside the proficiencies frame
        proficiencies_subframe = Frame(proficiencies_frame)
        proficiencies_subframe.grid(row=0, column=0)
        prof_xscroll = Scrollbar(proficiencies_subframe, orient='horizontal')
        prof_xscroll.grid(row=1, column=0, sticky='nsew')

        # text box
        self.proficiencies_box = Text(proficiencies_subframe, width=30, height=15, xscrollcommand=prof_xscroll.set)
        prof_xscroll.config(command=self.proficiencies_box.xview)
        self.proficiencies_box.config(undo=True, wrap=NONE)
        self.proficiencies_box.grid(row=0, column=0)

        # end of proficiencies frame

        for widget in character_info_frame.winfo_children():
            widget.grid_configure(padx=3)
        
        for widget in attributes_frame.winfo_children():
            widget.grid_configure(padx=3)    

    def nothing(self):
        pass
    
    def validate_hit_points(self, entry):
        number = entry.get()
        if number:
            if number.isdigit() and int(number) >= 0:
                entry.config(fg='black')
                return True
            else:
                entry.config(fg='red')
                return False
        return False

    def validate_attribute(self, entry, modifier):
        attribute = entry.get()
        # checks if attribute is empty or not
        if attribute:
            # checks if atribute is in between 1 and 30 inclusive
            if attribute.isdigit() and int(attribute) in range (1, 31):
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

    def parse_race_default_csv(self, filename):
        races_default_dict = {}
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                key = row[0]
                value = row[1:]
                races_default_dict[key] = value

        return races_default_dict
    
    def parse_class_default_csv(self, filename):
        class_default_dict = {}
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                key = row[0]
                value = row[1:]
                class_default_dict[key] = value

        return class_default_dict

    def lock_button(self, entry, button):
        # if button is enabled, disabled it and recess it. otherwise do the opposite
        if entry.cget('state') == 'normal':
            entry.config(state='disabled')
            button.config(relief=SUNKEN)
        else:
            entry.config(state='normal')
            button.config(relief=RAISED)
    
    def load_default_race_values(self, race):
        race_options = self.race_default_dict[race]
        attributes_list = [self.strength_box, self.dexterity_box, self.constitution_box,
                           self.intelligence_box, self.wisdom_box, self.charisma_box]
        race_attributes = race_options[1:-1]

        # have message box appear to determine if code should run
        race_change = messagebox.askyesno(title='None',
                                                message='Do you want to change the character\'s race values? '
                                                'This will replace all attributes, speed, and hitpoints to the default '
                                                'values of the selected race (\'No\' will change the race but leave all '
                                                'values as is).')
        
        if race_change:
            # change speed
            self.speed_text.delete(0, END)
            self.speed_text.insert(END, str(race_options[0]))

            # change attributes
            for i, option in enumerate(race_attributes):
                #attributes_list[i].config(text=str(option))
                attributes_list[i].delete(0, END)
                if option != 0:
                    attributes_list[i].insert(END, str(option))
            
            # change proficiencies
            self.proficiencies_box.delete('1.0', END)
            self.proficiencies_box.insert(END, race_options[-1].replace('\\n', '\n'))

    def load_default_class_values(self, user_class):
        class_options = self.class_default_dict[user_class]
        
        # change hit die
        self.hit_dice_text.delete(0, END)
        self.hit_dice_text.insert(END, str(class_options[0]))

        # change max hp
        max_hp = int(class_options[1]) + int(self.constitution_modifier.cget('text'))
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




    def determine_modifier(self, score):
        if score % 2 != 0:
            score -= 1
        
        modifier = int((score - 10) / 2)

        if modifier >= 0:
            return '+' + str(modifier)
        return str(modifier)
    
    def generate_attributes(self):
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
                # we need to do a check for the race so that it gets added properly
                # possibly have a variable for each attribute so that we can add it
                # to the race modifier and then update the total
                attribute.delete(0, END)
                attribute.insert(0,str(total))

                # update modifier
                self.modifiers_list[index].config(text=str(self.determine_modifier(total)))

                #attribute.config(text=str(total))
                
                # also need to run the modifier

    def save_and_close_spells(self, window, textbox):
        # Save the contents of the text box to the character model
        self.character_model.spells = textbox.get("1.0", 'end-1c')

        # Close the window
        window.destroy()

    def open_spell_window(self):
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
        spell_name_textbox = Text(frame, height=20, width=40, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        spell_name_textbox.pack(side=LEFT, fill=BOTH, expand=True)

        # Configure the scrollbars to move with the text box
        y_scrollbar.config(command=spell_name_textbox.yview)
        x_scrollbar.config(command=spell_name_textbox.xview)

        # Load the spells from the character model into the text box
        spell_name_textbox.insert(END, self.character_model.spells)

        # Bind the WM_DELETE_WINDOW protocol to a method that saves the contents of the text box to the character model
        add_spell_window.protocol("WM_DELETE_WINDOW", lambda: self.save_and_close_spells(add_spell_window, spell_name_textbox))

    def save_to_model(self, character_model) -> None:
        """
        This functions assumes that all data is valid and saves it to the character model
        """
        # Save Name, Class, Race, Level to Model
        character_model.character_name = self.character_name_entry.get()
        character_model.character_class = self.character_class_option.get()
        character_model.race = self.character_race_option.get()
        character_model.level = int(self.character_level_entry.get())

        # Save Hitpoints to Model
        character_model.hitpoints['max'] = int(self.max_hp_text.get())
        character_model.hitpoints['current'] = int(self.current_hp_text.get())

        # Save Armor Class, Initiative
        character_model.armor_class = int(self.armour_class_text.get())
        character_model.initiative = int(self.initiative_text.get())
        character_model.speed = int(self.speed_text.get())

        # Save Hit Dice to Model
        character_model.hit_dice['total'] = self.hit_dice_text.get()
        character_model.hit_dice['current'] = self.hit_dice_total_text.get()
        
        # Save Attributes to Model
        character_model.attributes['strength'] = int(self.strength_box.get())
        character_model.attributes['dexterity'] = int(self.dexterity_box.get())
        character_model.attributes['constitution'] = int(self.constitution_box.get())
        character_model.attributes['intelligence'] = int(self.intelligence_box.get())
        character_model.attributes['wisdom'] = int(self.wisdom_box.get())
        character_model.attributes['charisma'] = int(self.charisma_box.get())

        # Save Saving Throws Checkbox Values to Model
        character_model.saving_throws['strength'] = self.st_strength_var.get()
        character_model.saving_throws['dexterity'] = self.st_charisma_var.get()
        character_model.saving_throws['constitution'] = self.st_constitution_var.get()
        character_model.saving_throws['intelligence'] = self.st_intelligence_var.get()
        character_model.saving_throws['wisdom'] = self.st_wisdom_var.get()
        character_model.saving_throws['charisma'] = self.st_charisma_var.get()

        # Save Death Saves to Model
        for i in range(3):
            character_model.death_saves['successes'][i] = self.successes_checkboxes_value[i].get()
            character_model.death_saves['failures'][i] = self.failure_checkboxes_value[i].get()

        # Save Skills to Model
        character_model.skills['acrobatics'] = self.acrobatics_var.get()
        character_model.skills['animal_handling'] = self.animal_handling_var.get()
        character_model.skills['arcana'] = self.arcana_var.get()
        character_model.skills['athletics'] = self.athletics_var.get()
        character_model.skills['deception'] = self.deception_var.get()
        character_model.skills['history'] = self.history_var.get()
        character_model.skills['insight'] = self.insight_var.get()
        character_model.skills['intimidation'] = self.intimidation_var.get()
        character_model.skills['investigation'] = self.investigation_var.get()
        character_model.skills['medicine'] = self.medicine_var.get()
        character_model.skills['nature'] = self.nature_var.get()
        character_model.skills['perception'] = self.perception_var.get()
        character_model.skills['performance'] = self.performance_var.get()
        character_model.skills['persuasion'] = self.persuasion_var.get()
        character_model.skills['religion'] = self.religion_var.get()
        character_model.skills['sleight_of_hand'] = self.sleight_var.get()
        character_model.skills['stealth'] = self.stealth_var.get()
        character_model.skills['survival'] = self.survival_var.get()

        # Save Weapon Attacks & Abilities to Model
        character_model.weapon_attacks = []
        for entry in self.weapon_entries:
            weapon = {
                'name': entry[0].get(),
                'bonus_to_hit': entry[1].get(),
                'damage': entry[2].get()
            }
            character_model.weapon_attacks.append(weapon)

        character_model.abilities = self.abilities_box.get('1.0', END)

        # Save Inventory, Proficiencies, and Spells to Model
        character_model.inventory = self.inventory_box.get('1.0', END)
        character_model.other_proficiencies = self.proficiencies_box.get('1.0', END)


    def save_character(self):
        try:
            # TODO: VALIDATE ALL ENTRIES AND PROPMTS. ADD THEM TO THE MODEL WHEN IT IS ALL VALID
            # If not valid, throw an exception and tell the user what is invalid
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
                        raise Exception('Attributes must be between 1 and 30 inclusive.')
                else:
                    raise Exception('All attributes must be filled in.')
            # check hitpoints
            for entry in self.all_pos_int_entries:
                text = entry.get()
                if text:
                    valid_test = self.validate_hit_points(entry)
                    if not valid_test:
                        raise TypeError('Hit Points must be positive integers.')

            self.save_to_model(self.character_model)

            filename = filedialog.asksaveasfilename(initialdir="./EXPORTED_CHARACTERS", defaultextension=".json", filetypes=[("JSON files", "*.json")]) 

            if filename:
                with open(filename, 'w') as f:
                    f.write(character.character_model.to_json())

                print("File Created")
            else:
                Exception("No file selected")
        except Exception as e:
            print(f"An error occurred: {e}")
            # TODO: Tell user which entry is invalid via popup. Have multiple exeptions for each entry

    def model_to_gui(self, character_model):
        """
        This function will take the character model and fill in all the fields in the GUI
        This function assumes that all fields in the character model are valid based on the save function
        """
        # Fill in the character information
        self.character_name_entry.delete(0, 'end')
        self.character_name_entry.insert(0, character_model.character_name)
        self.character_class_option.set(character_model.character_class)
        self.character_race_option.set(character_model.race)
        self.character_level_entry.delete(0, 'end')
        self.character_level_entry.insert(0, str(character_model.level))

        # Fill in the attributes
        self.strength_box.delete(0, 'end')
        self.strength_box.insert(0, str(character_model.attributes['strength']))
        self.dexterity_box.delete(0, 'end')
        self.dexterity_box.insert(0, str(character_model.attributes['dexterity']))
        self.constitution_box.delete(0, 'end')
        self.constitution_box.insert(0, str(character_model.attributes['constitution']))
        self.intelligence_box.delete(0, 'end')
        self.intelligence_box.insert(0, str(character_model.attributes['intelligence']))
        self.wisdom_box.delete(0, 'end')
        self.wisdom_box.insert(0, str(character_model.attributes['wisdom']))
        self.charisma_box.delete(0, 'end')
        self.charisma_box.insert(0, str(character_model.attributes['charisma']))

        # Fill in the hitpoints
        self.max_hp_text.delete(0, 'end')
        self.max_hp_text.insert(0, str(character_model.hitpoints['max']))
        self.current_hp_text.delete(0, 'end')
        self.current_hp_text.insert(0, str(character_model.hitpoints['current']))

        # Fill in the armor class, initiative
        self.armour_class_text.delete(0, 'end')
        self.armour_class_text.insert(0, str(character_model.armor_class))
        self.initiative_text.delete(0, 'end')
        self.initiative_text.insert(0, str(character_model.initiative))
        self.speed_text.delete(0, 'end')
        self.speed_text.insert(0, str(character_model.speed))

        # Fill in the saving throws
        self.st_strength_var.set(character_model.saving_throws['strength'])
        self.st_dexterity_var.set(character_model.saving_throws['dexterity'])
        self.st_constitution_var.set(character_model.saving_throws['constitution'])
        self.st_intelligence_var.set(character_model.saving_throws['intelligence'])
        self.st_wisdom_var.set(character_model.saving_throws['wisdom'])
        self.st_charisma_var.set(character_model.saving_throws['charisma'])

        # Fill in the hit dice
        self.hit_dice_text.delete(0, 'end')
        self.hit_dice_text.insert(0, character_model.hit_dice['total'])
        self.hit_dice_total_text.delete(0, 'end')
        self.hit_dice_total_text.insert(0, character_model.hit_dice['current'])

        # Fill in the death saves
        for i in range(3):
            self.successes_checkboxes_value[i].set(character_model.death_saves['successes'][i])
            self.failure_checkboxes_value[i].set(character_model.death_saves['failures'][i])

        # Fill in the weapon attacks
        for i, weapon in enumerate(character_model.weapon_attacks):
            self.weapon_entries[i][0].delete(0, 'end')
            self.weapon_entries[i][0].insert(0, weapon['name'])
            self.weapon_entries[i][1].delete(0, 'end')
            self.weapon_entries[i][1].insert(0, weapon['bonus_to_hit'])
            self.weapon_entries[i][2].delete(0, 'end')
            self.weapon_entries[i][2].insert(0, weapon['damage'])

        # Fill in the abilities
        self.abilities_box.delete('1.0', 'end')
        self.abilities_box.insert('1.0', character_model.abilities)
        
        # Fill in the skills
        self.acrobatics_var.set(character_model.skills['acrobatics'])
        self.animal_handling_var.set(character_model.skills['animal_handling'])
        self.arcana_var.set(character_model.skills['arcana'])
        self.athletics_var.set(character_model.skills['athletics'])
        self.deception_var.set(character_model.skills['deception'])
        self.history_var.set(character_model.skills['history'])
        self.insight_var.set(character_model.skills['insight'])
        self.intimidation_var.set(character_model.skills['intimidation'])
        self.investigation_var.set(character_model.skills['investigation'])
        self.medicine_var.set(character_model.skills['medicine'])
        self.nature_var.set(character_model.skills['nature'])
        self.perception_var.set(character_model.skills['perception'])
        self.performance_var.set(character_model.skills['performance'])
        self.persuasion_var.set(character_model.skills['persuasion'])
        self.religion_var.set(character_model.skills['religion'])
        self.sleight_var.set(character_model.skills['sleight_of_hand'])
        self.stealth_var.set(character_model.skills['stealth'])
        self.survival_var.set(character_model.skills['survival'])

        # Fill in the other proficiencies
        self.proficiencies_box.delete('1.0', 'end')
        self.proficiencies_box.insert('1.0', character_model.other_proficiencies)

        # Fill in the inventory
        self.inventory_box.delete('1.0', 'end')
        self.inventory_box.insert('1.0', character_model.inventory)

    def import_character(self):
        try:
            filename = filedialog.askopenfilename(initialdir="./EXPORTED_CHARACTERS", filetypes=[("JSON files", "*.json")])

            if filename:
                with open(filename, 'r') as f:
                    json_str = f.read()
                    data = json.loads(json_str)

                    # Validate the JSON data against the schema
                    validate(instance=data, schema=character_model_schema)

                    # If the JSON data is valid, ask the user if they want to import the character
                    if messagebox.askyesno("Import Character", "The character file is valid. Do you want to import the character and replace all fields?"):
                        self.character_model = character.character_model.from_json(json_str)
                        
                        print("Character Model Loaded")

                        # Fill in the GUI with the character model
                        self.model_to_gui(self.character_model)
                        
        except jsonschema.exceptions.ValidationError as ve:
            messagebox.showerror("Error", "Invalid JSON File! Please import a valid character")
        except Exception as e:
            messagebox.showerror("An error occurred", str(e))


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
            'total': "",
            'current': ""
        }
        self.death_saves = {
            'successes': [False, False, False],
            'failures': [False, False, False]
        }
        # Weapon attacks will be in a form of a list of dictionaries
        # Example: [{'name': 'Sword', 'bonus_to_hit': '5', 'damage': '1d6 + 3'}, ...]
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
        self.spells = ""

    # Saving Data (instance attributes) to a JSON file. 
    # This will be used to save the Character Model
    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        try:
            instance = cls()
            instance.__dict__ = json.loads(json_str)
            return instance
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            return None

if __name__ == '__main__':
    root = Tk()
    root.title('Character Smith')
    root.geometry('800x1000')
    root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

    character = Character(root)

    # JSON FILE TEST
    # with open('character.json', 'w') as f:
    #     f.write(character.character_model.to_json())
    # 
    # with open('character.json', 'r') as f:
    #     json_str = f.read()
    #     loaded_character = character.character_model.from_json(json_str)
    #     # TODO: Prompt user before loading the character_model
    #     character.character_model = loaded_character
    # 
    # print("Level: " + str(character.character_model.level))

    print('Running...')

    root.mainloop()
