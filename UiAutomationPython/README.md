<h2>**Task: Write UI tests**</h2>

Create UI tests using Python3 + Pytest + Selenium + ChromeDriver.
For reporting, please use allure reports with test titles. <br>
After running tests please verify `setup/teardown/title` are shown by running
```
allure serve %allure_result_folder%
```

<h3>**Test case:**</h3>

1. Open https://blog.griddynamics.com
2. Click ‘filter’ (check it’s visible and available)
3. Filter by the year 2017
4. Check there is more than 1 article
5. Reset all filters
6. Check the first article in the list is different than in step 4 and check there is more than 1 article.

<h3>**How to run:**</h3>

On Unix or MacOS, run:

`python3 -m venv uiAutomation-env` 
<br>
`source uiAutomation-env/bin/activate`

Install required packages:
`pip3 install -r requirements.txt`

Run test:
```
$ py.test --alluredir=%allure_result_folder% FilterTest.py
```

To run Allure report:
```
$ allure serve %allure_result_folder%
```