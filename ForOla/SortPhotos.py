import os


class ImageSorter:
    def __init__(self, path_to_directory, create_copy=False, extentions=['.JPG', '.JPEG', '.RAW']):
        self.path_to_directory = path_to_directory
        self.extentions = extentions
        self.create_copy = create_copy
        self.copy_to = os.path.join(path_to_directory, 'Sorted')
        self.sort_file_name = 'Photos.csv'

    def __del__(self):
        os.remove(self.sort_file_name)

    def sort_by_date(self, unit, interval):
        self.interval=int(interval)
        self.unit=str(unit)
        self.get_data()
        self.group_photos_by_id()

    def get_data(self):
        from PIL import Image, ExifTags
        import pandas as pd
        
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
                            
                            df = df.append( {'FILE': full_path_to_file,'DATE': time}, ignore_index=True )
        
        # Format date the way we want as currently it is string and we want datetime obj
        df['DATE'] = pd.to_datetime(df['DATE'], format='%Y:%m:%d %H:%M:%S')
        # Then we want to group data and save it to one pd.DataFrame obj
        df.set_index('DATE', inplace=True, drop=True)
        time = self.interval
        if self.unit == "MINUTY":
            time *= 60
        if self.unit == 'DNI':
            time *= 86400
        df['groupid'] = (  ( df.index.to_series()-df.index[0] ).dt.seconds / time   ).astype(int)
        df2 = pd.DataFrame( df.groupby('groupid').describe()["FILE"]['count'].astype(int) )
        df3 = df.merge(df2, on='groupid', how='left')
        # And save it to file
        df3.to_csv(self.sort_file_name, index=False, encoding='utf-8')

    def group_photos_by_id(self):
        import csv

        with open(self.sort_file_name, encoding='utf-8') as file:
            for line in csv.DictReader(file):
                if int(line['count']) > 1:
                    head,filename = os.path.split( line['FILE'] )
                    if self.create_copy:
                        import shutil
                        try:
                            os.makedirs( os.path.join( self.copy_to,line['groupid'] ), exist_ok=True )
                            shutil.copy2(  line['FILE'], os.path.join( self.copy_to,line['groupid'],filename )  )
                        except:
                            continue 
                    else:
                        os.makedirs( os.path.join( head,line['groupid'] ), exist_ok=True )
                        os.rename( line['FILE'], os.path.join(head,line['groupid'],filename) )


if __name__ == "__main__":
    path_to_directory = 'PATH_TO_DIRECTORY'
    sorter = ImageSorter(path_to_directory)
    sorter.sort_by_date(20, "SEKUND")
