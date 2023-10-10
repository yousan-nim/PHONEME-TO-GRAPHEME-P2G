import os
# import p2g
import pandas as pd

from .main import P2G

def Translate(word):
    data = p2g.main.P2G(word)
    print(data)
    return data

def Tool(file, experiments_name, csv_=True, txt_=True):
    data = pd.read_csv(f'{file}')

    path_ = []
    
    word_ref = []
    word_hyp = []
    
    phone_ref = []
    phone_hyp = []

    level_ref = []
    level_hyp = []

    for ele in data.values: 
        path = ele[0][-13:-4]
        
        ##################### REF #####################
        data_ref = ele[1].replace("|"," ")
        ### WORD
        data_word_ref = data_ref

        ### PHONE
        data_phone_ref = p2g.main.saparate_componant(data_ref, type_='phone')

        ### TONE
        data_level_ref = p2g.main.saparate_componant(data_ref, type_='level')
    
    
        ##################### HYP #####################
        data_hyp = ele[2].replace("|"," ") 
        ### WORD
        data_word_hyp = data_hyp
        
        ### PHONE
        data_phone_hyp = p2g.main.saparate_componant(data_hyp, type_='phone')

        ### TONE
        data_level_hyp = p2g.main.saparate_componant(data_hyp, type_='level')


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
                

def Create_set(file, experiments_name, sep_=True, csv_=True, type_='default'):
    path_ = []
    phone_ = []
    
    if sep_:
        data = pd.read_csv(f'{file}', sep ='\t')
#         print("--tsv--")
    else:
        data = pd.read_csv(f'{file}')
#         print("--csv--")

    for ele in data.values: 
        path  = ele[0]
        phone = ele[1]
        
        ### PHONE
        
        data_phone = p2g.main.saparate_componant(phone, type_=type_ )
        
        
        if type_ == "delimeter":
            data_phone = data_phone.replace(" ","")

        path_.append(path)
        phone_.append(data_phone)

    if csv_:
        dataFrame = pd.DataFrame()
        dataFrame['path'] = path_
        dataFrame['phone'] = phone_
        dataFrame.to_csv(f'{experiments_name}/{file}', index=False, sep='\t')

    print(f"create file : {file}")
    
    
    
                
                
if __name__ == '__main__':
    
    experiments_name = './9010100_noise_validationset'
    
    file = 'benchmark_9010100_noise_validationset.csv'
    
    if not os.path.exists(experiments_name):
        os.makedirs(experiments_name)
        os.makedirs(experiments_name+"/wer")
        os.makedirs(experiments_name+"/per")
        os.makedirs(experiments_name+"/ter")
    
    print(f"create : {experiments_name}")
    
    Tool(file, experiments_name)


    
    
