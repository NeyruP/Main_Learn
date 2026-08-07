#!/usr/bin/env python3
import sys
import time


def slow_print(text, delay=0.08):
    """Print text with character-by-character delay for dramatic effect."""
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')
    sys.stdout.flush()
    time.sleep(0.01)


class Player:
    """Main player class for Eldoria game."""
    
    def __init__(self, name):
        self.name = name
        self.max_health = 100
        self.health = 100
        self.max_mana = 50
        self.mana = 50
        self.money = 50
        self.weapon = 'Punhos'
        self.weapon_level = 1
        self.level = 1
        self.exp = 0
        self.exp_to_next = 50

        # [SISTEMA DE ARMADURA] - Atributo inicial
        self.armor = None

        self.inventory = {
            'pocoes': 1,
            'cabecas_boss': []
        }

        self.skills = [
            {'nome': 'Golpe de Mana', 'custo': 10}
        ]

    def display_status(self):
        """Display player's current status."""
        # [SISTEMA DE ARMADURA] - status
        armor_name = self.armor['nome'] if self.armor else 'Nenhuma'
        armor_lvl = f" (Nív. {self.armor.get('level', 1)})" if self.armor else ""
        dur = f"{self.armor['durabilidade']}/{self.armor['max_durabilidade']}" if self.armor else '0/0'
        print(
            f'\n👤 {self.name} | LVL {self.level} | '
            f'❤️ {self.health}/{self.max_health} | '
            f'✨ {self.mana}/{self.max_mana} | '
            f'💰 {self.money}g\n'
            f'⚔️ {self.weapon} Lvl.{self.weapon_level} | '
            f'🛡️ {armor_name}{armor_lvl} (Dur: {dur})'
        )

    def gain_exp(self, amount):
        """Gain experience and handle level-ups."""
        self.exp += amount
        print(f'✨ +{amount} EXP')
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            self.exp_to_next = int(self.exp_to_next * 1.25)
            self.max_health += 15
            self.max_mana += 10
            self.health = self.max_health
            self.mana = self.max_mana
            slow_print(f'🎉 LEVEL UP {self.level}!')
            if self.level == 3:
                self.skills.append({'nome': 'Escudo Solar', 'custo': 15})
            if self.level == 5:
                self.skills.append({'nome': 'Explosão Estelar', 'custo': 25})
