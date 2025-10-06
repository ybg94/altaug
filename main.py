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

Resources.autogui.copy_item()
for affix in active_affixes:
    check_paste = Resources.autogui.check_clipboard_for(affix[0])
    if check_paste:
        print(f"Found the modifier '{affix[0]}'")
        found_affix = True
        break
if not found_affix:
    print("No matching affix found after checking all active affixes")

#item_name = Resources.autogui.get_item_name()
#before, _, after = item_name.partition(active_base)
#prefix = before.strip()
#suffix = after.strip()
#if prefix and suffix:
#    print(f"Prefix is {prefix} and suffix is {suffix}")
#elif prefix and not suffix:
#    print(f"Prefix is {prefix}")
#elif not prefix and suffix:
#    print(f"suffix is {suffix}")
#else:
#    print("This is a normal item")




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

