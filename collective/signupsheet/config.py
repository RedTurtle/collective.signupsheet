# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger('Signupsheet.configuration')

PROJECTNAME = "SignupSheet"

ADD_PERMISSIONS = {
    'SignupSheet': PROJECTNAME + ': Add SignupSheet',
}

INITIAL_MAIL = u"""<html xmlns='http://www.w3.org/1999/xhtml'>\r\n\r\n
<head><title></title></head>\r\n\r\n<body>\r\n<p tal:content='here/getBody_pre |nothing' />
\r\n %s \r\n<dl>\r\n<tal:block repeat='field options/wrappedFields | nothing'>\r\n
<dt tal:content='field/fgField/widget/label' />\r\n
<dd tal:content='structure python:field.htmlValue(request)' />\r\n
</tal:block>\r\n</dl>\r\n<p tal:content='here/getBody_post | nothing' />\r\n
<pre tal:content='here/getBody_footer | nothing' />\r\n</body>\r\n</html>
"""
INITIAL_MAIL_MESSAGE = u"""
Thank you for registering to <tal:title tal:replace='here/aq_inner/aq_parent/Title'/>\r\n
<tal:show tal:condition='request/review_state|nothing'><p>Your registration state is: <tal:review_state tal:replace='request/review_state' /></p></tal:show>
<p>Those informations has been provided:</p>
"""

MANAGER_MAIL = u"""
<html xmlns='http://www.w3.org/1999/xhtml'>\r\n\r\n<head><title></title></head>
\r\n\r\n<body>\r\n %s \n
\r\n</body>\r\n</html>
"""
MANAGER_MAIL_MESSAGE = """
New registrant registered for <tal:s tal:content=\"here/Title\" />
\nPlease check current registrans: <tal:s tal:content=\"string:${here/absolute_url}/view_registrants\" />
"""