from django.test import TestCase

import aristotle_mdr.models as models
import aristotle_mdr.perms as perms
import aristotle_mdr.tests.utils as utils
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test.utils import setup_test_environment
setup_test_environment()

class PostingAndCommentingAtObjectLevel(TestCase):

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

class WorkgroupMembersCanMakePostsAndComments(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(WorkgroupMembersCanMakePostsAndComments, self).setUp()
        self.viewer2 = User.objects.create_user('viewer2','','viewer') # not in any workgroup
        self.viewer3 = User.objects.create_user('viewer3','','viewer') # not in our "primary testing workgroup" (self.wg1)
        self.wg1.giveRoleToUser('Viewer',self.viewer3)
        self.wg2 = models.Workgroup.objects.create(name="Test WG 2")

    def can_the_current_logged_in_user_post(self):
        response = self.client.get(reverse('aristotle:discussionsNew'),)
        self.assertEqual(response.status_code,200)

        response = self.client.post(reverse('aristotle:discussionsNew'),
            {
                'title':"New post that will not work",
                'body':"I am not a member of this workgroup, so this shouldn't work.",
                'workgroup': self.wg2.id
            }
        )
        self.assertEqual(self.wg2.discussions.count(),0)
        self.assertEqual(response.status_code,200)

        self.assertEqual(self.wg1.discussions.count(),0)
        forbidden_item = models.ObjectClass.objects.create(name="OC2",workgroup=self.wg2)
        response = self.client.post(reverse('aristotle:discussionsNew'),
            {
                'title':"New post that will not work",
                'body':"I am a member of this workgroup but am trying to post about an item that I'm not allowed to see.",
                'workgroup': self.wg1.id,
                'relatedItems': [forbidden_item.id]
            }
        )
        # We allow the request to add the forbidden_item to pass, but the item is never attached.
        self.assertEqual(self.wg1.discussions.count(),1)
        self.assertEqual(self.wg1.discussions.first().relatedItems.count(),0)
        self.assertEqual(response.status_code,302)

        response = self.client.post(reverse('aristotle:discussionsNew'),
            {
                'title':"New post that will work",
                'body':"I am a member of this workgroup.",
                'workgroup': self.wg1.id
            }
        )
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.wg1.discussions.count(),2)

    def test_viewer_can_post_in_workgroup(self):
        self.login_viewer()
        self.can_the_current_logged_in_user_post()

    def test_editor_can_post_in_workgroup(self):
        self.login_editor()
        self.can_the_current_logged_in_user_post()

    def can_the_current_logged_in_user_comment(self):
        p1 = models.DiscussionPost.objects.create(author=self.su,workgroup=self.wg1,title="test",body="test")
        p2 = models.DiscussionPost.objects.create(author=self.su,workgroup=self.wg2,title="test",body="test")

        response = self.client.get(reverse('aristotle:discussionsPost',args=[p1.id]))
        self.assertEqual(response.status_code,200)
        response = self.client.get(reverse('aristotle:discussionsPost',args=[p2.id]))
        self.assertEqual(response.status_code,403)

        response = self.client.post(reverse('aristotle:discussionsPostNewComment',args=[p2.id]),
            {'body':"I am not a member of this workgroup, so this shouldn't work."}
        )
        self.assertEqual(p2.comments.count(),0)
        self.assertEqual(response.status_code,403)

        response = self.client.post(reverse('aristotle:discussionsPostNewComment',args=[p1.id]),
            {'body':"I am a member of this workgroup, so I can comment."}
        )
        self.assertEqual(p1.comments.count(),1)
        c = p1.comments.first().id
        self.assertRedirects(response,reverse('aristotle:discussionsPost',args=[p1.id])+"#comment_%s"%c )

    def test_viewer_can_comment_in_workgroup(self):
        self.login_viewer()
        self.can_the_current_logged_in_user_comment()
    def test_editor_can_comment_in_workgroup(self):
        self.login_editor()
        self.can_the_current_logged_in_user_comment()


class ViewDiscussionPostPage(utils.LoggedInViewPages,TestCase):
    def setUp(self):
        super(ViewDiscussionPostPage, self).setUp()
        self.viewer2 = User.objects.create_user('viewer2','','viewer') # not in any workgroup
        self.viewer3 = User.objects.create_user('viewer3','','viewer') # not in our "primary testing workgroup" (self.wg1)
        self.wg2.giveRoleToUser('Viewer',self.viewer3)

    def test_member_can_see_posts(self):
        self.login_viewer()
        self.wg3 = models.Workgroup.objects.create(name="Test WG 3")
        self.wg3.giveRoleToUser('Viewer',self.viewer)

        p1 = models.DiscussionPost.objects.create(author=self.su,workgroup=self.wg1,title="test",body="test")
        p2 = models.DiscussionPost.objects.create(author=self.su,workgroup=self.wg1,title="test",body="test")
        p3 = models.DiscussionPost.objects.create(author=self.su,workgroup=self.wg3,title="test",body="test")

        response = self.client.get(reverse('aristotle:discussionsWorkgroup',args=[self.wg1.id]))
        self.assertEqual(len(response.context['discussions']),2)
        self.assertListEqual(list(response.context['discussions'].all()),[p2,p1])
        response = self.client.get(reverse('aristotle:discussions'))
        self.assertEqual(len(response.context['discussions']),3)
        self.assertListEqual(list(response.context['discussions']),[p3,p2,p1])

    def test_viewer_can_see_posts_for_a_workgroup(self):
        self.login_viewer()
        post = models.DiscussionPost.objects.create(author=self.su,workgroup=self.wg1,title="test",body="test")
        models.DiscussionPost.objects.create(author=self.su,workgroup=self.wg2,title="test",body="test")
        response = self.client.get(reverse('aristotle:discussionsWorkgroup',args=[self.wg1.id]))
        self.assertEqual(len(response.context['discussions']),1)
        self.assertEqual(response.context['discussions'][0],post)

    def test_viewer_can_see_post_in_workgroup(self):
        post = models.DiscussionPost.objects.create(author=self.viewer,workgroup=self.wg1,title="test",body="test")
        comment = models.DiscussionComment.objects.create(author=self.viewer2,post=post,body="test")
        self.login_viewer()
        response = self.client.get(reverse('aristotle:discussionsPost',args=[post.id]))
        self.assertEqual(response.status_code,200)
        self.wg1.removeRoleFromUser('Viewer',self.viewer)
        response = self.client.get(reverse('aristotle:discussionsPost',args=[post.id]))
        self.assertEqual(response.status_code,403)
