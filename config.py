import importlib
import random

import cv2
import numpy as np

from dataset import get_dataset


class Config(object):
    """Configuration file."""

    def __init__(self):
        self.seed = 88888888
        self.logging = True

        # turn on debug flag to trace some parallel processing problems more easily
        self.debug = False
        model_name = "sonnet"

        # whether to predict the nuclear type, availability depending on dataset!
        self.type_classification = True

        # shape information - 
        # below config is for original mode. 
        # If original model mode is used, use [270,270] and [80,80] for act_shape and out_shape respectively
        # If fast model mode is used, use [256,256] and [164,164] for act_shape and out_shape respectively
        aug_shape = [540, 540] # patch shape used during augmentation (larger patch may have less border artefacts)
        act_shape = [270, 270] # patch shape used as input to network - central crop performed after augmentation
        out_shape = [76, 76] # patch shape at output of network

        self.dataset_name = "glysac" # extracts dataset info from dataset.py
        # self.dataset_name = "consep"

        self.log_dir = "logs/" # where checkpoints will be saved
        nt_class_num = 5 if self.dataset_name == "consep" else 4  # for glysac # number of nuclear types (including background)
        num_classes = 1024  # number of nuclear types (including background)
        nf_class_num = 2
        no_class_num = 16
        # paths to training and validation patches
        self.valid_dir_list = [
            f"./dataset/training_data/{self.dataset_name}/valid/540x540_164x164"
        ]
        self.train_dir_list = [
            f"./dataset/training_data/{self.dataset_name}/train/540x540_164x164",
            # f"./dataset/training_data/{self.dataset_name}/train_mix_0_p1_40/540x540_164x164"
        ]
        self.shape_info = {
            "train": {"input_shape": act_shape, "mask_shape": out_shape,},
            "valid": {"input_shape": act_shape, "mask_shape": out_shape,},
        }

        # * parsing config to the running state and set up associated variables
        self.dataset = get_dataset(self.dataset_name)

        module = importlib.import_module(
            "models.%s.opt" % model_name
        )
        self.model_config = module.get_config(num_classes, nt_class_num, nf_class_num, no_class_num)
