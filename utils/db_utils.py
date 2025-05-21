class MongoDB:
    """A utility class for interacting with MongoDB collections."""

    def get_campaign_name(self, db, campaign_name):
        """Fetches a campaign document by its name from the campaign collection."""
        campaign_collection = db['campaign']
        campaign = campaign_collection.find_one({'name': campaign_name})
        if campaign:
            return campaign['name']
        return None
