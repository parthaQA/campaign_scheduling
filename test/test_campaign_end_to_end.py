from datetime import datetime
import pytest
import time
import json
from config import config_helper
from model.campaign_request import CampaignRequest, UpdateCampaignRequest
from utils.api_utils import APIUtils
from utils.db_utils import MongoDB



@pytest.mark.usefixtures("mongo_client")
class TestCampaignAPI:
    """Handles API interactions and database validation for Campaign Scheduling."""

    api_utils = APIUtils()
    mongo_db = MongoDB()

    @pytest.mark.e2eTest
    @pytest.mark.description("Create a campaign with valid data")
    @pytest.mark.parametrize("campaignName, emailTemplateId, recipientListId, scheduledTime",
                             [("partha", "EM-001", "RL-001", 0)])
    def test_create_valid_campaign(self, campaignName, emailTemplateId, recipientListId, scheduledTime):
        """Test creating a valid campaign and validate in DB."""
        campaignName = campaignName + str(datetime.now().strftime("%H%M%S"))
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName, emailTemplateId, recipientListId,
                                                                    scheduledTime)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        assert response["meta"]["status"] == "SUCCESS"
        assert response["data"]["campaignName"] == campaignName
        assert response["data"]["id"] is not None
        assert response["data"]["emailTemplateId"] == emailTemplateId
        assert response["data"]["recipientListId"] == recipientListId
        assert response["data"]["scheduledTime"] == scheduledTime
        time.sleep(3)
        retrieved_campaign_name = self.mongo_db.get_campaign_name(self.db_admin, campaign_name=campaignName)
        assert campaignName in retrieved_campaign_name

    @pytest.mark.e2eTest
    @pytest.mark.description("Create a campaign with invalid email template id")
    @pytest.mark.parametrize("campaignName, emailTemplateId, recipientListId, scheduledTime",
                             [("parthacam", "EM", "RL-001", 0)])
    def test_create_campaign_invalid_email_template_id(self, campaignName, emailTemplateId, recipientListId,
                                                       scheduledTime):
        """Test creating a campaign with invalid emailTemplateId."""
        campaignName = campaignName + str(datetime.now().strftime("%H%M%S"))
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName, emailTemplateId, recipientListId,
                                                                    scheduledTime)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        assert response["meta"]["status"] == "FAILURE"
        assert response["errors"][0]["errorCode"] == "CAM-E-002"
        assert response["errors"][0]["message"] == "Email Template Not Found"

    @pytest.mark.e2eTest
    @pytest.mark.description("Create a campaign with invalid email recipient id")
    @pytest.mark.parametrize("campaignName, emailTemplateId, recipientListId, scheduledTime",
                             [("parthacam", "EM-001", "RL-00", 0)])
    def test_create_campaign_invalid_recipient_id(self, campaignName, emailTemplateId, recipientListId, scheduledTime):
        """Test creating a campaign with invalid recipientListId."""
        campaignName = campaignName + str(datetime.now().strftime("%H%M%S"))
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName, emailTemplateId, recipientListId,
                                                                    scheduledTime)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        assert response["meta"]["status"] == "FAILURE"
        assert response["errors"][0]["errorCode"] == "CAM-E-003"
        assert response["errors"][0]["message"] == "Recipient List Not Found"

    @pytest.mark.e2eTest
    @pytest.mark.description("Create a campaign with invalid scheduled time)")
    @pytest.mark.parametrize("campaignName, emailTemplateId, recipientListId, scheduledTime",
                             [("parthacamcam1", "EM-001", "RL-001", -1)])
    def test_create_campaign_invalid_scheduled_time(self, campaignName, emailTemplateId, recipientListId,
                                                    scheduledTime):
        """Test creating a campaign with invalid scheduled time"""
        campaignName = campaignName + str(datetime.now().strftime("%H%M%S"))
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName, emailTemplateId, recipientListId,
                                                                    scheduledTime)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        assert response["meta"]["status"] == "FAILURE"
        assert response["errors"][0]["errorCode"] == "BAS-E-002"
        assert response["errors"][0]["message"] == "Input Validation Error"

    @pytest.mark.e2eTest
    @pytest.mark.description("fetch a campaign details by id")
    @pytest.mark.parametrize("campaignName, emailTemplateId, recipientListId, scheduledTime",
                             [("parthacam221", "EM-001", "RL-001", 10)])
    def test_get_campaign_details_by_id(self, campaignName, emailTemplateId, recipientListId, scheduledTime):
        """Test retrieving an existing campaign by ID and validate database entry."""
        campaignName = campaignName + str(datetime.now().strftime("%H%M%S"))
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName, emailTemplateId, recipientListId,
                                                                    scheduledTime)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        assert response["meta"]["status"] == "SUCCESS"
        assert response["data"]["campaignName"] == campaignName
        assert response["data"]["id"] is not None
        assert response["data"]["emailTemplateId"] == emailTemplateId
        assert response["data"]["recipientListId"] == recipientListId
        assert response["data"]["scheduledTime"] == scheduledTime
        time.sleep(3)
        retrieved_campaign_name = self.mongo_db.get_campaign_name(self.db_admin, campaign_name=campaignName)
        assert campaignName in retrieved_campaign_name
        get_campaign_id = response["data"]["id"]
        response = self.api_utils.make_get_request(f"{config_helper.api_urls['get_campaign']}/{get_campaign_id}")
        assert response["meta"]["status"] == "SUCCESS"
        assert response["data"]["campaignName"] == campaignName
        assert response["data"]["emailTemplateId"] == emailTemplateId
        assert response["data"]["recipientListId"] == recipientListId
        assert response["data"]["scheduledTime"] == scheduledTime

    @pytest.mark.e2eTest
    @pytest.mark.description("fetch a campaign details by invalid id")
    @pytest.mark.parametrize("campaignId", [(0)])
    def test_get_campaign_non_existent(self, campaignId):
        """Test retrieving a non-existent campaign."""
        response = self.api_utils.make_get_request(f"{config_helper.api_urls['get_campaign']}/{campaignId}")
        assert response["meta"]["status"] == "FAILURE"
        assert response["errors"][0]["errorCode"] == "CAM-E-001"
        assert response["errors"][0]["message"] == "Campaign not found"

    @pytest.mark.e2eTest
    @pytest.mark.description("update a campaign name with valid data")
    # No parametrize for campaign_id, campaignName will be dynamic
    def test_update_campaign_name(self): # Removed campaignName, campaign_id from signature
        """Test updating the campaign name and validate in DB."""
        # 1. Create a campaign
        original_campaign_name = "OriginalCampaign_" + str(datetime.now().strftime("%H%M%S%f"))
        email_template_id = "EM-001"
        recipient_list_id = "RL-001"
        scheduled_time = 0

        create_payload = CampaignRequest.get_payload_for_campaign_creation(
            original_campaign_name, email_template_id, recipient_list_id, scheduled_time
        )
        create_response = self.api_utils.make_post_request(create_payload, config_helper.api_urls["create_campaign"])
        assert create_response is not None, f"Campaign creation API call failed or returned None. Payload: {create_payload}"
        assert create_response["meta"]["status"] == "SUCCESS", f"Campaign creation failed: Response: {create_response}"
        created_campaign_id = create_response["data"]["id"]
        assert created_campaign_id is not None

        # 2. Update the campaign name
        updated_campaign_name = "UpdatedCampaign_" + str(datetime.now().strftime("%H%M%S%f"))
        update_payload = UpdateCampaignRequest.get_payload_for_campaign_update(updated_campaign_name) 
        
        update_response = self.api_utils.make_patch_request(
            update_payload,
            f"{config_helper.api_urls['update_campaign']}/{created_campaign_id}/name"
        )
        assert update_response is not None, f"Campaign update API call failed or returned None. Payload: {update_payload}, URL: {config_helper.api_urls['update_campaign']}/{created_campaign_id}/name"
        assert update_response["meta"]["status"] == "SUCCESS", f"Campaign update failed: Response: {update_response}"
        assert update_response["data"]["campaignName"] == updated_campaign_name
        assert update_response["data"]["id"] == created_campaign_id

    @pytest.mark.e2eTest
    @pytest.mark.description("update a campaign name with invalid campaign name")
    @pytest.mark.parametrize("campaignName, campaign_id", [("cam", "1")]) # campaign_id is for the URL
    def test_update_non_existent_campaign(self, campaignName, campaign_id): # campaign_id is for the URL
        """Test updating a campaign name for a non-existent campaign."""
        # campaignName is parameterized for this test case, no need to append timestamp
        payload = UpdateCampaignRequest.get_payload_for_campaign_update(campaignName) # campaign_id removed
        response = self.api_utils.make_patch_request(payload,
                                                     f"{config_helper.api_urls['update_campaign']}/{campaign_id}/name") # campaign_id used in URL
        assert response is not None, "API call for non-existent campaign update failed or returned None"
        assert response["meta"]["status"] == "FAILURE"
        assert response["errors"][0]["errorCode"] == "CAM-E-001"
        assert response["errors"][0]["message"] == "Campaign not found"

    @pytest.mark.e2eTest
    @pytest.mark.description("update a campaign name with empty name")
    @pytest.mark.parametrize("campaignName, campaign_id", [(" ", "1")]) # campaign_id is for the URL
    def test_update_campaign_empty_name(self, campaignName, campaign_id): # campaign_id is for the URL
        """Test updating a campaign name with empty name."""
        payload = UpdateCampaignRequest.get_payload_for_campaign_update(campaignName) # campaign_id removed
        response = self.api_utils.make_patch_request(payload,
                                                     f"{config_helper.api_urls['update_campaign']}/{campaign_id}/name") # campaign_id used in URL
        assert response["meta"]["status"] == "FAILURE"
        assert response["errors"][0]["errorCode"] == "BAS-E-002"
        assert response["errors"][0]["message"] == "Input Validation Error"

    @pytest.mark.down
    @pytest.mark.description("Create a campaign when email template server is down")
    @pytest.mark.parametrize("campaignName, emailTemplateId, recipientListId, scheduledTime",
                             [("Test Campaign8", "EM-001", "RL-001", 0)])
    def test_create_campaign_when_email_template_service_is_down(self, campaignName, emailTemplateId, recipientListId, scheduledTime):
        """Test creating a valid campaign and validate in DB."""
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName, emailTemplateId, recipientListId,
                                                                    scheduledTime)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        assert response["meta"]["status"] == "FAILURE"
        assert response["errors"][0]["errorCode"] == "BAS-E-001"
        assert response["errors"][0]["message"] == "Internal Server Error"
        assert response["errors"][0]["detail"] == "I/O error on GET request for \"http://host.docker.internal:7071/email/templates/EM-001\": null"

    @pytest.mark.e2eTest
    @pytest.mark.description("Create a campaign with duplicate data")
    @pytest.mark.parametrize("campaignName, emailTemplateId, recipientListId, scheduledTime",
                             [("Test_partha6", "EM-001", "RL-001", 0)])
    def test_create_campaign_with_duplicate_data(self, campaignName, emailTemplateId, recipientListId, scheduledTime):
        """Test creating a valid campaign and validate in DB."""
        payload = CampaignRequest.get_payload_for_campaign_creation(campaignName, emailTemplateId, recipientListId,
                                                                    scheduledTime)
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        assert response["meta"]["status"] == "FAILURE"
        assert response["errors"][0]["errorCode"] == "CAM-E-004"
        assert response["errors"][0]["message"] == "Campaign Name must be unique"

    @pytest.mark.e2eTest
    @pytest.mark.description("Create a campaign without passing campaignName as payload")
    @pytest.mark.parametrize("emailTemplateId, recipientListId, scheduledTime",
                             [("EM-001", "RL-001", 0)])
    def test_create_campaign_without_passing_campaignName_as_payload(self, emailTemplateId, recipientListId, scheduledTime):
        """Test creating a valid campaign and validate in DB."""
        payload = json.dumps({
            "emailTemplateId": "EM-001",
            "recipientListId": "RL-001",
            "scheduledTime": 0
        })
        response = self.api_utils.make_post_request(payload, config_helper.api_urls["create_campaign"])
        assert response["meta"]["status"] == "FAILURE"
        assert response["errors"][0]["errorCode"] == "BAS-E-002"
        assert response["errors"][0]["message"] == "Input Validation Error"