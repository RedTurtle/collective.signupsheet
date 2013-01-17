# -*- coding: utf-8 -*-
from cStringIO import StringIO
import csv

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


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

        #updates schema if not done before export
        # BBB
        #self.atse_updateManagedSchema(portal_type=export_type,
        #                              schema_template='signupsheet_schema_editor')

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
        setheader('Content-Disposition', 'filename=%s.csv' % self.context.getId())
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
            objs = self.listFolderContents(
                contentFilter={'portal_type': export_type}
            )

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
            for obj in objs:
                row = []
                #code to append creationDate since it is not part of the fields list
                row.append(obj.CreationDate())
                for fieldname in fields:
                    if fieldname.find('.') != -1:
                        fieldname, key = fieldname.split('.')
                    try:
                        field = obj.Schema()[fieldname]
                        value = field.getAccessor(obj)()
                        row.append(value)
                    except KeyError:
                        row.append('')
                rows.append(row)
            rows[0].insert(0, 'date')
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


class ViewRegistrants(BrowserView, Common):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getRegistrants(self):
        """
        get all the registrants under this form
        """
        form = self.context
        adapters = form.actionAdapter
        registrants_folder = None
        for ad in adapters:
            #I will take only the first object I will find in form
            if form[ad].portal_type == 'FormSaveData2ContentAdapter':
                registrants_folder = form[ad]
                break

        if not registrants_folder:
            return []

        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(path={'query': '/'.join(registrants_folder.getPhysicalPath()),
                             'depth': 1})

        registrants = []
        for brain in brains:
            registrants.append(brain.getObject())

        return registrants
