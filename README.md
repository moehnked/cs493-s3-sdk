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
