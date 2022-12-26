import os

# The login page of the annex bubt website
baseUrl = os.environ.get("BASE_URL")

# Path or Endpoint
loginPath = os.environ.get("LOGIN_PATH")
dashboardPath = os.environ.get("DASHBOARD_PATH")
routinePath = os.environ.get("ROUTINE_PATH")
routinePrinterPath = os.environ.get("ROUTINE_PRINTER_PATH")

# Urls
loginUrl = baseUrl + loginPath
dashboardUrl = baseUrl + dashboardPath
routineUrl = dashboardUrl + routinePath
routinePrinterUrl = dashboardUrl + routinePrinterPath

# Images directory path
imageDirPath = 'app/images/%s.png'
routineDirPath = 'app/v1/helper/%s.png'
studentStorageBucketPath = 'images/students/%s.png'
teacherStorageBucketPath = 'images/teachers/%s.png'
routineStorageBucketPath = 'images/routine/%s.png'
