# convert Region Notes.txt data into region list, entrances, and locations
region_file = open("Region Notes.txt", "r")
list_file = open("1 - region list.txt", "w")
entrances_file = open("2 - region entrances.txt", "w")
locations_file = open("3 - locations.txt", "w")

for line in region_file:
    line = line.strip()
    if line.startswith("REGION"):
        region_name = line.split(":", 1)[0].split(" ")[1]
        list_file.write(region_name + "\n")
    elif "->" in line:
        entrances_file.write(line + "\n")
    elif line.startswith("LOCATION"):
        location_data = line.split("LOCATION ", 1)[1]
        locations_file.write(location_data + "\n")
        
list_file.close()
entrances_file.close()
locations_file.close()

file_in = open("4 - gem events.csv", "r")
file_out = open("4 - gem events.txt", "w")

for line in file_in:
    if line.split(",")[1] == "":  # skip lines which just specify a level name and no data
        continue
    region, gems, description, rule = line.split(",", maxsplit=3)
    rule = rule.strip()
    if "\"" in rule:  # oddity from storing data in Excel for csv. No clue why some " appear but all relevant quotes are ' so it's safe to remove "
        rule = rule.replace("\"", "")

    new_line = f"{region} | {gems} Gems ({description}) | {rule}"
    file_out.write(new_line + "\n")