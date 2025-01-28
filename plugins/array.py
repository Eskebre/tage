from tage.api import api

def load(tage):
    print("loaded")
    return True

#name = "open"

def split_char(tage, name, data: str, *args, **kargs):
        api.set_variable(tage, name, len(data), False)
        for i, char in enumerate(data):
             api.set_variable(tage, f"{name}[{i}]", char, False)

def split_string(tage, name, data: str, seperator:str = " " , *args, **kargs):
    split = data.split(seperator)
    api.set_variable(tage, name, len(split), False)
    for i, char in enumerate(split):
        api.set_variable(tage, f"{name}[{i}]", char, False)

def iterate(tage, name, *args, **kargs):
    iteration = int(api.get_variable(tage, f"{name}.iteration"))
    parent = api.get_variable(tage, f"{name}.parent")
    parent_length = int(api.get_variable(tage, f"{parent}"))
    if iteration >= (parent_length-1):
        api.set_variable(tage, f"{name}.is_complete", 1)
        return
    iteration += 1
    api.set_variable(tage, name, api.get_variable(tage, f'{parent}[{iteration}]'), False)
    api.set_variable(tage, f"{name}.iteration", iteration)

def create_iterable(tage, name, iterable_name, *args, **kargs):
    api.set_variable(tage, f"{iterable_name}.parent", name, False)
    api.set_variable(tage, iterable_name, api.get_variable(tage, f"{name}[0]"), False)
    api.set_variable(tage, f"{iterable_name}.iteration", 0, False)
    api.set_variable(tage, f"{iterable_name}.is_complete", 0, False)

def array_get(tage, name, location, set_name, *args, **kargs):
     data = api.get_variable(tage,f"{name}[{location}]")
     api.set_variable(tage, set_name, data, False)
    

def get_command():
    return {
         "array.split_char": split_char,
         "array.split": split_string,
         "array.iterate": iterate,
         "array.iterate.create": create_iterable,
         "array.get": array_get
         }
