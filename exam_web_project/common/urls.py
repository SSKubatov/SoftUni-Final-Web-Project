from django.urls import path

from exam_web_project.common.views import IndexView, ShowcaseSectionView, InfoSectionView, CommunitySectionView

urlpatterns = (
    path('', IndexView.as_view(), name='home'),
    path('showcase-section/', ShowcaseSectionView.as_view(), name='showcase section'),
    path('information-section/', InfoSectionView.as_view(), name='info section'),
    path('community-section/', CommunitySectionView.as_view(), name='community section'),

)
