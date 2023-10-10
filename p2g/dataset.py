from .main import P2G

def make_distribution(data_dict): 
    path_ = []
    phone_ = []


    for ele in data_dict: 
        path = data['path']
        
        ##################### Phone #####################
        phone = p2g.main.saparate_componant(data['phone'], type_='both')

        path_.append(path)
        phone_.append(phone)

    return {
        'path': audio_files,
        'phonetics': phonetic_files,
    }