import glob
import os
import argparse
import subprocess

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--data_folder', required=True, action='store', default='.', help="folder")
    parser.add_argument('-n', '--name', required=True, action='store', default='.', help="Either train or test")
    
    return parser.parse_args()

def create_file(data_folder, name):

    #DIR = '/home/serge/repos/yolov4_darknet/build/darknet/x64/data/obj/' 
    video_files = glob.glob('{}/*.MTS'.format(data_folder.rstrip('/')))
    video_files.sort()

    with open('concat_list.txt', 'w') as list_file:
        for i, vid in enumerate(video_files):
            mp4 = vid.replace('.MTS', '.mp4')
            list_file.write(f"file '{mp4}'\n")

            cmd = f'ffmpeg -i {vid} -vf yadif=1 -acodec ac3 -ab 192k -vcodec mpeg4 -f mp4 -y -qscale 0 {mp4}'
            subprocess.run(cmd.split())
            print(cmd)
            
    #run concat command.
    cmd = f'ffmpeg -f concat -safe 0 -i concat_list.txt -c copy {name}'
    print(cmd)
    subprocess.run(cmd.split())

def main():
    args = get_args()
    create_file(args.data_folder, args.name)

if __name__ == '__main__':
    main()

