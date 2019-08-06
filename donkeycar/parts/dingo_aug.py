from glob import glob
import os
from PIL import Image
import numpy as np
import tqdm
import json

def save_img(img, save_path):
    I_out = Image.fromarray(np.uint8(img))
    I_out.save(os.path.join(save_path))

def mirror_image(I):
    # mirror image
    I = mirror_about_y(I)
    return I

def mirror_about_y(img_arr):
    return np.fliplr(img_arr)

def jitter(value, min_delta, max_delta):
    offset = np.random.uniform(low=min_delta, high=max_delta)
    return value + offset

def salt_and_pepper(img_arr, prob=0.333):
    bools = np.array([True, False])
    probs = np.array([prob/2, 1-(prob/2)])
    salt_mask  = np.random.choice(bools, size=img_arr.shape[:2], p=probs)
    pepper_mask  = np.random.choice(bools, size=img_arr.shape[:2], p=probs)
    img_arr_copy = img_arr[:]
    img_arr_copy[salt_mask]   = 255
    img_arr_copy[pepper_mask] = 0
    return img_arr_copy

def hundreds_and_thousands(img_arr, prob=0.333):
    bools = np.array([True, False])
    probs = np.array([prob, 1-prob])
    rgb_mask  = np.random.choice(bools, size=img_arr.shape, p=probs)
    num_true  = rgb_mask.sum()
    rand_ints = np.random.randint(low=0, high=256, size=(num_true,))
    img_arr_copy = img_arr[:]
    img_arr_copy[rgb_mask] = rand_ints

    return img_arr_copy

def overlay_random_image(I, max_alpha, image_list):
    rand_alpha      = np.random.uniform(high = max_alpha)
    rand_image_path = np.random.choice(image_list)
    h,w,_           = I.shape
    rand_image      = Image.open(rand_image_path).resize([w,h],
                                                    resample = Image.BILINEAR)
    rand_image = np.asarray(rand_image, dtype=np.float32) / 255.
    rand_image*= rand_alpha
    if len(rand_image.shape) == 2:
        # Grayscale image
        rand_image = np.dstack((rand_image, rand_image, rand_image))

    I          = I.astype(np.float32) / 255.
    I         *= (1-rand_alpha)
    I          = np.array((I+rand_image)*255, dtype=int)
    return I

def saturation(I, rand_min, rand_max):
    sat = np.random.randint(rand_min, rand_max, size=I.shape)
    return np.clip(I+sat, 0,255)


def rgb2gray(rgb_img):
    # weighted luminosity method to convert to grayscale
    # https://www.tutorialspoint.com/dip/grayscale_to_rgb_conversion.htm
    I_gr = I[:,:,0]*0.3 + I[:,:,1]*0.59 + I[:,:,2]*0.11

def shuffle_channels(I):
    channel_order = np.array([0,1,2])
    np.random.shuffle(channel_order)
    I =  I[...,channel_order]
    return I
    #I = I[...,0] * np.random.uniform(1.0, 1.5)
    #I = I[...,1] * np.random.uniform(1.0, 1.5)
    #I = I[...,2] * np.random.uniform(1.0, 1.5)
    #return np.clip(I, 0,255)

def blockout(I, min_frac, max_frac):
    h,w,_    = I.shape
    if min_frac * min([h,w]) < 2:
        #print("***** WARNING *****")
        #print("The minimum blockout rectangle size must be > 2."
        #    " Make min_frac and max_frac larger. Maybe check"
        #    " the size of your images")
        #print("image h : {}, image_w : {}".format(h,w))
        #print("Skipping")
        return I
    frac     = np.random.uniform(min_frac, max_frac)
    block_w  = np.random.randint(1, w*frac)
    block_h  = np.random.randint(1, h*frac)
    x_offset = np.random.randint(0, w-block_w)
    y_offset = np.random.randint(0, h-block_h)
    I[y_offset:y_offset+block_h+1, x_offset:x_offset+block_w,...] = 0
    return I

AUG_CONFIG         = None
OVERLAY_IMAGE_POOL = None
def apply_aug_config(record, aug_config=None, normalize_result=False):
    global AUG_CONFIG, OVERLAY_IMAGE_POOL

    if AUG_CONFIG is None:
        print("LOADING CONFIG")
        if aug_config is None:
            with open("aug_config_sample.json", 'r') as f:
                AUG_CONFIG = json.load(f)
        else:
            AUG_CONFIG = aug_config

    if (OVERLAY_IMAGE_POOL is None) and ("image_overlay" in AUG_CONFIG):
        pattern = AUG_CONFIG["image_overlay"]["pattern"]
        OVERLAY_IMAGE_POOL = glob(pattern)
        print(f"Found {len(OVERLAY_IMAGE_POOL)} overlay images")

    IMAGE_KEY    = 'cam/image_array'
    STEERING_KEY = 'user/angle'
    image        = record[IMAGE_KEY]
    steering     = record[STEERING_KEY]
    aug = "mirror_y"
    if aug in AUG_CONFIG and random_bool(AUG_CONFIG[aug]["aug_prob"]):
        #print(f"\n {aug}")
        image = mirror_image(image)
        steering *= -1.

    aug = "salt_ane_pepper"
    if aug in AUG_CONFIG and random_bool(AUG_CONFIG[aug]["aug_prob"]):
        #print(f"\n {aug}")
        image = salt_and_pepper(image, prob=AUG_CONFIG[aug]["noise"])

    aug = "100s_and_1000s"
    if aug in AUG_CONFIG and random_bool(AUG_CONFIG[aug]["aug_prob"]):
        #print(f"\n {aug}")
        image = hundreds_and_thousands(image, prob=AUG_CONFIG[aug]["noise"])

    aug = "image_overlay"
    if aug in AUG_CONFIG and random_bool(AUG_CONFIG[aug]["aug_prob"]):
        #print(f"\n {aug}")
        max_alpha = float(AUG_CONFIG[aug]["max_alpha"])
        image = overlay_random_image(image, max_alpha, OVERLAY_IMAGE_POOL)

    aug = "pixel_saturation"
    if aug in AUG_CONFIG and random_bool(AUG_CONFIG[aug]["aug_prob"]):
        #print(f"\n {aug}")
        image = saturation(image, AUG_CONFIG[aug]["min_val"], AUG_CONFIG[aug]["max_val"])

    aug = "shuffle_channels"
    if aug in AUG_CONFIG and random_bool(AUG_CONFIG[aug]["aug_prob"]):
        #print(f"\n {aug}")
        image = shuffle_channels(image)

    aug = "blockout"
    if aug in AUG_CONFIG and random_bool(AUG_CONFIG[aug]["aug_prob"]):
        #print(f"\n {aug}")
        image = blockout(image, AUG_CONFIG[aug]["min_frac"], AUG_CONFIG[aug]["max_frac"])

    if normalize_result:
        image = np.divide(image, 255.)

    record[IMAGE_KEY]    = image
    record[STEERING_KEY] = steering
    return record

def random_bool(true_prob):
    return np.random.choice([True, False], 1, p=[true_prob, 1.-true_prob])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input-pattern', type=str)
    parser.add_argument('-o', '--output-dir', type=str)
    parser.add_argument('--config', type=str)
    parser.add_argument('-c', '--count', type=int)
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # load image paths
    image_paths = glob(args.input_pattern)
    assert len(image_paths) > 0, ("You need more than zero images to perform"
                                  " augmentation dummy!"
                                  " --> {}".format(args.input_pattern))

    print(("{} images found to perform augmentation"
          " on.").format(len(image_paths)))
    if args.count:
        if args.count > len(image_paths):
            to_augment = np.random.choice(image_paths,
                                         size=args.count,
                                         replace=True)
        else:
            to_augment = np.random.choice(image_paths,
                                         size=args.count,
                                         replace=False)
    else:
        to_augment = image_paths


    # Load randomization config
    with open(args.config, 'r') as f:
        config = json.load(f)

    aug = "image_overlay"
    if aug in config:
        pattern = config[aug]["pattern"]
        overlay_image_pool = glob(pattern)
        assert len(overlay_image_pool) > 0,\
            ("Image pool must be greater than zero,"
             " if you want to add noise overlays,"
             " check your pattern '{}'").format(pattern)

    # Loop over all imagee
    count=-1
    for i, img_path in enumerate(tqdm.tqdm(to_augment)):
        count += 1
        name = os.path.basename(img_path)
        I = np.asarray(Image.open(img_path))
        I = np.array(I)

        I = apply_aug_config(I, config)

        # save augmented image
        new_image_path = os.path.join(args.output_dir, "{}_{}".format(i,name))
        save_img(I, new_image_path)
