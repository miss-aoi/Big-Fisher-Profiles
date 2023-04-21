"""
I got tired of manually updating everything.
Let's see if this other idea works out better...
"""
import requests, json, time, random
import xml.etree.ElementTree as ET
from pathlib import Path

sit_percent = 0.70
gt_url = 'https://garlandtools.org/'
with open("gt_zone_mapping.json", "r") as file:
    gt_zone_mapping = json.load(file)
with open("big_fish_ids.json", "r") as file:
    big_fish_ids = json.load(file)
with open("baits.json", "r") as file:
    baits = json.load(file)
with open("endwalker_folklore_fish.json", "r") as file:
    endwalker_folklore_fish = json.load(file)


def process_bait_details(fish_spot):
    """
    Process fish spot details and return what's needed
    """
    mooch_fish = []
    patience_tugs = []

    # Bait Details
    bait_lst = fish_spot.get('baits')[0]
    for bait_id in bait_lst:
        resp = requests.get(f'{gt_url}/db/doc/item/en/3/{bait_id}.json')
        bait_data = json.loads(resp.text).get('item')
        if 'fish' in bait_data:
            mooch_fish.append(bait_data.get('id'))
        else:
            bait_id_keep = str(bait_id)
            bait_name = bait_data.get('name')
            bait_amount = baits.get(str(bait_id)).get('Amount')
            bait_type = baits.get(str(bait_id)).get('Type')

    # Mooch Details
    if mooch_fish:
        for mooch_fish_id in mooch_fish:
            resp = requests.get(f'{gt_url}/db/doc/item/en/3/{mooch_fish_id}.json')
            mooch_fish_spots = json.loads(resp.text).get('item').get('fish').get('spots')
            mooch_fish_spot = [a for a in mooch_fish_spots if a.get('spot') == fish_spot.get('spot')]
            patience_tugs.append({"level": str(len(patience_tugs)), "tug": mooch_fish_spot[0].get('tug')})
        patience_tugs.append({"level": str(len(patience_tugs)), "tug": fish_spot.get('tug')})

    return {'bait_id': bait_id_keep, 'bait_name': bait_name, 'bait_amount': bait_amount, 'bait_type': bait_type, 'patience_tugs': patience_tugs}


def process_predator(fish_spot):
    """
    Process Predator data and return what's needed
    """
    if 'predator' in fish_spot:
        pred_fish_id = fish_spot.get('predator')[0].get('id')
        resp = requests.get(f'{gt_url}/db/doc/item/en/3/{pred_fish_id}.json')
        pred_fish_name = json.loads(resp.text).get('item').get('name')
        pred_baits = json.loads(resp.text).get('item').get('fish').get('spots')[0].get('baits')
        pred_fish_spot = {'spot': fish_spot.get('spot'), 'baits': pred_baits, 'tug': fish_spot.get('tug')}
        pred_fish_details = process_bait_details(pred_fish_spot)
        predator_data = {
            'bait_id': pred_fish_details.get('bait_id'),
            'bait_name': pred_fish_details.get('bait_name'),
            'fish_id': pred_fish_id,
            'fish_name': pred_fish_name,
            'patience_tugs': pred_fish_details.get('patience_tugs')
            }
        return predator_data
    return {}


def build_xml_profile(fish_profile_data):
    """
    Build the xml profile and return XML tree
    """
    # Add base structure of tree
    root_string = add_starting_xml()

    # Add Basic Fish Checks
    root_string = add_fish_checks(root_string, fish_profile_data)

    # Add ExFish Check and Finish
    root_string = add_exfish(root_string, fish_profile_data)

    return root_string


def add_starting_xml():
    """
    Return a new XML tree from template
    """
    base_xml_tree = '<Profile></Profile>'
    root = ET.fromstring(base_xml_tree)
    
    # Add starting stuff
    ET.SubElement(root, 'Name')
    ET.SubElement(root, 'BehaviorDirectory')
    ET.SubElement(root, 'Order')
    ET.SubElement(root, 'GrindAreas')
    ET.SubElement(root, 'CodeChunks')
    
    return ET.tostring(root)


def add_fish_checks(root_string, fish_profile_data):
    """
    Add initial checks to string and return
    """
    root = ET.fromstring(root_string)
    root.find("Name").text = f"{fish_profile_data.get('fish_name')}"

    # Check if don't have at least 1 fish
    order_elem = root.find("Order")
    ET.SubElement(order_elem, "Log", Message=f"Starting Fishing: {fish_profile_data.get('fish_name','ERROR')}...")

    # Check if have the required bait
    if_not_has_bait_elem = ET.SubElement(order_elem, "If", condition=f"not HasAtLeast({fish_profile_data.get('bait_id','ERROR')},50)")
    lisbeth_order = "[{'Group':1,'Item':TEMP,'Amount':50,'Enabled':true,'Type':'Purchase'}]"
    lisbeth_order = lisbeth_order.replace('TEMP',str(fish_profile_data.get('bait_id','ERROR')))
    lisbeth_order = lisbeth_order.replace('50',str(fish_profile_data.get('bait_amount')))
    lisbeth_order = lisbeth_order.replace('Purchase',fish_profile_data.get('bait_type'))
    ET.SubElement(if_not_has_bait_elem, "Lisbeth", IgnoreHome="True", Json=lisbeth_order)
    if fish_profile_data.get('predator') and fish_profile_data.get('predator').get('bait_id') != fish_profile_data.get('bait_id'):
        if_not_has_pred_bait_elem = ET.SubElement(order_elem, "If", condition=f"not HasAtLeast({fish_profile_data.get('predator').get('bait_id')},50)")
        lisbeth_order = "[{'Group':1,'Item':TEMP,'Amount':50,'Enabled':true,'Type':'Purchase'}]".replace('TEMP',fish_profile_data.get('predator').get('bait_id'))
        ET.SubElement(if_not_has_pred_bait_elem, "Lisbeth", IgnoreHome="True", Json=lisbeth_order)

    # Check if on right SubMap
    submap_check_elem = ET.SubElement(order_elem, "If", condition=f"not IsOnSubMap({fish_profile_data.get('submap_id')})")
    ET.SubElement(submap_check_elem, "LisbethTravel", Area=f"{fish_profile_data.get('lisbeth_cords').get('Area')}", XYZ=f"{fish_profile_data.get('lisbeth_cords').get('XYZ')}")
    
    # Change to fisher
    if_not_fisher = ET.SubElement(order_elem, "If", condition="not ClassName == ClassJobType.Fisher")
    ET.SubElement(if_not_fisher, "ChangeClass", Job="Fisher")

    # Add wait time if getting there early
    if fish_profile_data.get('time_window'):
        start = fish_profile_data.get('time_window').get('start') - 1
        end = fish_profile_data.get('time_window').get('start')
        wait_time = ET.SubElement(order_elem, "While", condition=f"IsTimeBetween({start},{end})")
        ET.SubElement(wait_time, "WaitTimer", WaitTime="30")
    
    return ET.tostring(root)


def add_exfish(root_string, fish_profile_data):
    """
    Add ExFish and Finishing entries
    """
    # Build Conditions Block
    condition_block = build_conditions(fish_profile_data)
    # Add Elements
    root = ET.fromstring(root_string)
    order_elem = root.find("Order")
    while_check_elem = ET.SubElement(order_elem, "While", condition=condition_block)
    
    # Add predator entry for cases where Fisher's Intuition is needed
    if fish_profile_data.get('predator'):
        pred_exfish_elem = ET.SubElement(while_check_elem, "ExFish", Bait=f"{fish_profile_data.get('predator').get('bait_name')}")
        pred_exfish_elem.set('Condition', "not Core.Player.HasAura(568)")
        pred_exfish_elem.set('MinFish', '15')
        pred_exfish_elem.set('MaxFish', '25')
        pred_exfish_elem.set('ShuffleFishSpots', 'True')
        pred_exfish_elem.set('ThaliaksFavor', 'True')
        pred_exfish_elem.set('Cordial', 'Auto')
        if random.random() < sit_percent:
            pred_exfish_elem.set('Sit', 'True')
        if len(fish_profile_data.get('predator').get('patience_tugs')) > 0:
            pred_exfish_elem.set('Mooch', f"{len(fish_profile_data.get('predator').get('patience_tugs'))}")
            pred_exfish_elem.set('Patience', 'Patience2')
            pred_exfish_elem.set('MinimumGPPatience', '650')
            pred_patience_tugs_elem = ET.SubElement(pred_exfish_elem, "PatientTugs")
            for entry in fish_profile_data.get('predator').get('patience_tugs'):
                ET.SubElement(pred_patience_tugs_elem, "PatienceTug", moochLevel=entry.get('level'), TugType=entry.get('tug'))
        else:
            pred_exfish_elem.set('Chum', 'True')
        fishspots_elem = ET.SubElement(pred_exfish_elem, "FishSpots")
        for fishspot in fish_profile_data.get('fishspot_cords'):
            ET.SubElement(fishspots_elem, "FishSpot", XYZ=f"{fishspot.get('XYZ')}", Heading=f"{fishspot.get('Heading')}")
        pred_keepers_elem = ET.SubElement(pred_exfish_elem, "Keepers")
        ET.SubElement(pred_keepers_elem, "Keeper", name=f"{fish_profile_data.get('predator').get('fish_name')}")
    
    # Main target that is pursued
    exfish_elem = ET.SubElement(while_check_elem, "ExFish", Bait=f"{fish_profile_data.get('bait_name','ERROR')}")
    if fish_profile_data.get('predator'):
        exfish_elem.set('Condition', "Core.Player.HasAura(568)")
    exfish_elem.set('MinFish', '15')
    exfish_elem.set('MaxFish', '25')
    exfish_elem.set('ShuffleFishSpots', 'True')
    exfish_elem.set('ThaliaksFavor', 'True')
    exfish_elem.set('Cordial', 'Auto')
    if random.random() < sit_percent:
        exfish_elem.set('Sit', 'True')
    if len(fish_profile_data.get('patience_tugs')) > 0:
        exfish_elem.set('Mooch', f"{len(fish_profile_data.get('patience_tugs'))}")
        exfish_elem.set('Patience', 'Patience2')
        exfish_elem.set('MinimumGPPatience', '650')
        patience_tugs_elem = ET.SubElement(exfish_elem, "PatientTugs")
        for entry in fish_profile_data.get('patience_tugs'):
            ET.SubElement(patience_tugs_elem, "PatienceTug", moochLevel=entry.get('level'), TugType=entry.get('tug'))
    else:
        exfish_elem.set('Chum', 'True')

    fishspots_elem = ET.SubElement(exfish_elem, "FishSpots")
    for fishspot in fish_profile_data.get('fishspot_cords'):
        ET.SubElement(fishspots_elem, "FishSpot", XYZ=f"{fishspot.get('XYZ')}", Heading=f"{fishspot.get('Heading')}")
    keepers_elem = ET.SubElement(exfish_elem, "Keepers")
    ET.SubElement(keepers_elem, "Keeper", name=f"{fish_profile_data.get('fish_name')}")
    ET.SubElement(exfish_elem, "SurfaceSlaps")
    
    if fish_profile_data.get('predator'):
        if_pref_fish_elem = ET.SubElement(order_elem, "If", condition=f"HasAtLeast({fish_profile_data.get('predator').get('fish_id')},1)")
        ET.SubElement(if_pref_fish_elem, "Desynth", ItemIds=f"{fish_profile_data.get('predator').get('fish_id')}", DesynthDelay="6000", DesynthTimeout="10")
    ET.SubElement(order_elem, "LLoadProfile", Path="../../Start.xml")

    return ET.tostring(root)


def build_conditions(fish_profile_data):
    """
    Build conditions and return string
    """
    # Build Conditions Block
    condition_block =  f"not HasAtLeast({fish_profile_data.get('fish_id','ERROR')},&{fish_profile_data.get('fish_name','ERROR').replace(' ','_')};)"
    condition_block += f" and HasAtLeast({fish_profile_data.get('bait_id','ERROR')},1)"
    if fish_profile_data.get('time_window'):
        if fish_profile_data.get('time_window').get('start') > fish_profile_data.get('time_window').get('end'):
            condition_block += f" and (IsTimeBetween({fish_profile_data.get('time_window').get('start')},24) or IsTimeBetween(0,{fish_profile_data.get('time_window').get('end')}))"
        else:
            time_span = ",".join([str(a) for a in fish_profile_data.get('time_window').values()])
            condition_block += f" and IsTimeBetween({time_span})"
    if fish_profile_data.get('weather'):
        weather = ', '.join(f"'{w}'" for w in fish_profile_data.get('weather'))
        condition_block += f" and ExBuddy.Helpers.SkywatcherPlugin.IsWeatherInZone({fish_profile_data.get('fish_hole').get('zone_id')}, {weather})"
    if fish_profile_data.get('transition'):
        weather = ', '.join(f"'{w}'" for w in fish_profile_data.get('weather'))
        condition_block += f" and ExBuddy.Helpers.SkywatcherPlugin.PredictWeatherInZone({fish_profile_data.get('fish_hole').get('zone_id')}, TimeSpan.FromHours(-8), {weather})"
    return condition_block


def save_to_file(fish_xml_profile, fish_profile_data):
    """
    Save to local file
    """
    region = fish_profile_data.get('fish_hole').get('region')
    zone = fish_profile_data.get('fish_hole').get('zone')
    file_path = f"{region}/{zone}".replace(' ', '_')
    file_name = fish_profile_data.get("fish_name","ERROR").replace(' ', '_')
    Path(file_path).mkdir(parents=True, exist_ok=True)

    # Add comments
    root = ET.fromstring(fish_xml_profile)
    for elem in root.iter("If"):
        if ",3)" in elem.attrib.get('condition') or ",50)" in elem.attrib.get('condition'):
            elem.insert(0,ET.Comment(f"{fish_profile_data.get('bait_name','ERROR')}"))

    tree = ET.ElementTree(root)
    ET.indent(tree, space='\t')
    tree.write(f'{file_path}/{file_name}.xml', encoding='utf8', method='xml')

    with open(f'{file_path}/{file_name}.xml', 'r') as file:
        contents = file.readlines()
    header_comment = f'<!--\n\tProfile: {fish_profile_data.get("fish_name")} ({fish_profile_data.get("fish_id")})\n\tAuthors: miss-aoi\n-->\n'
    doctype_entity = f'<!DOCTYPE Profile [\n\t<!-- Adjust to desired amount -->\n\t<!ENTITY {file_name} "1">\n]>\n'
    contents.insert(1,header_comment)
    contents.insert(2, doctype_entity)
    contents = [a.replace('&amp;', '&') for a in contents]
    with open(f'{file_path}/{file_name}.xml', 'w') as file:
        contents = "".join(contents)
        file.write(contents)

    return f"{file_path}/{file_name}.xml"


def process_fish():
    """
    Create a profile for each fish specified 
    """
    counter = 1
    for fish_id, fish_name in big_fish_ids.items():
        
        resp = requests.get(f'{gt_url}/db/doc/item/en/3/{fish_id}.json')
        fish_data = json.loads(resp.text)
        try:
            fish_spot = fish_data.get('item','').get('fish','').get('spots',[])[0]
        except IndexError:
            if fish_name in endwalker_folklore_fish:
                fish_spot = endwalker_folklore_fish.get(fish_name)
            else:
                print(f"[{counter}/{len(big_fish_ids)}] Skipped {fish_name} - Fishing spot data not found.")
                counter += 1
                time.sleep(0.5)
        fish_details = process_bait_details(fish_spot)
        predator = process_predator(fish_spot)

        fish_profile_data = {
            "fish_id": fish_id,
            "fish_name": fish_name,
            "bait_id": str(fish_details.get('bait_id')),
            "bait_name": fish_details.get('bait_name'),
            "bait_type": fish_details.get('bait_type'),
            "bait_amount": fish_details.get('bait_amount'),
            "time_window": fish_spot.get('during', {}),
            "hookset": fish_spot.get('hookset',''),
            "tug": fish_spot.get('tug',''),
            "weather": fish_spot.get('weather',[]),
            "transition": fish_spot.get('transition', []),
            "fish_hole": gt_zone_mapping.get(str(fish_spot.get('spot'))),
            "patience_tugs": fish_details.get('patience_tugs', []),
            "predator": predator,
            "submap_id": gt_zone_mapping.get(str(fish_spot.get('spot'))).get('submap_id'),
            "lisbeth_cords": gt_zone_mapping.get(str(fish_spot.get('spot'))).get('lisbeth_cords'),
            "fishspot_cords": gt_zone_mapping.get(str(fish_spot.get('spot'))).get('fishspot_cords')
        }

        fish_xml_profile = build_xml_profile(fish_profile_data)

        # Save to file
        file_path = save_to_file(fish_xml_profile, fish_profile_data)

        print(f"[{counter}/{len(big_fish_ids)}] Created {file_path}")
        counter += 1
        time.sleep(0.5)


if __name__ == "__main__":
    process_fish()
