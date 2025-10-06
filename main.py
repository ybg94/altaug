#Authors billy_smalls and kipper86

import Resources.read_config
import Resources.read_file
import Resources.autogui
import pyautogui
import time

CONFIG_DATA = Resources.read_config.read_config()
active_affixes, base_names = Resources.read_file.read_json_data()
#sleep to give user 3 seconds to switch to PoE client
time.sleep(3)
active_base = Resources.autogui.check_active_base(base_names)


#for affix in active_affixes:
#    print(affix[0]) 0 will return the affix Name
#    print(affix[1]) 1 will return Prefix or Suffix

found_affix = False
while not found_affix:
    Resources.autogui.copy_item()
    for affix in active_affixes:
        check_paste = Resources.autogui.check_clipboard_for(affix[0])
        if check_paste:
            print(f"Found the modifier '{affix[0]}'")
            found_affix = True
        else:
            found_affix = True




        #else if affix['affix] == Pre
            #if item has open pre
                #aug
                #check paste
        #else if affix['affix'] == Suff
            #if item has open suff
                #aug
                #check paste
        #else
            #alt 
            #loop and it will check affixes at start of loop again

