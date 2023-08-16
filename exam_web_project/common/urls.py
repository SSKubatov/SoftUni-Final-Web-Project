from django.urls import path

from exam_web_project.common.views import HomeView, ShowcaseSectionView, InfoSectionView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('showcase/', ShowcaseSectionView.as_view(), name='showcase'),
    path('information/', InfoSectionView.as_view(), name='info section'),

)
