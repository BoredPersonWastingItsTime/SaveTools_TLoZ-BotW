# coding=latin
import binfx
import code #.interact()
import math
import os
import pdb #.set_trace()
import pickle
import sys #.stdin.buffer, ~.read() ~.write()
import time #.sleep()
# start of menu
def nav_fmenu(*args):
    global curr_fmenu
    global skp
    while True:
        print('You are in', '> '.join(curr_fmenu.rsplit('_')))
        print('Options:')
        for arg in args:
            print(' [',arg[0],'] ',arg[1],sep='')
        if curr_fmenu=='fmenu': darg=('quit','Close the menu')
        else: darg=('back','Go to previous submenu')
        print(' [',darg[0],'] ',darg[1],sep='')
        inp=insist_input('Choose an option: ').lower()
        for arg in args:
            if arg[0].lower().startswith(inp):
                skp=False
                clearscr()
                curr_fmenu=curr_fmenu+'_'+arg[0]
                eval(curr_fmenu+'()')
                curr_fmenu='_'.join(curr_fmenu.rsplit('_')[:-1])
                if not skp: input('Press enter to return to fmenu.')
                clearscr()
                break
        else:
            if darg[0].lower().startswith(inp):
                skp=True
                return
            else:
                print('Your input was not a valid choice.')
                time.sleep(0.7)
                clearscr()
def fmenu():
    global curr_fmenu
    global skp
    curr_fmenu='fmenu'
    skp=False
    nav_fmenu(
    ('file','Load or save data'),
    ('edit','Modify the loaded data'),
    ('temp','Misc functions')
    )
def fmenu_file():
    nav_fmenu(
    ('ddir','Use the current .py directory'),
    ('cdir','Change the directory where to load file'),
    ('unpi','Load from previous pickle'),
    ('load','Load from .sav file'),
    ('pick','Pickle to file'),
    ('save','Save to .sav file (adds _mod to file name)')
    )
def fmenu_file_ddir():
    global cdir
    cdir=os.path.dirname(os.path.realpath(__file__))+'\\'
    print('Using',cdir,'as cwd.')#print('getcwd:', os.getcwd())
def fmenu_file_cdir():
    global cdir
    cdir=input('Type in the directory to use: ')
    print('Using',cdir,'as cwd.')
def fmenu_file_unpi():
    global savedata
    try: savedata=pickle.load(open(cdir+'game_data.pickle', 'rb'))
    except: print('Unpickling failed.')
    else: print('Successfully unpickled data!')
def fmenu_file_load():
    global savedata
    try: savedata=sav_load(cdir+'game_data.sav')
    except: print("Loading failed.")
    else: print('Successfully loaded .sav file!')
def fmenu_file_pick():
    global savedata
    try: pickle.dump(savedata, open(cdir+'game_data.pickle','wb'))
    except: print('Error while pickling.')
    else: print('Successfully pickled!')
def fmenu_file_save():
    global savedata
    try: sav_dump(cdir+'game_data_mod.sav',savedata)
    except: print('Error while saving.')
    else: print('Successfully saved game_data_mod.sav file! Please check the file size to be sure.')
def fmenu_edit():
    nav_fmenu(
    ('auto','Quick predefined edits'),
    ('sear','Display hashes and modify their data')
    )
def fmenu_edit_auto():
    nav_fmenu(
    ('fillp','Order the porch and fill all slots for MarcRobledo\'s editor'),
    ('sfood','Change the first 12 meals with powerful effects')
    )
def fmenu_edit_auto_fillp(curr_fdb=False):
    """ Using hashes:
    8932285f  PorchItem           (420*64/4B)
    59fc096a  PorchItem_Value1    (420*4B)
    be924882  PorchItem_EquipFlag ¿420*4B? That's a waste of space
    """
    print('ToDo: edit', curr_fmenu)
    print('ToCheck: unequip flags')
    temp_PorchItem=hashgen_PorchItem()
    temp_PorchItem_Value1=hashgen_PorchItem_Value1()
    for i in savedata:
        if '8932285f'==hx(i[0]):
            load_PorchItem=fsplit(i[1],64)
        if '59fc096a'==hx(i[0]):
            load_PorchItem_Value1=fsplit(i[1],4)
    if not load_PorchItem or not load_PorchItem_Value1:
        print('Error while loading')
        return
    pos={'w':0,'b':0,'a':0,'s':0,'c':0,'m':0,'f':0,'o':0}
    max={'w':20,'b':14,'a':6,'s':20,'c':100,'m':160,'f':60,'o':40}
    stt={'w':0,'b':20,'a':34,'s':40,'c':60,'m':160,'f':320,'o':380}
    if curr_fdb:
        for i in enumerate(temp_PorchItem[stt['m']:stt['f']]): print(i[0],i[1].strip(b'\x00'))
        print('Length of temp_PorchItem:',len(temp_PorchItem))
        print('Length of load_PorchItem:',len(load_PorchItem))
        print('Length of temp_PorchItem_Value1:',len(temp_PorchItem_Value1))
        print('Length of load_PorchItem_Value1:',len(load_PorchItem_Value1))
    for i in range(420):
        citem_PorchItem=load_PorchItem[i]
        citem_PorchItem_Value1=load_PorchItem_Value1[i]
        index=hashfx_porchpage(citem_PorchItem)
        if index=='m':
            def is_in(a, l):
                for i in enumerate(l):
                    if a in i[1]:
                        return i[0]
                return -1
            tt=is_in(citem_PorchItem.strip(b'\x00'), temp_PorchItem[stt['m']:stt['f']])
            if tt!=-1:
                if curr_fdb:
                    print(citem_PorchItem.strip(b'\x00'),'\tis in',tt,'of temp',
                    '\twith val', citem_PorchItem_Value1)
                temp_PorchItem_Value1[stt['m']+tt]=citem_PorchItem_Value1
            elif pos[index]<max[index]:
                if curr_fdb: print(citem_PorchItem.strip(b'\x00'),'\t*NOT* in temp')
                ti=stt[index]+max[index]-pos[index]-1
                temp_PorchItem[ti]=citem_PorchItem
                temp_PorchItem_Value1[ti]=citem_PorchItem_Value1
                pos[index]+=1
        elif index!=None:
            if pos[index]<max[index]:
                ti=stt[index]+pos[index]
                temp_PorchItem[ti]=citem_PorchItem
                temp_PorchItem_Value1[ti]=citem_PorchItem_Value1
                pos[index]+=1
    for i in range(len(temp_PorchItem)):
        print(temp_PorchItem[i].strip(b'\x00'),temp_PorchItem_Value1[i])
    input('Break')
    for i in savedata:
        if '8932285f'==hx(i[0]):
            i[1]=b''.join(temp_PorchItem)
        if '59fc096a'==hx(i[0]):
            i[1]=b''.join(temp_PorchItem_Value1)
        if 'be924882'==hx(i[0]):
            i[1]=vfill(b'\x00',sze=len(i[1]))
    if curr_fdb:
        pdb.set_trace()
        for i in savedata:
            if '8932285f'==hx(i[0]):
                print(i[1])
            if '59fc096a'==hx(i[0]):
                print(i[1])
    else: print('Filled Porch!')
def fmenu_edit_auto_sfood():
    """ Using hashes:
    ch[0] 05a995ff  CookEffect0     [look BotW-HashValues.ods]
    ch[1] 93999288  CookEffect1     [unknown,none?(0)]
    ch[2] cdb860da  StaminaRecover  [hearts(30hp=0x78),time(100min=0x1770)]
    """
    # Unlike _fillp, I try to make this _sfood function
    # kinda generic so I can reuse for other purposes
    ch=hashfx_sdpos('05a995ff','93999288','cdb860da')
    mods=[
        hashgen_CookEffect0(),
        hashgen_CookEffect1(),
        hashgen_StaminaRecover()
        ]
    for i in range(len(ch)):
        print('Editing pos',ch[i],'with length',len(savedata[ch[i]][1]))
        savedata[ch[i]][1]=mods[i]+savedata[ch[i]][1][len(mods[i]):]
        print('Edited  pos',ch[i],'with length',len(savedata[ch[i]][1]),'\n')
    print('Done, please check lengths are the same than before edition')
def fmenu_edit_sear():
    nav_fmenu(
    ('hex','Directly search for a hash'),
    ('str','Look for hashes by name')
    )
def fmenu_edit_sear_hex():
    sea=insist_input('Enter hex search query or [q] to quit: ').lower()
    while sea!='q':
        fnd=[]
        clearscr()
        for n in range(1,len(savedata)):
            if sea in hx(savedata[n][0]):
                fnd.append(n)
        if len(fnd)>=1 and len(fnd)<=7:
            for i in fnd:
                print('Found index n =',i,'with hash',savedata[i][0].hex(),'and data',savedata[i][1])
            print('ToDo: edit', curr_fmenu)
            print('If launched with "py -i" you can "^c", edit savedata[n][1] and "fmenu()" to get back\nOtherwise, I can launch the interactive interpreter ("^z" to return to program execution)')
            if 'y'==input('Input "y" if you wish to launch the interpreter '):
                code.interact()
        else:
            print(len(fnd),'results not displayed.')
        sea=insist_input('Enter hex search query or [q] to quit: ').lower()
def fmenu_edit_sear_str():
    try: nameref=tsvload('dump')
    except: return
    while True:
        sea=insist_input('Enter str search query or [q] to quit: ').lower()
        if sea=='q': return
        hashs=[]
        for m in nameref:
            if sea in m[1].lower():
                hashs.append([m[0],m[1]])
        l=len(hashs)
        if l>7:
            print('Too many (',l,') results, try again.')
            continue
        elif l>1:
            print('Results:')
            for i in range(l):
                print(i,':',hashs[i])
            seh=input('Enter index: ')
            try: seh=hashs[int(seh)][0]
            except: continue
        elif l==1:
            print('Found a single result:',hashs[0])
            seh=hashs[0][0]
        else:
            print('No results found.')
            continue
        print('Searching for', seh)
        for n in range(len(savedata)):
            if seh in hx(savedata[n][0]):
                print('Found hash in index n=',n)
        print('ToDo: edit', curr_fmenu)
        print('If launched with "py -i" you can "^c", edit savedata[n][1] and "fmenu()" to get back\nOtherwise, I can launch the interactive interpreter ("^z" to return to program execution)')
        if 'y'==input('Input "y" if you wish to launch the interpreter '):
            code.interact()
def fmenu_temp():
    print('ToDo: write', curr_fmenu)
def fmenu_None():
    print('ToDo: write', curr_fmenu)
# end of menu
def insist_input(msg):
    var=input(msg)
    while not var:
        print('Could not get input, please try again.')
        var=input(msg)
    return var
def clearscr():
    if os.name=='nt': os.system('cls')
    else: os.system('clear')
def sav_load(file):
    file=open(file, 'rb')
    c_data=file.read(4)
    pobj=[[b'', c_data]]
    print('Loading file...')
    c_hash = file.read(4)
    c_data = file.read(4)
    while c_hash:
        if c_hash==pobj[-1][0]: pobj[-1][1] += c_data
        else: pobj.append([c_hash, c_data])
        c_hash = file.read(4)
        c_data = file.read(4)
    print('Hashes Read:', len(pobj))
    file.close()
    return pobj
def sav_dump(file, pobj):
    file=open(file, 'wb')
    for i in pobj:
        for j in fsplit(fjoin(i[1]),4):
            file.write(i[0])
            file.write(j)
    file.close()
def hx(bin):
    #print('Hx:', bin)
    #print(int.from_bytes(bin, 'big'))
    return format(int.from_bytes(bin, 'big'),'08x')
def bn(hex):
    sz=len(hex)>>1
    return int(hex, 16).to_bytes(sz, 'big')
def hashgen_PorchItem():
    obj=[]
    elm=[
        #Weapons
        [vfill(b'Weapon_Sword_001'),10],
        [vfill(b'Weapon_Lsword_001'),5],
        [vfill(b'Weapon_Spear_001'),5],
        #Bows+Arrows
        [vfill(b'Weapon_Bow_001'),14],
        [vfill(b'NormalArrow'),1],
        [vfill(b'FireArrow'),1],
        [vfill(b'IceArrow'),1],
        [vfill(b'ElectricArrow'),1],
        [vfill(b'BombArrow_A'),1],
        [vfill(b'AncientArrow'),1],
        #Shields
        [vfill(b'Weapon_Shield_035'),20],
        #Clothes
        [vfill(b'Armor_043_Upper'),50],
        [vfill(b'Armor_043_Lower'),50],
        #Materials
        [vfill(b'Item_Fruit_A'),1],
        [vfill(b'Item_Fruit_B'),1],
        [vfill(b'Item_Fruit_C'),1],
        [vfill(b'Item_Fruit_D'),1],
        [vfill(b'Item_Fruit_E'),1],
        [vfill(b'Item_Fruit_F'),1],
        [vfill(b'Item_Fruit_G'),1],
        [vfill(b'Item_Fruit_H'),1],
        [vfill(b'Item_Fruit_I'),1],
        [vfill(b'Item_Fruit_J'),1],
        [vfill(b'Item_Fruit_K'),1],
        [vfill(b'Item_Fruit_L'),1],
        [vfill(b'Item_Mushroom_A'),1],
        [vfill(b'Item_Mushroom_B'),1],
        [vfill(b'Item_Mushroom_C'),1],
        [vfill(b'Item_MushroomGet_D'),1],
        [vfill(b'Item_Mushroom_E'),1],
        [vfill(b'Item_Mushroom_F'),1],
        [vfill(b'Item_Mushroom_H'),1],
        [vfill(b'Item_Mushroom_J'),1],
        [vfill(b'Item_Mushroom_L'),1],
        [vfill(b'Item_Mushroom_M'),1],
        [vfill(b'Item_Mushroom_N'),1],
        [vfill(b'Item_Mushroom_O'),1],
#v       [vfill(b'Item_Mushroom_D'),1],
#        [vfill(b'Item_Fruit_E_00'),1],
#        [vfill(b'Item_Mushroom_N_00'),1],
#        [vfill(b'Item_Mushroom_F_00'),1],
#        [vfill(b'Item_MushroomGet_A'),1],
#        [vfill(b'Item_MushroomGet_B'),1],
#        [vfill(b'Item_MushroomGet_C'),1],
#        [vfill(b'Item_MushroomGet_E'),1],
#        [vfill(b'Item_MushroomGet_F'),1],
#        [vfill(b'Item_MushroomGet_H'),1],
#        [vfill(b'Item_MushroomGet_J'),1],
#        [vfill(b'Item_MushroomGet_L'),1],
#        [vfill(b'Item_MushroomGet_M'),1],
#        [vfill(b'Item_MushroomGet_N'),1],
#        [vfill(b'Item_MushroomGet_O'),1],
#v       [vfill(b'Item_Plant_A'),1],
#v       [vfill(b'Item_Plant_B'),1],
#v       [vfill(b'Item_Plant_C'),1],
#v       [vfill(b'Item_Plant_E'),1],
#v       [vfill(b'Item_Plant_F'),1],
#v       [vfill(b'Item_Plant_G'),1],
#v       [vfill(b'Item_Plant_H'),1],
#v       [vfill(b'Item_Plant_I'),1],
#v       [vfill(b'Item_Plant_J'),1],
#v       [vfill(b'Item_Plant_L'),1],
#v       [vfill(b'Item_Plant_M'),1],
#v       [vfill(b'Item_Plant_O'),1],
#v       [vfill(b'Item_Plant_Q'),1],
        [vfill(b'Item_PlantGet_A'),1],
        [vfill(b'Item_PlantGet_B'),1],
        [vfill(b'Item_PlantGet_C'),1],
        [vfill(b'Item_PlantGet_E'),1],
        [vfill(b'Item_PlantGet_F'),1],
        [vfill(b'Item_PlantGet_G'),1],
        [vfill(b'Item_PlantGet_H'),1],
        [vfill(b'Item_PlantGet_I'),1],
        [vfill(b'Item_PlantGet_J'),1],
        [vfill(b'Item_PlantGet_L'),1],
        [vfill(b'Item_PlantGet_M'),1],
        [vfill(b'Item_PlantGet_O'),1],
        [vfill(b'Item_PlantGet_Q'),1],
        [vfill(b'Item_Meat_01'),1],
        [vfill(b'Item_Meat_02'),1],
        [vfill(b'Item_Meat_06'),1],
        [vfill(b'Item_Meat_07'),1],
        [vfill(b'Item_Meat_11'),1],
        [vfill(b'Item_Meat_12'),1],
        [vfill(b'Item_FishGet_A'),1],
        [vfill(b'Item_FishGet_B'),1],
        [vfill(b'Item_FishGet_C'),1],
        [vfill(b'Item_FishGet_D'),1],
        [vfill(b'Item_FishGet_E'),1],
        [vfill(b'Item_FishGet_F'),1],
        [vfill(b'Item_FishGet_G'),1],
        [vfill(b'Item_FishGet_H'),1],
        [vfill(b'Item_FishGet_I'),1],
        [vfill(b'Item_FishGet_J'),1],
        [vfill(b'Item_FishGet_K'),1],
        [vfill(b'Item_FishGet_L'),1],
        [vfill(b'Item_FishGet_M'),1],
        [vfill(b'Item_FishGet_X'),1],
        [vfill(b'Item_FishGet_Z'),1],
        [vfill(b'Animal_Insect_A'),1],
        [vfill(b'Animal_Insect_B'),1],
        [vfill(b'Animal_Insect_C'),1],
        [vfill(b'Animal_Insect_E'),1],
        [vfill(b'Animal_Insect_F'),1],
        [vfill(b'Animal_Insect_G'),1],
        [vfill(b'Animal_Insect_H'),1],
        [vfill(b'Animal_Insect_I'),1],
        [vfill(b'Animal_Insect_M'),1],
        [vfill(b'Animal_Insect_N'),1],
        [vfill(b'Animal_Insect_P'),1],
        [vfill(b'Animal_Insect_Q'),1],
        [vfill(b'Animal_Insect_R'),1],
        [vfill(b'Animal_Insect_S'),1],
        [vfill(b'Animal_Insect_T'),1],
        [vfill(b'Animal_Insect_X'),1],
        [vfill(b'Animal_Insect_AA'),1],
        [vfill(b'Animal_Insect_AB'),1],
        [vfill(b'Item_InsectGet_K'),1],
        [vfill(b'Item_InsectGet_O'),1],
        [vfill(b'Item_InsectGet_Z'),1],
#v       [vfill(b'Animal_Insect_O'),1],
#v       [vfill(b'Animal_Insect_K'),1],
#v       [vfill(b'Animal_Insect_Z'),1],
#        [vfill(b'Item_InsectGet_A'),1],
#        [vfill(b'Item_InsectGet_B'),1],
#        [vfill(b'Item_InsectGet_C'),1],
#        [vfill(b'Item_InsectGet_E'),1],
#        [vfill(b'Item_InsectGet_F'),1],
#        [vfill(b'Item_InsectGet_G'),1],
#        [vfill(b'Item_InsectGet_H'),1],
#        [vfill(b'Item_InsectGet_I'),1],
#        [vfill(b'Item_InsectGet_M'),1],
#        [vfill(b'Item_InsectGet_N'),1],
#        [vfill(b'Item_InsectGet_P'),1],
#        [vfill(b'Item_InsectGet_Q'),1],
#        [vfill(b'Item_InsectGet_R'),1],
#        [vfill(b'Item_InsectGet_S'),1],
#        [vfill(b'Item_InsectGet_T'),1],
#        [vfill(b'Item_InsectGet_X'),1],
#        [vfill(b'Item_InsectGet_AA'),1],
#        [vfill(b'Item_InsectGet_AB'),1],
#        [vfill(b'Item_Ore_A_00'),1],
        [vfill(b'BeeHome'),1],
        [vfill(b'Obj_FireWoodBundle'),1],
        [vfill(b'Item_Enemy_00'),1],
        [vfill(b'Item_Enemy_01'),1],
        [vfill(b'Item_Enemy_02'),1],
        [vfill(b'Item_Enemy_03'),1],
        [vfill(b'Item_Enemy_04'),1],
        [vfill(b'Item_Enemy_05'),1],
        [vfill(b'Item_Enemy_06'),1],
        [vfill(b'Item_Enemy_07'),1],
        [vfill(b'Item_Enemy_08'),1],
        [vfill(b'Item_Enemy_12'),1],
        [vfill(b'Item_Enemy_13'),1],
        [vfill(b'Item_Enemy_14'),1],
        [vfill(b'Item_Enemy_15'),1],
        [vfill(b'Item_Enemy_16'),1],
        [vfill(b'Item_Enemy_17'),1],
        [vfill(b'Item_Enemy_18'),1],
        [vfill(b'Item_Enemy_19'),1],
        [vfill(b'Item_Enemy_20'),1],
        [vfill(b'Item_Enemy_21'),1],
        [vfill(b'Item_Enemy_24'),1],
        [vfill(b'Item_Enemy_25'),1],
        [vfill(b'Item_Enemy_26'),1],
        [vfill(b'Item_Enemy_27'),1],
        [vfill(b'Item_Enemy_28'),1],
        [vfill(b'Item_Enemy_29'),1],
        [vfill(b'Item_Enemy_30'),1],
        [vfill(b'Item_Enemy_31'),1],
        [vfill(b'Item_Enemy_32'),1],
        [vfill(b'Item_Enemy_33'),1],
        [vfill(b'Item_Enemy_34'),1],
        [vfill(b'Item_Enemy_38'),1],
        [vfill(b'Item_Enemy_39'),1],
        [vfill(b'Item_Enemy_40'),1],
        [vfill(b'Item_Enemy_41'),1],
        [vfill(b'Item_Enemy_42'),1],
        [vfill(b'Item_Enemy_43'),1],
        [vfill(b'Item_Enemy_44'),1],
        [vfill(b'Item_Enemy_45'),1],
        [vfill(b'Item_Enemy_46'),1],
        [vfill(b'Item_Enemy_47'),1],
        [vfill(b'Item_Enemy_48'),1],
        [vfill(b'Item_Enemy_49'),1],
        [vfill(b'Item_Enemy_50'),1],
        [vfill(b'Item_Enemy_51'),1],
        [vfill(b'Item_Enemy_52'),1],
        [vfill(b'Item_Enemy_53'),1],
        [vfill(b'Item_Enemy_54'),1],
        [vfill(b'Item_Enemy_55'),1],
        [vfill(b'Item_Enemy_56'),1],
        [vfill(b'Item_Enemy_57'),1],
        [vfill(b'Item_Enemy_Put_57'),1],
        [vfill(b'Item_Material_01'),1],
        [vfill(b'Item_Material_02'),1],
        [vfill(b'Item_Material_03'),1],
        [vfill(b'Item_Material_04'),1],
        [vfill(b'Item_Material_05'),1],
        [vfill(b'Item_Material_06'),1],
        [vfill(b'Item_Material_07'),1],
        [vfill(b'Item_Material_08'),1],
        [vfill(b'Item_Ore_A'),1],
        [vfill(b'Item_Ore_B'),1],
        [vfill(b'Item_Ore_C'),1],
        [vfill(b'Item_Ore_D'),1],
        [vfill(b'Item_Ore_E'),1],
        [vfill(b'Item_Ore_F'),1],
        [vfill(b'Item_Ore_G'),1],
        [vfill(b'Item_Ore_H'),1],
        [vfill(b'Item_Ore_I'),1],
        [vfill(b'Item_Ore_J'),1],
        [vfill(b'Obj_FireWoodBundle'),10],
        #Food
        [vfill(b'Item_Cook_C_17'),40],
        [vfill(b'Item_Cook_C_16'),15],
        [vfill(b'Item_Boiled_01'),5],
        #Misc
        [vfill(b'KeySmall'),40]
    ]
    for i in elm:
        add=[i[0]]
        add*=i[1]
        obj+=add
    return obj
def hashgen_PorchItem_Value1():
    obj=[]
    elm=[
        #W+BA+S
        [b'\x28\x23\x00\x00',60],
        #Clothes
        [b'\x00\x00\x00\x00',100],
        #Materials
        [b'\x30\x00\x00\x00',160],
        #Food
        [b'\x03\x00\x00\x00',60],
        #Misc
        [b'\x01\x00\x00\x00',40]
    ]
    for i in elm:
        add=[i[0]]
        add*=i[1]
        obj+=add
    return obj
def hashgen_CookEffect0():
    obj=[]
    elm=[
        [b'\x02\x00\x00\x00\x78\x00\x00\x00',1],
        [b'\x04\x00\x00\x00\x03\x00\x00\x00',1],
        [b'\x05\x00\x00\x00\x03\x00\x00\x00',1],
        [b'\x06\x00\x00\x00\x03\x00\x00\x00',1],
        [b'\x0A\x00\x00\x00\x03\x00\x00\x00',1],
        [b'\x0B\x00\x00\x00\x03\x00\x00\x00',1],
        [b'\x0C\x00\x00\x00\x03\x00\x00\x00',1],
        [b'\x0D\x00\x00\x00\x03\x00\x00\x00',1],
        [b'\x0E\x00\x00\x00\xFF\x0F\x00\x00',1],
        [b'\x0F\x00\x00\x00\x0F\x00\x00\x00',1],
        [b'\x10\x00\x00\x00\x03\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x03\x00\x00\x00',1]
    ]
    for i in elm:
        add=[i[0]]
        add*=i[1]
        obj+=add
    return fjoin(obj)
def hashgen_CookEffect1():
    obj=[]
    elm=[
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1],
        [b'\x00\x00\x00\x00\x00\x00\x00\x00',1]
    ]
    for i in elm:
        add=[i[0]]
        add*=i[1]
        obj+=add
    return fjoin(obj)
def hashgen_StaminaRecover():
    obj=[]
    elm=[
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1],
        [b'\x78\x00\x00\x00\x77\x17\x00\x00',1]
    ]
    for i in elm:
        add=[i[0]]
        add*=i[1]
        obj+=add
    return fjoin(obj)
def hashfx_porchpage(obj, rid=1):
    if obj.startswith(b'Weapon_Sword'): return (0,'w')[rid]
    if obj.startswith(b'Weapon_Lsword'): return (0,'w')[rid]
    if obj.startswith(b'Weapon_Spear'): return (0,'w')[rid]
    if obj.startswith(b'Weapon_Bow'): return (1,'b')[rid]
    if b'Arrow' in obj: return (2,'a')[rid]
    if obj.startswith(b'Weapon_Shield'): return (3,'s')[rid]
    if obj.startswith(b'Armor'): return (4,'c')[rid]
    if obj.startswith(b'Item_Fruit'): return (5,'m')[rid]
    if obj.startswith(b'Item_Mushroom'): return (5,'m')[rid]
    if obj.startswith(b'Item_Plant'): return (5,'m')[rid]
    if obj.startswith(b'Item_Meat'): return (5,'m')[rid]
    if obj.startswith(b'Item_Fish'): return (5,'m')[rid]
    if obj.startswith(b'Animal_Insect'): return (5,'m')[rid]
    if obj.startswith(b'Item_Insect'): return (5,'m')[rid]
    if obj.startswith(b'Bee'): return (5,'m')[rid]
    if b'FireWoodBundle' in obj: return (5,'m')[rid]
    if obj.startswith(b'Item_Enemy'): return (5,'m')[rid]
    if b'Item_Material_05_00' in obj: return (6,'f')[rid]
    if obj.startswith(b'Item_Material'): return (5,'m')[rid]
    if obj.startswith(b'Item_Ore'): return (5,'m')[rid]
    if obj.startswith(b'Item_Boiled'): return (6,'f')[rid]
    if obj.startswith(b'Item_Chilled'): return (6,'f')[rid]
    if obj.startswith(b'Item_Roast'): return (6,'f')[rid]
    if obj.startswith(b'Item_Cook'): return (6,'f')[rid]
    if obj.startswith(b'Obj'): return (7,'o')[rid]
    if b'Player' in obj: return (7,'o')[rid]
    if obj.startswith(b'Key'): return (7,'o')[rid]
    if obj.startswith(b'Game'): return (7,'o')[rid]
    if obj.startswith(b'Get_TwnObj_DLC'): return (7,'o')[rid]
    return None#(-1,'x')[rid]
def hashfx_sdpos(*lh):
    ch=[None]*len(lh)
    for i in range(len(savedata)):
        for j in enumerate(lh):
            if j[1]==hx(savedata[i][0]): ch[j[0]]=i
    return ch
def vfill(var, fll=b'\x00', sze=64):
    while len(var)<sze: var+=fll
    return var
def chunks(lst, n=4):
    for i in range(0,len(lst),n): yield lst[i:i+n]
def fsplit(lst, n=4):
    ret=[]
    for i in chunks(lst,n): ret+=[i]
    return ret
def getsl(obj, typ=(list, tuple)):
    # I almost wrote the same as https://gist.github.com/aljiwala/c77a01f382f5bbc10d2d2b97a7ed0f0a but didn't wotk what I wrote
    if isinstance(obj, typ):
        for sub in obj:
            for itm in getsl(sub, typ):
                yield itm
    else: yield obj
def fjoin(obj, typ=(list, tuple)):
    ret=b''
    for i in getsl(obj, typ): ret+=i
    return ret
def tsvload(name):
    global cdir
    try:
        x=open(cdir+name+'.tsv')
        l=[]
        for line in x:
            l.append(line.strip('\n').split('\t'))
        x.close()
    except:
        return None
    else:
        return l
# unused?
def hash_dtype(t):
    if t<7: return [4,1]
    elif t<9: return [4,2]
    elif t<11: return [4,3]
    elif t<13: return [4,4]
    elif t<15: return [32,1]
    elif t<17: return [64,1]
    else: return [256,1]
def hash_defdat(t):
    if t==1:
        rt=[]
        ra=''
        for i in range(20):
            rt.append(ra)
        ra=''
        for i in range(20):
            rt.append(ra)
        return rt
    return None
def hashfx_porchpage_test():
    for i in list(dict_PorchItemList):
        for j in list(dict_PorchItemList[i]):
            print(hshfx_porchpage(j.encode('latin')),j)
# program start
fmenu_file_ddir()
time.sleep(0.7)
try: fmenu_file_load()
except:
    print('File not loaded, load it manually please.')
    input('Press enter to porceed... ')
else:
    print('File in cwd loaded!')
    time.sleep(1.2)
clearscr()
fmenu()
#end