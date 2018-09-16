from django import forms
from mapping.models import LanguagesMapping


class AddMap(forms.Form):
    root_w1 = forms.CharField(
        label='Word 1', max_length=255
    )
    root_w2 = forms.CharField(
        label='Word 2', max_length=255
    )
    w1_type = forms.ChoiceField(
        choices=LanguagesMapping.LANGUAGE_TYPE
    )
    w2_type = forms.ChoiceField(
        choices=LanguagesMapping.LANGUAGE_TYPE
    )

    def clean(self):
        clean_data = super(AddMap, self).clean()
        errors = []

        if not clean_data.get('root_w1'):
            errors.append(
                'Word 1 is required.'
            )

        if not clean_data.get('root_w2'):
            errors.append(
                'Word 2 is required.'
            )

        if not clean_data.get('w1_type'):
            errors.append(
                'Language type for Word 1 is required.'
            )

        if not clean_data.get('w2_type'):
            errors.append(
                'Language type for Word 2 is required.'
            )

        if clean_data.get('w1_type') == clean_data.get('w2_type'):
            errors.append(
                'Select different languages.'
            )

        if errors:
            raise forms.ValidationError(errors, code='invalid')

        w1 = LanguagesMapping.objects.filter(
            root_w=clean_data.get('root_w1'),
            lang_type=clean_data.get('w1_type')
        ).first()
        w2 = LanguagesMapping.objects.filter(
            root_w=clean_data.get('root_w2'),
            lang_type=clean_data.get('w2_type')
        ).first()

        # w1,w2 and mapping ---> error(exists)
        if w1 and w2:
            w1map = w1.mapping.filter(pk=w2.pk)
            w2map = w2.mapping.filter(pk=w1.pk)

            if w1map and w2map:
                errors.append(
                    'Both words already exist in database.'
                )

        if errors:
            raise forms.ValidationError(errors, code='info')

        return clean_data

    def save(self):
        clean_data = super(AddMap, self).clean()
        msg = ''
        success = True

        w1 = LanguagesMapping.objects.filter(
            root_w=clean_data.get('root_w1'),
            lang_type=clean_data.get('w1_type')
        ).first()
        w2 = LanguagesMapping.objects.filter(
            root_w=clean_data.get('root_w2'),
            lang_type=clean_data.get('w2_type')
        ).first()

        # w1,w2 and no mapping ---> map
        # w1,!w2 ---> add w2 and map
        # w1!,w2 ---> add w1 and map
        try:
            if not w1:
                w1 = LanguagesMapping.objects.create(
                    root_w=unicode(clean_data.get('root_w1')),
                    lang_type=clean_data.get('w1_type')
                )
                msg+= u'{} saved.\n'.format(w1.root_w)
            if not w2:
                w2 = LanguagesMapping.objects.create(
                    root_w=unicode(clean_data.get('root_w2')),
                    lang_type=clean_data.get('w2_type')
                )
                msg += u'{} saved.\n'.format(w2.root_w)

            w1map = w1.mapping.filter(pk=w2.pk)
            w2map = w2.mapping.filter(pk=w1.pk)

            if w1map and not w2map:
                w2.mapping.add(w1)
                msg += u'{} mapped to {}.\n'.format(w1.root_w, w2.root_w)
            elif not w1map and w2map:
                w1.mapping.add(w2)
                msg += u'{} mapped to {}.\n'.format(w2.root_w, w1.root_w)
            else:
                w1.mapping.add(w2)
                w2.mapping.add(w1)
                msg += u'Words({}, {}) mapped to each other.\n'.format(
                        w1.root_w, w2.root_w
                    )
        except Exception as e:
            success = False
            msg += u'''
                Failed creation/mapping with error:
                    {}
                Please try again!\n
            '''.format(e)
        return success, msg


class AddWord(forms.Form):
    root_w = forms.CharField(label='Word', max_length=255, required=True)
    w_type = forms.ChoiceField(
        choices=LanguagesMapping.LANGUAGE_TYPE
    )

    def clean(self):
        clean_data = super(AddWord, self).clean()
        errors = []

        if not clean_data.get('root_w'):
            errors.append(
                u'Word is required.'
            )

        rw = LanguagesMapping.objects.filter(
            root_w=clean_data.get('root_w'),
            lang_type=clean_data.get('w_type')
        ).first()

        if rw:
            errors.append(
                u'{} alredy in database.'.format(rw.root_w)
            )

        if errors:
            raise forms.ValidationError(errors, code='invalid')

        return clean_data

    def save(self):
        clean_data = super(AddWord, self).clean()
        success = True
        msg = ''
        try:
            rw = LanguagesMapping.objects.create(
                root_w=unicode(clean_data.get('root_w')),
                lang_type=clean_data.get('w_type')
            )
            msg+= u'{} saved.\n'.format(rw.root_w)
        except Exception as e:
            success = False
            msg += u'''
                Failed creation with error:
                    {}
                Please try again!
            '''.format(e)
        return success, msg
