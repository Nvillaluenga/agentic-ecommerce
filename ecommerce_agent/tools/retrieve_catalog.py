from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

file_path = './catalog.json'
# If modifying these scopes, delete the file token.json.
# More specific scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = "13qKGV3bRdtH0pPl6DEO5lxyy8Uk2NzPAI6WaKm91_vA"
CATALOG_RANGE = "A1:G"


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


def retrieve_catalog_sheets() -> dict:
    """
    Retrieves elements from the catalog.

    Args:
    Returns:
        dict: dict containing the elements of the catalog
    """
    creds = Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES)
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=CATALOG_RANGE).execute()

        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        catalog = []
        keys = values[0]
        for row in values[1:]:
            {key: row[i] for (i, key) in enumerate(keys)}

        print(values)
        return catalog

    except HttpError as err:
        print(f"An error occurred: {err}")
        return {"message": "Error, couldn't retrieve catalog"}


if __name__ == "__main__":
    # catalog = retrieve_catalog_sheets()
    # print(catalog)
    pass
