from evennia import DefaultCharacter
from evennia.utils.create import create_object
from evennia.utils.utils import (list_to_string, inherits_from, lazy_property)
from world.combat_handler import CombatHandler


class Character(DefaultCharacter):
    pass

class Player_Character(DefaultCharacter):

    @lazy_property
    def combat(self):
        return CombatHandler(self)

    def at_object_creation(self):
        # Stats
        if not self.attributes.get('def_skills'):
            self.attributes.add('gsp', 10)
        if not self.attributes.get('def_skills'):
            self.attributes.add('hp', {'max_hp': 100, 'current_hp': 100})

        # Statuses
        self.attributes.add('approached', [])
        self.attributes.add('ko', False)
        self.attributes.add('feinted', None)
        self.attributes.add('busy', False)
        self.attributes.add('wielding', {'left': None, 'right': None, 'both': None})
        self.attributes.add('stance', None)

        # Skills
        if not self.attributes.get('def_skills'):
            self.attributes.add('def_skills', {'weapon': {'high': {}, 'mid': {}, 'low': {}}, 'dodge': {'high': {}, 'mid': {}, 'low': {}}, 'shield': {'high': {}, 'mid': {}, 'low': {}}})
        if not self.attributes.get('def_rb'):
            self.attributes.add('def_rb', {'high': 0, 'mid': 0, 'low': 0})

        # Hands
        self.attributes.add('hands', {'left': None, 'right': None})
        
        

    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""
        
        # get description, build string
        string  = self.create_desc()
        return string

    def create_desc(self):
        desc = ""
        
        figure = self.db.figure
        facial = self.db.facial
        hair = self.db.hair

        height = figure.get('height')
        build = figure.get('build')
        sex = figure.get('gender')

        eye_color = facial.get('eye_color')
        nose = facial.get('nose')
        lips = facial.get('lips')
        chin = facial.get('chin')
        face = facial.get('face')
        skin_color = facial.get('skin_color')

        length = hair.get('length')
        texture = hair.get('texture')
        hair_color = hair.get('hair_color')
        style = hair.get('style')

        # The figure should result in "You see a <height> <build> <gender>."
        gender = ('man' if sex == 'male' else 'woman')
        desc += f"You see a {height} {build} {gender}. "
        
        # The facial should result in "He has <color> eyes set above an <shape> nose, <shape> lips and a <shape> chin in a <shape> <color> face."
        gender = ('He' if sex == 'male' else 'She')
        desc += (f"{gender} has {eye_color} eyes set above a {nose} nose, "
                f"{lips} lips and a {chin} chin in a {face} {skin_color} face. ")

        # The hair should result in "<gender> has <length> <texture> <color> hair <style>."
        if length == 'bald':
            desc += f"{gender} is {length}. "
        else:
            desc += f"{gender} has {length} {texture} {hair_color} hair {style}. "
        return desc