import os
import pandas as pd

X_train = pd.read_csv("table_for_train.csv")
lili = sorted(list(X_train.loc[X_train.directory_size > 150].car_model.unique()))

path_0="../data_" # path to the dataset

#this folders have issues with not unidecoded names 
raras = ['bmw_m1', 'citroen_c-elysÃ©e', 'lamborghini_huracan',
         'skoda_rapid_spaceback', 'smart_city-coupe-cabrio']

raras_in_lili = ["bmw_1er-m-coupé", "citroen_c-elysée", "lamborghini_huracán", 
                 "skoda_rapid%2fspaceback", "smart_city-coupé%2fcity-cabrio"]


merger_dict = dict()

# Abarth_5 ===> Todos juntos
# Abarth_124_spider junto con Fiat_124_spider
merger_dict['abarth_500']= [x for x in lili if x.startswith('abarth_5')]
merger_dict['abarth_124'] = [x for x in lili if x.endswith('124-spider')]

# BMW
# Juntar por  bmw_1,2,etc_ revisar si son sedan o cortitos
for x in lili:
    prefix = "bmw_"    
    if x.startswith(prefix) and len(x)==len(prefix)+3:
        new_name = x[:4]+"serie_"+x[4]
        if new_name not in merger_dict.keys():
            merger_dict[new_name] = []
        merger_dict[new_name].append(x)
        
# # Juntar bmw_x con bmw_xm
for x in lili:
    prefix = "bmw_x"
    if x.startswith(prefix):
        if x[:-2] not in merger_dict.keys():
            merger_dict[x[:6]] = []
        merger_dict[x[:6]].append(x)
                
# Audi
# Juntar audi_a con s
for i in range(1,9):
    if i!=2:
        x = f"audi_a{i}"
        merger_dict[x] = [x]
        merger_dict[x].append(f"audi_s{i}")
        
# Juntar todos los audi_rs
prefix = "audi_rs"
merger_dict[prefix] = []
for x in lili:
    if x.startswith(prefix):
        merger_dict[prefix].append(x)

# Juntar audi_sq con audi_q
merger_dict["audi_q5"] = ["audi_q5","audi_sq5"]
merger_dict["audi_q7"] = ["audi_q7","audi_sq7"]

merger_dict["audi_tt"] = ["audi_tt-rs", "audi_tts"] 

# juntar Fiat500 con Fiat500c
# juntar fiat_punto con fiat_punto-evo.
merger_dict["fiat_500"] = ["fiat_500", "fiat_500c"] 
# juntar Abart_grande-punto con, abarth_punto-evo , Fiat_punto y Fiat_grande-punto
merger_dict["fiat_punto"] = [x for x in lili if "punto" in x]

# FORD
# juntar todas las Turneos 
# juntar todas las Transit
for prefix in ["ford_tourneo", "ford_transit"]:
    merger_dict[prefix]= [x for x in lili if x.startswith(prefix)]

# CHRYSLER
merger_dict["chrysler_voyager"] = ["chrysler_voyager", "chrysler_grand-voyager"] 
  
#Renault:
#Juntar espace con grand espace
merger_dict["renault_espace"] = ["renault_espace", "renault_grand-espace"] 
#scenic con scenic erase
merger_dict["renault_scenic"] = ["renault_scenic", "renault_grand-scenic"] 

#Smart
#Juntar Fortwo con Brabus
merger_dict["smart_fortwo"] = ["smart_fortwo", "smart_brabus"]
    
# CITROEN & DS
for i in [3,4,5]:
    merger_dict[f"citroen_ds{i}"] = [f"citroen_ds{i}",
                                     f"ds-automobiles_ds-{i}"]
        
#Volkswagen
#juntar golf y golf gti
merger_dict["volkswagen_golf"]=["volkswagen_golf","volkswagen_golf-gti"]

#Juntar T4 con T4,
# T5 con T5
#, T6 con T6, y asi.
for i in [4,5,6]:
    prefix =  f"volkswagen_t{i}"
    merger_dict[prefix]=[]
    for x in lili:
        if x.startswith(prefix):
            merger_dict[prefix].append(x)
            
#Juntar beetle, new beetle, Maggiolino con Coccinelle 
prefix = "volkswagen_"
merger_dict["volkswagen_beetle"]= [prefix+j for j in 
                                   ["beetle","maggiolino",
                                    "new-beetle","coccinelle" ]]

#Juntar Passat con Passat variant y alltrack
#(la carpeta original del Dataset venia fotos MEZCLADAS 
#entre estos tres modelos)
prefix = "volkswagen_passat"
merger_dict[prefix]= [prefix+j for j in ["", "-alltrack", "-variant"]]   
        
merger_dict["volkswagen_passat-cc"]= ["volkswagen_passat-cc", "volkswagen_cc"]
    
        
# MERCEDES
lista_mbz = []
prefix = "mercedes-benz_"
for x in lili:
    if prefix in x:
        lista_mbz.append(x[len(prefix):])

remaining_mbz = []
three_characters_mbz = ["cla","clk","cls","gla","glc","gle","glk","slc","slk"]

for x in lista_mbz:
    if len(x)==5 and x[-3:].isnumeric() and x[1]=="-":
        if prefix+"class_"+x[0] not in merger_dict.keys():
            #print(f"se creó la carpeta clase {x}")
            merger_dict[prefix+"class_"+x[0]] = []
        merger_dict[prefix+"class_"+x[0]].append(prefix+x)
        #print(x)
    elif len(x)==7 and x[-3:].isnumeric() and x[3]=="-" and x[:3] in three_characters_mbz:
        if prefix+x[:3] not in merger_dict.keys():
            merger_dict[prefix+x[:3]] = []
        merger_dict[prefix+x[:3]].append(prefix+x)
    else:
        remaining_mbz.append(x)

merger_dict[prefix+"ml"]=[prefix+g for g in['ml-250','ml-270','ml-280',
                   'ml-300','ml-320','ml-350', "ml-63-amg"]]
merger_dict[prefix+"sl"]= [prefix+'sl-350', prefix+'sl-500', prefix+'sl-55-amg']

merger_dict["mercedes-benz_class_a"].extend(["mercedes-benz_a-45-amg"])
merger_dict["mercedes-benz_class_c"].extend(["mercedes-benz_c-43-amg", 
                                        "mercedes-benz_c-63-amg"])
merger_dict["mercedes-benz_class_e"].extend(["mercedes-benz_e-43-amg", 
                                        "mercedes-benz_e-63-amg"])
merger_dict["mercedes-benz_class_g"].extend(["mercedes-benz_g-63-amg"])
merger_dict["mercedes-benz_class_s"].extend(["mercedes-benz_s-63-amg"])

merger_dict["mercedes-benz_class_v"].append("mercedes-benz_marco-polo")

#----------------------------------------------------
merger_dict["mercedes-benz_gle"].extend(["mercedes-benz_gle-43-amg", 
                                        "mercedes-benz_gle-63-amg"])

merger_dict["mercedes-benz_cla"].extend(["mercedes-benz_cla-45-amg"]) 
merger_dict["mercedes-benz_cls"].extend(["mercedes-benz_cls-63-amg"]) 
merger_dict["mercedes-benz_gla"].extend(["mercedes-benz_gla-45-amg"]) 
merger_dict["mercedes-benz_glc"].extend(["mercedes-benz_glc-43-amg"]) 
merger_dict["mercedes-benz_slc"].extend(["mercedes-benz_slc-43-amg"]) 
    
# MINI-COOPER
merger_dict["mini_cooper-cabrio"]=["mini_cooper-cabrio", "mini_cooper-d-cabrio", 
                                   "mini_cooper-s-cabrio", "mini_one-cabrio"]

merger_dict["mini_cooper-clubman"]=["mini_cooper-clubman", "mini_cooper-s-clubman", 
                                    "mini_cooper-d-clubman", "mini_cooper-sd-clubman", 
                                    "mini_one-d-clubman"]

merger_dict["mini_cooper-paceman"]=["mini_cooper-paceman", 
                                      "mini_cooper-s-paceman", "mini_cooper-d-paceman"]

merger_dict["mini_cooper-countryman"]=["mini_cooper-countryman", "mini_cooper-d-countryman",
                                       "mini_cooper-s-countryman", "mini_cooper-sd-countryman",
                                      "mini_john-cooper-works-countryman"]

merger_dict["ford_c-max"]=['ford_grand-c-max']
merger_dict["fiat_panda"] = [x for x in lili if "panda" in x]
merger_dict["ford_focus"] = [x for x in lili if "focus" in x]
merger_dict["lexus_is-220d"] = [x for x in lili if "lexus_is-2" in x]
merger_dict["opel_zafira"] = [x for x in lili if "zafira" in x]
merger_dict["fiat_600"] = ["fiat_600", "fiat_seicento"]

# porsches_9
merger_dict["porsche_911"] = [x for x in lili if "porsche_9" in x]


for x in lili:
    if "daewoo" in x:
        merger_dict[x.replace("daewoo", "chevrolet")] = [x]

merger_dict["nissan_qashqai"] = ["nissan_qashqai+2"]            
merger_dict["suzuki_ignis"]=["daihatsu_sirion", "subaru_justy"]

merger_dict["seat_altea"]= ["seat_altea-xl"]
merger_dict["renault_modus"]= ["renault_grand-modus"]

for key, values in merger_dict.items():
    merger_dict[key] = [x for x in values if x!=key]

l1=[]
for key, values in merger_dict.items():
    if len(merger_dict[key]) == 0:
        l1.append(key)
for key in l1:
    merger_dict.pop(key)

new_dirs = []
for key, values in merger_dict.items():
    if key not in lili:
        new_dirs.append(key)

merged_folders = []
merged_values = []
for key, listi in merger_dict.items():
    merged_folders.extend(listi)
    merged_values.extend(listi)
    if key not in new_dirs:
        merged_folders.append(key)


to_erase = ['caravans-wohnm_others', 'mercedes-benz_180', 'mercedes-benz_200',
            'mercedes-benz_220', 'mercedes-benz_250', 'mercedes-benz_350', 
            'mercedes-benz_clc', 'mercedes-benz_v', 'mini_cooper', 'mini_cooper-d',
            'mini_cooper-s', 'mini_cooper-sd','mini_one', 'mini_one-countryman', 
            'mini_one-d', 'mini_one-d-countryman','volkswagen_others',
             'volkswagen_transporter'
             ]


path_1 = path_0+"_"
os.rename(path_0, path_1)
os.makedirs(path_0)

for sub in ["test", "train", "val"]:
    deeper_path = os.path.join(path_1, sub)
    for sa in os.listdir(os.path.join(path_1, sub)):
        if sa not in to_erase and sa not in merged_values:
            if os.path.isdir(os.path.join(path_1, sub, sa)):
                os.makedirs(os.path.join(path_0, sub, sa), exist_ok=True)
                for single_car in os.listdir(os.path.join(path_1, sub, sa)):
                    if single_car.endswith(".jpg"):
                        input_route = os.path.join(path_1, sub, sa, single_car)
                        output_route = os.path.join(path_0, sub, sa, single_car)
                        os.rename(input_route, output_route)
                        
    for key, values in merger_dict.items():
        if key in new_dirs:
            os.makedirs(os.path.join(path_0, sub, key), exist_ok=True)
        for car_model in values:
            another_path = os.path.join(deeper_path, car_model)
            if os.path.isdir(another_path):
                for single_car in os.listdir(another_path):
                    if single_car.endswith(".jpg"):
                        input_route = os.path.join(another_path, single_car)
                        output_route = os.path.join(path_0, sub, key, single_car)
                        os.rename(input_route, output_route)