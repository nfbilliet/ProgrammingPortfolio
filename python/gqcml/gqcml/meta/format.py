import json

def print_json(json_file, indent=4):
    """
    A function to pretty print a json file

    Arguments
        :json_file (str): A string containing the filepath to the json file (including filename)
    Returns
        :json_summary: Prints the contents of the meta dict in the json file
    """
    with open(json_file, "r") as js_file:
        js_str = js_file.loads(js_file.read())
        print(json_dumps(js_str, indent=indent, sort_keys=True))

def load_meta(json_file):
    """
    A function that reads a json file and returns the meta data as a dictionary

    Arguments
        :json_file (str): A string containing the filepath to the json file (including filename)
    Returns 
        :dict: The meta data dictionary
    """
    with open(json_file, "r") as js_file:
        return json.loads(js_file.read())

    
    
