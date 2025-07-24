from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CashFlowCreateView, CashFlowDeleteView, CashFlowDetailView,
                    CashFlowListView, CashFlowUpdateView, CategoryCreateView,
                    CategoryDeleteView, CategoryDetailView, CategoryListView,
                    StatusCreateView, StatusDeleteView, StatusDetailView,
                    StatusListView, SubCategoryCreateView,
                    SubCategoryDeleteView, SubCategoryDetailView,
                    SubCategoryListView, TypeCreateView, TypeDeleteView,
                    TypeDetailView, TypeListView)

router = DefaultRouter()

urlpatterns = [
    # CashFlow URLs
    path("cashflow/", CashFlowListView.as_view(), name="cashflow_list"),
    path("cashflow/create/", CashFlowCreateView.as_view(), name="cashflow_create"),
    path("cashflow/<int:pk>/", CashFlowDetailView.as_view(), name="cashflow_detail"),
    path(
        "cashflow/<int:pk>/delete/",
        CashFlowDeleteView.as_view(),
        name="cashflow_delete",
    ),
    path(
        "cashflow/<int:pk>/edit/", CashFlowUpdateView.as_view(), name="cashflow_update"
    ),
    # Category URLs
    path("category/", CategoryListView.as_view(), name="category_list"),
    path("category/create/", CategoryCreateView.as_view(), name="category_create"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path(
        "category/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    # SubCategory URLs
    path("subcategory/", SubCategoryListView.as_view(), name="subcategory_list"),
    path(
        "subcategory/create/",
        SubCategoryCreateView.as_view(),
        name="subcategory_create",
    ),
    path(
        "subcategory/<int:pk>/",
        SubCategoryDetailView.as_view(),
        name="subcategory_detail",
    ),
    path(
        "subcategory/<int:pk>/delete/",
        SubCategoryDeleteView.as_view(),
        name="subcategory_delete",
    ),
    # Type URLs
    path("type/", TypeListView.as_view(), name="type_list"),
    path("type/create/", TypeCreateView.as_view(), name="type_create"),
    path("type/<int:pk>/", TypeDetailView.as_view(), name="type_detail"),
    path("type/<int:pk>/delete/", TypeDeleteView.as_view(), name="type_delete"),
    # Status URLs
    path("status/", StatusListView.as_view(), name="status_list"),
    path("status/create/", StatusCreateView.as_view(), name="status_create"),
    path("status/<int:pk>/", StatusDetailView.as_view(), name="status_detail"),
    path("status/<int:pk>/delete/", StatusDeleteView.as_view(), name="status_delete"),
    path("", include(router.urls)),
]
