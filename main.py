#Authors billy_smalls and kipper86

import Resources.read_config
import Resources.read_file
import Resources.autogui
import pyautogui
import time
from datetime import datetime

CONFIG_DATA = Resources.read_config.read_config()
active_affixes, base_names = Resources.read_file.read_json_data()
start_time = datetime.now()
print(f"🔹 Started rolling at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
#sleep to give user 3 seconds to switch to PoE client
time.sleep(3)
active_base = Resources.autogui.check_active_base(base_names)


#for affix in active_affixes:
#    print(affix[0]) 0 will return the affix Name
#    print(affix[1]) 1 will return Prefix or Suffix

MAX_ATTEMPTS = 10  # safety cap so it doesn't loop forever
found_affix = False
attempts = 0

while not found_affix and attempts < MAX_ATTEMPTS:
    attempts += 1

    # Copy item text
    Resources.autogui.copy_item()

    # Check clipboard against all known affixes
    for affix in active_affixes:
        if Resources.autogui.check_clipboard_for(affix[0]):
            print(f"✅ Found the modifier '{affix[0]}' on attempt #{attempts}")
            found_affix = True
            break

    # If still not found, use Alteration and reroll
    if not found_affix:
        print(f"No affix found (attempt #{attempts}). Using Alteration orb...")
        Resources.autogui.use_alt()

        # Copy the new item and analyze prefixes/suffixes
        Resources.autogui.copy_item()
        item_name = Resources.autogui.get_item_name()

        if item_name:
            before, _, after = item_name.partition(active_base)
            prefix = before.strip()
            suffix = after.strip()

            if prefix and suffix:
                print(f"Prefix: {prefix} | Suffix: {suffix}")
            elif prefix and not suffix:
                print("No suffix found → Using Augmentation orb.")
                Resources.autogui.use_aug()
            elif not prefix and suffix:
                print("No prefix found → Using Augmentation orb.")
                Resources.autogui.use_aug()
            else:
                print("Normal item (no affixes).")
        else:
            print("Error: could not read item name after alteration.")

# --- End timestamp ---
end_time = datetime.now()
elapsed = end_time - start_time

if not found_affix:
    print(f"⚠️ No matching affix found after {MAX_ATTEMPTS} attempts.")
else:
    print(f"🎯 Success after {attempts} attempts.")

print(f"🔹 Finished at {end_time.strftime('%Y-%m-%d %H:%M:%S')} (Elapsed: {elapsed})")


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

