
import numpy as np
from PIL import Image, ImageDraw
import os
import time
import concurrent.futures
import pandas as pd
# import pyximport; pyximport.install()
# import cython_optimized

def loop_over_files(directory):
    # changing current working dir
    os.chdir(directory)
    
    # check if edited folder is present or not
    if os.path.isdir('edited') == False:
        os.mkdir('edited')
        
    ### Multi-Threading
        try:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                # mapping                   ->func         ->list of file paths
                results = executor.map(process_file, os.listdir(os.getcwd()))
                
                for filename, luminance in results:
                    file.append(filename)
                    brightness.append(luminance)    
                    
        except Exception as error:
            print('Exception Handling: Something wrong with {}'.format(error))
      
    #### Regular Excecution  
    # for filename in os.listdir(directory):
        
    #     if filename not in processed_files:
    #         processed_files.append(filename)                
    #         try:
    #             process_file(directory, filename)
                
    #         except:
    #             print('Something wrong with {}'.format(filename))
        
    #     else:
    #         continue
                
        

def process_file(filename):
    
    if filename != 'edited':
    
        print('Processing {}.'.format(filename))
        
        # initializing arrays
        Rarr = np.array([])
        Garr = np.array([])
        Barr = np.array([])
        # loading image
        im = Image.open(filename)
        # converting to RGB
        rgb_im = im.convert('RGB')

        # looping every pixel
        for w in range(0, rgb_im.width):
            for h in range(0, rgb_im.height):
                # getting RGB
                r, g, b = rgb_im.getpixel((w, h))
                # appending RGB in respective arrays
                Rarr = np.append(Rarr, r)
                Garr = np.append(Garr, g)
                Barr = np.append(Barr, b)
                
        # applying formula and averaging it
        luminance = np.average(np.sqrt( 0.299*Rarr**2 + 0.587*Garr**2 + 0.114*Barr**2 ))
        # modifing the image
        draw = ImageDraw.Draw(rgb_im)
        # defining text and it's coordinates
        draw.text((rgb_im.width //2, rgb_im.height // 4), "Luminance: {}".format(luminance))
        # saving new image in edited folder in current working dir
        new_file_name, ext = filename.split('.')
        edited_dir = os.path.join(os.getcwd(), 'edited')
        rgb_im.save(os.path.join(edited_dir, new_file_name + '(edited)' + '.' + ext))
        
        return [filename, luminance]

if __name__ == "__main__":
    
    
    data_frame = {}
    file = []
    brightness = []
    start = time.perf_counter()
    loop_over_files('G:\\path\\to\\test folder')
    # writing results to file
    data_frame = {'File Name': file,
                  'luminance': brightness}

    print('Generating .csv file')
    df = pd.DataFrame(data_frame)
    df.to_csv(os.path.join(os.getcwd(), 'luminance.csv'), index=False, header=True)
    end = time.perf_counter()
    
    print('With Muti-Processing took {0} minute(s) to process {1} images'.format((end - start)/60, len(data_frame['luminance'])))
    