# Universal Multi Importer
[![Teaser](https://img.youtube.com/vi/pFKmG-QfxGg/0.jpg)](https://youtu.be/pFKmG-QfxGg)


<span style="font-size:3em;">[Download on Extension Platform](https://extensions.blender.org/add-ons/universal-multi-importer/)</span>


## Key Features

- With this addon, you can import multiple files of different formats from the same import dialog.
- You can scan for files to import in a folder hierarchy.
- (Blender 4.1+ only) Drag and drop any file to import them.
- The viewport stays interactive during the import process, you can setup autosaves during import. Everything is made to smooth the experience.
- You can process the imported files with python command during import that opens a lot of possibilities

## Credits
This addon is adding batch import features to existing importers for blender. The credits for the importers goes to each importer addon developers and to the blender team themself. You can click on the link below to know more about the author of each importers.

- [Web3D X3D/VRML2](https://projects.blender.org/extensions/io_scene_x3d) by Bujus Krachus
- [Autodesk 3D Studio](https://projects.blender.org/extensions/io_scene_3ds) by Bob Holcomb, Campbell Barton, Sebastian Schrand, Sebastian Sille
- [Autodesk MAX Importer](https://github.com/nrgsille76/io_scene_max) by Sebastian Sille
- [Atomic Blender PDB/XYZ](https://projects.blender.org/extensions/io_mesh_atomic) by Clemens Barth
- [AutoCAD DXF](https://projects.blender.org/extensions/io_import_dxf) by Lukas Treyer, Manfred Moitzi, Vladimir Elistratov, Bastien Montagne, Remigiusz Fiedler
- [Blender Embroidery](https://github.com/javl/blender-embroidery) by Jasper van Loenen

# Supported Formats
| Mesh Formats | Image Formats | Video Formats | Animation Formats | Embroidery Formats[:link:](https://github.com/javl/blender-embroidery) | Audio Formats | Volume Formats |
| -----------  | -----------   |  -----------  |   -----------     |   -----------      | -----------  | -----------  |
| blend        | jpg           |  mov          | bvh               |  pes               | wav          | vdb
| obj          | jpeg          |  mp4          |                   |  dst               | flac         |              |
| fbx          | gif           |  mkv          |                   |  exp               | mp2          |              |
| glb          | png           |  mpg          |                   |  jef               | mp3          |              |
| gltf         | tif           |  mpeg         |                   |  pec               | aac          |              |
| x3d[:link:](https://projects.blender.org/extensions/io_scene_x3d)| tiff|  dvd         |                   |  jpx               | ogg        |              |
| wrl          | bmp           |  dvd          |                   |  phc               | pcm          |              |
| stl          | cin           |  vob          |                   |  vp3               | opus         |              |
| ply          | dpx           |  avi          |                   |  10o               | l16          |              |
| abc          | jp2           |  dv           |                   |  zxy               | aiff         |              |
| dae          | j2c           |  flv          |                   |  bro               | au           |              |
| svg          | sig           |  webm         |                   |  dat               |              |              |
| usd          | rgb           |               |                   |  dsb               |              |              |
| usda         | bw            |               |                   |  dsz               |              |              |
| usdc         | exr           |               |                   |  emd               |              |              |
| usdz         | hdr           |               |                   |  exy               |              |              |
| max[:link:](https://github.com/nrgsille76/io_scene_max) |webp||       |  fxy              |              |              |
| pdb[:link:](https://projects.blender.org/extensions/io_mesh_atomic) ||||  gcode       |              |              |
| xyz[:link:](https://projects.blender.org/extensions/io_mesh_atomic) ||||  hus         |              |              |
| dxf[:link:](https://projects.blender.org/extensions/io_import_dxf) ||||  inb          |              |              |
| 3ds[:link:](https://projects.blender.org/extensions/io_scene_3ds)  ||||  new          |              |              |
|              |               |               |                   |  pcd               |              |              |
|              |               |               |                   |  pcm               |              |              |
|              |               |               |                   |  pcq               |              |              |
|              |               |               |                   |  pcs               |              |              |
|              |               |               |                   |  phb               |              |              |
|              |               |               |                   |  sew               |              |              |
|              |               |               |                   |  shv               |              |              |
|              |               |               |                   |  stc               |              |              |
|              |               |               |                   |  stx               |              |              |
|              |               |               |                   |  tap               |              |              |
|              |               |               |                   |  tbf               |              |              |
|              |               |               |                   |  xxx               |              |              |
|              |               |               |                   |  zhs               |              |              |

# Import Settings
## Import Folder
|  |  |
| ----------- | ----------- |
| Recursion Depth | ( Folder mode only ) Determine how many subfolders will be scanned for compatible files to import. `0` will grab all files in current folder, `1` will grab everything in current folder and all direct subfolders, `2` will grab all files in the current folder, the direct subfolders and the subfolders of each direct subfolders etc ... |
## File Count
|  |  |
| ----------- | ----------- |
| Max Simultaneously | Determine the max number of file to import simultaneously. Each group of files to be imported simultaneously is called a "Batch". Importing multiple file at the same time allow to reduce the import time for small file, but can cause screen freezing or memory issue for bigger file. To smartly balance this, you can check `Max batch size` and `Minimize batch number`|
| Max batch size | Determine the max batch file size to Import. If a file is a candidate to be include in the current batch, but his file size would make the batch bigger than `Max batch size`, then the file will be included in the next batch |
| Minimize batch number | The importer will smartly group files in batches in order to be as close as possible to `Max batch size` for each batch without exceeding it and without exceeding `Max Import Simultaneously`|
| Refresh Viewport After time (s) | The viewport will refresh after the X seconds. It help to control viewport interactivity. A value of 0 will disable it, and the viewport will refresh after each batch`|
## Options
|  |  |
| ----------- | ----------- |
| Recreate folder structure as collections | ( `Import Folder` mode only ) Recreate the folder structure from the hard drive into blender collections |
| Create collection per file | Each imported file will be placed in a new collection named like the file |
| Skip already imported files | if a file have already been imported, the import is skipped for this file, this option is only available if "`Create collection per file`" is Enable |
|||
## Log Display
|  |  |
| ----------- | ----------- |
| Show Log on 3D View | Display the Log and Progress of the Importing files in the 3D viewport while importing |
| Auto Hide Log When Finished | Automatic hide the log once the Import is Completed |
| Wait Before Hiding (s) | How much time to wait before Hiding the Log |
| Refresh viewport after each Import | Force refresh the viewport after each imported files. It improves interactivity, but will slow down the global import time |
## Backup
|  |  |
| ----------- | ----------- |
| Save file after import | At the end of the import process, save the current file |
| Backup file after each import | A backup file is saved after each "`Backup Step`" file is imported |
| Backup Step | The number of file that is imported before saving a backup |
## Command Batcher

The command Batcher allows you to run python commands while importing files or at anytime in blender by running `Object`>`Command Batcher`
![UMI-Command-Batcher-Improvements.png](https://i.postimg.cc/rs81wdqF/UMI-Command-Batcher-Improvements.png)
These commands will be executed in a row to all the imported objects after each imported batch.

It will process in that order :
- Execute all commands in `Pre-Process` list
- Import Batch 1
- Run all Commands in `Each Element` list
- Repeat for next Batches until the last bacth...
- Execute all commands in `Post-Process` list

For example, if you add this command "`bpy.ops.transform.translate(value=(10, 0, 0))`", each imported file will be translated 10 meters away on positive X axis

Please note how the commands are written with `bpy.ops` and all parameters in parentheses

/!\ ***You can't create variable, for loops or if statements. Just commands that blender will execute***


You can also insert variables in the command that will be replaced by the proper value at runtime.

You can choose if the command has to be executed for a specific datatype or many by checking the proper data type in the `applies to` panel.


![UMI-Add-command.png](https://i.postimg.cc/zXQBLsxC/Blender-Add-Command.png)
|  Variable |  Description  |
| ----------- | ----------- |
| <ITEM_NAME>           | (str) Name of the processed Item. |
| <GLOBAL_ITEM_INDEX>   | (int) The global index of processed intm |
| <DATA_ITEM_INDEX>     | (int) The index of the item per data type. Each Data type have it's own index, which help with processing item per type |
| <ITEM_DATA>           | (str) A string when evaluated refers to the data of the processed item. eg: `bpy.data.objects['table']` or `bpy.data.sounds['beep']` |
| \<OBJECTS>             | (list) Returns a list of objects using the given data. The Command will be executed for each objects in the list |
| <OBJECT_BBOX>         | (vector3) Works for object data type only. Returns the bounding box size of the processed object. If you use this variable on other datatype, it will return `(0, 0, 0)` |
| \<TIMEF>               | (float) Returns a value that represent the current time |
| \<TIMESTR>             | (str) Returns a readable sentence the read the current date and time. eg : `Mon May 12 23:04:03 2025`|
| \<BVERSION>            | (str) Returns the current blender version. eg: `4.4.0`|

| Other Settings |  |
| ----------- | ----------- |
| Ignore Command Batcher Errors | Batch Processing imported files can cause error. Enabling this will continue the import of the following files even if an error occurs. Otherwise, the import process will stop |
| Presets | You can save any list of commands from `batch process Imported files` to a preset that will be saved on disk. Here you can manage the presets: <br>- Creating preset<br>- Loading Preset <br>- Removing Preset<br>- Renaming Preset|




# Changelog
### v2.3.1 : Add Support VDB Format
### v2.3.0 : Add Support for Blender 4.5.0
### v2.3.0 : Command Batcher can execute commands for a specific or multiple datatypes
![UMI-Add-command.png](https://i.postimg.cc/y8xhWMZY/UMI-add-command.png)
### v2.3.0 : Command Batcher can use predefined variable in order to access imported data
### v2.2.2 : Bump Compatible version of GLTF addon for blender 4.4.1 support
### v2.2.2 : Add Setting to setup default window width in the addon preference
### v2.2.1 : Add feature to recreate folder structure as collections in `Import Folder` mode
### v2.2.0 : Support for Blender 4.4.0
### v2.2.0 : Support for webp and audio formats
### v2.2.0 : Command Batcher now have 3 lists :
- Pre-process : which will be executed ONCE at the begining
- Each Elements : which will be exectute for each Objects / Imported files
- Post-Process : which will be exectued ONCE at the end of the process
### v2.2.0 : Command Batcher can now Search for valid operators. Each operators can be enabled or disabled
![UMI-Command-Batcher-Improvements.png](https://i.postimg.cc/rs81wdqF/UMI-Command-Batcher-Improvements.png)
### v2.2.0 : Allow to hide or resize import settings for more flexibility
### v2.1.8 : Better expose addon version inconsistency to the user, and propose solution to adress them
![UMI-Addon-Version-Missmatch.png](https://i.postimg.cc/PJp1Pncc/UMI-Addon-Version-Missmatch.png)
### v2.1.8 : Rewrite format definition to simplify maintainance, and extending support to new formats
### v2.1.8 : Extend support from Blender 3.0 to 4.3
### v2.1.7 : Add support for 3DS files
### v2.1.6 : Support for Blender 4.3
### v2.1.6 : Use Collapsable Panels for import settings
### v2.1.6 : Support for new formats : Autodesk 3Dsmax, Embroidery files, AutoCAD DXF, Atomic PBD and XYZ
### v2.1.6 : Add Timer for refresh viewport to better control its interactivity
### v2.1.5 : Add Addon Dependency Checker to easily fix any missing import formats
[![Addon-Dependency-Checker-03.webp](https://i.postimg.cc/qMzp19SL/Addon-Dependency-Checker-03.webp)](https://postimg.cc/kBPr4hn6)
### v2.1.0 : Support for Blender 4.2 and the extension platform
### v2.1.0 : Add Settings to choose text colors in the addon preferences
![Theme Settings](https://i.postimg.cc/Y9mdfBgG/blender-7qd3o6bgs-W.png)
### v2.1.0 : Bug Fixes
----
### v2.0 : Overview
[![Teaser](https://img.youtube.com/vi/Ciz48xzeO-0/0.jpg)](https://youtu.be/Ciz48xzeO-0)
[![Feature Breackdown](https://img.youtube.com/vi/gn0fUx0Idjc/0.jpg)](https://youtu.be/gn0fUx0Idjc)

### v2.0 : Import Folder Hierarchy
You can select a folder and recursively scan for compatible formats in subfolders. Just Click on `File`>`Import`>`Universal Multi Importer Folder`, pick a root folder, adjust the `Recursion Depth` which indicate in how many subfolders you want to search for files, and click on `Import ALL`

Then, you will see a prompt to select the compatible files that have been found within the scanned folders.

### v2.0 : Support for Appending or Linking Blend files

### v2.0 : Support for Importing Images, Movies and BVH Files

### v2.0 : Unified and Improved Import Window UX
![Import Dialog](https://i.postimg.cc/2j4G5hJN/import-dialog.png)

### v2.0 : Save and Load Import Presets

### v2.0 : Support for 4.0+

### v2.0 : Support for drag and drop import ( Blender 4.1+ only )
Drag and drop multiple files in 3D viewport to import all the files at once and place the imported objects in current collection.
Dropping in a collection of the outliner will place the imported objects in the collection under the cursor.

-----
### v1.0 : Import any number of supported formats
Just click on `File`>`Import`>`Universal Multi Importer Files`, select the files and click on `Import ALL`,  and the addon will take care of using the proper import command.

### v1.0 : Interactive Import
This addon also allows you to progressively import each files and see the viewport updating live, preventing the windows to freeze for many seconds. It is also designed to import big set of files with ease, making the import process more stable and predictable.

### v1.0 : Command Batcher
Just select any objects in your scene, then click on `Object`>`Command Batcher` and you will be able to process all selected files with the python commands that you’ve entered.

Here is a full breakdown of this feature :

[![Full Breakdown](https://img.youtube.com/vi/Q87E13E2wBI/0.jpg)](https://youtu.be/Q87E13E2wBI?si=XPmF8cQbV3XN63LZ&t=485)


### v1.0 : Import and Batch
You can batch process imported files right after each import combining the capability of the Batch Importer and the Command Batcher
