import addon_utils
from bl_pkg import repo_cache_store_ensure
        
repo_cache_store = None
    
class AddonVersion:
    def __init__(self, addon_name, repo_id=0):
        self.addon_name = addon_name
        self.repo_if = repo_id

        self.local_pkg, self.remote_pkg = self.get_packages(repo_id)
    
    def get_packages(self, repo_id=0):
        global repo_cache_store

        
        if repo_cache_store is None:
            repo_cache_store = repo_cache_store_ensure()
        packages = list(zip( repo_cache_store.pkg_manifest_from_local_ensure(error_fn=print), repo_cache_store.pkg_manifest_from_remote_ensure(error_fn=print), strict=True))
        
        local_pkg = packages[repo_id][0]
        remote_pkg = packages[repo_id][1]
        
        return local_pkg, remote_pkg
        
    @property
    def is_extension(self):
        return self.addon_name.startswith('bl_ext')
    
    @property
    def pkg_name(self):
        return self.addon_name.split('.')[-1] if self.is_extension else self.addon_name
    
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
            return BlenderVersion((0,0,0))
        return BlenderVersion(self.module.bl_info['version'])
    
    @property
    def local_version(self):
        if not self.is_extension:
            return self.version
        assert self.addon_name in self.local_pkg.keys()
        return self.local_pkg[self.pkg_name].version
    
    @property
    def remote_version(self):
        if not self.is_extension:
            return BlenderVersion((0,0,0))
        
        assert self.addon_name in self.remote_pkg.keys()
        return self.remote_pkg[self.pkg_name].version
        
    

class BlenderVersion:
    def __init__(self, version:set):
        self._version = version
    
    @property
    def version(self):
        return self._version
    
    def __str__(self):
        return f'{self.version[0]}.{self.version[1]}.{self.version[2]}'
    
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
    print(a.module)
    print(a.pkg_name)
    print(a.local_version)

