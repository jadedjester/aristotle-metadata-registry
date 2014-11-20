# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RegistrationAuthority'
        db.create_table(u'aristotle_mdr_registrationauthority', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('tinymce.models.HTMLField')()),
            ('locked_state', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('public_state', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('notprogressed', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('incomplete', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('candidate', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('recorded', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('qualified', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('standard', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('preferred', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('superseded', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('retired', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'aristotle_mdr', ['RegistrationAuthority'])

        # Adding M2M table for field managers on 'RegistrationAuthority'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_registrationauthority_managers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registrationauthority', models.ForeignKey(orm[u'aristotle_mdr.registrationauthority'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['registrationauthority_id', 'user_id'])

        # Adding M2M table for field registrars on 'RegistrationAuthority'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_registrationauthority_registrars')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registrationauthority', models.ForeignKey(orm[u'aristotle_mdr.registrationauthority'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['registrationauthority_id', 'user_id'])

        # Adding model 'Workgroup'
        db.create_table(u'aristotle_mdr_workgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('tinymce.models.HTMLField')()),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'aristotle_mdr', ['Workgroup'])

        # Adding M2M table for field managers on 'Workgroup'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_workgroup_managers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workgroup', models.ForeignKey(orm[u'aristotle_mdr.workgroup'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workgroup_id', 'user_id'])

        # Adding M2M table for field registrationAuthorities on 'Workgroup'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_workgroup_registrationAuthorities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workgroup', models.ForeignKey(orm[u'aristotle_mdr.workgroup'], null=False)),
            ('registrationauthority', models.ForeignKey(orm[u'aristotle_mdr.registrationauthority'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workgroup_id', 'registrationauthority_id'])

        # Adding M2M table for field viewers on 'Workgroup'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_workgroup_viewers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workgroup', models.ForeignKey(orm[u'aristotle_mdr.workgroup'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workgroup_id', 'user_id'])

        # Adding M2M table for field submitters on 'Workgroup'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_workgroup_submitters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workgroup', models.ForeignKey(orm[u'aristotle_mdr.workgroup'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workgroup_id', 'user_id'])

        # Adding M2M table for field stewards on 'Workgroup'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_workgroup_stewards')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workgroup', models.ForeignKey(orm[u'aristotle_mdr.workgroup'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workgroup_id', 'user_id'])

        # Adding model 'DiscussionPost'
        db.create_table(u'aristotle_mdr_discussionpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('workgroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'discussions', to=orm['aristotle_mdr.Workgroup'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'aristotle_mdr', ['DiscussionPost'])

        # Adding M2M table for field relatedItems on 'DiscussionPost'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_discussionpost_relatedItems')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('discussionpost', models.ForeignKey(orm[u'aristotle_mdr.discussionpost'], null=False)),
            ('_concept', models.ForeignKey(orm[u'aristotle_mdr._concept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['discussionpost_id', '_concept_id'])

        # Adding model 'DiscussionComment'
        db.create_table(u'aristotle_mdr_discussioncomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'comments', to=orm['aristotle_mdr.DiscussionPost'])),
        ))
        db.send_create_signal(u'aristotle_mdr', ['DiscussionComment'])

        # Adding model '_concept'
        db.create_table(u'aristotle_mdr__concept', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('tinymce.models.HTMLField')()),
            ('readyToReview', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('workgroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'items', to=orm['aristotle_mdr.Workgroup'])),
            ('_is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_is_locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'aristotle_mdr', ['_concept'])

        # Adding model 'Status'
        db.create_table(u'aristotle_mdr_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('concept', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'statuses', to=orm['aristotle_mdr._concept'])),
            ('registrationAuthority', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.RegistrationAuthority'])),
            ('changeDetails', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('inDictionary', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('registrationDate', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'aristotle_mdr', ['Status'])

        # Adding unique constraint on 'Status', fields ['concept', 'registrationAuthority']
        db.create_unique(u'aristotle_mdr_status', ['concept_id', 'registrationAuthority_id'])

        # Adding model 'ObjectClass'
        db.create_table(u'aristotle_mdr_objectclass', (
            (u'_concept_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aristotle_mdr._concept'], unique=True, primary_key=True)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('references', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('originURI', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comments', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('submittingOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('responsibleOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('superseded_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'supersedes', null=True, to=orm['aristotle_mdr.ObjectClass'])),
        ))
        db.send_create_signal(u'aristotle_mdr', ['ObjectClass'])

        # Adding model 'Property'
        db.create_table(u'aristotle_mdr_property', (
            (u'_concept_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aristotle_mdr._concept'], unique=True, primary_key=True)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('references', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('originURI', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comments', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('submittingOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('responsibleOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('superseded_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'supersedes', null=True, to=orm['aristotle_mdr.Property'])),
        ))
        db.send_create_signal(u'aristotle_mdr', ['Property'])

        # Adding model 'Measure'
        db.create_table(u'aristotle_mdr_measure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('tinymce.models.HTMLField')()),
        ))
        db.send_create_signal(u'aristotle_mdr', ['Measure'])

        # Adding model 'UnitOfMeasure'
        db.create_table(u'aristotle_mdr_unitofmeasure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('tinymce.models.HTMLField')()),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.Measure'])),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'aristotle_mdr', ['UnitOfMeasure'])

        # Adding model 'DataType'
        db.create_table(u'aristotle_mdr_datatype', (
            (u'_concept_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aristotle_mdr._concept'], unique=True, primary_key=True)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('references', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('originURI', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comments', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('submittingOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('responsibleOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('superseded_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'supersedes', null=True, to=orm['aristotle_mdr.DataType'])),
        ))
        db.send_create_signal(u'aristotle_mdr', ['DataType'])

        # Adding model 'ConceptualDomain'
        db.create_table(u'aristotle_mdr_conceptualdomain', (
            (u'_concept_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aristotle_mdr._concept'], unique=True, primary_key=True)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('references', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('originURI', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comments', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('submittingOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('responsibleOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('superseded_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'supersedes', null=True, to=orm['aristotle_mdr.ConceptualDomain'])),
        ))
        db.send_create_signal(u'aristotle_mdr', ['ConceptualDomain'])

        # Adding model 'RepresentationClass'
        db.create_table(u'aristotle_mdr_representationclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('tinymce.models.HTMLField')()),
        ))
        db.send_create_signal(u'aristotle_mdr', ['RepresentationClass'])

        # Adding model 'ValueDomain'
        db.create_table(u'aristotle_mdr_valuedomain', (
            (u'_concept_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aristotle_mdr._concept'], unique=True, primary_key=True)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('references', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('originURI', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comments', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('submittingOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('responsibleOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('superseded_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'supersedes', null=True, to=orm['aristotle_mdr.ValueDomain'])),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('maximumLength', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('unitOfMeasure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.UnitOfMeasure'], null=True, blank=True)),
            ('dataType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.DataType'], null=True, blank=True)),
            ('conceptualDomain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.ConceptualDomain'], null=True, blank=True)),
            ('representationClass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.RepresentationClass'], null=True, blank=True)),
        ))
        db.send_create_signal(u'aristotle_mdr', ['ValueDomain'])

        # Adding model 'PermissibleValue'
        db.create_table(u'aristotle_mdr_permissiblevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('meaning', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('valueDomain', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'permissibleValues', to=orm['aristotle_mdr.ValueDomain'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'aristotle_mdr', ['PermissibleValue'])

        # Adding model 'SupplementaryValue'
        db.create_table(u'aristotle_mdr_supplementaryvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('meaning', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('valueDomain', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'supplementaryValues', to=orm['aristotle_mdr.ValueDomain'])),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'aristotle_mdr', ['SupplementaryValue'])

        # Adding model 'DataElementConcept'
        db.create_table(u'aristotle_mdr_dataelementconcept', (
            (u'_concept_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aristotle_mdr._concept'], unique=True, primary_key=True)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('references', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('originURI', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comments', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('submittingOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('responsibleOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('superseded_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'supersedes', null=True, to=orm['aristotle_mdr.DataElementConcept'])),
            ('objectClass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.ObjectClass'], null=True, blank=True)),
            ('property', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.Property'], null=True, blank=True)),
            ('conceptualDomain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.ConceptualDomain'], null=True, blank=True)),
        ))
        db.send_create_signal(u'aristotle_mdr', ['DataElementConcept'])

        # Adding model 'DataElement'
        db.create_table(u'aristotle_mdr_dataelement', (
            (u'_concept_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aristotle_mdr._concept'], unique=True, primary_key=True)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('references', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('originURI', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comments', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('submittingOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('responsibleOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('superseded_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'supersedes', null=True, to=orm['aristotle_mdr.DataElement'])),
            ('dataElementConcept', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.DataElementConcept'], null=True, blank=True)),
            ('valueDomain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.ValueDomain'], null=True, blank=True)),
        ))
        db.send_create_signal(u'aristotle_mdr', ['DataElement'])

        # Adding model 'DataElementDerivation'
        db.create_table(u'aristotle_mdr_dataelementderivation', (
            (u'_concept_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aristotle_mdr._concept'], unique=True, primary_key=True)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('references', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('originURI', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comments', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('submittingOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('responsibleOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('superseded_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'supersedes', null=True, to=orm['aristotle_mdr.DataElementDerivation'])),
            ('derives', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'derived_from', to=orm['aristotle_mdr.DataElement'])),
            ('derivation_rule', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'aristotle_mdr', ['DataElementDerivation'])

        # Adding M2M table for field inputs on 'DataElementDerivation'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_dataelementderivation_inputs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dataelementderivation', models.ForeignKey(orm[u'aristotle_mdr.dataelementderivation'], null=False)),
            ('dataelement', models.ForeignKey(orm[u'aristotle_mdr.dataelement'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dataelementderivation_id', 'dataelement_id'])

        # Adding model 'Package'
        db.create_table(u'aristotle_mdr_package', (
            (u'_concept_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aristotle_mdr._concept'], unique=True, primary_key=True)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('references', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('originURI', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comments', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('submittingOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('responsibleOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('superseded_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'supersedes', null=True, to=orm['aristotle_mdr.Package'])),
        ))
        db.send_create_signal(u'aristotle_mdr', ['Package'])

        # Adding M2M table for field items on 'Package'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_package_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm[u'aristotle_mdr.package'], null=False)),
            ('_concept', models.ForeignKey(orm[u'aristotle_mdr._concept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['package_id', '_concept_id'])

        # Adding model 'GlossaryItem'
        db.create_table(u'aristotle_mdr_glossaryitem', (
            (u'_concept_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aristotle_mdr._concept'], unique=True, primary_key=True)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('synonyms', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('references', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('originURI', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comments', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('submittingOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('responsibleOrganisation', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('superseded_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'supersedes', null=True, to=orm['aristotle_mdr.GlossaryItem'])),
        ))
        db.send_create_signal(u'aristotle_mdr', ['GlossaryItem'])

        # Adding model 'GlossaryAdditionalDefinition'
        db.create_table(u'aristotle_mdr_glossaryadditionaldefinition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('glossaryItem', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'alternate_definitions', to=orm['aristotle_mdr.GlossaryItem'])),
            ('registrationAuthority', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.RegistrationAuthority'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'aristotle_mdr', ['GlossaryAdditionalDefinition'])

        # Adding unique constraint on 'GlossaryAdditionalDefinition', fields ['glossaryItem', 'registrationAuthority']
        db.create_unique(u'aristotle_mdr_glossaryadditionaldefinition', ['glossaryItem_id', 'registrationAuthority_id'])

        # Adding model 'PossumProfile'
        db.create_table(u'aristotle_mdr_possumprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name=u'profile', unique=True, to=orm['auth.User'])),
            ('savedActiveWorkgroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aristotle_mdr.Workgroup'], null=True, blank=True)),
        ))
        db.send_create_signal(u'aristotle_mdr', ['PossumProfile'])

        # Adding M2M table for field favourites on 'PossumProfile'
        m2m_table_name = db.shorten_name(u'aristotle_mdr_possumprofile_favourites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('possumprofile', models.ForeignKey(orm[u'aristotle_mdr.possumprofile'], null=False)),
            ('_concept', models.ForeignKey(orm[u'aristotle_mdr._concept'], null=False))
        ))
        db.create_unique(m2m_table_name, ['possumprofile_id', '_concept_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'GlossaryAdditionalDefinition', fields ['glossaryItem', 'registrationAuthority']
        db.delete_unique(u'aristotle_mdr_glossaryadditionaldefinition', ['glossaryItem_id', 'registrationAuthority_id'])

        # Removing unique constraint on 'Status', fields ['concept', 'registrationAuthority']
        db.delete_unique(u'aristotle_mdr_status', ['concept_id', 'registrationAuthority_id'])

        # Deleting model 'RegistrationAuthority'
        db.delete_table(u'aristotle_mdr_registrationauthority')

        # Removing M2M table for field managers on 'RegistrationAuthority'
        db.delete_table(db.shorten_name(u'aristotle_mdr_registrationauthority_managers'))

        # Removing M2M table for field registrars on 'RegistrationAuthority'
        db.delete_table(db.shorten_name(u'aristotle_mdr_registrationauthority_registrars'))

        # Deleting model 'Workgroup'
        db.delete_table(u'aristotle_mdr_workgroup')

        # Removing M2M table for field managers on 'Workgroup'
        db.delete_table(db.shorten_name(u'aristotle_mdr_workgroup_managers'))

        # Removing M2M table for field registrationAuthorities on 'Workgroup'
        db.delete_table(db.shorten_name(u'aristotle_mdr_workgroup_registrationAuthorities'))

        # Removing M2M table for field viewers on 'Workgroup'
        db.delete_table(db.shorten_name(u'aristotle_mdr_workgroup_viewers'))

        # Removing M2M table for field submitters on 'Workgroup'
        db.delete_table(db.shorten_name(u'aristotle_mdr_workgroup_submitters'))

        # Removing M2M table for field stewards on 'Workgroup'
        db.delete_table(db.shorten_name(u'aristotle_mdr_workgroup_stewards'))

        # Deleting model 'DiscussionPost'
        db.delete_table(u'aristotle_mdr_discussionpost')

        # Removing M2M table for field relatedItems on 'DiscussionPost'
        db.delete_table(db.shorten_name(u'aristotle_mdr_discussionpost_relatedItems'))

        # Deleting model 'DiscussionComment'
        db.delete_table(u'aristotle_mdr_discussioncomment')

        # Deleting model '_concept'
        db.delete_table(u'aristotle_mdr__concept')

        # Deleting model 'Status'
        db.delete_table(u'aristotle_mdr_status')

        # Deleting model 'ObjectClass'
        db.delete_table(u'aristotle_mdr_objectclass')

        # Deleting model 'Property'
        db.delete_table(u'aristotle_mdr_property')

        # Deleting model 'Measure'
        db.delete_table(u'aristotle_mdr_measure')

        # Deleting model 'UnitOfMeasure'
        db.delete_table(u'aristotle_mdr_unitofmeasure')

        # Deleting model 'DataType'
        db.delete_table(u'aristotle_mdr_datatype')

        # Deleting model 'ConceptualDomain'
        db.delete_table(u'aristotle_mdr_conceptualdomain')

        # Deleting model 'RepresentationClass'
        db.delete_table(u'aristotle_mdr_representationclass')

        # Deleting model 'ValueDomain'
        db.delete_table(u'aristotle_mdr_valuedomain')

        # Deleting model 'PermissibleValue'
        db.delete_table(u'aristotle_mdr_permissiblevalue')

        # Deleting model 'SupplementaryValue'
        db.delete_table(u'aristotle_mdr_supplementaryvalue')

        # Deleting model 'DataElementConcept'
        db.delete_table(u'aristotle_mdr_dataelementconcept')

        # Deleting model 'DataElement'
        db.delete_table(u'aristotle_mdr_dataelement')

        # Deleting model 'DataElementDerivation'
        db.delete_table(u'aristotle_mdr_dataelementderivation')

        # Removing M2M table for field inputs on 'DataElementDerivation'
        db.delete_table(db.shorten_name(u'aristotle_mdr_dataelementderivation_inputs'))

        # Deleting model 'Package'
        db.delete_table(u'aristotle_mdr_package')

        # Removing M2M table for field items on 'Package'
        db.delete_table(db.shorten_name(u'aristotle_mdr_package_items'))

        # Deleting model 'GlossaryItem'
        db.delete_table(u'aristotle_mdr_glossaryitem')

        # Deleting model 'GlossaryAdditionalDefinition'
        db.delete_table(u'aristotle_mdr_glossaryadditionaldefinition')

        # Deleting model 'PossumProfile'
        db.delete_table(u'aristotle_mdr_possumprofile')

        # Removing M2M table for field favourites on 'PossumProfile'
        db.delete_table(db.shorten_name(u'aristotle_mdr_possumprofile_favourites'))


    models = {
        u'aristotle_mdr._concept': {
            'Meta': {'object_name': '_concept'},
            '_is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            '_is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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