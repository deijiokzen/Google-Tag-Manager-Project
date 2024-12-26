# Google Tag Manager Automation Script

This script is designed to automate operations in Google Tag Manager (GTM). It interacts with GTM APIs to create and manage tags and triggers within a specified workspace. The following sections explain each function and its purpose:

## Imports and Initialization**

The script uses the google.oauth2.service\_account and googleapiclient.discovery libraries to authenticate and interact with Google APIs.

**from google.oauth2 import service\_account**

**from googleapiclient.discovery import build**

## Key Functions 

**1\. create\_tag\_and\_trigger**

*   **Purpose**: Creates a new trigger and a tag that fires on the trigger.
*   **Parameters**:
    *   service: Authenticated GTM API service object.
    *   account\_id, container\_id, workspace\_id: Identifiers for the GTM account, container, and workspace.
    *   tag\_name: Name for the new tag.
    *   trigger\_name: Name for the new trigger.
    *   trigger\_type (default: "pageview"): Type of the trigger.
*   **Process**:
    *   *   Checks if the trigger exists using get\_or\_create\_trigger.
        *   Deletes an existing tag with the same name, if any.
        *   Creates a new tag linked to the trigger.

**2\. get\_or\_create\_trigger**

*   **Purpose**: Ensures a trigger exists by creating it if it doesn't already exist.
*   **Parameters**: Similar to create\_tag\_and\_trigger.
*   **Process**:
    1.  Lists all triggers in the workspace.
    2.  Searches for a trigger by name using find\_trigger\_id.
    3.  Creates the trigger if not found.

**3\. find\_trigger\_id**

*   **Purpose**: Searches for a specific trigger by name.
*   **Parameters**:
    *   existing\_triggers: List of existing triggers.
    *   trigger\_name: Name of the trigger to find.
*   **Process**: Iterates through the triggers and returns the triggerId if a match is found.

**4\. create\_tag\_body**

*   **Purpose**: Constructs the body of a new HTML tag.
*   **Parameters**:
    *   tag\_name: Name of the tag.
    *   trigger\_id: ID of the trigger the tag will use.
*   **Process**: Returns a dictionary representing the tag's structure, including a popup HTML and JavaScript code.

**5\. get\_existing\_tag\_id**

*   **Purpose**: Searches for an existing tag by name.
*   **Parameters**:
    *   existing\_tags: List of existing tags.
    *   tag\_name: Name of the tag to find.
*   **Process**: Iterates through the tags and returns the tagId if a match is found.

**6\. update\_tag**

*   **Purpose**: Updates an existing tag.
*   **Parameters**: Similar to create\_tag\_and\_trigger, plus the tag\_id of the tag to update.

**7\. create\_tag**

*   **Purpose**: Creates a new tag, deleting an existing one with the same name if necessary.
*   **Parameters**: Similar to update\_tag.
*   **Process**:
    1.  Lists all tags.
    2.  Deletes an existing tag if a name match is found.
    3.  Creates the new tag.

**8\. delete\_tag**

*   **Purpose**: Deletes a tag by its ID.
*   **Parameters**:
    *   service: Authenticated GTM API service object.
    *   account\_id, container\_id, workspace\_id, tag\_id: Identifiers for the GTM tag.
*   **Process**: Deletes the tag using the API.

**9\. create\_ga4\_event\_tag**

*   **Purpose**: Creates a new GA4 event tag.
*   **Parameters**: Similar to create\_tag, plus measurement\_id for GA4 configuration.
*   **Process**: Constructs a GA4 tag body and creates it after deleting any existing tag with the same name.

**10\. get\_workspace\_id**

*   **Purpose**: Retrieves the ID of the first workspace in a GTM container.
*   **Parameters**: Similar to create\_tag\_and\_trigger.

**11\. create\_or\_update\_ga4\_config\_tag**

*   **Purpose**: Creates or updates a GA4 configuration tag.
*   **Parameters**: Similar to create\_ga4\_event\_tag, plus trigger\_ids for the tag's firing conditions.
*   **Process**: Deletes any existing tag with the same name and creates a new one.

## main Function

The main function orchestrates the script's execution:

1.  **Authentication**:
    *   Reads service account credentials.
    *   Initializes the GTM API service.
2.  **Retrieve Workspace ID**:
    *   Calls get\_workspace\_id to get the workspace ID.
3.  **Create Trigger and Tag**:
    *   Calls create\_tag\_and\_trigger to set up a new trigger and tag.
4.  **Combine Trigger IDs**:
    *   Combines default and newly created trigger IDs.
5.  **Create/Update Tags**:
    *   Calls create\_or\_update\_ga4\_config\_tag for GA4 configuration.
    *   Calls create\_ga4\_event\_tag for GA4 event tagging.

**Example Usage**

The script is executed by running the main function. Modify the main function's parameters to use specific GTM account, container, and workspace details.

main()