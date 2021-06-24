import glob, h5py, pdb, io
import os.path as osp 
import numpy as np
from PIL import Image
import pandas as pd 
from tqdm import tqdm


def open_annotation_tsv(path):
    df = pd.read_csv(path, sep='\t', names=["name","caption","url"])
    name_to_caption = {}
    for index, row in df.iterrows():
        name_to_caption[row['name'].strip()] = row['caption'].strip()
    return name_to_caption


def to_h5py(ann_path, out_h5_path, out_txt_path, invalid_txt_path):
    name_to_caption = open_annotation_tsv(ann_path)
    id_tab_caption = []
    invalid = []
    with h5py.File(out_h5_path, 'x') as fid:
        for name, caption in tqdm(name_to_caption.items()):
            img_id = osp.basename(name)
            with open(name, 'rb') as fid_img:
                binary_data = fid_img.read()
            np_data = np.frombuffer(binary_data, dtype='uint8')
            try:
                img = Image.open(io.BytesIO(np_data)).convert('RGB')
                fid_v = fid.create_dataset(img_id, np.shape(np_data), dtype=h5py.h5t.STD_U8BE, data=np_data)
                id_tab_caption.append('%s\t%s'%(img_id, caption))
            except:
                invalid.append(img_id)
    # pdb.set_trace()
    with open(out_txt_path, 'x') as fid:
        fid.write('\n'.join(id_tab_caption))
    with open(invalid_txt_path, 'x') as fid:
        fid.write('\n'.join(invalid))

to_h5py('valid_val.tsv', 'cc3m_val.h5', 'cc3m_val.txt', 'cc3m_val_invalid.txt')