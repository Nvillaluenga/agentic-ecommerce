from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_core.tools.base import InjectedToolCallId
from langgraph.types import Command
from typing_extensions import Annotated

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


@tool
def retrieve_catalog_sheets(tool_call_id: Annotated[str, InjectedToolCallId]):
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
            catalog_entry = {key: row[i] for (i, key) in enumerate(keys)}
            catalog.append(catalog_entry)

        return Command(
            update={
                "catalog": catalog,
                # update the message history
                "messages": [
                    ToolMessage(
                        "Successfully retrieved the catalog", tool_call_id=tool_call_id
                    )
                ],
            }
        )

    except HttpError as err:
        print(f"An error occurred: {err}")
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        "Error, couldn't retrieve catalog", tool_call_id=tool_call_id
                    )
                ],
            }
        )


if __name__ == "__main__":
    # catalog = retrieve_catalog_sheets()
    # print(catalog)
    pass
