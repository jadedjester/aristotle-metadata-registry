# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

# The extends the name from a short "CharField" to the much longer TextField

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Measure.name'
        db.alter_column(u'aristotle_mdr_measure', 'name', self.gf('django.db.models.fields.TextField')())

        # Changing field 'RegistrationAuthority.name'
        db.alter_column(u'aristotle_mdr_registrationauthority', 'name', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Workgroup.name'
        db.alter_column(u'aristotle_mdr_workgroup', 'name', self.gf('django.db.models.fields.TextField')())

        # Changing field 'RepresentationClass.name'
        db.alter_column(u'aristotle_mdr_representationclass', 'name', self.gf('django.db.models.fields.TextField')())

        # Changing field 'UnitOfMeasure.name'
        db.alter_column(u'aristotle_mdr_unitofmeasure', 'name', self.gf('django.db.models.fields.TextField')())

        # Changing field '_concept.name'
        db.alter_column(u'aristotle_mdr__concept', 'name', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'Measure.name'
        db.alter_column(u'aristotle_mdr_measure', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'RegistrationAuthority.name'
        db.alter_column(u'aristotle_mdr_registrationauthority', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Workgroup.name'
        db.alter_column(u'aristotle_mdr_workgroup', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'RepresentationClass.name'
        db.alter_column(u'aristotle_mdr_representationclass', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'UnitOfMeasure.name'
        db.alter_column(u'aristotle_mdr_unitofmeasure', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field '_concept.name'
        db.alter_column(u'aristotle_mdr__concept', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        u'aristotle_mdr._concept': {
            'Meta': {'object_name': '_concept'},
            '_is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            '_is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'readyToReview': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'workgroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'items'", 'to': u"orm['aristotle_mdr.Workgroup']"})
        },
        u'aristotle_mdr.conceptualdomain': {
            'Meta': {'object_name': 'ConceptualDomain'},
            u'_concept_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aristotle_mdr._concept']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'originURI': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'references': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'responsibleOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submittingOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'superseded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'supersedes'", 'null': 'True', 'to': u"orm['aristotle_mdr.ConceptualDomain']"}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.dataelement': {
            'Meta': {'object_name': 'DataElement'},
            u'_concept_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aristotle_mdr._concept']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'dataElementConcept': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.DataElementConcept']", 'null': 'True', 'blank': 'True'}),
            'originURI': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'references': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'responsibleOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submittingOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'superseded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'supersedes'", 'null': 'True', 'to': u"orm['aristotle_mdr.DataElement']"}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'valueDomain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.ValueDomain']", 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.dataelementconcept': {
            'Meta': {'object_name': 'DataElementConcept'},
            u'_concept_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aristotle_mdr._concept']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'conceptualDomain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.ConceptualDomain']", 'null': 'True', 'blank': 'True'}),
            'objectClass': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.ObjectClass']", 'null': 'True', 'blank': 'True'}),
            'originURI': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'property': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.Property']", 'null': 'True', 'blank': 'True'}),
            'references': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'responsibleOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submittingOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'superseded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'supersedes'", 'null': 'True', 'to': u"orm['aristotle_mdr.DataElementConcept']"}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.dataelementderivation': {
            'Meta': {'object_name': 'DataElementDerivation'},
            u'_concept_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aristotle_mdr._concept']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'derivation_rule': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'derives': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'derived_from'", 'to': u"orm['aristotle_mdr.DataElement']"}),
            'inputs': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'input_to_derivation'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['aristotle_mdr.DataElement']"}),
            'originURI': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'references': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'responsibleOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submittingOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'superseded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'supersedes'", 'null': 'True', 'to': u"orm['aristotle_mdr.DataElementDerivation']"}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.datatype': {
            'Meta': {'object_name': 'DataType'},
            u'_concept_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aristotle_mdr._concept']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'originURI': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'references': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'responsibleOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submittingOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'superseded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'supersedes'", 'null': 'True', 'to': u"orm['aristotle_mdr.DataType']"}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.discussioncomment': {
            'Meta': {'ordering': "[u'-modified']", 'object_name': 'DiscussionComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'comments'", 'to': u"orm['aristotle_mdr.DiscussionPost']"})
        },
        u'aristotle_mdr.discussionpost': {
            'Meta': {'ordering': "[u'-modified']", 'object_name': 'DiscussionPost'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'relatedItems': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'relatedDiscussions'", 'blank': 'True', 'to': u"orm['aristotle_mdr._concept']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'workgroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'discussions'", 'to': u"orm['aristotle_mdr.Workgroup']"})
        },
        u'aristotle_mdr.glossaryadditionaldefinition': {
            'Meta': {'unique_together': "((u'glossaryItem', u'registrationAuthority'),)", 'object_name': 'GlossaryAdditionalDefinition'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'glossaryItem': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'alternate_definitions'", 'to': u"orm['aristotle_mdr.GlossaryItem']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registrationAuthority': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.RegistrationAuthority']"})
        },
        u'aristotle_mdr.glossaryitem': {
            'Meta': {'object_name': 'GlossaryItem'},
            u'_concept_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aristotle_mdr._concept']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'originURI': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'references': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'responsibleOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submittingOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'superseded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'supersedes'", 'null': 'True', 'to': u"orm['aristotle_mdr.GlossaryItem']"}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.measure': {
            'Meta': {'object_name': 'Measure'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'aristotle_mdr.objectclass': {
            'Meta': {'object_name': 'ObjectClass'},
            u'_concept_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aristotle_mdr._concept']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'originURI': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'references': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'responsibleOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submittingOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'superseded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'supersedes'", 'null': 'True', 'to': u"orm['aristotle_mdr.ObjectClass']"}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.package': {
            'Meta': {'object_name': 'Package'},
            u'_concept_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aristotle_mdr._concept']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'packages'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['aristotle_mdr._concept']"}),
            'originURI': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'references': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'responsibleOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submittingOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'superseded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'supersedes'", 'null': 'True', 'to': u"orm['aristotle_mdr.Package']"}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.permissiblevalue': {
            'Meta': {'ordering': "[u'order']", 'object_name': 'PermissibleValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meaning': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'valueDomain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'permissibleValues'", 'to': u"orm['aristotle_mdr.ValueDomain']"})
        },
        u'aristotle_mdr.possumprofile': {
            'Meta': {'object_name': 'PossumProfile'},
            'favourites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'favourited_by'", 'blank': 'True', 'to': u"orm['aristotle_mdr._concept']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'savedActiveWorkgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.Workgroup']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'aristotle_mdr.property': {
            'Meta': {'object_name': 'Property'},
            u'_concept_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aristotle_mdr._concept']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'originURI': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'references': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'responsibleOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submittingOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'superseded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'supersedes'", 'null': 'True', 'to': u"orm['aristotle_mdr.Property']"}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.registrationauthority': {
            'Meta': {'object_name': 'RegistrationAuthority'},
            'candidate': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incomplete': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'locked_state': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'registrationauthority_manager_in'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'notprogressed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'preferred': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'public_state': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'qualified': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'recorded': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'registrars': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'registrar_in'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'retired': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'standard': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'superseded': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'aristotle_mdr.representationclass': {
            'Meta': {'object_name': 'RepresentationClass'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'aristotle_mdr.status': {
            'Meta': {'unique_together': "((u'concept', u'registrationAuthority'),)", 'object_name': 'Status'},
            'changeDetails': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'concept': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'statuses'", 'to': u"orm['aristotle_mdr._concept']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inDictionary': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'registrationAuthority': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.RegistrationAuthority']"}),
            'registrationDate': ('django.db.models.fields.DateField', [], {}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'aristotle_mdr.supplementaryvalue': {
            'Meta': {'ordering': "[u'order']", 'object_name': 'SupplementaryValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meaning': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'valueDomain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'supplementaryValues'", 'to': u"orm['aristotle_mdr.ValueDomain']"})
        },
        u'aristotle_mdr.unitofmeasure': {
            'Meta': {'object_name': 'UnitOfMeasure'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.Measure']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.valuedomain': {
            'Meta': {'object_name': 'ValueDomain'},
            u'_concept_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aristotle_mdr._concept']", 'unique': 'True', 'primary_key': 'True'}),
            'comments': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'conceptualDomain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.ConceptualDomain']", 'null': 'True', 'blank': 'True'}),
            'dataType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.DataType']", 'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'maximumLength': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'originURI': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'references': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'representationClass': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.RepresentationClass']", 'null': 'True', 'blank': 'True'}),
            'responsibleOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submittingOrganisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'superseded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'supersedes'", 'null': 'True', 'to': u"orm['aristotle_mdr.ValueDomain']"}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'unitOfMeasure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aristotle_mdr.UnitOfMeasure']", 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'aristotle_mdr.workgroup': {
            'Meta': {'object_name': 'Workgroup'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'workgroup_manager_in'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'registrationAuthorities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'workgroups'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['aristotle_mdr.RegistrationAuthority']"}),
            'stewards': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'steward_in'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'submitters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'submitter_in'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'viewers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'viewer_in'", 'blank': 'True', 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['aristotle_mdr']