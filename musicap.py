import boto3
import logging
import sys
import os
import glob
from os import walk
from botocore.exceptions import ClientError

#DEFINITIONS
#
s3_bucket = 'cs493-sdk-music'

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def uploadAlbum(dirPath, colName=""):
    print "uploading..."
    profile = sys.argv[1]
    session = boto3.Session(profile_name=profile)
    s3_client = session.client('s3')
    f = glob.glob(dirPath+"/*.mp3")
    try:
        for fi in f:
            #upload the file to dirpath
            fiparts = splitall(fi)
            obj = fiparts[len(fiparts) - 1]
            response = s3_client.upload_file(fi, s3_bucket, colName+'/'+obj)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def uploadArtist(dirPath, colName=""):
    print "uploading artist..."
    profile = sys.argv[1]
    session = boto3.Session(profile_name=profile)
    s3_client = session.client('s3')
    a = glob.glob(dirPath+"*")
    for fi in a:
        #find any directories and upload them as albums
        if(os.path.isdir(fi)):
            fpart = splitall(fi)
            f = fpart[len(fpart) - 1]
            f = f.replace('/', '')
            uploadAlbum(fi, colName + '/' + f)
        #find any songs and upload them as songs to /[artist]
        else :
            fpart = splitall(fi)
            f = fpart[len(fpart) - 1]
            f = f.replace('/', '')
            print "uploading song " + f + " under artist: " + colName
            uploadSong(fi, colName + '/' + f)

def uploadSong(songpath, colName=""):
    print "uploading song to " + colName + "..."
    profile = sys.argv[1]
    session = boto3.Session(profile_name=profile)
    s3_client = session.client('s3')
    try:
        fi = splitall(songpath)
        #if no collection is given
        if colName == "":
            #try to find collection from directory
            if len(fi) > 1:
                colName = fi[len(fi) - 2]
                response = s3_client.upload_file(songpath, s3_bucket, colName + '/' + fi[len(fi)-1])
            else:
                response = s3_client.upload_file(songpath, s3_bucket, fi[len(fi)-1])
        else:
            response = s3_client.upload_file(songpath, s3_bucket, colName)
            
    except ClientError as e:
        logging.error(e)
        return False
    return True

#
#

#check arguments
#        argv  0    1           2                   3                               4
#use: python s3.py <profile> <filepath to upload> <collection type: artist; album; song> <collection name>

if len(sys.argv) < 4:
    print "error: incorrect arguments"
    print  "use in the following order: \n <profile> \n<filepath to upload> \n<collection type: artist; album> \n<collection name>"
    sys.exit()

#set up s3 objects
filepath = sys.argv[2]
col_name = ""

if len(sys.argv) == 5:
    col_name = sys.argv[4]

#uploading an ALBUM
if sys.argv[3] == "album":
    #check to see if its actually a directory
    if os.path.isdir(filepath):
        print "album specified is a directory"
        uploadAlbum(filepath, col_name)
#uploading ARTIST
if sys.argv[3] == "artist":
    if os.path.isdir(filepath):
        print "artist specified is a directory"
        uploadArtist(filepath, col_name)

#uploading SONG
if sys.argv[3] == 'song':
    if os.path.isfile(filepath):
        print "song specified is a file"
        uploadSong(sys.argv[2], col_name)


#determine if file path is a directory

#isDirectory = os.path.isdir(sys.argv[2])
#if isDirectory:
#    print "directory specified"
    #permute contents of directory
    #upload directory as a folder in the s3bucket cs493-music-app/[dir]
#    f = glob.glob(sys.argv[2]+"*")
#    for path in f:
#        if os.path.isdir(path):
#            uploadAlbum(path, sys.argv[2])


