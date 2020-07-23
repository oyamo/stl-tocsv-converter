import os
import csv
import re

csv_path = ''
stl_path = ''

stl_path_is_valid = False
csv_path_is_valid = False

out_file = "out.csv"

# The output csv will take this format ie The header row will have the following 
csv_header = ['n_x','n_y','n_z','v1_x','v1_y','v1_z'\
            ,'v2_x','v2_y','v2_z','v3_x','v3_y','v3_z']

# Safe way of getting paths from the user
while not stl_path_is_valid or not csv_path_is_valid:
    # Check if the stl path provided is valid
    if not stl_path_is_valid :
        # If not Repeat the process of getting an stl file
        stl_path = input("Enter Full Path to STL File:")
        stl_path = stl_path.replace('\'','')
        stl_path = stl_path.replace('\"','')
        stl_path = stl_path.strip()# Remove any leading white spaces
        stl_path_is_valid = os.path.exists(stl_path) and os.path.isfile(stl_path)
        if not stl_path_is_valid :
            print(f"Error: {stl_path} does not exist")
            print("Example: ~/Desktop/sketch.stl")
            continue
    #Check if csv output path is valid and exists
    if not csv_path_is_valid:
        csv_path = input("Enter full path to destination file:")
        split_path = os.path.split(csv_path)
        folder = split_path[0].replace("//","/").replace('\\\\','\\')
        csv_path_is_valid = (os.path.exists(folder) and os.path.isdir(folder) and len(split_path) >=2 and '.csv' in split_path[1])
        if len(folder) < 4:
            csv_path_is_valid = False
        if not csv_path_is_valid:
            _ = csv_path
            csv_path_is_valid ="\\" not in _ and ".\\" not in _ and "/" not in _ and "./" not in _ and _[-4:] == ".csv" 
            csv_path = './' + csv_path
        if not csv_path_is_valid:
            print(f"Error: {folder} does not exist")
            print("Example: ~/Desktop/out.csv")
            continue





# Memory efficient way 
def parse():
    with open(stl_path,'r') as payload, open(csv_path,'w') as out:
        # Get the contents of the stl and split the facets into an array
        print("Loading facets:",end="")
        contents =  re.split('endfacet', payload.read())
        print( len(contents),"facets found")
        # Initialise dictionary Writer
        writer   =  csv.DictWriter(out,fieldnames=csv_header)
        writer.writeheader()
        print("Converting.....")
        for content in contents:
            # Use regular expressions to get the contents of the vertices
            normal = re.findall(r"facet normal +([\dEe\-.\+\s]+)+\n\s?",content)
            vertex = re.findall(r"\s*vertex+([\dEe\-.\+\s]+)+\n\s?",content)
            
            # Output the vertices and normals onto a dictionary
            if len(normal) ==1 and len(vertex) ==3:
                out_dict    = dict()
                n           = re.split(r'\s+',normal[0].strip())
                if len(n) == 3:
                    out_dict['n_x'] = n[0]
                    out_dict['n_y'] = n[1]
                    out_dict['n_z'] = n[2]
                for i in range(1,4):
                    v = vertex[i-1].strip()
                    v = re.split(r"\s+", v)  
                    if len(v) == 3:
                        out_dict[f'v{i}_x'] = v[0]
                        out_dict[f'v{i}_y'] = v[1]
                        out_dict[f'v{i}_z'] = v[2]
                
                if len(out_dict) == 12:
                    write = writer.writerow(out_dict)
    print("Done: Output saved as",csv_path)


parse()
