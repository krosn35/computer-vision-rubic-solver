import cv2
import numpy as np
import tkinter as tk
import kociemba
from tkinter import messagebox

cap = cv2.VideoCapture(0)

bili = [0, 0, 0, 0, 1, 0, 0, 0, 0]   #bila=1
zluty = [0, 0, 0, 0, 2, 0, 0, 0, 0]   #zluta=2
zeleny = [0, 0, 0, 0, 3, 0, 0, 0, 0]     #zelena=3
cerveny = [0, 0, 0, 0, 4, 0, 0, 0, 0]    #cervena=4
modry = [0, 0, 0, 0, 5, 0, 0, 0, 0]   #modra=5
oranzovy = [0, 0, 0, 0, 6, 0, 0, 0, 0]  #oranzova=6

CISLO_NA_SMER = {
    1: "U",
    2: "D",
    3: "F",
    4: "R",
    5: "B",
    6: "L"
}

PREKLAD = {
    "U":"bílou do leva",
    "U'":"bílou do prava",
    "U2":"bílou 2x do prava",
    "R":"červenou nahoru",
    "R'":"červenou dolů",
    "R2":"červenou 2x nahoru",
    "F":"zelenou po směru hodinových ručiček",
    "F'":"zelenou proti směru hodinových ručiček",
    "F2":"zelenou otočit o 180",
    "D":"žlutou do prava",
    "D'":"žlutou do leva",
    "D2":"žlutou 2x do prava",
    "L":"oranžovou dolu",
    "L'":"oranžovou nahoru",
    "L2":"oranžovou 2x nahoru",
    "B":"modrou po směru hodinových ručiček",
    "B'":"modrou proti směru hodinových ručiček",
    "B2":"modrou o 180"
}

BARVY_CISLO = {
    0:"grey",
    1:"white",
    2:"yellow",
    3:"green",
    4:"red",
    5:"blue",
    6:"orange"
}

BARVY_NA_CISLA = {
    "neznama": 0,
    "bila": 1,
    "zluta": 2,
    "zelena": 3,
    "cervena": 4,
    "modra": 5,
    "oranzova": 6,
    "neznama": 0
}

BARVYLIST = {
    0:"grey",
    1:bili,
    2:zluty,
    3:zeleny,
    4:cerveny,
    5:modry,
    6:oranzovy
}

ROZSAHY_HSV = {
    "bila": {"lower": np.array([0, 0, 150]), "upper": np.array([180, 50, 255])},
    "oranzova": {"lower": np.array([5, 100, 100]), "upper": np.array([15, 255, 255])},
    "zluta": {"lower": np.array([21, 100, 100]), "upper": np.array([35, 255, 255])},
    "zelena": {"lower": np.array([40, 70, 70]), "upper": np.array([85, 255, 255])},
    "modra": {"lower": np.array([90, 100, 100]), "upper": np.array([130, 255, 255])},
    "cervena_1": {"lower": np.array([0, 100, 100]), "upper": np.array([5, 255, 255])},
    "cervena_2": {"lower": np.array([150, 100, 100]), "upper": np.array([180, 255, 255])},
}

def detekuj_barvu(prumerny_hsv):
    c1, c2 = ROZSAHY_HSV["cervena_1"], ROZSAHY_HSV["cervena_2"]
    if (c1["lower"][0] <= prumerny_hsv[0] <= c1["upper"][0] and
        c1["lower"][1] <= prumerny_hsv[1] <= c1["upper"][1] and
        c1["lower"][2] <= prumerny_hsv[2] <= c1["upper"][2]) or \
       (c2["lower"][0] <= prumerny_hsv[0] <= c2["upper"][0] and
        c2["lower"][1] <= prumerny_hsv[1] <= c2["upper"][1] and
        c2["lower"][2] <= prumerny_hsv[2] <= c2["upper"][2]):
        return "cervena"

    for nazev, meze in ROZSAHY_HSV.items():
        if "cervena" in nazev:
            continue
        if (meze["lower"][0] <= prumerny_hsv[0] <= meze["upper"][0] and
            meze["lower"][1] <= prumerny_hsv[1] <= meze["upper"][1] and
            meze["lower"][2] <= prumerny_hsv[2] <= meze["upper"][2]):
            return nazev
    return "neznama"

POZICE_KRUHU = [
    (200, 120), (320, 120), (440, 120),
    (200, 240), (320, 240), (440, 240),
    (200, 360), (320, 360), (440, 360)
]

BGR_BARVY = {
    "bila": (255, 255, 255), "oranzova": (0, 165, 255), "zluta": (0, 255, 255),
    "zelena": (0, 255, 0), "modra": (255, 0, 0), "cervena": (0, 0, 255), "neznama": (128, 128, 128)
}

def solve():
    try:
        vse = bili + cerveny + zeleny + zluty + oranzovy + modry
        kod = "".join(CISLO_NA_SMER[cislo] for cislo in vse)
        reseni = kociemba.solve(kod)
        
    except Exception as e:
        print("problem se slozenim")
    try:
        messagebox.showinfo("reseni",preklad(reseni))
    except Exception as e:
        print("nedokaze se prelozit")
        print(reseni)
def preklad(text):
    global off
    tahy = text.split() 
    vysledny_postup = ""
    for tah in tahy:
        if tah in PREKLAD:
            vysledny_postup += PREKLAD[tah] + "\n"
        else:
            vysledny_postup += f"Neznámý tah: {tah}\n"
    off = True
    return vysledny_postup
off = False
root = tk.Tk()
pole = tk.Frame(root)
pole.pack(expand=True, fill="both") #mainframe
for i in range(4):
    pole.columnconfigure(i, weight=1)
    if i < 4:
        pole.rowconfigure(i, weight=1)
hotovo = tk.Button(root, text="done" , command=lambda:solve())
hotovo.pack()
framebila = tk.Frame(pole)
for i in range(3):
    framebila.columnconfigure(i, weight=1)
    framebila.rowconfigure(i, weight=1)
framebila.grid(row=0, column=1)
# Nejdříve si vytvoříš prázdný seznam pro tlačítka bílé stěny
tlacitka_bila = []

for i in range(9):
    btn = tk.Button(
        framebila, 
        background=BARVY_CISLO[bili[i]], 
        activebackground=BARVY_CISLO[bili[i]]
    )
    
    btn.grid(row=i // 3, column=i % 3, sticky="nsew", padx=2, pady=2)
    
    tlacitka_bila.append(btn)

frameoranzova = tk.Frame(pole)
for i in range(3):
    frameoranzova.columnconfigure(i, weight=1)
    frameoranzova.rowconfigure(i, weight=1)
frameoranzova.grid(row=1, column=0)
tlacitka_oranzova = []

for i in range(9):
    btn = tk.Button(
        frameoranzova, 
        background=BARVY_CISLO[oranzovy[i]], 
        activebackground=BARVY_CISLO[oranzovy[i]]
    )
    
    btn.grid(row=i // 3, column=i % 3, sticky="nsew", padx=2, pady=2)
    tlacitka_oranzova.append(btn)

framezelena = tk.Frame(pole)
for i in range(3):
    framezelena.columnconfigure(i, weight=1)
    framezelena.rowconfigure(i, weight=1)
framezelena.grid(row=1, column=1)
tlacitka_zelena = []

for i in range(9):
    btn = tk.Button(
        framezelena, 
        background=BARVY_CISLO[zeleny[i]], 
        activebackground=BARVY_CISLO[zeleny[i]]
    )
    
    btn.grid(row=i // 3, column=i % 3, sticky="nsew", padx=2, pady=2)
    tlacitka_zelena.append(btn)


framecervena = tk.Frame(pole)
for i in range(3):
    framecervena.columnconfigure(i, weight=1)
    framecervena.rowconfigure(i, weight=1)
framecervena.grid(row=1, column=2)
tlacitka_cervena = []

for i in range(9):
    btn = tk.Button(
        framecervena, 
        background=BARVY_CISLO[cerveny[i]], 
        activebackground=BARVY_CISLO[cerveny[i]]
    )
    
    btn.grid(row=i // 3, column=i % 3, sticky="nsew", padx=2, pady=2)
    tlacitka_cervena.append(btn)


framemodra = tk.Frame(pole)
for i in range(3):
    framemodra.columnconfigure(i, weight=1)
    framemodra.rowconfigure(i, weight=1)
framemodra.grid(row=1, column=3)
tlacitka_modra = []

for i in range(9):
    btn = tk.Button(
        framemodra, 
        background=BARVY_CISLO[modry[i]], 
        activebackground=BARVY_CISLO[modry[i]]
    )
    
    btn.grid(row=i // 3, column=i % 3, sticky="nsew", padx=2, pady=2)
    tlacitka_modra.append(btn)


framezluta = tk.Frame(pole)
for i in range(3):
    framezluta.columnconfigure(i, weight=1)
    framezluta.rowconfigure(i, weight=1)
framezluta.grid(row=2, column=1)
tlacitka_zluta = []

for i in range(9):
    btn = tk.Button(
        framezluta, 
        background=BARVY_CISLO[zluty[i]], 
        activebackground=BARVY_CISLO[zluty[i]]
    )
    
    btn.grid(row=i // 3, column=i % 3, sticky="nsew", padx=2, pady=2)
    tlacitka_zluta.append(btn)

def update_gui():
    steny_mapping = [
        (tlacitka_bila, BARVYLIST[1]),
        (tlacitka_zluta, BARVYLIST[2]),
        (tlacitka_zelena, BARVYLIST[3]),
        (tlacitka_cervena, BARVYLIST[4]),
        (tlacitka_modra, BARVYLIST[5]),
        (tlacitka_oranzova, BARVYLIST[6]),
    ]

    
    for tlacitka_steny, data_steny in steny_mapping:
        for i in range(9):
            cislo_barvy = data_steny[i]
            nazev_barvy = BARVY_CISLO.get(cislo_barvy, "grey")
            
            
            tlacitka_steny[i].config(
                background=nazev_barvy, 
                activebackground=nazev_barvy
            )

barvy_steny = []
def barvy_binar(obsah):

    return [BARVY_NA_CISLA.get(barva, 0) for barva in obsah]
def shot():
    global barvy_steny
    barvy_steny = []

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for (cx, cy) in POZICE_KRUHU:
        r = 10
        roi = hsv[cy - r:cy + r, cx - r:cx + r]
        prumerny_hsv = cv2.mean(roi)[:3]

        detekovana_barva = detekuj_barvu(prumerny_hsv)
        barvy_steny.append(detekovana_barva)

        # DEBUG
        #print(f"({cx},{cy}) HSV={tuple(round(v,1) for v in prumerny_hsv)} -> {detekovana_barva}")

    #print("Detekovano:", barvy_steny)

    if len(barvy_steny) == 9:
        barvy_steny_b = barvy_binar(barvy_steny)
        stredova_barva = barvy_steny_b[4]

        if stredova_barva in BARVYLIST and stredova_barva != 0:
            BARVYLIST[stredova_barva][:] = barvy_steny_b
            update_gui()
            #print(f"Stěna s číslem {stredova_barva} byla úspěšně uložena!")
        else:
            print(f"Chyba: střed = {barvy_steny[4]} (HSV nebylo v žádném rozsahu)")

        barvy_steny = []
def tisk():
    pass
while True:
    if off:
        break
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for (cx, cy) in POZICE_KRUHU:
        r = 10
        roi = hsv[cy - r:cy + r, cx - r:cx + r]
        prumerny_hsv = cv2.mean(roi)[:3]

        detekovana_barva = detekuj_barvu(prumerny_hsv)

        barva_bgr = BGR_BARVY[detekovana_barva]
        cv2.circle(frame, (cx, cy), 15, barva_bgr, 2)
        cv2.putText(frame, detekovana_barva[:3], (cx - 12, cy + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, barva_bgr, 1)

        
        #cv2.putText(frame, f"{int(prumerny_hsv[0])},{int(prumerny_hsv[1])},{int(prumerny_hsv[2])}",
         #      (cx - 20, cy + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

    cv2.imshow('Skenovani kostky', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        shot()
    if key == ord("q"):
        break
    if key == ord("p"):
        tisk()

    root.update_idletasks()
    root.update()
    
cap.release()
cv2.destroyAllWindows()