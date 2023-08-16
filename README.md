# Universal Multi Importer
### Import any number of suported formats
With this addon, you can import multiple files of different formats from the same import dialog. Just click on `File`>`Import`>`Universal Multi Importer`, select the files and clic on `Import ALL`,  and the addon will take care of using the proper import command.

### Progressive import
This addon also allows you to progressively import each files and see the viewport updating live, prevent the windows to freeze for many seconds. It is also designed to import big data sets with ease, making the import process more stable and predictable.

### Command Batcher
You can also batch process imported files right after import with custom macros

# Supported Formats
| Formats | 
| ----------- | 
| obj |
| fbx |
| glb |
| x3d |
| stl |
| ply |
| abc |
| dae |
| svg |
| usd |
| usda |
| usdc |
| usdz |

# Import Settings
| Settings | Description |
| ----------- | ----------- |
| **File Count** ||
| Max Import Simultaneously | Determine the max number of file to import simultaneously. Each group of files to be imported simultaneously is called a "Batch". Importing multiple file at the same time allow to reduce the import time for small file, but can cause screen freezing or memory issue for biger file. To smartly ballance this, you can check `Max batch size` and `inimize batch number`|
| Max batch size | Determine the max batch file size to Import. If a file is a candidate to be include in the current batch, but his filesize would make the batch bigger than `Max batch size`, then the file will be included in the next batch |
| Minimize batch number | The importer will smartly group files in batches in order to be as close as possible to `Max batch size` for each batch without exceeding it and without exceeding `Max Import Simultaneously`|
| **Settings** ||
| Ignore Post Process Errors | Batch Processing imported files can cause error. Enabling this will continue the import of the following files even if an error occurs. Otherwise, the import process will stop |
| Save file after import | At the end of the imprort process, save the current file |
| Create collection per file | Each imported file will be placed in a new collection named like the file |
| Skip already imported files | if a file have already been imported, the import is skipped for this file, this option is only available if "`Create collection per file`" is Enable |
| **Backup** ||
| Backup file after each import | A backup file is saved after each "`Backup Step`" file is imported |
| Backup Step | The number of file that is imported before saving a backup |
| **Command Batcher** ||
| Batch Process Imported Files | You create a macro like pyhon commands list. These commands will be executed in a row to all the imported objects after each importes batch.<br><br> It will process in that order :<br> - Import Batch 1<br>-  Run all batch commands in order<br>-  Repeat for next Batches...  <br><br>For exemple, if you add this command "`bpy.ops.transform.translate(value=(10, 0, 0))`", each imported file will be translated 10 meters away on positive X axis <br><br> Please note how the commands are written with `bpy.ops` and all parameters in parentheses <br> You can't create variable, for loops or if statements. Just commands that blender will execute|
| Batch Process Preset | You can save any list of commands from `batch process Imported files` to a preset that will be saved on disk. Here you can manage the presets: <br>- Creating preset<br>- Loading Preset <br>- Removing Preset<br>- Renaming Preset|

# Standalone Batch Processor
You can be use in a standalone mode. Just select any objects in your scene, then clic on `Object`>`Command Batcher` and you will be able to process all selected files with the selected commands