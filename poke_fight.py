#Poke Fight! ---------------------------------------------------------------

#Import package, read file and clean data
import pandas as pd
import random
import sys
import functions as fn

#Variables
atk_coef = 0.35
def_coef = 0.005
eva_coef = 0.35
pl_action = "hold"
pl_sel_choices = ["A","a","S","s","P","p","R","r"]
pl_sel_sp = ["S","s"]
ai_action = "A"
ai_sel_choices = ["A","S","P"]

#Intro
#------------------------------------------------------------
#Mode Selection & Roster Count Selection & Pokemon Pool Selection & File Import and Clean
intro = "hold"
game_modes = ["1","2"]
while intro not in game_modes:
    intro = input("\nWelcome to Poke Fight!\nPlease select a game mode\n"
    "[1] One Player\n[2] Two Player   ")
count_choice = "hold"
count_range = [str(i) for i in range(2,7)]
while count_choice not in count_range:
    count_choice = input("\nHow many Pokemon would you like to battle with? (2-6)   ")
poke_pools = [str(i) for i in range(1,5)]
pool_choice = "hold"
while pool_choice not in poke_pools:
    pool_choice = input("\nWhich Pokemon roster would you like to play with?"
    "\n[1] Red & Blue\n[2] Silver & Gold\n[3] All Generations\n[4] Legendary Only    ")
if pool_choice == "1":
    poke_file = "Pokemon/pokemon_gen1.csv"
if pool_choice == "2":
    poke_file = "Pokemon/pokemon_gen2.csv"
if pool_choice == "3":
    poke_file = "Pokemon/pokemon_med_str.csv"
if pool_choice == "4":
    poke_file = "Pokemon/pokemon_legendary.csv"
poke = pd.read_csv(poke_file)
del poke["Legendary"]
del poke["Generation"]
del poke["Type 2"]
poke.rename(columns={
    "Type 1":"Type",
    "Attack":"ATK",
    "Defense":"DEF",
    "Sp. Atk":"SP ATK",
    "Sp. Def":"SP DEF",
    "Speed":"SPEED",
    "SPATK Count":"SP ATK Charges"
},inplace=True)


    
#Name Selection & Roster Selection
p1name = input("\nPlayer 1, please enter your name:   ")
players = [("Player 1",p1name)]
#One Player
if intro == "1":
    fn.player_roster_sel(1,players,count_choice,poke)
    p1roster = fn.p1roster
    p2name = "AI Opponent"
    players.append(("Player 2",p2name))
    fn.ai_roster_sel(count_choice,poke)
    p2roster = fn.p2roster
#Two Player
if intro == "2":
    p2name = input("\nPlayer 2, please enter your name:   ")
    players.append(("Player 2",p2name))
    fn.player_roster_sel(1,players,count_choice,poke)
    p1roster = fn.p1roster
    print("BREAK")
    fn.player_roster_sel(2,players,count_choice,poke)
    p2roster = fn.p2roster

print(p2roster.iloc[1,4])

#1st Pokemon_Selection
#One Player
if intro == "1":
    print(f"\nAI Opponent's Pokemon\n{p2roster.to_string(index=False)}")
    fn.player_poke_sel(1,players,p1roster)
    p1active = fn.plactive
    p1idx = fn.plidx
    fn.ai_poke_sel(p2roster)
    p2active = fn.plactive
    p2idx = fn.aiidx
#Two Player
if intro == "2":
    fn.player_poke_sel(1,players,p1roster)
    p1active = fn.plactive
    p1idx = fn.plidx
    fn.player_poke_sel(2,players,p2roster)
    p2active = fn.plactive
    p2idx = fn.plidx

#Turn Loop
#------------------------------------------------------------
#Turn Order & Top While Loop
p1_ros_hp = "Fine"
p2_ros_hp = "Fine"
while p1_ros_hp == "Fine" and p2_ros_hp == "Fine":
    if p1active["SPEED"] > p2active["SPEED"]:
        turn_ord = [1,2]
    if p1active["SPEED"] < p2active["SPEED"]:
        turn_ord = [2,1]
    if p1active["SPEED"] == p2active["SPEED"]:
        coin_toss = random.randint(0,100)
        if coin_toss > 50:
            turn_ord = [1,2]
        if coin_toss < 50:
            turn_ord = [2,1]
    #Turn Actions & Inner For Loop
    for i in turn_ord:
        if i == 1:
            plroster = p1roster
            plactive = p1active
            plidx = p1idx
            oproster = p2roster
            opactive = p2active
            opidx = p2idx
            j = 2
        if i == 2:
            plroster = p2roster
            plactive = p2active
            plidx = p2idx
            oproster = p1roster
            opactive = p1active
            opidx = p1idx
            j = 1
        print(f"\n{players[i-1][1]}'s turn!\n{plactive[0]}")
        if players[1][1] == "AI Opponent" and i == 2:
            pl_action = ai_action
        while pl_action not in pl_sel_choices:
            pl_action = input(f"Choose Action:\n[A] Attack\n[S] Special Attack\n[P] Swap Pokemon\n[R] Retreat\n")
            if pl_action in pl_sel_sp and plactive[9] == 0:
                pl_action = "hold"
                print(f"{plactive[0]} is out of special attacks!")
        if pl_action in pl_sel_sp:
            plroster.iloc[plidx,9] = int(plroster.iloc[plidx,9]) - 1
        if pl_action == "R" or pl_action == "r":
            print(f"{players[i-1][1]} retreated! {players[j-1][1]} wins")
            sys.exit()
        if pl_action == "P" or pl_action == "p":
            fn.player_poke_sel(i,players,plroster)
            plactive = fn.plactive
            plidx = fn.plidx
        else:
            fn.attack(i,pl_action,plactive,opactive,atk_coef,def_coef,eva_coef)
            oproster.iloc[opidx,3] = fn.defender_hp
            opactive = oproster.iloc[opidx,:]
        if opactive.iloc[3] == 0:  
            fn.HP_CHK(oproster)
            if fn.hp == 0:
                if i == 1:
                    p2_ros_hp = "KO'd"
                if i == 2:
                    p1_ros_hp = "KO'd"
                fn.endgame(players,p1roster,p2roster,p1_ros_hp,p2_ros_hp)
                sys.exit()
            if players[1][1] == "AI Opponent" and i == 1:
                fn.ai_poke_sel(p2roster)
            else:
                fn.player_poke_sel(j,players,oproster)
            opactive = fn.plactive
            opidx = fn.plidx
        if i == 1:
            p1roster = plroster
            p1active = plactive
            p1idx = plidx
            p2roster = oproster
            p2active = opactive
            p2idx = opidx
        if i == 2:
            p2roster = plroster
            p2active = plactive
            p2idx = plidx
            p1roster = oproster
            p1active = opactive
            p1idx = opidx
        pl_action = "hold"
    print("\n------------------------------------")
    print(f"{p1active[0]} - {p1active[3]} HP")
    print(f"{p2active[0]} - {p2active[3]} HP")
    print("------------------------------------")

