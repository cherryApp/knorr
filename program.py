import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import re
import os
""" 
# PID lista készítése a fájl alapján.
file_name = input('Adja meg a lista fájl nevét: ')

# Megnyitjuk a fájlt a megadott név alapján.
try:
  list_file = open(file_name, "r", encoding="iso-8859-2")
except:
  print('HIBA: nem sikerült megnyitni a fájlt. Ellenőrizze a fájlnevet!')
  exit()

# Fájl tartalmának beolvasása és PID kigyűjtése.
pid_dict = {}
pattern = r"PID\d{8}[A-Z]\d{3}"
for line in list_file.readlines():
  hasPID = 'PID' in line
  if hasPID:
    pid = re.findall(pattern, line)[0]
    pid_dict[pid] = []

pid_list = list( pid_dict.keys() )
list_file.close()
print("\nPID lista beolvasva!")

# Adott mappában található .txt fájlok beolvasása.
txt_dir = input('\n\nAdja meg a .txt fájlokat tartalmazó mappa nevét: ')
try:
  txt_file_list = os.listdir(txt_dir)
except:
  print('HIBA: a megadott mappanév helytelen, vagy a mappa nem létezik!')
  exit()

# Létrehozunk egy dictionary-t amiben a Continental azonosítók lesznek a kulcsok.
conti_az = {}

# Egyesével végigmegyünk a megadott mappában található .txt fájlokon.
for txt_file_name in txt_file_list:
  # Megynyitjuk a soron következő .txt fájlt.
  with open(txt_dir + '/' + txt_file_name, 'r', encoding='iso-8859-2') as file:

    # Soronként beolvassuk a tartalmat a megnyitott .txt fájlból.
    for line in file.readlines():
      # Az adott sort szétvágjuk a határoló csillagok mentén és listává alakítjuk.
      # Példa: ['1', 'K205905V02N49', '25021025B001', 'A2C779610110000224B06001F9', '0', ...]
      row = line.split('*')

      # Az adatsor(row) harmadik eleme a PID, de elé kell írnunk mert a PID szöveget nem tartalmazza.
      key = 'PID' + row[2]

      # Az adott mérési eredmény PID-hez rendelése
      # Ha a pid_listában nincs benne a key, akkor beletesszük és létrehozzuk a
      # hozzá tartozó listát, amibe majd később kerülnek az adatsorok
      if not key in pid_list:
        pid_list.append(key)
        pid_dict[key] = []

      # Bettesszük az adatsort (row) a pic_dict key kulcsú listájába
      pid_dict[key].append(row)

      # A conti_az -hez tartozó eredmények csoportosítása
      # Lekérjük, hogy jelenleg milyen kulcsok vanna a conti_az dictionary-ban.

      # Ha nem szerepel benne a Continental azonosító, ami a lista sor 4. eleme,
      # akkor létrehozzuk az új listát, aminek a kulcs a 4. elem lesz
      conti_keys = list( conti_az.keys() )
      if not row[3] in conti_keys:
        conti_az[row[3]] = []

      # A cont_az, lista 4. elemében található nevű listájába betesszük a key
      # változóban tárolt PID-t.
      conti_az[row[3]].append(key)

pid = 'PID25021025B001'
print(pid_dict[pid])

print( conti_az['A2C779610110000224B270016A'])
 """
################################################################################

# Változók előkészítése
list_file = None
txt_dir = None
txt_file_list = []
pid_dict = {}
pid_list = []
conti_az = {}
root = None
table_data = []
columns = ("Device", "PN", "PID", "ContiAZ", "ErrorCode")
current_csv = ''


# Üres ablak létrehozása
root = tk.Tk()
root.title("Knorr-Bremse Log elemző program")
root.geometry("800x600")

# Label to display the selected file/folder path
label_file_path = tk.Label(root, text="Lista fájl nincs kiválasztva!", font=("Arial", 14))
label_file_path.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

def browse_file():
    global list_file
    # Open a file dialog to select a file
    file_path = filedialog.askopenfilename(title="Select a File")
    if file_path:
        # Megnyitjuk a fájlt a megadott név alapján.
        try:
            list_file = open(file_path, "r", encoding="iso-8859-2")
            label_file_path.config(text="Fájl betöltve: {0}".format(file_path))
            read_list_file()
        except:
            label_file_path.config(text="Fájl betöltve: {0}".format(file_path))
            print('HIBA: nem sikerült megnyitni a fájlt!')

def read_list_file():
    global list_file
    global pid_dict
    global pid_list
    pattern = r"PID\d{8}[A-Z]\d{3}"
    for line in list_file.readlines():
        hasPID = 'PID' in line
        if hasPID:
            pid = re.findall(pattern, line)[0]
            pid_dict[pid] = []

    pid_list = list( pid_dict.keys() )
    list_file.close()
    label_file_path.config(text="PID lista beolvasva! {0}db".format(len(pid_list)))


def read_txt_dir():
    global txt_dir
    global txt_file_list
    global conti_az
    global root
    global table_data
    
    # A táblázatban megjelenő adatok
    data = []
    
    # Adott mappában található .txt fájlok beolvasása.
    txt_dir = filedialog.askdirectory(title="Adja meg a .txt fájlokat tartalmazó mappa nevét")
    try:
        txt_file_list = os.listdir(txt_dir)
        label_file_path.config(text="Mappa megnyitva")
    except:
        label_file_path.config(text="HIBA: nem lehet megnyitni a mappát!")
        return

    # Létrehozunk egy dictionary-t amiben a Continental azonosítók lesznek a kulcsok.
    conti_az = {}

    # Egyesével végigmegyünk a megadott mappában található .txt fájlokon.
    for txt_file_name in txt_file_list:
        # Megynyitjuk a soron következő .txt fájlt.
        with open(txt_dir + '/' + txt_file_name, 'r', encoding='iso-8859-2') as file:

            # Soronként beolvassuk a tartalmat a megnyitott .txt fájlból.
            for line in file.readlines():
                # Az adott sort szétvágjuk a határoló csillagok mentén és listává alakítjuk.
                # Példa: ['1', 'K205905V02N49', '25021025B001', 'A2C779610110000224B06001F9', '0', ...]
                # A sor elején állhat: 0, 1, 103, 104
                row = line.split('*')
                if row[0] not in ['0', '1', '103', '104']:
                    continue 
                  
                data.append(row)               

                # Az adatsor(row) harmadik eleme a PID, de elé kell írnunk mert a PID szöveget nem tartalmazza.
                key = 'PID' + row[2]

                # Az adott mérési eredmény PID-hez rendelése
                # Ha a pid_listában nincs benne a key, akkor beletesszük és létrehozzuk a
                # hozzá tartozó listát, amibe majd később kerülnek az adatsorok
                if not key in pid_list:
                    pid_list.append(key)
                    pid_dict[key] = []

                # Bettesszük az adatsort (row) a pic_dict key kulcsú listájába
                pid_dict[key].append(row)

                # A conti_az -hez tartozó eredmények csoportosítása
                # Lekérjük, hogy jelenleg milyen kulcsok vanna a conti_az dictionary-ban.

                # Ha nem szerepel benne a Continental azonosító, ami a lista sor 4. eleme,
                # akkor létrehozzuk az új listát, aminek a kulcs a 4. elem lesz
                conti_keys = list( conti_az.keys() )
                if not row[3] in conti_keys:
                    conti_az[row[3]] = []

                # A cont_az, lista 4. elemében található nevű listájába betesszük a key
                # változóban tárolt PID-t.
                conti_az[row[3]].append(key)
    
    table_data = data       
    show_table(root, columns, data)
    
def show_table(parent, columns, data, height=20):
    global current_csv
    
    # Létrehozza a táblázatot
    tree = ttk.Treeview(parent, columns=columns, show="headings", height=height)

    # Létrehozza az oszlopokat a táblázatban
    for col in columns:
        tree.heading(col, text=col)  # fejléc neve és szövege
        tree.column(col, anchor="center", width=200)  # oszlop, középre igazított szöveggel és 100 széles

    # Adatok beszúrása a táblázatba
    for row in data:
        tree.insert("", "end", values=row)

    # Add the Treeview widget to the parent
    tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    # CSV generálás
    current_csv = ''
    for row in data:
      current_csv += ';'.join(row) + '\n'

    return tree
        
    
def filter_by_error_code():
    global table_data
    global root
    
    code = error_code_input.get()
    if code == "":
        show_table(root, columns, table_data)
        return
    
    filtered_data = [row for row in table_data if row[4] == code]
    show_table(root, columns, filtered_data)
    

def save_data():
    file_name = filedialog.asksaveasfile(mode='w', defaultextension=".csv")
    file = open(file_name.name, 'w', encoding='utf-8')
    file.write(current_csv)
    file.close()

# A lista fájl kiválasztása
header =  tk.Label(root, text="Adja meg a lista fájl nevét: ", font=("Arial", 20))
btn_browse_file = tk.Button(root, text="Lista Fájl", command=browse_file)
btn_browse_file.grid(row=1, column=0, padx=5)

# A mappa kiválasztása
btn_browse_folder = tk.Button(root, text="Txt Mappa", command=read_txt_dir)
btn_browse_folder.grid(row=1, column=1, padx=5)

# Szűrés hibakódra
error_code_input = tk.Entry(root, width=25, font=("Arial", 20))
error_code_input.grid(row=2, column=0, padx=10, pady=10)
error_code_btn = tk.Button(root, text="Szűrés hibakódra", command=filter_by_error_code)
error_code_btn.grid(row=2, column=1, padx=10, pady=10)

# Táblázatos adatok mentése
btn_save_data = tk.Button(root, text="Mentés CSV fájlba", command=save_data)
btn_save_data.grid(row=4, column=0, padx=10, pady=10)

# Run the tkinter main loop
root.mainloop()
