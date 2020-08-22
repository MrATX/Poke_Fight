def ai_roster_sel(count_choice,poke):
    import random
    ros_count = int(count_choice)
    idx = []
    i = ros_count
    while i > 0:
        p2pick = random.randint(0,(len(poke)-1))
        if p2pick not in idx:
            idx.append(p2pick)
            i = i - 1
    global p2roster
    p2roster = poke.iloc[[idx[i] for i in range(0,ros_count)],1:]
    p2roster.reset_index(inplace=True)
    p2roster = p2roster.iloc[:,1:]

def player_roster_sel(plnum,players,count_choice,poke):
        ros_count = int(count_choice)
        poke_names = poke["Name"]
        indexnums = poke["#"]
        indexnums = str(indexnums)
        idx = []
        poke_choice = "hold"
        plup = players[plnum-1][1]
        print(poke.to_string(index = False))
        print(f'\nWelcome {plup}! Please choose {count_choice} Pokemon from the list above.')
        wip = "hold"
        while wip == "hold":
            poke_choice = input(f'\nUse the number in the left most column to make your selection --->>   ')
            if poke_choice not in indexnums or poke_choice == "0" or poke_choice == "" or " " in poke_choice:
                print(f"Make sure your input is a number (1 to {len(poke)}) --->>   ")
            if poke_choice in indexnums and poke_choice != "0" and poke_choice != "" and " " not in poke_choice:
                idx.append(int(poke_choice)-1)
            if len(idx) == ros_count:
                print("")
                for i in idx:
                    print(poke_names.iloc[i])
                player_ready = input(f"\nAre these the Pokemon you want to take into battle, {plup}? (Y/N)   ")
                ready_yes = ["Y","y"]
                if player_ready in ready_yes and player_ready != "0" and player_ready != "" and " " not in player_ready:
                    if plnum == 1:
                        global p1roster
                        p1roster = poke.iloc[[idx[i] for i in range(0,ros_count)],1:]
                        p1roster.reset_index(inplace=True)
                        p1roster = p1roster.iloc[:,1:]
                    if plnum == 2:
                        global p2roster
                        p2roster = poke.iloc[[idx[i] for i in range(0,ros_count)],1:]
                        p2roster.reset_index(inplace=True)
                        p2roster = p2roster.iloc[:,1:]
                    wip = "pass"
                if player_ready not in ready_yes:
                    idx = []

def ai_poke_sel(roster):
    import random
    global plidx
    wip = "hold"
    while wip == "hold":
        plidx = random.randint(0,len(p2roster)-1)
        if p2roster.iloc[plidx,3] > 0:
            global p2active
            p2active = p2roster.iloc[plidx]
            wip = "pass"
            print(f"\nAI Opponent sends out {p2active[0]} - {p2active[3]} HP\n")

def player_poke_sel(plnum,players,roster):
    print(f"\n{players[plnum-1][1]}'s Pokemon")
    print(roster.to_string(index=False))
    global plactive
    global plidx
    plidx_range = []
    for i in range(len(roster)):
        plidx_range.append(str(i+1))
    wip = "hold"
    while wip == "hold":
        plidx = input(f"\nWhich Pokemon would you like to send into battle, {players[plnum-1][1]}?\nSelect with index number (1 to {len(roster)})   ")
        if plidx not in plidx_range or plidx == "" or " " in plidx or plidx == "0":
            print(f"\nBe sure and use a proper index (1 to {len(roster)})   ")
        if plidx in plidx_range and plidx != "" and " " not in plidx and plidx != "0":
            plidx = int(plidx) - 1
            if roster.iloc[plidx,3] == 0:
                print(f"\n{roster.iloc[plidx,0]} is KO'd. Please select a different Pokemon.   ")
            if roster.iloc[plidx,3] > 0:
                plactive = roster.iloc[plidx]
                wip = "pass"
                print(f"\n{players[plnum-1][1]} sends out {plactive[0]} - {plactive[4]} HP")
                if plnum == 1:
                    global p1active
                    p1active = plactive
                if plnum == 2:
                    global p2active
                    p2active = plactive

def attack(plnum,action,attacker,defender,atk_coef,def_coef,eva_coef,type_poke,type_matchups):
    import random
    global defender_hp
    if plnum == 1:
        oppnum = 2
    else:
        oppnum = 1
    attack_texts = ({"A":"attacked","a":"attacked","S":"used a special attack","s":"used a special attack"})
    #Damage Calucation
    if action == "A" or action == "a":
        atk_dmg = int((atk_coef*attacker.loc["ATK"]*(1 - (def_coef*defender.loc["DEF"]))))
    if action == "S" or action == "s":
        type_coef = type_poke.loc[attacker[1],defender[1]]
        effect = type_matchups.loc[0,str(type_coef)]
        atk_dmg = int((atk_coef*attacker.loc["SP ATK"]*(1-(def_coef*defender.loc["SP DEF"])))*type_coef*1.15)
    #Attack
    if action == "S" or action == "s":
        eva_coef = 0
    if random.randint(1,100) > (eva_coef*defender.loc["SPEED"]):
        defender_hp = defender.loc["HP"] - atk_dmg
        if defender_hp < 0:
            defender_hp = 0
        if defender_hp == 0:
            print(f"{attacker[0]} {attack_texts[action]} for {atk_dmg} DMG and KO'd {defender[0]}!")
        if defender_hp > 0:
            print(f'{attacker[0]} {attack_texts[action]} for {atk_dmg} DMG!')
            if action == "S" or action == "s":
                print(f"It was {effect}!")
    else:
        defender_hp = defender.loc["HP"]
        print(f'{attacker[0]} MISSED!')
    

def HP_CHK(roster):
    global hp
    hp = 0
    for i in range(0,len(roster)):
        hp = hp + int(roster.iloc[i,3])


def endgame(players,p1roster,p2roster,p1_ros_hp,p2_ros_hp):
    print(f"\n{players[0][1]}'s Pokemon")
    print(p1roster.to_string(index=False))
    print(f"\n{players[1][1]}'s Pokemon")
    print(p2roster.to_string(index=False))
    print("")
    if p1_ros_hp == "Fine":
        print(f"{players[0][1]} wins!!!")
    if p2_ros_hp == "Fine":
        print(f"{players[1][1]} wins!!!")