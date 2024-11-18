import addon_utils
from bl_pkg import repo_cache_store_ensure

repo_cache_store = None
local_pkg = None
remote_pkg = None
        
def get_packages():
    global repo_cache_store
    global local_pkg
    global remote_pkg
    
    repo_cache_store = repo_cache_store_ensure()
    local_pkg  = [p for p in repo_cache_store.pkg_manifest_from_local_ensure(error_fn=print)]
    remote_pkg = [p for p in repo_cache_store.pkg_manifest_from_remote_ensure(error_fn=print)]
    
    return local_pkg, remote_pkg
    

class AddonVersion:
    def __init__(self, addon_name):
        self.addon_name = addon_name
        
        global repo_cache_store
        global local_pkg
        global remote_pkg
        
        if repo_cache_store is None or local_pkg is None or remote_pkg is None:
            get_packages()
        
        print(local_pkg)
        self.repo_cache_store = repo_cache_store_ensure()
        self.local_pkg = local_pkg[addon_name]
        self.remote_pkg = remote_pkg[addon_name]
        print(self.local_pkg)
#        for pkg_id, (item_local, item_remote) in pkg_manifest_zip_all_items(self.local_pkg, self.remote_pkg):
#            item = item_local or item_remote
#            print(item_local.keys())
        
    @property
    def is_extension(self):
        return self.addon_name.startswith('bl_ext')
    
    @property
    def module(self):
        module = None
        for m in addon_utils.modules():
            if m.__name__ == self.addon_name:
                module = m
                break
        return module
    
    @property
    def version(self):
        if self.module is None:
            return (0,0,0)
        return BlenderVersion(self.module.bl_info['version'])
    

class BlenderVersion:
    def __init__(self, version:set):
        self._version = version
    
    @property
    def version(self):
        return self._version
    
    def __repr__(self):
        return self._version
    
    def __eq__(self, other):
        if self.version[0] == other.version[0] and self.version[1] == other.version[1] and self.version[2] == other.version[2]:
            return True
        
        return False
    
    def __gt__(self, other):
        if self.version[0] > other.version[0] and self.version[1] > other.version[1] and self.version[2] > other.version[2]:
            return True
        
        return False
    
    def __lt__(self, other):
        if self.version[0] < other.version[0] and self.version[1] < other.version[1] and self.version[2] < other.version[2]:
            return True
        
        return False

if __name__ == '__main__'  :
    a = AddonVersion('bl_ext.blender_org.io_scene_max')
    print(a)

