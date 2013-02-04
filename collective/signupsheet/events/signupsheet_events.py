# -*- coding: utf-8 -*-

# BBB Due to some event in PloneFormGen, we need to use this event to end the
# signupsheet configuration


def form_initialized(obj, event):
    action_adapters = list(obj.actionAdapter)
    if 'user_notification_mailer' in action_adapters:
        action_adapters.remove('user_notification_mailer')
    obj.actionAdapter = action_adapters
