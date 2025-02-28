Marketing Campaign Scheduling
The Marketing Campaign Scheduling feature allows users to schedule email campaigns to be sent at specific dates and times. Users can configure various parameters for their campaigns, such as selecting the recipient list, specifying the email template. The feature ensures that campaigns are sent out accurately and can handle large volumes of emails efficiently. 
User Stories
As a user, I want to create a new email campaign with a scheduled send time and date, so that the campaign is sent automatically at the specified time.
As a user, I want to select a recipient list for my scheduled campaign, so that the emails are sent to the intended audience. 
As a user, I want to choose an email template for my scheduled campaign, so that the campaign content is consistent and professional.
As a user, I want to edit the name of my scheduled campaigns.
As a user, I want to cancel a scheduled campaign, so that it is not sent if it is no longer needed.


The framework is built to test the campaign scheduling features with above user stories. Below tools and libraries are used to build the framework. 

pytest==8.3.4
pytest-html==4.1.1
requests==2.31.0
pydantic==2.10.6
pymongo==4.11.1
setuptools==75.8.0

Pytest is the testing library. Requests libray is used for api calls. pydantic is used for data validation, serialization and deserialization. Pymongo is used for database validation. For reporting I have used 
pytest-html library.



To run test_campaign_end_to_end.py use: pytest test/test_campaign_end_to_end.py --html=report/report.html

To run test_integration.py use: pytest test/test_integration.py --html=report/report.html

To run only integration test cases run use: pytest -m integrationTest --html=report/report.html

To run only E2E test cases run: pytest -m e2eTest --html=report/report.html

To run all test cases run:  pytest --html=report/report.html

The report will be generated under test folder -> report -> report.html
