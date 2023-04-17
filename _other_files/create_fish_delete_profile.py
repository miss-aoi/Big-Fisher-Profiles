"""
I got tired of manually updating everything.
Let's see if this other idea works out better...
"""
import requests, json, os, time

gt_url = 'https://garlandtools.org'

# Get JSON with all fishing areas
gt_fishing = f'{gt_url}/db/doc/browse/en/2/fishing.json'
resp = requests.get(gt_fishing)
fishing_data = json.loads(resp.text)
area_fish_data = {}
fishing_areas = fishing_data.get('browse', '')
counter = 1
for area in fishing_areas:
    id = area['i']
    gt_area = f'https://garlandtools.org/db/doc/fishing/en/2/{id}.json'
    resp = requests.get(gt_area)
    area_data = json.loads(resp.text)
    print_summary = [a.get('obj','').get('n','') for a in [a for a in area_data.get('partials','')]]
    print(f"({counter}/{len(fishing_areas)}) Zone: {id} - {', '.join(print_summary)}")
    counter += 1
    for item in area_data.get('partials',''):
        obj = item.get('obj','')
        fish_id = obj.get('i')
        fish_name = obj.get('n')
        area_fish_data[fish_id] = fish_name
    # time.sleep(1) # Be kind and don't spam their servers too much too quickly

current_dir = os.getcwd()
try:
    os.remove(f'{current_dir}/desynth_all_fishies.xml')
except:
    pass
with open(f'{current_dir}/desynth_all_fishies.xml', 'a') as file:
    file.write('<?xml version="1.0" encoding="utf-8"?>\n')
    file.write('<!--\n')
    file.write('\tProfile: Desynth All Fishies (Big and Small)\n')
    file.write('\tAuthors: miss-aoi\n')
    file.write('\tWil desynth all Big Fish - you have to do smalls yourself.\n')
    file.write('\tBe sure to update "1" as needed in Start.xml as needed\n')
    file.write('-->\n')
    file.write('<Profile>\n')
    file.write('\t<Name>Desynth All Fishies</Name>\n')
    file.write('\t<BehaviorDirectory></BehaviorDirectory>\n')
    file.write('\t<Order>\n')
    for id, name in area_fish_data.items():
        file.write(f'\t\t<If Condition="HasAtLeast({id},1)"> <!-- {name} -->\n')
        file.write(f'\t\t\t<Desynth ItemIds="{id}" DesynthDelay="6000" DesynthTimefile="10"/>\n')
        file.write('\t\t</If>\n')
    file.write('\t</Order>\n')
    file.write('</Profile>\n')
