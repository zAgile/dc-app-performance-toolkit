import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401

logger = init_logger(app_type='jira')
issue_key="ONE-2"
case_id="5008a00001ujPUfAAM"
attachment_id = "10602"
attachment_id_download = "00P8a000021Meo3EAC"
name_attachment = "SomePDF.pdf"
token_attachment = "Ch4J0bJUvWFp8AthNHmtcNR1IieCXN12nswJORtzpRI%3D"
url_dowload = "&token=Ch4J0bJUvWFp8AthNHmtcNR1IieCXN12nswJORtzpRI%3D&sObjName=Attachment&contentType=application/pdf"

@jira_measure("locust_app_specific_action")
# @run_as_specific_user(username='admin', password='admin')  # run as specific user

def app_specific_action(locust):
    """GET ATTACHMENTS"""
    r = locust.get(f'/rest/zagile-sf/1.0/attachment/{issue_key}?entityId={case_id}', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    token_pattern_example = '"token":"(.+?)"'
    id_pattern_example = '"id":"(.+?)"'
    token = re.findall(token_pattern_example, content)  # get TOKEN from response using regexp
    id = re.findall(id_pattern_example, content)    # get ID from response using regexp

    logger.locust_info(f'token: {token}, id: {id}')  # log info for debug when verbose is true in jira.yml file
    assert r.status_code is 200, "bad request or no exist attachments"


    """GET COMMENT"""
    r = locust.get(f'/rest/zagile-sf/1.0/comment/{case_id}?limit=20&offset=0',
                   catch_response=True)
    content = r.content.decode('utf-8')

    token_pattern_example = '"token":"(.+?)"'
    id_pattern_example = '"id":"(.+?)"'
    token = re.findall(token_pattern_example, content)
    id = re.findall(id_pattern_example, content)

    logger.locust_info(f'token: {token}, id: {id}')
    assert r.status_code is 200, "bad request or no exist comments"



    """GET FEEDS"""
    r = locust.get(f'/rest/zagile-sf/1.0/{issue_key}/feed/{case_id}?pageSize=20',
                   catch_response=True)
    content = r.content.decode('utf-8')

    token_pattern_example = '"token":"(.+?)"'
    id_pattern_example = '"id":"(.+?)"'
    token = re.findall(token_pattern_example, content)
    id = re.findall(id_pattern_example, content)

    logger.locust_info(f'token: {token}, id: {id}')
    assert r.status_code is 200, "bad request or no exist feeds"





    """GET EMAILS"""
    r = locust.get(f'/rest/zagile-sf/1.0/{issue_key}/email/{case_id}?limit=20&offset=0',
                   catch_response=True)
    content = r.content.decode('utf-8')

    token_pattern_example = '"token":"(.+?)"'
    id_pattern_example = '"id":"(.+?)"'
    token = re.findall(token_pattern_example, content)
    id = re.findall(id_pattern_example, content)

    logger.locust_info(f'token: {token}, id: {id}')
    assert r.status_code is 200, "bad request or no exist emails"




    """GET ATTACHMENTS - CLIP"""
    r = locust.get(f'/rest/zagile-sf/1.0/attachment/{issue_key}/sync-sf/{case_id}?concept=Case',
                   catch_response=True)
    content = r.content.decode('utf-8')

    token_pattern_example = '"token":"(.+?)"'
    id_pattern_example = '"id":"(.+?)"'
    token = re.findall(token_pattern_example, content)
    id = re.findall(id_pattern_example, content)

    logger.locust_info(f'token: {token}, id: {id}')
    assert r.status_code is 200, "bad request or no exist attach"





    """POST IMPORT"""
    pyload = {"entityId":"5008a00001ujPUfAAM","filename":"SomePDF.pdf","contentType":"application/pdf","attachmentObjName":"Attachment","attachmentId":"00P8a000021Meo3EAC"}

    r = locust.post(
        f'/rest/zagile-sf/1.0/attachment/{issue_key}/import?token=Ch4J0bJUvWFp8AthNHmtcNR1IieCXN12nswJORtzpRI%3D',
        json=pyload, headers={'content-type': 'application/json', 'Accept': 'application/json', 'Content-Length': '155'},
        catch_response=True)  # call app-specific POST endpoint

    assert r.status_code is 200, "import string was not found after request POST "  # assertion after POST request


    """POST DOWNLOAD"""
    r = locust.post(
        f'/plugins/servlet/downloadSalesforceAttachment?attachmentId={attachment_id_download}&issueKey={issue_key}&entityId={case_id}&attachmentName={name_attachment}{url_dowload}',
        headers={'content-type': 'application/json', 'Accept': 'application/json', 'X-Atlassian-Token': 'no-check'},
        catch_response=True)

    assert r.status_code is 200, "download string was not found after request POST"



    """POST SEND ATTACHMENT"""
    r = locust.post(
        f'/rest/zagile-sf/1.0/attachment/{attachment_id}/sync-sf/{case_id}',
        headers={'content-type': 'application/json', 'Accept': 'application/json', 'X-Atlassian-Token': 'no-check'},
        catch_response=True)

    assert r.status_code is 200, "the attachment not sent after request POST"