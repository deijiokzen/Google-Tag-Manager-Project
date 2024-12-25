from google.oauth2 import service_account
from googleapiclient.discovery import build

def create_tag_and_trigger(service, account_id, container_id, workspace_id, tag_name, trigger_name, trigger_type="pageview"):
    trigger_name_with_suffix = f"{trigger_name} Pop-up Trigger"
    trigger_id = get_or_create_trigger(service, account_id, container_id, workspace_id, trigger_name_with_suffix, trigger_type)
    full_tag_name = f'{tag_name} Pop-up Tag'
    tag_body = create_tag_body(full_tag_name, trigger_id)

    existing_tags = service.accounts().containers().workspaces().tags().list(
        parent=f'accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}'
    ).execute()

    existing_tag_id = get_existing_tag_id(existing_tags, full_tag_name)

    if existing_tag_id:
        delete_tag(service, account_id, container_id, workspace_id, existing_tag_id)

    create_tag(service, account_id, container_id, workspace_id, tag_body)

    return trigger_id

def get_or_create_trigger(service, account_id, container_id, workspace_id, trigger_name, trigger_type):
    existing_triggers = service.accounts().containers().workspaces().triggers().list(
        parent=f'accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}'
    ).execute()

    trigger_id = find_trigger_id(existing_triggers, trigger_name)

    if trigger_id is None:
        trigger_body = {
            "name": trigger_name,
            "type": trigger_type
        }
        response = service.accounts().containers().workspaces().triggers().create(
            parent=f'accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}',
            body=trigger_body
        ).execute()
        trigger_id = response['triggerId']

    return trigger_id

def find_trigger_id(existing_triggers, trigger_name):
    if 'trigger' in existing_triggers:
        for trigger in existing_triggers['trigger']:
            if trigger['name'] == trigger_name:
                return trigger['triggerId']
    return None

def create_tag_body(tag_name, trigger_id):
    return {
        'name': tag_name,
        'type': 'html',
        'parameter': [
            {
                'type': 'TEMPLATE',
                'key': 'html',
                'value': """<div id="myPopup" style="display:none;">
                            <h2>Welcome to Our Website!</h2>
                            <p>Subscribe to our newsletter for updates.</p>
                            </div>
                            <script>
                            setTimeout(function() {
                                document.getElementById("myPopup").style.display = "block";
                            }, 5000); // Show after 5 seconds
                            </script>"""
            }
        ],
        'firingTriggerId': [trigger_id]
    }

def get_existing_tag_id(existing_tags, tag_name):
    if 'tag' in existing_tags:
        for tag in existing_tags['tag']:
            if tag['name'] == tag_name:
                return tag['tagId']
    return None

def update_tag(service, account_id, container_id, workspace_id, tag_id, tag_body):
    service.accounts().containers().workspaces().tags().update(
        path=f'accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}/tags/{tag_id}',
        body=tag_body
    ).execute()

def create_tag(service, account_id, container_id, workspace_id, tag_body):
    # First, list all tags and check if any with the same name exist
    existing_tags = service.accounts().containers().workspaces().tags().list(
        parent=f'accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}'
    ).execute()

    tag_name = tag_body['name']
    existing_tag_id = get_existing_tag_id(existing_tags, tag_name)

    if existing_tag_id:
        print(f"Tag with name '{tag_name}' already exists. Deleting it.")
        delete_tag(service, account_id, container_id, workspace_id, existing_tag_id)

    print(f"Creating new tag: {tag_name}")
    service.accounts().containers().workspaces().tags().create(
        parent=f'accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}',
        body=tag_body
    ).execute()

# Helper to get the existing tag's ID if it exists
def get_existing_tag_id(existing_tags, tag_name):
    if 'tag' in existing_tags:
        for tag in existing_tags['tag']:
            if tag['name'] == tag_name:
                return tag['tagId']
    return None

# Helper to delete a tag
def delete_tag(service, account_id, container_id, workspace_id, tag_id):
    print(f"Deleting tag with ID: {tag_id}")
    service.accounts().containers().workspaces().tags().delete(
        path=f'accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}/tags/{tag_id}'
    ).execute()


def create_ga4_event_tag(service, account_id, container_id, workspace_id, measurement_id, event_tag_name):
    event_tag_body = {
        "name": event_tag_name + " - GA4 - Tag",
        "type": "gaawe",
        "parameter": [
            {
                "key": "eventName",
                "type": "template",
                "value": "dynamic_event"
            },
            {
                "key": "measurementId",
                "type": "template",
                "value": measurement_id
            },
            {
                "key": "triggerId",
                "type": "template",
                "value": ""
            },
            {
                "key": "eventParameters",
                "type": "MAP",
                "map": [
                    {
                        "key": "name",
                        "type": "TEMPLATE",
                        "value": "${parameterName}"
                    },
                    {
                        "key": "value",
                        "type": "TEMPLATE",
                        "value": "${parameterValue}"
                    }
                ]
            },
            {
                "key": "measurementIdOverride",
                "type": "template",
                "value": measurement_id
            },
            {
                "key": "eventSettingsTable",
                "type": "LIST",
                "list": []
            }
        ],
        "firingTriggerId": []
    }

    existing_tags = service.accounts().containers().workspaces().tags().list(
        parent=f'accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}'
    ).execute()

    existing_event_tag_id = get_existing_tag_id(existing_tags, event_tag_name)

    if existing_event_tag_id:
        delete_tag(service, account_id, container_id, workspace_id, existing_event_tag_id)

    create_tag(service, account_id, container_id, workspace_id, event_tag_body)

def get_workspace_id(service, account_id, container_id):
    workspaces_request = service.accounts().containers().workspaces().list(
        parent=f"accounts/{account_id}/containers/{container_id}"
    )
    workspaces_response = workspaces_request.execute()
    return workspaces_response['workspace'][0]['workspaceId']

def create_or_update_ga4_config_tag(service, account_id, container_id, workspace_id, measurement_id, config_tag_name, trigger_ids):
    existing_tags = service.accounts().containers().workspaces().tags().list(
        parent=f'accounts/{account_id}/containers/{container_id}/workspaces/{workspace_id}'
    ).execute()

    existing_config_tag_id = get_existing_tag_id(existing_tags, config_tag_name)

    config_tag_body = {
        "name": config_tag_name + " - Google Tag",
        "type": "gaawc",
        "parameter": [
            {
                "key": "measurementId",
                "type": "template",
                "value": measurement_id
            }
        ],
        "firingTriggerId": trigger_ids
    }

    if existing_config_tag_id:
        delete_tag(service, account_id, container_id, workspace_id, existing_config_tag_id)

    create_tag(service, account_id, container_id, workspace_id, config_tag_body)

def main():
    service_account_path = '/path to file/'
    account_id = 'account_id'
    container_id = 'container_id'
    measurement_id = "measurement_id"
    config_tag_name = "config_tag_name"
    event_tag_name = "event_tag_name"
    default_trigger_ids = ["Trigger ID#1", "Trigger ID#2", "Trigger ID#3"]

    credentials = service_account.Credentials.from_service_account_file(service_account_path)
    service = build('tagmanager', 'v2', credentials=credentials)

     # Get workspace ID
    workspace_id = get_workspace_id(service, account_id, container_id)

    # Create a new tag and trigger
    new_trigger_id = create_tag_and_trigger(service, account_id, container_id, workspace_id, config_tag_name, event_tag_name)

    # Combine trigger IDs
    combined_trigger_ids = default_trigger_ids + [new_trigger_id]

    # Create or update GA4 config tag
    create_or_update_ga4_config_tag(service, account_id, container_id, workspace_id, measurement_id, config_tag_name, combined_trigger_ids)

    # Create GA4 event tag
    create_ga4_event_tag(service, account_id, container_id, workspace_id, measurement_id, event_tag_name)


main()
