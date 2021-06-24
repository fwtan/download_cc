import pandas as pd
import zlib, shutil


def open_downloaded_tsv(path):
    df = pd.read_csv(path, sep='\t', names=["name","split","format","size","type","url"])
    url_to_name = {}
    for index, row in df.iterrows():
        if type(row['name']) is str and len(row['name'].strip()) > 10 and row['name'].strip()[:10] == 'validation':
            _, ext = row['format'].split('/')
            ext = ext.strip()
            old_name = row['name'].strip()
            new_name = old_name + '.' + ext
            if ext == 'jpeg':
                url_to_name[row['url'].strip()] = old_name
                # shutil.move(old_name, new_name)
    return url_to_name


def open_annotation_tsv(path):
    df = pd.read_csv(path, sep='\t', names=["caption","url"])
    url_to_caption = {}
    for index, row in df.iterrows():
        url_to_caption[row['url'].strip()] = row['caption'].strip()
    return url_to_caption


ann = open_annotation_tsv('Validation_GCC-1.1.0-Validation.tsv')
dwn = open_downloaded_tsv('downloaded_validation_report.tsv')

valid = []
for k, v in dwn.items():
    if k in ann:
        valid.append('%s\t%s\t%s'%(v, ann[k], k))

with open('valid.tsv', 'w') as f:
    f.write('\n'.join(valid))