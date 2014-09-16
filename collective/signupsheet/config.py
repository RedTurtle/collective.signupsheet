# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('signupsheet.configuration')

PROJECTNAME = "SignupSheet"

ADD_PERMISSIONS = {
    'SignupSheet': PROJECTNAME + ': Add SignupSheet',
}

INITIAL_MAIL = u"""<html xmlns="http://www.w3.org/1999/xhtml">
<head><title></title></head>
<body>

<p tal:content='here/getBody_pre |nothing' />

%s

<dl tal:condition="options/wrappedFields|nothing">
    <tal:block repeat="field options/wrappedFields">
        <dt tal:content="field/fgField/widget/label" />
        <dd tal:content="structure python:field.htmlValue(request)" />
    </tal:block>
</dl>

<p tal:content="here/getBody_post | nothing" />

<pre tal:content="here/getBody_footer | nothing" />

</body>
</html>
"""

MANAGER_MAIL = u"""<html xmlns="http://www.w3.org/1999/xhtml">
<head><title></title></head>

<body>

%s

</body>
</html>
"""

