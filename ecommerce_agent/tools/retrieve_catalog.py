file_path = './catalog.json'

def retrieve_catalog() -> dict:
    """
    Retrieves elements from the catalog.

    Args:
    Returns:
        dict: dict containing the elements of the catalog
    """
    # Load the JSON file into a string
    with open(file_path, 'r') as file:
        json_string = file.read()
    return {"catalog": json_string}