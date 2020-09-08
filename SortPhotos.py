import os


class ImageSorter:
    def __init__(self, path_to_directory, extentions=['.JPG', '.JPEG', '.RAW']):
        self.path_to_directory = path_to_directory
        self.extentions = extentions
        self.get_data()
        self.group_photos_by_id()

    def get_data(self):
        from PIL import Image, ExifTags
        import pandas as pd
        import numpy as np
        
        df = pd.DataFrame(columns=['FILE', 'DATE'])

        for root, _, files in os.walk(self.path_to_directory):
            if files:
                for file in files:
                    for ext in self.extentions:
                        if file.endswith(ext):
                            full_path_to_file = os.path.join(root, file)
                            img = Image.open(full_path_to_file)
                            exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
                            time = exif['DateTime']
                            
                            df = df.append( {'FILE': full_path_to_file,'DATE': time}, ignore_index=True)
        
        df['DATE'] = pd.to_datetime(df['DATE'], format='%Y:%m:%d %H:%M:%S')
        df.set_index('DATE', inplace=True, drop=True)
        df['groupid'] = (  ( df.index.to_series()-df.index[0] ).dt.seconds / (30)   ).astype(np.int32)
        df2 = pd.DataFrame( df.groupby('groupid').describe()["FILE"]['count'].astype(int) )
        df3 = df.merge(df2, on='groupid', how='left')
        df3.to_csv('Photos.csv', index=False, encoding='utf-8')

    def group_photos_by_id(self):
        import csv

        with open('Photos.csv') as file:
            reader = csv.DictReader(file)

        for line in reader:
            if int(line['count']) > 1:
                os.makedirs(line['groupid'], exist_ok=True)
                head,filename = os.path.split( line['FILE'] )
                os.rename(line['FILE'], (head+line['groupid']+filename) )


if __name__ == "__main__":
    path_to_directory = 'C:/Users/Krzysztof/Pictures/Fiz'
    sorter = ImageSorter(path_to_directory)
