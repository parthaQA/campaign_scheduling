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
        get_email_template_id = self.api_utils.make_get_request(
            f"{config_helper.api_urls['email_template']}/{get_email_template['data'][0]['id']}")
        assert get_email_template_id["meta"]["status"] == "SUCCESS"
        assert get_email_template_id["data"]["id"] is not None
        get_recipient_list = self.api_utils.make_get_request(config_helper.api_urls["recipient_list"])
        get_recipient_list_id = self.api_utils.make_get_request(
            f"{config_helper.api_urls['recipient_list']}/{get_recipient_list['data'][0]['id']}")
        assert get_recipient_list_id["meta"]["status"] == "SUCCESS"
        assert get_recipient_list_id["data"]["id"] is not None
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName,
                                                                    str(get_email_template_id["data"]["id"]),
                                                                    str(get_recipient_list_id["data"]["id"]),
                                                                    scheduledTime)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        assert response["meta"]["status"] == "SUCCESS"
        assert response["data"]["campaignName"] == campaignName
        assert response["data"]["id"] is not None
        assert response["data"]["emailTemplateId"] == get_email_template_id["data"]["id"]
        assert response["data"]["recipientListId"] == get_recipient_list_id["data"]["id"]
        assert response["data"]["scheduledTime"] == scheduledTime

    @pytest.mark.down
    @pytest.mark.description("Create a campaign when email template service is down as part of integration test")
    @pytest.mark.parametrize("campaignName, scheduledTime",
                             [("parthacam_email_down", 0)])
    def test_create_campaign_when_email_template_service_is_down_integration_test(self, campaignName, scheduledTime):
        campaignName = campaignName + str(datetime.now().strftime("%H%M%S"))

        # Assume recipient service is up for this test
        get_recipient_list = self.api_utils.make_get_request(config_helper.api_urls["recipient_list"])
        assert get_recipient_list is not None, "Recipient list API call failed or returned None"
        assert get_recipient_list["meta"]["status"] == "SUCCESS", f"Fetching recipient list failed: {get_recipient_list}"
        # Ensure data is not empty and has an id
        assert len(get_recipient_list["data"]) > 0, "Recipient list data is empty"
        recipient_list_id = get_recipient_list["data"][0]["id"]
        assert recipient_list_id is not None, "Recipient list ID is None"

        # Use a placeholder for emailTemplateId as the service is "down"
        email_template_id_placeholder = "EM-SIMULATE-DOWN"

        payload = CampaignRequest.get_payload_for_campaign_creation(
            campaignName,
            email_template_id_placeholder,
            str(recipient_list_id),
            scheduledTime
        )
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        
        assert response is not None, "Campaign creation API did not respond as expected."
        assert response["meta"]["status"] == "FAILURE", f"Campaign creation should fail when email service is down. Response: {response}"
        assert "errors" in response and len(response["errors"]) > 0, "Error details should be present."
        assert response["errors"][0]["errorCode"] == "BAS-E-001", f"Incorrect error code for email service down. Response: {response}"
        assert "Internal Server Error" in response["errors"][0]["message"], f"Incorrect error message. Response: {response}"

    @pytest.mark.down
    @pytest.mark.description("Create a campaign when recipient service is down as part of integration test")
    @pytest.mark.parametrize("campaignName, scheduledTime",
                             [("parthacam_recipient_down", 0)])
    def test_create_campaign_when_recipient_service_is_down_integration_test(self, campaignName, scheduledTime):
        campaignName = campaignName + str(datetime.now().strftime("%H%M%S"))

        # Assume email template service is up
        get_email_template = self.api_utils.make_get_request(config_helper.api_urls["email_template"])
        assert get_email_template is not None, "Email template API call failed or returned None"
        assert get_email_template["meta"]["status"] == "SUCCESS", f"Fetching email template failed: {get_email_template}"
        # Ensure data is not empty and has an id
        assert len(get_email_template["data"]) > 0, "Email template data is empty"
        email_template_id = get_email_template["data"][0]["id"]
        assert email_template_id is not None, "Email template ID is None"
        
        # Use a placeholder for recipientListId as the service is "down"
        recipient_list_id_placeholder = "RL-SIMULATE-DOWN"

        payload = CampaignRequest.get_payload_for_campaign_creation(
            campaignName,
            str(email_template_id),
            recipient_list_id_placeholder,
            scheduledTime
        )
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])

        assert response is not None, "Campaign creation API did not respond as expected."
        assert response["meta"]["status"] == "FAILURE", f"Campaign creation should fail when recipient service is down. Response: {response}"
        assert "errors" in response and len(response["errors"]) > 0, "Error details should be present."
        assert response["errors"][0]["errorCode"] == "BAS-E-001", f"Incorrect error code for recipient service down. Response: {response}"
        assert "Internal Server Error" in response["errors"][0]["message"], f"Incorrect error message. Response: {response}"
