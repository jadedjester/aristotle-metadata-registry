from django.test import TestCase

import aristotle_mdr.models as models
import aristotle_mdr.perms as perms
import aristotle_mdr.tests.utils as utils
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test.utils import setup_test_environment
setup_test_environment()

class ViewersPostingAndCommenting(TestCase):

    def setUp(self):
        self.wg1 = models.Workgroup.objects.create(name="Test WG 1")
        self.wg2 = models.Workgroup.objects.create(name="Test WG 2")
        self.viewer1 = User.objects.create_user('vicky','','viewer') #viewer 1 always posts
        self.viewer2 = User.objects.create_user('viewer2','','viewer')
        self.manager = User.objects.create_user('mandy','','manger')
        self.wg1.giveRoleToUser('Viewer',self.viewer1)
        self.wg1.giveRoleToUser('Viewer',self.viewer2)
        self.wg1.giveRoleToUser('Manager',self.manager)

    def test_ViewerCanAlterPost(self):
        post = models.DiscussionPost(author=self.viewer1,workgroup=self.wg1,title="test",body="test")
        self.assertTrue(perms.user_can_alter_post(self.viewer1,post))
        self.assertTrue(perms.user_can_alter_post(self.manager,post))
        self.assertFalse(perms.user_can_alter_post(self.viewer2,post))

    def test_ViewerCanAlterComment(self):
        post = models.DiscussionPost(author=self.viewer1,workgroup=self.wg1,title="test",body="test")
        comment = models.DiscussionComment(author=self.viewer2,post=post,body="test")
        self.assertFalse(perms.user_can_alter_comment(self.viewer1,comment))
        self.assertTrue(perms.user_can_alter_comment(self.manager,comment))
        self.assertTrue(perms.user_can_alter_comment(self.viewer2,comment))

class ViewDiscussionPostPage(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(ViewDiscussionPostPage, self).setUp()
        self.viewer2 = User.objects.create_user('viewer2','','viewer') # not in any workgroup
        self.viewer3 = User.objects.create_user('viewer3','','viewer') # not in out "primary testing workgroup" (self.wg1)
        self.wg2.giveRoleToUser('Viewer',self.viewer3)

    def test_viewer_can_see_post_in_workgroup(self):
        post = models.DiscussionPost.objects.create(author=self.viewer,workgroup=self.wg1,title="test",body="test")
        comment = models.DiscussionComment.objects.create(author=self.viewer2,post=post,body="test")
        self.login_viewer()
        response = self.client.get(reverse('aristotle:discussionsPost',args=[post.id]))
        self.assertEqual(response.status_code,200)
        self.wg1.removeRoleFromUser('Viewer',self.viewer)
        response = self.client.get(reverse('aristotle:discussionsPost',args=[post.id]))
        self.assertEqual(response.status_code,403)
