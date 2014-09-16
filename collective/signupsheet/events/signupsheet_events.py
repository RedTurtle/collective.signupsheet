# -*- coding: utf-8 -*-


def form_initialized(obj, event):
    """Due to some events in PloneFormGen, we need to use this event to end the signupsheet configuration"""
    action_adapters = []
    # We do not enable user_notification_mailer 
    for id in ('registrants', 'manager_notification_mailer'):
        action_adapters.append(id)
    obj.actionAdapter = action_adapters
