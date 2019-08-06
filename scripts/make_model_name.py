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

def update_model_info(new_model_dir, key, value):
    with open(os.path.join(new_model_dir,"model_info.json"), 'r') as f:
        model_info = json.load(f)

    if key in model_info:
        if isinstance(model_info[key], list):
            model_info[key].append(value)
    else:
        model_info[key]= value

    with open(os.path.join(new_model_dir,"model_info.json"), 'w') as f:
        json.dump(model_info, f, indent=2)


def write_model_info(new_model_dir, dingo_archive_paths, cfg, aug):
    path = os.path.join(new_model_dir,"model_info.json")
    now        = dt.now().strftime("%Y-%m-%d_%H:%M:%S")
    model_info = {"date" : now,
                  "dingo_archive_paths" : dingo_archive_paths,
                  "log" : ["model info file written."],
                  "aug" : aug}

    if aug:
        aug_info = {
                "AUG_MIRROR_STEERING"       : cfg.AUG_MIRROR_STEERING,
                "AUG_SALT_AND_PEPPER"       : cfg.AUG_SALT_AND_PEPPER,
                "AUG_100S_AND_1000S"        : cfg.AUG_100S_AND_1000S,
                "AUG_PIXEL_SATURATION"      : cfg.AUG_PIXEL_SATURATION,
                "AUG_SHUFFLE_CHANNELS"      : cfg.AUG_SHUFFLE_CHANNELS,
                "AUG_SHADOW_IMAGES_PATTERN" : cfg.AUG_SHADOW_IMAGES_PATTERN,
                "AUG_SHADOW_IMAGES"         : cfg.AUG_SHADOW_IMAGES,
                "AUG_BLOCKOUT"              : cfg.AUG_BLOCKOUT,
                "AUG_NORMALIZE"             : cfg.AUG_NORMALIZE,
                "AUG_WARP_PERSPECTIVE"      : cfg.AUG_WARP_PERSPECTIVE,
                "AUG_JITTER_STEERING"       : cfg.AUG_JITTER_STEERING,
                "AUG_JITTER_THROTTLE"       : cfg.AUG_JITTER_THROTTLE}
        model_info["aug"] = aug_info

    #model_info["note"] = timeout_input("Leave a note?", 30)

    with open(path, 'w') as f:
              json.dump(model_info, f, indent=2)
    cfg.write_to_file(os.path.join(new_model_dir, "config.py"))

def process_dingo_archives_gen_model_path(dingo_archive_paths,
                                          models_dir,
                                          cfg,
                                          aug):

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
    existing_model_dirs = glob(new_model_dir + "*")
    if len(existing_model_dirs) > 0:
        version_number  = max([int(name.split('v')[-1]) for name in existing_model_dirs]) + 1
    else:
        version_number = 0
    new_model_dir  += f"_v{version_number}"
    model_info_path = os.path.join(new_model_dir, "model_info.json")
    os.makedirs(new_model_dir, exist_ok=False)
    write_model_info(new_model_dir, dingo_archive_paths, cfg, aug)
    return new_model_dir, tub_paths
