"""
Create a config.ini with:
[default]
mc_api = <api_key>
list_id = <list id>
campaign_id = <campaign id>

mailchimp3: https://github.com/charlesthk/python-mailchimp
MailChimp API reference: https://developer.mailchimp.com/documentation/mailchimp/reference/overview/

# # add John Doe with email john.doe@example.com to list matching id '123456'
# client.lists.members.create('123456', {
#     'email_address': 'john.doe@example.com',
#     'status': 'subscribed',
#     'merge_fields': {
#         'FNAME': 'John',
#         'LNAME': 'Doe',
#     },
# })

"""
import ujson
import requests
from mailchimp3 import MailChimp
import configparser

# MailChimp client
client = None
# API key
mc_api = None
# List unique id
list_id = None
# Campaign id
campaign_id = None


def __get_config():
    """
    Get config from config.ini
    """
    global mc_api, list_id, campaign_id
    config = configparser.ConfigParser()
    config.read('config.ini')
    mc_api = config['default']['mc_api']
    list_id = config['default']['list_id']
    campaign_id = config['default']['campaign_id']
    return config


def mailchimp_connect():
    """
    Create MailChimp client object
    """
    global mc_api, client
    __get_config()
    headers = requests.utils.default_headers()
    client = MailChimp(mc_api=mc_api, timeout=30.0, request_headers=headers)
    return client


def get_client():
    global client
    if not client:
        client = mailchimp_connect()
    return client


def get_lists(p: bool = False, f: str = "lists.name,lists.id"):
    """
    returns all the lists
    """
    client = get_client()
    lists = client.lists.all(get_all=True, fields=f)
    lists_output = ujson.dumps(lists, indent=4)
    if p:
        print(lists_output)
    return list


def get_members(p: bool = False, l: str = ""):
    """
    returns all members inside list
    """
    client = get_client()
    members = client.lists.members.all(list_id, get_all=True)
    members_output = ujson.dumps(members, indent=4)
    if p:
        print(members_output)

    return members


def get_list_by_id(p: bool = False, l: str = ""):
    """
    returns the list matching
    """
    client = get_client()
    list_matching = client.lists.get(list_id)
    list_matching_output = ujson.dumps(list_matching, indent=4)
    if p:
        print(list_matching_output)

    return list_matching


def get_campaigns(p: bool = False):
    """
    returns all the campaigns
    """
    client = get_client()
    campaigns = client.campaigns.all(get_all=True)
    campaigns_output = ujson.dumps(campaigns, indent=4)
    if p:
        print(campaigns_output)

    return campaigns


def send_test_campaign(c: str = None, e: str = None):
    """
    Send a test campaign
    """
    client = get_client()

    if not c:
        global campaign_id
        c = campaign_id

    d = {"test_emails": [e], "send_type": "html", "settings": {"subject_line": "Found test"}}
    r = client.campaigns.actions.test(campaign_id=c, data=d)
    return r


def get_campaign_by_id(p: bool = False, c: str = None):
    """
    Get campaign by id
    """
    client = get_client()

    if not c:
        global campaign_id
        c = campaign_id

    r = client.campaigns.get(campaign_id=c)
    r_output = ujson.dumps(r, indent=4)
    if p:
        print(r_output)
    return r


if __name__ == "__main__":
    get_lists(p=True)
    get_members(p=True, l=list_id)
    get_list_by_id(p=True, l=list_id)
    get_campaigns(p=True)
    send_test_campaign(e="leo@leocelis.com")
    get_campaign_by_id(p=True)
