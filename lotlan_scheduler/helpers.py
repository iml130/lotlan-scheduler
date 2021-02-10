""" This moudle contains helper functions """

from os import walk
from os.path import splitext, join

from lotlan_scheduler.defines import LOTLAN_FILE_ENDING

def string_is_int(string):
    """
        Returns true if a string can be cast to an int
        returns false otherwise
    """
    try:
        int(string)
        return True
    except ValueError:
        return False

def string_is_float(string):
    """
        Returns true if a string can be cast to an float
        returns false otherwise
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_instance(instances, instance_name):
    """ Get instance from instances with the given instance name """
    for instance in instances.values():
        if instance_name == instance.name:
            return instance
    return None

def get_transport_order_step(transport_order_steps, tos_name):
    """ Get tos from transport_order_steps with the given tos name """
    for tos in transport_order_steps.values():
        if tos_name == tos.name:
            return tos
    return None

def is_template_instance(instances, instance_name, template_name):
    """ Checks if an instance with instance_name is a template_name instance """
    instance = get_instance(instances, instance_name)
    if instance is not None and instance.template_name == template_name:
        return True
    return False

def get_template(templates, template_name):
    """
        Returns template if there is one with the given name
        returns None otherwise
     """
    for temp in templates.values():
        if template_name == temp.name:
            return temp
    return None

def has_instance_type(instance, type_name):
    """ "Checks if given instance has 'type_name' as type"""
    for keyval in instance.keyval.values():
        if keyval == type_name:
            return True
    return False

def get_lotlan_file_names(folder_path):
    """ Get all lotlan files from the given path """
    file_names = []

    for root, dirs, files in walk(folder_path):
        for file in files:
            full_path = join(root, file)
            ext = splitext(file)[1]

            if ext == LOTLAN_FILE_ENDING:
                file_names.append(full_path)

    return file_names

def is_value(x):
    return isinstance(x, (float, int, str))
