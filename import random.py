import random
import time
import pickle
import sys

#========================
#------ SAVE SYSTEM ------
#========================

def player_to_dict(player):
    return player.__dict__

def dict_to_player(data):
    p = Player(data['name'])
    p.__dict__.update(data)
    return p

def save_game(player, filename='save.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(player_to_dict(player), f)
    print('💾 Jogo salvo com sucesso!')

def load_game(filename='save.pkl'):
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        print('📂 Save carregado!')
        return dict_to_player(data)
    except:
        print('❌ Nenhum save encontrado.')
        return None

#========================
#------ LORE ------
#========================

LORE_INTRO = [
    '--- AS CRÔNICAS DE ELDORIA ---',
    'O sol não brilha mais como antes...',
    'A Calamidade desperta nas profundezas...',
    'Eldoria aguarda um Sem-Nome.'
]

LORE_SCROLLS = [
    'O 18º andar não deveria existir.',
    'A luz aqui abaixo apodrece.',
    'A capital foi arrancada do mundo.',
]

BOSS_LORE = {
    1: ('Korg, o Cobrador', 'Você entrou sem pagar.'),
    2: ('Sombra Faminta', 'Eu sinto seu medo.'),
    9: ('Quimera Instável', 'Múltiplas almas, um corpo.'),
    15: ('Arquiduque do Pavor', 'Você não deveria ter chegado aqui.'),
    18: ('CALAMIDADE', 'O fim já começou.')
}

#========================
#------ UTIL ------
#========================

def slow_print(text, delay=0.08):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')
    sys.stdout.flush()
    time.sleep(0.01)

#========================
#------ PLAYER ------
#========================

class Player:
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

#========================
#------ VILA ------
#========================

def blacksmith(p):
    slow_print('⚒️ Ferreiro: aço não mente.')
    # [SISTEMA DE ARMADURA] - Opções de Compra, Upgrade e Reparo
    print('1. Comprar Armas | 2. Comprar Armaduras | 3. Upgrade | 4. Reparar Armadura (50g) | 5. Sair')
    op = input('> ')

    if op == '1':
        print('1. Espada (100g) | 2. Machado (200g)')
        c = input('> ')
        if c == '1' and p.money >= 100:
            p.money -= 100
            p.weapon = 'Espada'
        elif c == '2' and p.money >= 200:
            p.money -= 200
            p.weapon = 'Machado'

    elif op == '2':
        # [SISTEMA DE ARMADURA] - Tipos de Armadura para compra
        print('1. Cota de Malha (150g) [Def: 2]')
        print('2. Armadura de Espinhos (300g) [Def: 4]')
        print('3. Manto Vampírico (500g) [Def: 6]')
        c = input('> ')
        if c == '1' and p.money >= 150:
            p.money -= 150
            p.armor = {'nome': 'Cota de Malha', 'defesa': 2, 'durabilidade': 100, 'max_durabilidade': 100, 'efeito_especial': None, 'level': 1}
        elif c == '2' and p.money >= 300:
            p.money -= 300
            p.armor = {'nome': 'Armadura de Espinhos', 'defesa': 4, 'durabilidade': 120, 'max_durabilidade': 120, 'efeito_especial': 'espinhos_caoticos', 'level': 1}
        elif c == '3' and p.money >= 500:
            p.money -= 500
            p.armor = {'nome': 'Manto Vampírico', 'defesa': 6, 'durabilidade': 150, 'max_durabilidade': 150, 'efeito_especial': 'sede_de_sangue', 'level': 1}

    elif op == '3':
        print('O que deseja melhorar? (Custo: 100g)')
        print('1. Arma | 2. Armadura')
        u = input('> ')
        if p.money >= 100:
            if u == '1':
                p.money -= 100
                p.weapon_level += 1
                print(f'⚔️ Sua {p.weapon} agora é Nível {p.weapon_level}!')
            elif u == '2':
                # [SISTEMA DE ARMADURA] - Lógica de Upgrade
                if p.armor:
                    p.money -= 100
                    p.armor['level'] = p.armor.get('level', 1) + 1
                    p.armor['defesa'] += 3
                    p.armor['max_durabilidade'] += 20
                    print(f'🛡️ Sua {p.armor["nome"]} agora é Nível {p.armor["level"]}! (Defesa +3)')
                else:
                    print('❌ Você não tem armadura para melhorar.')
        else:
            print('❌ Dinheiro insuficiente.')

    elif op == '4' and p.money >= 50:
        # [SISTEMA DE ARMADURA] - Reparo de Durabilidade
        if p.armor:
            p.money -= 50
            p.armor['durabilidade'] = p.armor['max_durabilidade']
            print('🛠️ Armadura como nova!')
        else:
            print('❌ Sem armadura para reparar.')

def alchemist(p):
    slow_print('🧪 Alquimista: cura ou mana?')
    print('1. Poção (30g) | 2. Mana (40g)')
    c = input('> ')
    if c == '1' and p.money >= 30:
        p.money -= 30
        p.inventory['pocoes'] += 1
    elif c == '2' and p.money >= 40:
        p.money -= 40
        p.mana = p.max_mana

def guild(p):
    slow_print('📜 Guilda')
    print('1. Vender troféus | 2. Missão')
    c = input('> ')
    if c == '1':
        if p.inventory['cabecas_boss']:
            p.money += len(p.inventory['cabecas_boss']) * 100
            p.inventory['cabecas_boss'] = []
    elif c == '2':
        p.money += 50
        p.gain_exp(20)

#===========================================
#------ COMBATE (COM DEFESA ADAPTADA) ------
#===========================================

def calcular_defesa_integrada(dano_inimigo, player):
    # [SISTEMA DE ARMADURA] - Efeitos especias, dano, defesa
    if not player.armor:
        return dano_inimigo

    armadura = player.armor
    if armadura['durabilidade'] <= 0:
        print(f'⚠️ Sua {armadura["nome"]} está em pedaços!')
        return dano_inimigo

    dano_reduzido = max(0, dano_inimigo - armadura['defesa'])
    desgaste = max(1, int(dano_inimigo * 0.1))
    armadura['durabilidade'] = max(0, armadura['durabilidade'] - desgaste)

    efeito_ativado = False
    if armadura.get('efeito_especial') == 'sede_de_sangue':
        if random.randint(1, 100) <= 25:
            efeito_ativado = True
            cura = dano_inimigo
            player.health = min(player.max_health, player.health + cura)
            print(f'🦇 {armadura["nome"]} suga a vitalidade! +{cura} HP!')
            dano_reduzido = 0
    elif armadura.get('efeito_especial') == 'espinhos_caoticos':
        if random.randint(1, 100) <= 20:
            efeito_ativado = True
            print(f'💥 {armadura["nome"]} reflete parte do ataque!')
            dano_reduzido = int(dano_reduzido / 2)

    if not efeito_ativado:
        print(f'⚔️ Defesa: {armadura["defesa"]} | Dano final: {dano_reduzido}')

    return dano_reduzido

def combat(p, enemy, hp, dmg_range, boss=False):
    extra_defense = 0
    if boss: slow_print(f'🔥 {enemy}')

    while hp > 0 and p.health > 0:
        print(f'\n{enemy} HP:{hp} | Player HP:{p.health}')
        print('1.Atacar 2.Magia 3.Poção 4.Defender 5.Fugir')
        c = input('> ')

        if c == '1':
            dmg = random.randint(8, 18) * p.weapon_level
            hp -= dmg
        elif c == '2':
            for i, s in enumerate(p.skills): print(f'{i}. {s["nome"]}')
            try:
                idx = int(input('index: '))
                skill = p.skills[idx]
                if p.mana >= skill['custo']:
                    p.mana -= skill['custo']
                    hp -= (25 + p.level * 5)
                else: print('Mana insuficiente!')
            except: pass
        elif c == '3' and p.inventory['pocoes'] > 0:
            p.inventory['pocoes'] -= 1
            p.health = min(p.max_health, p.health + 50)
        elif c == '4':
            extra_defense = random.randint(5, 15)
        elif c == '5' and not boss:
            if random.random() < 0.5: return 'fled'

        if hp > 0:
            raw_dmg = random.randint(*dmg_range)
            final_dmg = calcular_defesa_integrada(raw_dmg, p) - extra_defense
            p.health -= max(0, final_dmg)
            extra_defense = 0

    if p.health <= 0: return False
    if boss: p.inventory['cabecas_boss'].append(enemy)
    p.gain_exp(100 if boss else 30)
    return True

#========================
#------ DUNGEON ------
#========================

def dungeon(p):
    floor = 1
    while floor <= 18:
        print(f'\n--- FLOOR {floor} ---')
        act = input('1.Avançar 2.Descansar 3.Sair ')
        if act == '1':
            # [SISTEMA DE ARMADURA] - Garantido no 6
            if floor == 6 and not p.armor:
                found = {'nome': 'Cota de Malha Velha', 'defesa': 2, 'durabilidade': 50, 'max_durabilidade': 80, 'efeito_especial': None, 'level': 1}
                slow_print(f'🎁 Você encontrou um baú no andar 6! Contém uma {found["nome"]}.')
                if input('Equipar? 1.Sim 2.Não > ') == '1':
                    p.armor = found
                    print('🛡️ Armadura equipada!')

            r = random.randint(1, 100)
            if r < 45:
                combat(p, f'Monstro {floor}', 50 + floor * 8, (5, 10 + floor))
            elif r < 75:
                slow_print(random.choice(LORE_SCROLLS))
            else:
                boss = BOSS_LORE.get(floor)
                if boss:
                    name, talk = boss
                    slow_print(f'{name}: {talk}')
                    if combat(p, name, 120 + floor * 20, (10, 20 + floor), True): floor += 1
                    else: break
                else: floor += 1
        elif act == '2':
            p.mana = p.max_mana
            print('✨ Mana restaurada!')
        elif act == '3': break

#========================
#------ MAIN ------
#========================

def main():
    for l in LORE_INTRO: slow_print(l)
    choice = input('1.Novo 2.Load ')
    p = load_game() if choice == '2' else None
    if not p: p = Player(input('Nome: '))

    while p.health > 0:
        p.display_status()
        print('\n1.Ferreiro 2.Alquimista 3.Guilda 4.Dungeon 5.Save 6.Sair')
        op = input('> ')
        if op == '1': blacksmith(p)
        elif op == '2': alchemist(p)
        elif op == '3': guild(p)
        elif op == '4': dungeon(p)
        elif op == '5': save_game(p)
        elif op == '6': break

if __name__ == '__main__':
    main()