class MongoDB:
    """Class to interact with MongoDB."""

    def get_campaign_name(self, db, campaign_name):
        """Test fetching all campaign documents from the campaign collection."""
        campaign_collection = db['campaign']
        print("campaign_collection :", campaign_collection)
        campaigns = list(campaign_collection.find({}))  # Convert cursor to list
        print("campaigns : ", campaigns[-1]['name'])
        return campaigns[-1]['name']
