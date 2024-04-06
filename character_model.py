import json

class Character_Model:
    def __init__(self) -> None:
        """
        A class to represent a Character Model
        """
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
            'persuasion': False,
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
        """
        This method will convert the instance attributes to a JSON string
        
        :return: JSON string
        """
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        """
        This method will convert a JSON string to a Character Model instance

        :param json_str: JSON string
        :return: Character Model instance
        """
        try:
            instance = cls()
            instance.__dict__ = json.loads(json_str)
            return instance
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            return None