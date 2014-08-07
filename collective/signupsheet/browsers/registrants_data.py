# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getUtility

from collective.signupsheet import signupsheetMessageFactory as _
from collective.signupsheet.interfaces import IGetRegistrants

from cStringIO import StringIO
import csv
import zope


class Common(object):

    def registrantFieldNames(self):
        """
        Select the field from pfg and return a list with his names
        """
        fields = self.context.fgFields(self.request)
        field_names = []
        for field in fields:
            field_names.append(field.getName())
        return field_names

    def get_registrants(self):
        form = self.context
        utility = getUtility(IGetRegistrants)
        return utility.get_registrants(form)

    def get_registrants_folder(self):
        form = self.context
        utility = getUtility(IGetRegistrants)
        folder = utility.get_registrants_folder(form)
        return folder

    def get_registrants_folder_url(self):
        return self.get_registrants_folder().absolute_url()


class RegistrantDataExport(BrowserView, Common):

    template = ViewPageTemplateFile('registrants_data_export.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if not 'exportCSV' in self.request.keys():
            return self.template()
        return self.exportCSV(fields=self.request.form.get('fields', None),
                              delimiter=self.request.form.get('delimiter',
                                                              'semicolon'))

    def exportCSV(self, fields=None, coding=None, delimiter='semicolon'):
        """
        Exports a list of objs as a CSV file.  Wraps generateCSV.
        """

        result = self.generateCSV(fields=fields, delimiter=delimiter)

        # encode the result
        charset = self._site_encoding()
        if coding:
            result = result.decode(charset).encode(coding)
        else:
            coding = charset

        # set headers and return
        setheader = self.request.RESPONSE.setHeader
        setheader('Content-Length', len(result))
        setheader('Content-Type',
            'text/x-comma-separated-values; charset=%s' % coding)
        setheader('Content-Disposition',
                  'attachment; filename=%s.csv' % self.context.getId())
        return result

    def generateCSV(self, objs=None, fields=None, delimiter='semicolon',
                  quote_char='double_quote', coding=None,
                  export_type='Registrant'):

        """
        Exports a list of objs as a CSV file.
        objs: if None it exports all registrants in the folder.
        fields: field names to export
        """

        #container = self.unrestrictedTraverse(
        #   self.REQUEST.get('current_path'))
        if objs is None:
            objs = self.get_registrants()

        delim_map = {
            'tabulator': '\t',
            'semicolon': ';',
            'colon': ':',
            'comma': ',',
            'space': ' ',
        }

        delimiter = delim_map[delimiter]
        quote_map = {'double_quote': '"', 'single_quote': "'", }
        quote_char = quote_map[quote_char]

        # generate result
        if fields is None:
            result = ''
        else:
            rows = [fields]
            pwf = self.context.portal_workflow
            for obj in objs:
                row = []
                #code to append creationDate since it is not part of the fields list
                row.append(obj.CreationDate())
                row.append(obj.getId())
                for fieldname in fields:
                    if fieldname.find('.') != -1:
                        fieldname, key = fieldname.split('.')
                    try:
                        field = obj.Schema()[fieldname]
                        value = field.getAccessor(obj)()
                        row.append(value)
                    except KeyError:
                        row.append('')
                row.append(self.translate(pwf.getInfoFor(obj, 'review_state')).encode('utf-8'))
                rows.append(row)
            rows[0].insert(0, 'id')
            rows[0].insert(0, 'date')
            rows[0].append('review_state')
            # convert lists to csv string
            ramdisk = StringIO()
            writer = csv.writer(ramdisk, delimiter=delimiter)
            writer.writerows(rows)
            result = ramdisk.getvalue()
            ramdisk.close()

        return result

    def _site_encoding(self):
        "Returns the site encoding"
        putils = getToolByName(self, 'plone_utils', None)
        if putils is not None:
            return putils.getSiteEncoding()
        else:
            portal_properties = self.portal_properties
            site_props = portal_properties.site_properties
            return site_props.default_charset or 'utf-8'

    def translate(self, value):
        return zope.i18n.translate(_(value), context=self.request)


class ViewRegistrants(BrowserView, Common):

    def __init__(self, context, request):
        self.context = context
        self.request = request


class ImportRegistrants(BrowserView, Common):

    template = ViewPageTemplateFile('import_registrants.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if not 'importRegistrants' in self.request.form:
            return self.template()
        else:
            csvfile = self.request.get('uploaded_csv', None)
            if not csvfile:
                response = _("No file loaded")
                return self.template(**{'status': 'error',
                                        'import_response': response})
            else:
                lines = csvfile.readlines()
                #clean the line
                reg_folder = self.get_registrants_folder()
                # We emulate on success
                csvfields = lines[0].replace('\n', '').replace('\r', '').split(';')
                form_fields = self.context._getFieldObjects()

                for line in lines[1:len(lines)]:
                    line_values = line.replace('\n', '').replace('\r', '').split(';')
                    for index in range(0, len(csvfields)):
                        self.request.form[csvfields[index]] = line_values[index]
                    self.request.form['last_referer'] = self.context.absolute_url()
                    reg_folder.onSuccess(form_fields, self.request)
                translator = zope.i18n.translate
                response = translator(_(u"registrants_imported",
                           default=u"Created ${registrants} new registrant",
                           mapping={'registrants': len(lines) - 1}),
                        context=self.context.REQUEST)
                return self.template(**{'status': 'done',
                                        'import_response': response})
