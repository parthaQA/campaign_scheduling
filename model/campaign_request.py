import pytest
from pydantic import BaseModel, Field, ValidationError


class CampaignRequest(BaseModel):
    """Schema validation for CampaignRequest"""
    campaignName: str = Field(..., min_length=1, description="Campaign name is required")
    emailTemplateId: str = Field(..., min_length=1, description="Email template ID is required")
    recipientListId: str = Field(..., min_length=1, description="Recipient list ID is required")
    scheduledTime: int = Field(..., description="Scheduled time can be positive or negative")

    @classmethod
    def get_payload_for_campaign_creation(cls, campaignName, emailTemplateId, recipientListId, scheduledTime):
        """Returns a valid JSON payload for CampaignRequest"""
        return cls(
            campaignName=campaignName,
            emailTemplateId=emailTemplateId,
            recipientListId=recipientListId,
            scheduledTime=scheduledTime
        ).json()


class UpdateCampaignRequest(BaseModel):
    """Schema validation for updating campaign name"""
    campaignName: str = Field(..., min_length=1, description="Campaign name is required")
    campaign_id: str = Field(...,description="Campaign id is required")

    @classmethod
    def get_payload_for_campaign_update(cls, campaignName, campaign_id):
        """Returns a valid JSON payload for updating a campaign name"""
        return cls(campaignName=campaignName, campaign_id=campaign_id).json()


