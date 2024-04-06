from tkinter import END

def convert_gui_to_model(character_gui, character_model) -> None:
    """
    This functions assumes that all data is valid and saves it to the character model

    :param character_gui: The character GUI object
    :param character_model: The character model object
    :return: None
    """
    # Save Name, Class, Race, Level to Model
    character_model.character_name = character_gui.character_name_entry.get()
    character_model.character_class = character_gui.character_class_option.get()
    character_model.race = character_gui.character_race_option.get()
    character_model.level = int(character_gui.character_level_entry.get())

    # Save Hitpoints to Model
    character_model.hitpoints['max'] = int(character_gui.max_hp_text.get())
    character_model.hitpoints['current'] = int(character_gui.current_hp_text.get())

    # Save Armor Class, Initiative
    character_model.armor_class = int(character_gui.armour_class_text.get())
    character_model.initiative = int(character_gui.initiative_text.get())
    character_model.speed = int(character_gui.speed_text.get())

    # Save Hit Dice to Model
    character_model.hit_dice['total'] = character_gui.hit_dice_text.get()
    character_model.hit_dice['current'] = character_gui.hit_dice_total_text.get()
    
    # Save Attributes to Model
    character_model.attributes['strength'] = int(character_gui.strength_box.get())
    character_model.attributes['dexterity'] = int(character_gui.dexterity_box.get())
    character_model.attributes['constitution'] = int(character_gui.constitution_box.get())
    character_model.attributes['intelligence'] = int(character_gui.intelligence_box.get())
    character_model.attributes['wisdom'] = int(character_gui.wisdom_box.get())
    character_model.attributes['charisma'] = int(character_gui.charisma_box.get())

    # Save Saving Throws Checkbox Values to Model
    character_model.saving_throws['strength'] = character_gui.st_strength_var.get()
    character_model.saving_throws['dexterity'] = character_gui.st_charisma_var.get()
    character_model.saving_throws['constitution'] = character_gui.st_constitution_var.get()
    character_model.saving_throws['intelligence'] = character_gui.st_intelligence_var.get()
    character_model.saving_throws['wisdom'] = character_gui.st_wisdom_var.get()
    character_model.saving_throws['charisma'] = character_gui.st_charisma_var.get()

    # Save Death Saves to Model
    for i in range(3):
        character_model.death_saves['successes'][i] = character_gui.successes_checkboxes_value[i].get()
        character_model.death_saves['failures'][i] = character_gui.failure_checkboxes_value[i].get()

    # Save Skills to Model
    character_model.skills['acrobatics'] = character_gui.acrobatics_var.get()
    character_model.skills['animal_handling'] = character_gui.animal_handling_var.get()
    character_model.skills['arcana'] = character_gui.arcana_var.get()
    character_model.skills['athletics'] = character_gui.athletics_var.get()
    character_model.skills['deception'] = character_gui.deception_var.get()
    character_model.skills['history'] = character_gui.history_var.get()
    character_model.skills['insight'] = character_gui.insight_var.get()
    character_model.skills['intimidation'] = character_gui.intimidation_var.get()
    character_model.skills['investigation'] = character_gui.investigation_var.get()
    character_model.skills['medicine'] = character_gui.medicine_var.get()
    character_model.skills['nature'] = character_gui.nature_var.get()
    character_model.skills['perception'] = character_gui.perception_var.get()
    character_model.skills['performance'] = character_gui.performance_var.get()
    character_model.skills['persuasion'] = character_gui.persuasion_var.get()
    character_model.skills['religion'] = character_gui.religion_var.get()
    character_model.skills['sleight_of_hand'] = character_gui.sleight_var.get()
    character_model.skills['stealth'] = character_gui.stealth_var.get()
    character_model.skills['survival'] = character_gui.survival_var.get()

    # Save Weapon Attacks & Abilities to Model
    character_model.weapon_attacks = []
    for entry in character_gui.weapon_entries:
        weapon = {
            'name': entry[0].get(),
            'bonus_to_hit': entry[1].get(),
            'damage': entry[2].get()
        }
        character_model.weapon_attacks.append(weapon)

    character_model.abilities = character_gui.abilities_box.get('1.0', END)

    # Save Inventory, Proficiencies, and Spells to Model
    character_model.inventory = character_gui.inventory_box.get('1.0', END)
    character_model.other_proficiencies = character_gui.proficiencies_box.get('1.0', END)