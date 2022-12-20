
from v1.helpers.req import USER_AGENTS
import random

LOGIN_USERNAME = ''
LOGIN_PASSWORD = ''

reptile_argument = [
    # '--headless',  # 无界面
    # '-disable-gpu',
    # 防反扒
    'disable-infobars',
    '--disable-blink-features=AutomationControlled',
    ('user-agent=%s' % random.choice(USER_AGENTS))
]