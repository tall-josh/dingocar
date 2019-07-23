import json
from glob import glob
import os
from zipfile import ZipFile


"""
tubs=t1,t2...tn
model_path = model/dir/tn(plus):date.h5
python manage train.py --tub=t1,t2...tn --model=model_path
"""

def extract_if_not_extracted(tub):
    if not os.path.exists(os.path.join(tub,'tub')):
        zip_p = os.path.join(tub, 'tub.zip')
        print(f"unzipping: {zip_p}")
        zip_f = ZipFile(zip_p)
        zip_f.extractall(os.path.join(tub))
        zip_f.close()
    

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--info_json', type=str)
    parser.add_argument('-m', '--model_dir', type=str)
    parser.add_argument('-t', '--tubs', nargs="+", type=str)
    args = parser.parse_args()

    with open(args.info_json, 'r') as f:
        info = json.load(f)
    
    tubs = args.tubs

    for t in tubs:
        extract_if_not_extracted(t)

    assert len(tubs) > 0, "Must supply at least 1 tub"

    if len(tubs) > 1:
      plus = f"_plus{len(tubs)-1}"
    else:
      plus = ""

    last_tub_path = tubs[-1]
    last_tub_name = last_tub_path.split(os.sep)[-1]
    # If a path is entered with a trailing '/' then the final
    # element of 'last_tub_path' will be "". This is not what we want.
    if last_tub_name == "":
        last_tub_name = last_tub_path.split(os.sep)[-2]
    new_model_name = f"{last_tub_name}{plus}"
    new_model_path = os.path.join(args.model_dir, new_model_name)
    version_number = len(glob(new_model_path + "*"))
    new_model_path += f"_v{version_number}.h5"
    print(new_model_path)
    

 
