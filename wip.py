import pandas as pd
poke_file = "Pokemon/type_matchups.csv"
type_poke = pd.read_csv(poke_file)
type_poke = type_poke.set_index("TYPE")
poke_file = "Pokemon/pokemon_gen1.csv"
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

p1active = poke.iloc[0,:]
p2active = poke.iloc[1,:]

type_matchups = pd.DataFrame({
    "0.0":["Ineffective"],
    "0.5":["Mildly Effective"],
    "1.0":["Effective"],
    "2.0":["Very Effective"]
})

a = type_poke.loc[p2active[2],p1active[2]]
b = type_matchups.loc[0,str(a)]
print(f"Coef {a} and result {b}")



