from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils import timezone
from django.http import HttpResponse

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

import random, string

class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context


class BlogPostPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPostPage', related_name='tagged_items')


class BlogPostPage(Page):
    intro = models.CharField(max_length=256)
    date = models.DateTimeField("Post date", default=timezone.now)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPostPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Blog information", classname="collapsible collapsed"),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('date'),
    ]

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            None


class BlogTagIndexPage(Page):

    def get_context(self, request):
        tag = request.GET.get('tag')
        blogpages = BlogPostPage.objects.filter(tags__name=tag)

        context = super(BlogTagIndexPage, self).get_context(request)
        context['blogpages'] = blogpages
        return context


class BlogPostGalleryImage(Orderable):
    page = ParentalKey(BlogPostPage, related_name="gallery_images")
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]




class RandomDownloadPage(Page):

    def serve(self, request):
        r = ''.join([random.choice(string.letters + string.digits + '\n') for _ in range(1000)])
        response = HttpResponse(r, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=random.txt'
        return response