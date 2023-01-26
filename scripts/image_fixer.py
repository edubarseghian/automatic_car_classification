# This script will detect and also fix the problem of Premature Ending in images.
# This is caused when the image is corrupted in such a way that their hex code does not 
# end with the default D9. 
# 
# Opening the image with opencv and other image libraries is usually still possible, 
# but the images might produce errors during DL training or other tasks.

# Loading such an image with opencv and then saving it again can solve the problem. 
# You can manually inspect using a notepad, that the image's hex finishes with D9 
# after the script has finished.

import os, cv2, argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Train your model.")
    parser.add_argument(
        "data_folder",
        type=str,
        help=(
            "Full path to the directory having all the cars images. "
        ),
    )
    args = parser.parse_args()
    return args

# Directory to search for images


def detect_0kb(img_path,img_name):
    statfile = os.stat(img_path)
    filesize = statfile.st_size
    if filesize < 1024:
        os.remove(img_path)
    else:
        detect_and_fix(img_path, img_name)

  # manage here the 'faulty image' case

def detect_and_fix(img_path, img_name):
    # detect for premature ending
    try:
        with open(img_path, 'rb') as im:
            im.seek(-2, 2)

            # file.seek() takes two arguments file.seek(offset, from)
            # You need to define from where to you want offset the file. 
            # **from** takes one of following values 0,1,2 (0 = beginning, 1 = current, 2 = end)

            if im.read() != b'\xff\xd9':  # EOI	  0xFF, 0xD9		End Of Image
                # fix image
                img = cv2.imread(img_path)
                cv2.imwrite(img_path, img)
                print('FIXED corrupted image :', img_name)
    except(IOError, SyntaxError) as e:
        print(e)
        print("Unable to load/write Image : {} . Image might be destroyed".format(img_path))

# with open(img_path, 'rb') as im:
#     check_chars = im.read()[-2:]
#     if check_chars != b'\xff\xd9':
#         print('Not complete image')
#     else:
#         pass


def main(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        print('processing ',root)
        for file in files:
            if file.endswith('.jpg'):
                img_path = os.path.join(root, file)
                detect_0kb(img_path, file)  
                # detect_and_fix(img_path=img_path, img_name=path)              
    print("Process Finished")

if __name__ == "__main__":
    args = parse_args()
    main(args.data_folder)
    # main('.//data/')

#dir_path = r'../home/app/src/data/auto'