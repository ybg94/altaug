from datetime import datetime
import time
import re
import dearpygui.dearpygui as dpg
import pyperclip
import Resources.autogui
import Resources.gui_tags as gui_tags
import Resources.read_file
import Resources.time_helpers as rtime

def use_json(max_attempts: int) -> None:
    active_affixes, base_names = Resources.read_file.read_json_data()
    active_base = Resources.autogui.check_active_base(base_names)

    #for affix in active_affixes:
    #    print(affix[0]) 0 will return the affix Name
    #    print(affix[1]) 1 will return Prefix or Suffix

    found_affix = False
    attempts = 0

    while not found_affix and attempts < max_attempts:
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
            #print(f"No affix found (attempt #{attempts}). Using Alteration orb...")
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
                    #print("No suffix found → Using Augmentation orb.")
                    Resources.autogui.use_aug()
                elif not prefix and suffix:
                    #print("No prefix found → Using Augmentation orb.")
                    Resources.autogui.use_aug()
                else:
                    print("Normal item (no affixes).")
            else:
                print("Error: could not read item name after alteration.")

    if not found_affix:
        print(f"⚠️ No matching affix found after {max_attempts} attempts.")
    else:
        print(f"🎯 Success after {attempts} attempts.")

    # found_affix = False
    # while not found_affix:
    #     Resources.autogui.copy_item()
    #     for affix in active_affixes:
    #         check_paste = Resources.autogui.check_clipboard_for(affix[0])
    #         if check_paste:
    #             print(f"Found the modifier '{affix[0]}'")
    #             found_affix = True
    #         else:
    #             found_affix = True

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

@rtime.timeit
def match_item_description(regex: re.Pattern) -> bool:
    Resources.autogui.copy_item()
    item_description: str = pyperclip.paste()

    match = regex.search(item_description)
    if match:
        return True
    
    return False

def use_regex(regex_text: str, max_attempts: int) -> None:
    print(f"Using regex method with pattern: {regex_text}")
    regex = re.compile(regex_text, flags=re.RegexFlag.MULTILINE)

    for attempt in range(max_attempts):
        if match_item_description(regex):
            print(f"Attempt #{attempt}: success")
            break

        Resources.autogui.use_alt()
        if match_item_description(regex):
            print(f"Attempt #{attempt}: success")
            break

        Resources.autogui.use_aug()
        if match_item_description(regex):
            print(f"Attempt #{attempt}: success")
            break

        print(f"Attempt #{attempt}: fail...")

def start_crafting() -> None:
    regex_input: str = dpg.get_value(gui_tags.REGEX_INPUT_TAG)
    max_attempts: int = dpg.get_value(gui_tags.MAX_ATTEMPT_INPUT_TAG)

    #sleep to give user 3 seconds to switch to PoE client
    time.sleep(3)

    start_time: datetime = datetime.now()
    print(f"🔹 Started rolling at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    if (len(regex_input) > 0):
        use_regex(regex_input, max_attempts)
    else:
        use_json(max_attempts)

    # --- End timestamp ---
    end_time = datetime.now()
    elapsed = end_time - start_time
    print(f"🔹 Finished at {end_time.strftime('%Y-%m-%d %H:%M:%S')} (Elapsed: {elapsed})")