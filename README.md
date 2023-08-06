# Universal Multi Importer
With this addon, you can now import multiple files of different formats from the same import dialog. Just select the files and clic on "Import ALL",  and the addon will take care of using the proper import command.

# Supported Formats
| Formats | 
| ----------- | 
| obj |
| fbx |
| glt |
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
| Create collection per file | Each imported file will be placed in a new collection named like the file |
| Skip already imported files | if a file have already been imported, the import is skipped for this file, this option is only available if "`Create collection per file`" is Enable |
| Backup file after each import | A backup file is saved after each "`Backup Step`" file is imported |
| Backup Step | The number of file that is imported before saving a backup |
| Save file after import | At the end of the imprort process, save the current file |
| Ignore Post Process Errors | Batch Processing imported files can cause error. Enabling this will continue the import of the following files even if an error occurs. Otherwise, the import process will stop |
| Batch Process Imported Files | You create a Macro like pyhon commands list. These commands will be applied in a row to all the imported objects after each file import.<br><br> It will process in that order :<br> - Import File 1<br>-  Run all batch commands in order<br>-  Repeat for next Files...  <br><br>For exemple, if you add this command "`bpy.ops.transform.translate(value=(10, 0, 0))`", each imported file will be translated 10 meters away on positive X axis |
