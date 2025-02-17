from datetime import datetime

import pytest

from config import config_helper
from model.campaign_request import CampaignRequest
from utils.api_utils import APIUtils


@pytest.mark.integrationTest
class TestIntegration:
    api_utils = APIUtils()

    @pytest.mark.integrationTest
    @pytest.mark.description("Create a campaign with valid data as part of integration test")
    @pytest.mark.parametrize("campaignName, scheduledTime",
                             [("parthacam", 0)])
    def test_create_campaign_integration_test(self, campaignName, scheduledTime):
        campaignName = campaignName + str(datetime.now().strftime("%H%M%S"))
        get_email_template = self.api_utils.make_get_request(config_helper.api_urls["email_template"])
        print("get email template response : ", get_email_template["data"][0]["id"])
        get_email_template_id = self.api_utils.make_get_request(
            f"{config_helper.api_urls['email_template']}/{get_email_template['data'][0]['id']}")
        print("get email template by id response : ", get_email_template_id["data"]["id"])
        assert get_email_template_id["meta"]["status"] == "SUCCESS"
        assert get_email_template_id["data"]["id"] is not None
        get_recipient_list = self.api_utils.make_get_request(config_helper.api_urls["recipient_list"])
        print("get recipient list response : ", get_recipient_list["data"][0]["id"])
        get_recipient_list_id = self.api_utils.make_get_request(
            f"{config_helper.api_urls['recipient_list']}/{get_recipient_list['data'][0]['id']}")
        print("get recipient list by id response : ", get_recipient_list_id["data"]["id"])
        assert get_recipient_list_id["meta"]["status"] == "SUCCESS"
        assert get_recipient_list_id["data"]["id"] is not None
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName,
                                                                    str(get_email_template_id["data"]["id"]),
                                                                    str(get_recipient_list_id["data"]["id"]),
                                                                    scheduledTime)
        print("payload : ", payload)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        print("create campaign response : ", response)
        assert response["meta"]["status"] == "SUCCESS"
        assert response["data"]["campaignName"] == campaignName
        assert response["data"]["id"] is not None
        assert response["data"]["emailTemplateId"] == get_email_template_id["data"]["id"]
        assert response["data"]["recipientListId"] == get_recipient_list_id["data"]["id"]
        assert response["data"]["scheduledTime"] == scheduledTime

    @pytest.mark.integrationTest
    @pytest.mark.description("Create a campaign when email template service is down as part of integration test")
    @pytest.mark.parametrize("campaignName, scheduledTime",
                             [("parthacam", 0)])
    def test_create_campaign_when_email_template_service_is_down_integration_test(self, campaignName, scheduledTime):
        campaignName = campaignName + str(datetime.now().strftime("%H%M%S"))
        get_email_template = self.api_utils.make_get_request(config_helper.api_urls["email_template"])
        print("get email template response : ", get_email_template)
        assert "Request failed: HTTPConnectionPool(host='localhost', port=7071):" in get_email_template
        print("get email template response : ", get_email_template["data"][0]["id"])
        get_email_template_id = self.api_utils.make_get_request(
            f"{config_helper.api_urls['email_template']}/{get_email_template['data'][0]['id']}")
        print("get email template by id response : ", get_email_template_id["data"]["id"])
        assert get_email_template_id["meta"]["status"] == "SUCCESS"
        assert get_email_template_id["data"]["id"] is not None
        get_recipient_list = self.api_utils.make_get_request(config_helper.api_urls["recipient_list"])
        print("get recipient list response : ", get_recipient_list["data"][0]["id"])
        get_recipient_list_id = self.api_utils.make_get_request(
            f"{config_helper.api_urls['recipient_list']}/{get_recipient_list['data'][0]['id']}")
        print("get recipient list by id response : ", get_recipient_list_id["data"]["id"])
        assert get_recipient_list_id["meta"]["status"] == "SUCCESS"
        assert get_recipient_list_id["data"]["id"] is not None
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName,
                                                                    str(get_email_template_id["data"]["id"]),
                                                                    str(get_recipient_list_id["data"]["id"]),
                                                                    scheduledTime)
        print("payload : ", payload)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        print("create campaign response : ", response)
        assert response["meta"]["status"] == "Success"
        assert response["data"]["campaignName"] == campaignName
        assert response["data"]["id"] is not None
        assert response["data"]["emailTemplateId"] == get_email_template_id["data"]["id"]
        assert response["data"]["recipientListId"] == get_recipient_list_id["data"]["id"]
        assert response["data"]["scheduledTime"] == scheduledTime

    @pytest.mark.integrationTest
    @pytest.mark.description("Create a campaign when recipient service is down as part of integration test")
    @pytest.mark.parametrize("campaignName, scheduledTime",
                             [("parthacam", 0)])
    def test_create_campaign_when_recipient_service_is_down_integration_test(self, campaignName, scheduledTime):
        campaignName = campaignName + str(datetime.now().strftime("%H%M%S"))
        get_email_template = self.api_utils.make_get_request(config_helper.api_urls["email_template"])
        print("get email template response : ", get_email_template)
        assert "Request failed: HTTPConnectionPool(host='localhost', port=7072):" in get_email_template
        print("get email template response : ", get_email_template["data"][0]["id"])
        get_email_template_id = self.api_utils.make_get_request(
            f"{config_helper.api_urls['email_template']}/{get_email_template['data'][0]['id']}")
        print("get email template by id response : ", get_email_template_id["data"]["id"])
        assert get_email_template_id["meta"]["status"] == "SUCCESS"
        assert get_email_template_id["data"]["id"] is not None
        get_recipient_list = self.api_utils.make_get_request(config_helper.api_urls["recipient_list"])
        print("get recipient list response : ", get_recipient_list)
        assert get_recipient_list["meta"]["status"] == "SUCCESS"
        print("get recipient list response : ", get_recipient_list["data"][0]["id"])
        get_recipient_list_id = self.api_utils.make_get_request(
            f"{config_helper.api_urls['recipient_list']}/{get_recipient_list['data'][0]['id']}")
        print("get recipient list by id response : ", get_recipient_list_id["data"]["id"])
        assert get_recipient_list_id["meta"]["status"] == "SUCCESS"
        assert get_recipient_list_id["data"]["id"] is not None
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName,
                                                                    str(get_email_template_id["data"]["id"]),
                                                                    str(get_recipient_list_id["data"]["id"]),
                                                                    scheduledTime)
        print("payload : ", payload)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        print("create campaign response : ", response)
        assert response["meta"]["status"] == "Success"
        assert response["data"]["campaignName"] == campaignName
        assert response["data"]["id"] is not None
        assert response["data"]["emailTemplateId"] == get_email_template_id["data"]["id"]
        assert response["data"]["recipientListId"] == get_recipient_list_id["data"]["id"]
        assert response["data"]["scheduledTime"] == scheduledTime
