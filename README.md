To run test_campaign_end_to_end.py use: pytest test/test_campaign_end_to_end.py --html=report/report.html

To run test_integration.py use: pytest test/test_integration.py --html=report/report.html

To run only integration test cases run use: pytest -m integrationTest --html=report/report.html

To run only E2E test cases run: pytest -m e2eTest --html=report/report.html

To run all test cases run:  pytest --html=report/report.html

The report will be generated under test folder -> report -> report.html
