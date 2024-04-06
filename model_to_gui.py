from tkinter import END

def convert_model_to_gui(character_gui, character_model):
    """
    This function will take the character model and fill in all the fields in the GUI
    This function assumes that all fields in the character model are valid based on the save function

    :param character_gui: The character GUI object
    :param character_model: The character model object
    :return: None
    """
    # Fill in the character information
    character_gui.character_name_entry.delete(0, END)
    character_gui.character_name_entry.insert(0, character_model.character_name)
    character_gui.character_class_option.set(character_model.character_class)
    character_gui.character_race_option.set(character_model.race)
    character_gui.character_level_entry.delete(0, END)
    character_gui.character_level_entry.insert(0, str(character_model.level))

    # Fill in the attributes
    character_gui.strength_box.delete(0, END)
    character_gui.strength_box.insert(0, str(character_model.attributes['strength']))
    character_gui.dexterity_box.delete(0, END)
    character_gui.dexterity_box.insert(0, str(character_model.attributes['dexterity']))
    character_gui.constitution_box.delete(0, END)
    character_gui.constitution_box.insert(0, str(character_model.attributes['constitution']))
    character_gui.intelligence_box.delete(0, END)
    character_gui.intelligence_box.insert(0, str(character_model.attributes['intelligence']))
    character_gui.wisdom_box.delete(0, END)
    character_gui.wisdom_box.insert(0, str(character_model.attributes['wisdom']))
    character_gui.charisma_box.delete(0, END)
    character_gui.charisma_box.insert(0, str(character_model.attributes['charisma']))

    # Fill in the hitpoints
    character_gui.max_hp_text.delete(0, END)
    character_gui.max_hp_text.insert(0, str(character_model.hitpoints['max']))
    character_gui.current_hp_text.delete(0, END)
    character_gui.current_hp_text.insert(0, str(character_model.hitpoints['current']))

    # Fill in the armor class, initiative
    character_gui.armour_class_text.delete(0, END)
    character_gui.armour_class_text.insert(0, str(character_model.armor_class))
    character_gui.initiative_text.delete(0, END)
    character_gui.initiative_text.insert(0, str(character_model.initiative))
    character_gui.speed_text.delete(0, END)
    character_gui.speed_text.insert(0, str(character_model.speed))

    # Fill in the saving throws
    character_gui.st_strength_var.set(character_model.saving_throws['strength'])
    character_gui.st_dexterity_var.set(character_model.saving_throws['dexterity'])
    character_gui.st_constitution_var.set(character_model.saving_throws['constitution'])
    character_gui.st_intelligence_var.set(character_model.saving_throws['intelligence'])
    character_gui.st_wisdom_var.set(character_model.saving_throws['wisdom'])
    character_gui.st_charisma_var.set(character_model.saving_throws['charisma'])

    # Fill in the hit dice
    character_gui.hit_dice_text.delete(0, END)
    character_gui.hit_dice_text.insert(0, character_model.hit_dice['total'])
    character_gui.hit_dice_total_text.delete(0, END)
    character_gui.hit_dice_total_text.insert(0, character_model.hit_dice['current'])

    # Fill in the death saves
    for i in range(3):
        character_gui.successes_checkboxes_value[i].set(character_model.death_saves['successes'][i])
        character_gui.failure_checkboxes_value[i].set(character_model.death_saves['failures'][i])

    # Fill in the weapon attacks
    for i, weapon in enumerate(character_model.weapon_attacks):
        character_gui.weapon_entries[i][0].delete(0, END)
        character_gui.weapon_entries[i][0].insert(0, weapon['name'])
        character_gui.weapon_entries[i][1].delete(0, END)
        character_gui.weapon_entries[i][1].insert(0, weapon['bonus_to_hit'])
        character_gui.weapon_entries[i][2].delete(0, END)
        character_gui.weapon_entries[i][2].insert(0, weapon['damage'])

    # Fill in the abilities
    character_gui.abilities_box.delete('1.0', END)
    character_gui.abilities_box.insert('1.0', character_model.abilities)
    
    # Fill in the skills
    character_gui.acrobatics_var.set(character_model.skills['acrobatics'])
    character_gui.animal_handling_var.set(character_model.skills['animal_handling'])
    character_gui.arcana_var.set(character_model.skills['arcana'])
    character_gui.athletics_var.set(character_model.skills['athletics'])
    character_gui.deception_var.set(character_model.skills['deception'])
    character_gui.history_var.set(character_model.skills['history'])
    character_gui.insight_var.set(character_model.skills['insight'])
    character_gui.intimidation_var.set(character_model.skills['intimidation'])
    character_gui.investigation_var.set(character_model.skills['investigation'])
    character_gui.medicine_var.set(character_model.skills['medicine'])
    character_gui.nature_var.set(character_model.skills['nature'])
    character_gui.perception_var.set(character_model.skills['perception'])
    character_gui.performance_var.set(character_model.skills['performance'])
    character_gui.persuasion_var.set(character_model.skills['persuasion'])
    character_gui.religion_var.set(character_model.skills['religion'])
    character_gui.sleight_var.set(character_model.skills['sleight_of_hand'])
    character_gui.stealth_var.set(character_model.skills['stealth'])
    character_gui.survival_var.set(character_model.skills['survival'])

    # Fill in the other proficiencies
    character_gui.proficiencies_box.delete('1.0', END)
    character_gui.proficiencies_box.insert('1.0', character_model.other_proficiencies)

    # Fill in the inventory
    character_gui.inventory_box.delete('1.0', END)
    character_gui.inventory_box.insert('1.0', character_model.inventory)