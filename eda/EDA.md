Considerazioni rilevanti sul dataset Recipe NLG
 
shape:(2231142, 4)
title             str
ingredients       str
directions        str
NER            object

numero di elementi null:
title          1
ingredients    0
directions     0
NER            0

Titoli duplicati: 918,271
count    1.312870e+06
mean     1.699438          
std      1.359383e+01
min      1.00
25%      1.00
50%      1.00
75%      1.00
max      4.099e+03  
//in media ogni titolo è presente 1,7 volte => in generale ci sono molte ricette uniche, i titoli duplicati sono sbilanciati verso alcune ricette in particloare visto che 50%(mediana) e 75% valgoni 1.

20 titoli con più duplicati
Chicken Casserole         4099
Broccoli Casserole        3985
Squash Casserole          2508
Cheese Ball               2426
Zucchini Bread            2298
Pecan Pie                 2285
Banana Bread              2085
Meat Loaf                 1769
Pumpkin Bread             1729
Corn Casserole            1726
Cranberry Salad           1713
Fruit Salad               1710
Potato Casserole          1671
Broccoli Salad            1610
Baked Beans               1573
Banana Nut Bread          1538
Peanut Butter Cookies     1522
Sweet Potato Casserole    1497
Carrot Cake               1496
Taco Salad                1458

Analisi del numero di ingredienti nelle ricette(analizzando la colonna NER)

mean     8.480523
std      3.955563
min      0.000000 (strano)
50%      8.000000
90%      13.000
95%      16.000
99%      21.000
max      402.00 (strano)

- Ci sono 58 ricette con più di 50 ingredienti
- Ci sono 573 ricette con 0 ingredienti(colonna NER=[])

Ricette con almeno 70 ingredienti:

719239                         Grandma'S Chicken Fricassee            402
122527                                       Layered Salad            328
27310                                    Strawberry Butter            276
719917                               Dumplings And Cabbage            219
1997023                           D.I.Y Spice Blends (No3)             98
1874449                           D.I.Y Spice Blends (No1)             93
1648729                           D.I.Y Spice Blends (No2)             86
1769297                                        Smorgasbord             85
146754   Kate'S Date Pudding("Will Keep For Months And ...             81
2153680                  Rebuilt Louisiana Seafood Platter             74
206825                                        Venison Stew             73
808450                                           Fish Loaf             71
1309190                   Sable Fish With Florida Truffle              70

Alcune ricette con 0 ingredineti:
                               title                             ingredients NER
1448             Pork Shoulder Roast                  ["roast (3 to 5 lb.)"]  []
2547   Peek-A-Boo Cake(Bingo Cake)    ["1 box Duncan Hines yellow cake mix"]  []
15584              Pocket Sandwiches   ["10 oz. tube refrigerated biscuits"]  []
19473    Pressure Cooker Swiss Steak               ["1 1/2 lb. round steak"]  []
25245               Ribs(Serves 8)                    ["4 ribs (baby back)"]  []


Coppie di ingredienti più frequenti:
flour + salt: 281706
salt + sugar: 273818
flour + sugar: 242307
butter + salt: 221497
eggs + salt: 214235
eggs + sugar: 201370
onion + salt: 188812
eggs + flour: 188553
butter + flour: 182451
sugar + vanilla: 177300
butter + sugar: 171569
garlic + salt: 170043
milk + salt: 162134
salt + water: 151463
butter + eggs: 137969
flour + vanilla: 136650
pepper + salt: 136285
eggs + vanilla: 134046
salt + vanilla: 132510
milk + sugar: 131013