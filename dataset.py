from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import pandas as pd
import os

class customized_dataset(Dataset):
    def __init__(self, dataframe: pd.DataFrame, mode: str, label_to_samples=None):
        self.df = dataframe
        self.mode = mode
        transforms_list1 = [transforms.Resize((128,128)),
                          transforms.RandomHorizontalFlip(p=0.5),
                          transforms.ToTensor(),
                          transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                std=[0.229, 0.224, 0.225])]
        transforms_list2 = [transforms.Resize((128,128)),
                          transforms.ToTensor(),
                          transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                std=[0.229, 0.224, 0.225])]
        self.transforms_train = transforms.Compose(transforms_list1)
        self.transforms_test = transforms.Compose(transforms_list2)
        #self.label_to_samples = np.array(label_to_samples)
        self.label_to_samples = label_to_samples
    def __len__(self) -> int:
        return self.df.shape[0]
    
    def __getitem__(self, index: int):
        # target label
        target = self.df.iloc[index]['target']
        #image_path = self.df.iloc[index]['path']

        current_folder = '/kaggle/working'
        relative_path = self.df.iloc[index]['path']
        #code_folder = 'Code'
        

        # Construct the full path
        image_path = os.path.join(current_folder, relative_path)
        image_path = os.path.normpath(image_path)
        if image_path.startswith('/./'):
            image_path = image_path[3:]
        image_path = image_path.replace('/train2/', '/train/')    
        #parts = image_path.split(os.path.sep)
        # Replace 'train2' with 'train1'
        #parts[3] = 'train'
        #image_path = os.path.join(*parts)
        #print("image_path", image_path)
        img = ""
        pair_img = ""
        # original image
        try :
            img = Image.open(image_path)
        except :
            print("image path not present")
        if self.mode=='train' or self.mode=='valid':
            img = self.transforms_train(img)
            return {'image':img, 'target':target}
        else:
            img = self.transforms_test(img)
            pair_path = self.df.iloc[index]['pair_path']
            pair_path = os.path.join(current_folder, pair_path)
            pair_path = os.path.normpath(pair_path)
            if pair_path.startswith('/./'):
                pair_path = pair_path[3:]
            pair_path = pair_path.replace('/train2/', '/train/')
            try :
                pair_img = Image.open(pair_path)
            except :
                print("pair path not present")
            
            pair_target = self.df.iloc[index]['pair_target']
            pair_img = self.transforms_test(pair_img)
            return {'image':img, 'target':target, 'pair_image':pair_img, 'pair_target':pair_target}
