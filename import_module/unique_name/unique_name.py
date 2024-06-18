import bpy
import re
import uuid

def unique_name_clean_func(name):
    word_pattern = re.compile(r'(\.[0-9]{3})$', re.IGNORECASE)
    name_iter = word_pattern.finditer(name)
    name_iter_match = [w.group(1) for w in name_iter]

    if len(name_iter_match) and name_iter_match[0] is not None:
        return name.replace(name_iter_match[0], ''), True
    else:
        return name, False

class UniqueName():
    def __init__(self):
        self.element_correspondance = {}
    
    @property
    def uuid(self):
        return uuid.uuid1().hex

    def get_name_collisions_from_file(self, filepath, local_names):
        name_collision = {}
        # register name collision for objects in local_names
        with bpy.data.libraries.load(filepath, link=False) as (data_from, _):
            for name in data_from.objects:
                if name in local_names:
                    name_collision[name] = f'{name}_{self.uuid}'
            
        return name_collision
        
    def get_next_valid_name(self, name):
        return self.unique_name(-11, name, self.element_correspondance, clean_func=unique_name_clean_func, register=False)
    
    def get_unique_name(self, name):
        return name + '_' + self.uuid
    
    def register_element_correspondance(self, elem):
        if elem not in self.element_correspondance.keys():
            self.element_correspondance[elem] = elem.name

    # a modified version of bpy_extras.io_utils
    def unique_name(self, key, name, name_dict, name_max=-1, clean_func=None, sep=".", register=True):
        """
        Helper function for storing unique names which may have special characters
        stripped and restricted to a maximum length.

        :arg key: unique item this name belongs to, name_dict[key] will be reused
        when available.
        This can be the object, mesh, material, etc instance itself.
        :type key: any hashable object associated with the *name*.
        :arg name: The name used to create a unique value in *name_dict*.
        :type name: string
        :arg name_dict: This is used to cache namespace to ensure no collisions
        occur, this should be an empty dict initially and only modified by this
        function.
        :type name_dict: dict
        :arg clean_func: Function to call on *name* before creating a unique value.
        :type clean_func: function
        :arg sep: Separator to use when between the name and a number when a
        duplicate name is found.
        :type sep: string
        """
        name_new = name_dict.get(key)
        if name_new is None:
            count = 1
            has_number = False
            name_dict_values = list(name_dict.values())

            if clean_func is None:
                name_new = name_new_orig = name
            else:
                name_new, has_number = clean_func(name)
                name_new_orig = name_new
            if has_number or name_new in name_dict_values:
                if name_max == -1:
                    while name_new in name_dict_values:
                        name_new = "%s%s%03d" % (
                            name_new_orig,
                            sep,
                            count,
                        )
                        count += 1
                else:
                    name_new = name_new[:name_max]
                    while name_new in name_dict_values:
                        count_str = "%03d" % count
                        name_new = "%.*s%s%s" % (
                            name_max - (len(count_str) + 1),
                            name_new_orig,
                            sep,
                            count_str,
                        )
                        count += 1

            if register:
                name_dict[key] = name_new

        return name_new