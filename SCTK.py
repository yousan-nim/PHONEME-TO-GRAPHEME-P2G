import os
import p2g
import pandas as pd
import argparse

import zlib
import zipfile
    
def Tool(file, experiments_name, csv_=True, txt_=True):
    data = pd.read_csv(f'{experiments_name}/bin/{file}')

    path_ = []
    
    word_ref = []
    word_hyp = []
    
    phone_ref = []
    phone_hyp = []

    level_ref = []
    level_hyp = []

    for ele in data.values: 
        
        if len(ele[0]) == 9:
            path = ele[0]
        else:
            path = ele[0][-13:-4]
        
        ##################### REF #####################
        data_ref = ele[1].replace("|"," ")
        ### WORD
        data_word_ref = data_ref

        ### PHONE
        data_phone_ref = p2g.saparate_componant(data_ref, only_phone=True)
        data_phone_ref = " ".join(data_phone_ref)
        ### TONE
        data_level_ref = p2g.saparate_componant(data_ref, only_level=True)
        data_level_ref = " ".join(data_level_ref)
    
    
        ##################### HYP #####################
        data_hyp = ele[2].replace("|"," ") 
        ### WORD
        data_word_hyp = data_hyp
        
        ### PHONE
        data_phone_hyp = p2g.saparate_componant(data_hyp, only_phone=True)
        data_phone_hyp = " ".join(data_phone_hyp)
        ### TONE
        data_level_hyp = p2g.saparate_componant(data_hyp, only_level=True)
        data_level_hyp = " ".join(data_level_hyp)

        path_.append(path)
        
        word_ref.append(data_word_ref)
        word_hyp.append(data_word_hyp)
        
        phone_ref.append(data_phone_ref)
        phone_hyp.append(data_phone_hyp)

        level_ref.append(data_level_ref)
        level_hyp.append(data_level_hyp)

    if csv_:
        dataFrame = pd.DataFrame()
        dataFrame['path'] = path_
        dataFrame['word_ref'] = word_ref
        dataFrame['word_hyp'] = word_hyp
        dataFrame['phone_ref'] = phone_ref
        dataFrame['phone_hyp'] = phone_hyp
        dataFrame['level_ref'] = level_ref
        dataFrame['level_hyp'] = level_hyp
        dataFrame.to_csv(f'{experiments_name}/{file}', index=False)
        data = pd.read_csv(f'{experiments_name}/{file}')
        print(f"create file : {experiments_name}/{file}")
    
    if txt_:
        ######################## WER ########################
        data = pd.read_csv(f'{experiments_name}/{file}')
        
        with open(f'{experiments_name}/wer/00_ref_word.ref', 'w') as f:
            for i in data.values:
                path = i[0]
                phone = i[1]
                text = phone.replace("  "," ") + " " + f"({path})"
                text = text.replace("|"," ")
                f.writelines(text)
                f.write('\n')

        with open(f'{experiments_name}/wer/00_hyp_word.hyp', 'w') as f:
            for i in data.values:
                path = i[0]
                pre_phone = i[2]
                text = pre_phone.replace("  "," ") + " " + f"({path})"
                f.writelines(text)
                f.write('\n')
            
        ######################## PER ########################
        with open(f'{experiments_name}/per/01_ref_phone.ref', 'w') as f:
            for i in data.values:
                path = i[0]
                phone = i[3]
                text = phone.replace("  "," ") + " " + f"({path})"
                f.writelines(text)
                f.write('\n')

        with open(f'{experiments_name}/per/01_hyp_phone.hyp', 'w') as f:
            for i in data.values:
                path = i[0]
                pre_phone = i[4]
                text = pre_phone.replace("  "," ") + " " + f"({path})"
                f.writelines(text)
                f.write('\n')
        
        ######################## TER ########################
        with open(f'{experiments_name}/ter/02_ref_level.ref', 'w') as f:
            for i in data.values:
                path = i[0]
                tone = i[5]
                tone = " ".join(tone)
                text = tone.replace("  "," ") + " " + f"({path})"
                f.writelines(text)
                f.write('\n')

        with open(f'{experiments_name}/ter/02_hyp_level.hyp', 'w') as f:
            for i in data.values:
                path = i[0]
                tone = i[6]
                tone = " ".join(tone)
                text = tone.replace("  "," ") + " " + f"({path})"
                f.writelines(text)
                f.write('\n')
                


def zipit(folders, path, zip_filename):
    zip_file = zipfile.ZipFile(f"{path}/{zip_filename}.zip", 'w', zipfile.ZIP_DEFLATED)

    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                zip_file.write(
                    os.path.join(dirpath, filename),
                    os.path.relpath(os.path.join(dirpath, filename), os.path.join(folders[0], '../..')))

    zip_file.close()

                
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--name", help="", type=str , default='Experiment') 
    parser.add_argument("--file", help="", type=str , default='')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.name):
        os.makedirs(args.name)

    if not os.path.exists(args.name+"/wer"):
        os.makedirs(args.name+"/wer")
        
    if not os.path.exists(args.name+"/per"):
        os.makedirs(args.name+"/per")
    
    if not os.path.exists(args.name+"/ter"):
        os.makedirs(args.name+"/ter")
        

    
    print(f"create : {args.name}")
    
    Tool(args.file, args.name)
    
    folders = [
        args.name+"/per",
        args.name+"/wer",
        args.name+"/ter",
    ]
    
    name = args.file[:-4]
    
    zipit(folders, args.name, name)
    
    # python wav2vec2_SCTK.py --name Experiment_MeVoice_Clean --file TestSet.csv
    # python wav2vec2_SCTK.py --name Experiment_MeVoiceLotu_Clean --file ValidationSet.csv

