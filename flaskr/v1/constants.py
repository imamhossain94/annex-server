# Base url
# The login page of the annex bubt website
baseUrl = 'https://annex.bubt.edu.bd/'

# Path or Endpoint
loginPath = 'global_file/action/login_action.php'
dashboardPath = 'ONSIS_SEITO/'
routinePath = '?page=routine'
routinePrinterPath = 'includes/helpers/routine_format.php'

# Urls
loginUrl = baseUrl + loginPath
dashboardUrl = baseUrl + dashboardPath
routineUrl = dashboardUrl + routinePath
routinePrinterUrl = dashboardUrl + routinePrinterPath


# Images directory path
imageDirPath = 'flaskr/images/%s.png'
screenshotDirPath = 'flaskr/screenshot/'
studentStorageBucketPath = 'images/students/%s.png'
teacherStorageBucketPath = 'images/teachers/%s.png'
routineStorageBucketPath = 'images/routine/%s.png'
