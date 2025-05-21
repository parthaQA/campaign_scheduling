"""
Configuration file for storing API endpoint URLs.

This module centralizes all external API URLs used throughout the application,
making it easier to manage and update them.
"""
api_urls = {
    "create_campaign": "http://localhost:7070/campaigns",
    "update_campaign": "http://localhost:7070/campaigns",
    "get_campaign": "http://localhost:7070/campaigns",
    "recipient_list": "http://localhost:7072/recipients/lists",
    "email_template": "http://localhost:7071/email/templates"
}