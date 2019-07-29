import json
import donkeycar as dk
from glob import glob
import os
from zipfile import ZipFile
from datetime import datetime as dt
from shutil import copy

"""
dingo_archive_paths=t1,t2...tn
model_path = model/dir/tn(plus):date.h5
python manage train.py --tub=t1,t2...tn --model=model_path
"""
def extract_if_not_extracted(dingo_archive):
    extracted_path = os.path.join(dingo_archive,'tub')
    os.path.expanduser(extracted_path)
    if not os.path.exists(extracted_path):
        zip_p = os.path.join(dingo_archive, 'tub.zip')
        print(f"unzipping: {zip_p}")
        zip_f = ZipFile(zip_p)
        zip_f.extractall(dingo_archive)
        zip_f.close()
    return extracted_path

def write_model_info(new_model_dir, dingo_archive_paths, cfg, status="training"):
    now        = dt.now().strftime("%Y-%m-%d_%H:%M:%S")
    model_info = {"date" : now,
                  "dingo_archive_paths" : dingo_archive_paths,
                  "training_status" : status}
    with open(os.path.join(new_model_dir,"model_info.json"), 'w') as f:
              json.dump(model_info, f, indent=2)
    cfg.write_to_file(os.path.join(new_model_dir, "config.py"))

def process_dingo_archives_gen_model_path(dingo_archive_paths, models_dir, cfg):

    tub_paths = [extract_if_not_extracted(t) for t in dingo_archive_paths]
    assert len(tub_paths) > 0, "Must supply at least 1 dingo_archive"

    if len(tub_paths) > 1:
      plus = f"_plus{len(tub_paths)-1}"
    else:
      plus = ""

    last_tub_path = tub_paths[-1]
    last_dingo_archive_name = last_tub_path.split(os.sep)[-2]
    # If a path is entered with a trailing '/' then the final
    # element of 'last_dingo_archive_path' will be "". This is not what we want.
    if last_dingo_archive_name == "tub":
        last_dingo_archive_name = last_tub_path.split(os.sep)[-3]
    new_model_name  = f"{last_dingo_archive_name}{plus}"
    new_model_dir   = os.path.join(models_dir, new_model_name)
    version_number  = len(glob(new_model_dir + "*"))
    new_model_dir  += f"_v{version_number}"
    new_model_path  = os.path.join(new_model_dir, "model.h5")
    model_info_path = os.path.join(new_model_dir, "model_info.json")
    os.makedirs(new_model_dir, exist_ok=False)
    write_model_info(new_model_dir, dingo_archive_paths, cfg, status="training")
    return new_model_path, tub_paths
