import os
from pydub import AudioSegment
import requests
import boto3
from botocore.client import Config
import json
from dotenv import load_dotenv

class SongSnip:

    def __init(self):

        self.Name = None
        self.Artist = None
        self.Spotify_Link = None
        self.local_storage = None
        self.external_storage = None
        self.time_code = None

    def print(self):
        print("SONG:", self.Name, " : ", self.Artist, self.time_code)

    def return_print(self):
        # print("SONG:", self.Name, " : ", self.Artist, self.time_code, "\n", self.Spotify_Link, "\n")
        return "SONG:" + self.Name + " : " +  self.Artist + self.time_code + "\n" + self.Spotify_Link + " \n"

def main(sc_url = None):
    sc_url = 'https://soundcloud.com/egroove/egnu060-felipe-rivelino'
    song_save_location = 'C:\\Users\\jesse\\Desktop\\Samples\\Full_Song'

    os_command = 'scdl -l '+ sc_url + ' --path ' + song_save_location

    #TODO Save Song Name

    if (sc_url == None):
        print("ERROR: No Soundcloud Link")
        return
    else:
        os.system(os_command)

def download_sc_song():
    sc_url = 'https://soundcloud.com/egroove/egnu060-felipe-rivelino'
    song_save_location = 'C:\\Users\\jesse\\Desktop\\Samples\\Full_Song'

    os_command = 'scdl -l '+ sc_url + ' --path ' + song_save_location

    #TODO Save Song Name

    if (sc_url == None):
        print("ERROR: No Soundcloud Link")
        return
    else:
        os.system(os_command)


def slice_song(id): # Get ID
    mp3_song = AudioSegment.from_file(id)

    second = 1000
    halfmin = 30000
    minute = 60000

    print(len(mp3_song))
    length = len(mp3_song)
    name = 'f'
    save_path = 'Full_Song/Felip_Rivellino/'

    if length < 10*minute:
        time_slice = halfmin
    elif length > 25*minute:
        time_slice = 3*minute
    else:
        time_slice = minute

    remainder_time = length % time_slice

    # TODO deal with time that doesn't divide nicely
    for i in range(0, int(length/time_slice)):
        snip_name = save_path+name+str(i) + '.mp3'
        snip_start = i*time_slice
        snip_end = (i+1)*time_slice
        print("NEW SNIP: ", snip_start, ":", snip_end, snip_name)
        new_snip = mp3_song[snip_start:snip_end]
        new_snip.export(snip_name, format='mp3')

    if remainder_time > 0:
        snip_name = save_path+name+str(int((length/time_slice)))+'.mp3'
        snip_start = time_slice * int(length/time_slice)
        snip_end = snip_start+remainder_time
        print("Remainder_Snip : ", snip_start, ":", snip_end, snip_name)
        new_snip = mp3_song[snip_start:snip_end]
        new_snip.export(snip_name, format='mp3')

def search_song(link_list):

    print("Starting Song Search")
    song_list = []

    api_token = os.getenv("AUDD_KEY")

    for n in link_list:

        song = SongSnip()

        data = {
            'url': n,
            'return': 'timecode,spotify',
            'api_token': api_token
        }

        result = requests.post('https://api.audd.io', data=data)

        d = json.loads(result.text)
        print(d['status'])
        print(d)

        if d['status'] == 'success' and d['result'] != None:

            try:
                song.Name = d['result']['title']
            except:
                song.Name = "SONG NAME FAILED"

            try:
                song.Artist = d['result']['artist']

            except:
                song.Artist = "ARTIST NAME FAILED"

            try:
                song.Spotify_Link = d['result']['spotify']['external_urls']['spotify']

            except:
                song.Spotify_Link = "SPOTIFY LINK FAILED"

            try:
                song.time_code = d['result']['timecode']

            except:
                song.time_code = "TIME CODE FAILED"

        else:
            song.Name = "ERROR"
            song.Artist = "ERROR"
            song.Spotify_Link = "ERROR"
            song.time_code = "ERROR"

        song_list.append(song)

    return song_list


def get_all_files_in_folder(folder_name):
    file_list = []

    try:
        for filename in os.listdir(folder_name):
            file_list.append(folder_name+filename)

        return file_list if file_list else None

    except OSError as e:
        print("FOLDER NOT FOUND", e)
        return None


def digital_ocean_upload():

    ACCESS_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")

    upload_target = 'Full_Song/Felip_Rivellino/'
    get_all_files_in_folder(upload_target)

    file_targets = get_all_files_in_folder(upload_target)
    file_targets2 = get_all_files_in_folder("asdf/")

    print(file_targets)
    # print(file_targets2)

    if file_targets:
        print(file_targets)

        session = boto3.session.Session()

        client = session.client('s3', region_name='sfo2', endpoint_url='https://msk.sfo2.digitaloceanspaces.com/',
                             aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

        for file in file_targets:
            print("UPLOADING: ", file)
            client.upload_file(file, 'Audio-Hosting', file)

def do_get_share_links():

    ACCESS_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")

    session = boto3.session.Session()

    client = session.client('s3', region_name='sfo2', endpoint_url='https://msk.sfo2.digitaloceanspaces.com/',
                            aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    url_list = []

    for i in range(0, 27):
        name = 'Full_Song/Felip_Rivellino/f' + str(i) + '.mp3'
        url = client.generate_presigned_url(ClientMethod='get_object',
                                        Params={'Bucket':'Audio-Hosting',
                                                'Key': name},
                                        ExpiresIn=300)

        url_list.append(url)

    return url_list

def file_write(songs):

    file1 = open("Felip_test.txt", "w")
    for i in songs:
        print(i.return_print())
        file1.write(i.return_print())

def test_keys():

    key1 = os.getenv("AUDD_KEY")
    key2 = os.getenv("API_KEY")
    key3 = os.getenv("SECRET_KEY")
    print(key1, key2, key3)

if __name__ == '__main__':
    load_dotenv()
    # Download SC Song and Save to location

    # Slice Song

    # download_sc_song()
    # main()
    # slice_song("Full_Song/EGNU.060 Felip Rivellino.mp3")
    # search_song()
    # digital_ocean_upload()
    # urls = do_get_share_links()
    #
    # songs = search_song(urls)
    #
    # file_write(songs)

    test_keys()