from pydantic import BaseModel, Field, ValidationError


class CampaignRequest(BaseModel):
    """Pydantic model for validating campaign creation requests."""
    campaignName: str = Field(..., min_length=1, description="Campaign name is required")
    emailTemplateId: str = Field(..., min_length=1, description="Email template ID is required")
    recipientListId: str = Field(..., min_length=1, description="Recipient list ID is required")
    scheduledTime: int = Field(..., ge=0, description="Scheduled time must be a non-negative integer.")

    @classmethod
    def get_payload_for_campaign_creation(cls, campaignName: str, emailTemplateId: str, recipientListId: str, scheduledTime: int) -> str:
        """Generates a JSON payload string for creating a new campaign.

        Args:
            campaignName: The name of the campaign.
            emailTemplateId: The ID of the email template.
            recipientListId: The ID of the recipient list.
            scheduledTime: The scheduled time for the campaign (non-negative integer).

        Returns:
            A JSON string representing the campaign creation payload.
        """
        return cls(
            campaignName=campaignName,
            emailTemplateId=emailTemplateId,
            recipientListId=recipientListId,
            scheduledTime=scheduledTime
        ).json()


class UpdateCampaignRequest(BaseModel):
    """Pydantic model for validating campaign update requests (name only)."""
    campaignName: str = Field(..., min_length=1, description="Campaign name is required")

    @classmethod
    def get_payload_for_campaign_update(cls, campaignName: str) -> str:
        """Generates a JSON payload string for updating a campaign's name.

        Args:
            campaignName: The new name for the campaign.

        Returns:
            A JSON string representing the campaign name update payload.
        """
        return cls(campaignName=campaignName).json()


