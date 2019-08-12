from evennia import utils
from world import skillsets
from world import build_skill_str
import time
import random

class CombatHandler:
    def __init__(self, owner):
        self.owner = owner

    def attack(self, target, damage_type, skillset, skill):  
        damage = 20

        # Create cooldown attribute if non-existent.
        if not self.owner.attributes.has('attack_cd'):
            self.owner.db.attack_cd = 0

        # Calculate current time, total cooldown, and remaining time.
        now = time.time()
        lastcast = self.owner.attributes.get('attack_cd')
        cooldown = lastcast + 3
        time_remaining = cooldown - now

        # Inform the attacker that they are in cooldown and exit the function.
        if time_remaining > 0:
            if time_remaining >= 2:
                message = f"You need to wait {int(time_remaining)} more seconds."
            elif time_remaining >= 1 and time_remaining < 2:
                message = f"You need to wait {int(time_remaining)} more second."
            elif time_remaining < 1:
                message = f"You are in the middle of something."
            self.owner.msg(message)
            return

        # roll = random.randint(1, 100)
        # success = random.randint(5, 95)
        roll = 100
        success = 0

        #temp values
        damage_tier = 0
        body_part = 'head'

        a_desc, t_desc = build_skill_str.create_attack_desc(self.owner, target, damage_type, damage_tier, body_part)
        outcome = a_desc
        success_attack = skillsets.skillsets[skillset][skill]['attack_desc']['self']
        weapon = 'quarterstave'

        if roll > success:
            self.owner.msg(f"[Success: {success} Roll: {roll}] " + success_attack + " and hit! " + a_desc)
            self.take_damage(target, damage)
        else:
            self.owner.msg(f"[Success: {success} Roll: {roll}] You miss {target} with your stave!")
        utils.delay(3, self.unbusy)
        self.owner.db.attack_cd = now

    def take_damage(self, target, damage):
        mob = target.key
        location = target.location
        
        hp = target.db.hp
        hp -= damage
        target.db.hp = hp

        location.msg_contents(f'{mob} has {hp} health remaining!')
        if hp >= 1:
            target.db.ko = False
        elif hp <= 0 and target.db.ko != True:
            target.db.ko = True
            location.msg_contents(f'{mob} falls unconscious!')
        if hp <= -100:
            okay = target.delete()
            if not okay:
                location.msg_contents(f'\nERROR: {mob} not deleted, probably because delete() returned False.')
            else:
                location.msg_contents(f'{mob} breathes a final breath and expires.')
        return
    
    def unbusy(self):
            self.owner.msg('|yYou are no longer busy.|n')