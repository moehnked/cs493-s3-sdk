# cs493-s3-sdk

## How To
the program can be executed by etering the command
```
python musicap.py
```
and providing the necessary arguments in the following order
```
[profile] - the name of the profile defined in your .aws/config file
[filepath] - the path to the file or directory you want to upload. files must end in .mp3
[type of upload] - can be 'album', 'artist' or 'song'
[folder path] - the folder you would like to place the upload within
```
## Examples

uploading a song
```
python musicap.py s3advisor test.mp3 song
```

uploading a song from an album by an artist
```
python musicap.py s3advisor test.mp3 song artist/album
```

uploading an album
```
python musicap.py s3advisor good-ol-boys album good\ ol\ boys
```

uploading an album by an artist
```
python musicap.py s3advisor good-ol-boys album artist/good\ ol\ boys
```

uploading an artist
```
python musicap.py s3advisor the\ blowouts artist the\ blowouts
```

### semantics:
the folder path can be used to rename a song upload as well. if left blank, the
app will default to using the filename for the s3 object name, and preserve the
relative file structure as well. so from the working directory, a file like
```test.mp3```
would get uploaded into the music bucket as test.mp3
but if the song uploaded was within a sub directory, such as
``` ./subdir/foo.mp3```
the upload would create a folder "subdir" in the root of the music bucket and within that folder place foo.mp3

this is the behavior if no folder path argument is given

if a folder path argument is provided, the folder structures can be created on the fly. the folder should end with an object name for the file, such that a folder does not get replaced with a new object.
