# Character Smith: TTRPG Character Sheet Generator

A simple Python GUI program that allows the user to make, import, and save a TTRPG character sheet. This character sheet is modelled specifically for Dungeons and Dragons 5th Edition, using only classes and races found within The Player's Handbook.

# Prerequisites
JSONSchema must be installed with
```pip install jsonschema```

# Usage

## File
### Clear All
The clear all menu option will prompt the user with if they want to erase all of the data currently inputted into the character sheet. Selecting `Yes` will revert the current sheet back to it's original state. 

### Import
The import menu option will prompt the user for a valid JSON file containing the character sheet information. Invalid JSON files will not be imported and the user will be given an error.

### Save As
The save as menu option will prompt the user to save the current character sheet as a JSON file. If any of the entries are invalid, the user will be unable to save the sheet and will be given an error with what of the character sheet that is causing the issue, including highlighting the invalid entry in red.

## Character Information
### Name
The name of the TTRPG character.

### Class
The class of the character. Selecting a class prompts the user with a dialog box asking if they would like to import the default class options. Selecting `Yes` will remove any previously added skills, hit dice, max HP, or saving throws previously added. Selecting `No` will keep any previously added data, but will still change the class of the character.

### Race
The race of the character. Selecting a race prompts the user with a dialog box asking if they would like to import the default race options. Selecting `Yes` will remove any previously added attribute bonuses, proficiencies, and speed. Selecting `No` will keep any previously added data, but will still change the race of the character.

### Level
The level of the character. This must be a positive integer 1 or higher.

## Attributes
The attributes of the character. Each entry box cooresponds to the attribute listed above it. Below each entry box is the attribute modifier, which is determined by the value of the attribute above it. Attributes must be positive integers in between 1 and 30 inclusive.

### Generate Attributes
The generate attributes button will randomize each of the attributes to be a number between 1 and 30, overwriting any previously added attributes.

## Hit Points
### Max HP
The maximum hit points of the character. This is determined by the character's class and the constitution modifier. Must be a poisitve integer.

### Current HP
The current hit points of the character. Must be a poisitve integer.

### Armor Class
The armor class of the character. Must be a positive integer.

### Initiative
The combat initiative of the character. Must be a positive integer.

### Speed
The speed of the character. This is determined by the character's race. Must be a positive integer.

## Saving Throws
Each of the saving throws is a checkbox cooresponding to an attribute. Saving throws are determined by the character's class.

## Hit Dice
The hit dice are a number of dice of a certain type (d4, d6, d8, or d10) determined by the character's class.

## Death Saves
The death saves show the successes and failures of the character through checkboxes.

## Spells
The spells button opens up a new window containing a text box that houses all of the spells for the character.

## Weapons, Attacks, and Abilities
The first section has 5 rows for weapons the character is wielding, each with a name, a bonus to hit value, and a damage die.

The second section is a text box for the character's abilities.

## Inventory
The inventory is a text box that houses the inventory of the character. This includes the character's gold and silver.

## Skills
The skills house checkboxes that identify the skills in which the character is proficient in. Skills are determined by the character's class. For each class, it has a certain number of skills it selects from a certain subset of the skills, and thus each time a class is selected, the skills get rerolled to select new ones from the same subset.

## Other Proficiencies.
The other proficiencies box is a text box housing any other proficiencies of the character. The proficiencies are determined by the character's race.

# Credits
Created by Ryan Bachir, Calvin Ip, and Sajawal Nauman
