# Universal Multi Importer

## Key Features

- With this addon, you can import multiple files of different formats from the same import dialog.
- (NEW) You can scan for files to import in a folder hierarchy.
- (NEW) (Blender 4.1+ only) Drag and drop any file to import them.
- The viewport stays interactive durring the import process, you can setup autosaves durring import. Everything is made to smooth the experience. 
- You can process the imported files with python command durring import that opens a lot of possibilities

## Changelog

### v2.0 : Import Folder Hierachy
You can select a folder and recursively scan for compatible formats in subfolders. Just Click on `File`>`Import`>`Universal Multi Importer Folder`, pick a root folder, adjust the `Recursion Depth` which indicate in how many subfolders you want to search for files, and clic on `Import ALL`

Then, you will see a prompt to select the compatible files that have been found within the scaned folders.

### v2.0 : Support for 4.0+

### v2.0 : Support for Appending or Linking Blend files

### v2.0 : Support for Importing Images and Movies

### v2.0 : Unified and Improved Import Window UX
![Import Dialog](https://i.postimg.cc/2j4G5hJN/import-dialog.png)

### v2.0 : Save and Load Import Presets

### v2.0 : Support for drag and drop import ( Blender 4.1+ only )
Drag and drop multiple files in 3D viewport to import all the files at once and place the imported objects in current collection.
Dropping in a collection of the outliner will place the imported objects in the collection under the cursor.

### v1.0 : Import any number of suported formats
Just click on `File`>`Import`>`Universal Multi Importer Files`, select the files and clic on `Import ALL`,  and the addon will take care of using the proper import command.

### v1.0 : Interactive Import
This addon also allows you to progressively import each files and see the viewport updating live, preventing the windows to freeze for many seconds. It is also designed to import big set of files with ease, making the import process more stable and predictable.

### v1.0 : Command Batcher
Just select any objects in your scene, then clic on `Object`>`Command Batcher` and you will be able to process all selected files with the python commands that you inputed.

Here is a full breakdown of this feature :

[![Full Breakdown](https://img.youtube.com/vi/Q87E13E2wBI/0.jpg)](https://youtu.be/Q87E13E2wBI?si=XPmF8cQbV3XN63LZ&t=485)



### v1.0 : Import and Batch
You can batch process imported files right after each import combining the capability of the Batch Importer and the Command Batcher

# Supported Formats
| Mesh Formats | Image Fommats | Video Formats | Animation Formats |
| ----------- | ----------- |  ----------- |   ----------- | 
| blend | jpg | mov  | bvh |
| obj | jpeg |  mp4 |   |
| fbx | gif |  mkv |   |
| glb | png |  mpg |   |
| gltf | tif |  mpeg |   |
| x3d | tiff |  dvd |   |
| wrl | bmp |  dvd |   |
| stl | cin |  vob |   |
| ply | dpx |  avi |   |
| abc | jp2 | dv  |   |
| dae | j2c | flv |   |
| svg | sig |  webm |   |
| usd | rgb |   |   |
| usda | bw |   |   |
| usdc | exr |   |   |
| usdz | hdr |   |   |

# Import Settings
| Settings | Description |
| ----------- | ----------- |
| **Import Folder** ||
| Recursion Depth | ( Folder mode only ) Determine how many subfolders will be scaned for compatible files to import. `0` will grab all files in current folder, `1` will grab everything in current folder and all dirrect subfolders, `2` will grab all files in the current folder, the dirrect subfolders and the subfolders of each direct subfolders etc ... |
| **File Count** ||
| Max Simultaneously | Determine the max number of file to import simultaneously. Each group of files to be imported simultaneously is called a "Batch". Importing multiple file at the same time allow to reduce the import time for small file, but can cause screen freezing or memory issue for biger file. To smartly ballance this, you can check `Max batch size` and `inimize batch number`|
| Max batch size | Determine the max batch file size to Import. If a file is a candidate to be include in the current batch, but his filesize would make the batch bigger than `Max batch size`, then the file will be included in the next batch |
| Minimize batch number | The importer will smartly group files in batches in order to be as close as possible to `Max batch size` for each batch without exceeding it and without exceeding `Max Import Simultaneously`|
|||
| **Options** ||
| Create collection per file | Each imported file will be placed in a new collection named like the file |
| Skip already imported files | if a file have already been imported, the import is skipped for this file, this option is only available if "`Create collection per file`" is Enable |
|||
| **Log Display** ||
| Show Log on 3D View | Display the Log and Progress of the Importing files in the 3D viewport while importing |
| Auto Hide Log When Finished | Automatic hide the log once the Import is Completed |
| Wait Before Hiding (s) | How much time to wait before Hiding the Log |
| Refresh viewport after each Import | Force refresh the viewport after each imported files. It imporoves interactivity, but will slow down the global import time |
|||
| **Backup** ||
| Save file after import | At the end of the imprort process, save the current file |
| Backup file after each import | A backup file is saved after each "`Backup Step`" file is imported |
| Backup Step | The number of file that is imported before saving a backup |
|||
| **Command Batcher** ||
|Commands | You create a macro like pyhon commands list. These commands will be executed in a row to all the imported objects after each importes batch.<br><br> It will process in that order :<br> - Import Batch 1<br>-  Run all batch commands in order<br>-  Repeat for next Batches...  <br><br>For exemple, if you add this command "`bpy.ops.transform.translate(value=(10, 0, 0))`", each imported file will be translated 10 meters away on positive X axis <br><br> Please note how the commands are written with `bpy.ops` and all parameters in parentheses <br> You can't create variable, for loops or if statements. Just commands that blender will execute|
| Ignore Command Batcher Errors | Batch Processing imported files can cause error. Enabling this will continue the import of the following files even if an error occurs. Otherwise, the import process will stop |
| Presets | You can save any list of commands from `batch process Imported files` to a preset that will be saved on disk. Here you can manage the presets: <br>- Creating preset<br>- Loading Preset <br>- Removing Preset<br>- Renaming Preset|
