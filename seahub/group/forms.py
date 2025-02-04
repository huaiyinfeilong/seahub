# Copyright (c) 2012-2016 Seafile Ltd.
# encoding: utf-8
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from seahub.utils import is_valid_dirent_name

from seahub.group.utils import validate_group_name

class MessageForm(forms.Form):
    message = forms.CharField(max_length=2048)

class MessageReplyForm(forms.Form):
    message = forms.CharField(max_length=2048)

class GroupRecommendForm(MessageForm):
    """
    A form used to recommend a file or directory.
    """
    repo_id = forms.CharField(max_length=40)
    path = forms.CharField()
    attach_type = forms.CharField(max_length=5)

class GroupAddForm(forms.Form):
    """
    A form used to add a new group.
    """
    group_name = forms.CharField(max_length=255, error_messages={
            'required': _('Group name can\'t be empty'),
            'max_length': _('Group name is too long (maximum is 255 characters)'),
            })
    def clean_group_name(self):
        group_name = self.cleaned_data['group_name']
        group_name = group_name.strip()
        if not validate_group_name(group_name):
            error_msg = _('Group name can only contain letters, numbers, blank, hyphen or underscore')
            raise forms.ValidationError(error_msg)
        else:
            return group_name

class GroupJoinMsgForm(forms.Form):
    """
    A form used to send group join request message.
    """
    group_join_msg = forms.CharField(max_length=255, error_messages={
            'required': _('Verification message can\'t be empty'),
            'max_length': _('Verification message is too long (maximun is 255 characters)'),
            })

class WikiCreateForm(forms.Form):
    """
    A form used to create wiki.
    """
    repo_name = forms.CharField(max_length=settings.MAX_FILE_NAME,
                                error_messages={
            'required': _('Name can\'t be empty'),
            'max_length': _('Name is too long (maximum is 255 characters)')
            })
    repo_desc = forms.CharField(max_length=100, error_messages={
            'required': _('Description can\'t be empty'),
            'max_length': _('Description is too long (maximum is 100 characters)')
            })

    def clean_repo_name(self):
        repo_name = self.cleaned_data['repo_name']
        if not is_valid_dirent_name(repo_name):
            error_msg = _('"%s" is not a valid name') % repo_name
            raise forms.ValidationError(error_msg)
        else:
            return repo_name


class BatchAddMembersForm(forms.Form):
    """
    Form for importing group members from CSV file.
    """
    file = forms.FileField()
