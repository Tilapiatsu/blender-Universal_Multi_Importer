import addon_utils, bpy
from . import BVERSION
from .version import Version

class AddonVersion:
    '''
    This class helps to handle Addon versions, check if it needs update
    '''
    def __init__(self, addon_name, repo_id=0):
        self.addon_name = addon_name
        self.repo_if = repo_id

        if BVERSION >= 4.2:
            self.local_pkg, self.remote_pkg = self.get_packages(repo_id)

        else:
            self.local_pkg, self.remote_pkg = {}, {}

    def get_packages(self, repo_id=0):
        from bl_pkg import repo_cache_store_ensure
        repo_cache_store = repo_cache_store_ensure()
        packages = list(zip(repo_cache_store.pkg_manifest_from_local_ensure(error_fn=print),
                            repo_cache_store.pkg_manifest_from_remote_ensure(error_fn=print),
                            strict=True))

        local_pkg = packages[repo_id][0]
        remote_pkg = packages[repo_id][1]

        return local_pkg, remote_pkg

    @property
    def is_extension(self) -> bool:
        return self.addon_name.startswith('bl_ext')

    @property
    def pkg_name(self) -> str:
        return self.addon_name.split('.')[-1] if self.is_extension else self.addon_name

    @property
    def module(self):
        module = None
        modules = addon_utils.modules()
        for m in modules:
            if m.__name__ == self.addon_name:
                module = m
                break

        return module

    @property
    def version(self) -> Version:
        if self.module is None:
            return Version((0, 0, 0))

        return Version(self.module.bl_info['version']) if self.module.bl_info['version'] else Version((0, 0, 0))

    @property
    def local_version(self) -> Version:
        '''
        Returns the version of the addon installed localy
        '''
        if not self.is_extension:
            return self.version

        if self.pkg_name not in self.local_pkg.keys():
            return Version((0, 0, 0))

        return Version(self.local_pkg[self.pkg_name].version)

    @property
    def remote_version(self) -> Version:
        '''
        Returns the version of the addon in the repository
        '''
        if not self.is_extension:
            return Version((0, 0, 0))

        if self.pkg_name not in self.remote_pkg.keys():
            return Version((0, 0, 0))

        return Version(self.remote_pkg[self.pkg_name].version)

    @property
    def is_outdated(self) -> bool:
        '''
        An addon version is considered as outdated if the remote version is newer than the local version

        :returns: -> bool
        '''
        return self.remote_version > self.local_version

    @property
    def is_newer(self) -> bool:
        '''
        An addon version is considered newer if the remote version is older than the local version

        :returns: -> bool
        '''
        return self.remote_version < self.local_version

    @property
    def is_matching(self) -> bool:
        '''
        An addon version is considered as matching if the remote version and the local version are the same

        :returns: -> bool
        '''
        return self.remote_version == self.local_version

    @property
    def is_enable(self) -> bool:
        '''
        Return True if the addon is enable
        '''
        return self.addon_name in bpy.context.preferences.addons if self.addon_name else True

    @property
    def is_installed(self) -> bool:
        '''
        Return True if the addon is installed
        '''
        return self.is_enable or self.module is not None


    def __str__(self):
        return str(self.local_version)


if __name__ == '__main__':
    a = AddonVersion('bl_ext.blender_org.io_scene_max')
    print(a.module)
    print(a.pkg_name)
    print(a.local_version)
