from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CashFlowRecord, Category, Status, SubCategory, Type
from .serializers import (CashFlowRecordSerializer, CategorySerializer,
                          StatusSerializer, SubCategorySerializer,
                          TypeSerializer)


# ---------CashFlowViews---------
class CashFlowCreateView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/cashflow_create.html"

    def get(self, request):
        serializer = CashFlowRecordSerializer()
        return Response({"serializer": serializer}, template_name=self.template_name)

    def post(self, request):
        serializer = CashFlowRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("cashflow_list")
        print(serializer.errors)
        return Response(
            {"serializer": serializer}, template_name=self.template_name, status=400
        )


class CashFlowDeleteView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/cashflow_delete.html"

    def get(self, request, pk):
        obj = get_object_or_404(CashFlowRecord, pk=pk)
        serializer = CashFlowRecordSerializer(obj)
        return Response({"serializer": serializer, "obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(CashFlowRecord, pk=pk)
        obj.delete()
        return redirect("cashflow_list")


class CashFlowListView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/cashflow_list.html"

    def get(self, request, *args, **kwargs):
        queryset = CashFlowRecord.objects.all()

        selected_type = request.query_params.get("type")
        selected_category = request.query_params.get("category")
        selected_subcategory = request.query_params.get("subcategory")
        selected_status = request.query_params.get("status")
        search_query = request.query_params.get("search")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if selected_type:
            queryset = queryset.filter(type_id=selected_type)
        if selected_category:
            queryset = queryset.filter(category_id=selected_category)
        if selected_subcategory:
            queryset = queryset.filter(subcategory_id=selected_subcategory)
        if selected_status:
            queryset = queryset.filter(status_id=selected_status)

        if search_query:
            queryset = queryset.filter(
                Q(comment__icontains=search_query) | Q(amount__exact=search_query)
            )

        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        context = {
            "objects": queryset,
            "types": Type.objects.all(),
            "categories": Category.objects.all(),
            "subcategories": SubCategory.objects.all(),
            "statuses": Status.objects.all(),
            "selected_type": selected_type or "",
            "selected_category": selected_category or "",
            "selected_subcategory": selected_subcategory or "",
            "selected_status": selected_status or "",
            "search": search_query or "",
            "date_from": date_from or "",
            "date_to": date_to or "",
        }
        return Response(context)


class CashFlowDetailView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/cashflow_detail.html"

    def get(self, request, pk):
        obj = get_object_or_404(CashFlowRecord, pk=pk)
        serializer = CashFlowRecordSerializer(obj)
        return Response({"serializer": serializer, "obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(CashFlowRecord, pk=pk)
        serializer = CashFlowRecordSerializer(obj, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "obj": obj})
        serializer.save()
        return redirect("cashflow_list")


class CashFlowUpdateView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/cashflow_create.html"

    def get(self, request, pk):
        obj = get_object_or_404(CashFlowRecord, pk=pk)
        serializer = CashFlowRecordSerializer(obj)
        context = {
            "serializer": serializer,
            "title": f'Редактировать запись от {obj.created_at.strftime("%d.%m.%Y")}',
        }
        return Response(context)

    def post(self, request, pk):
        obj = get_object_or_404(CashFlowRecord, pk=pk)
        serializer = CashFlowRecordSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("cashflow_detail", pk=obj.pk)
        context = {
            "serializer": serializer,
            "title": f'Редактировать запись от {obj.created_at.strftime("%d.%m.%Y")}',
        }
        return Response(context, status=400)


# ---------CategoryViews---------
class CategoryCreateView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/category_create.html"

    def get(self, request):
        serializer = CategorySerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("category_list")
        return Response({"serializer": serializer})


class CategoryDeleteView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/category_delete.html"

    def get(self, request, pk):
        obj = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(obj)
        return Response({"serializer": serializer, "obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(Category, pk=pk)
        obj.delete()
        return redirect("category_list")


class CategoryListView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/category_list.html"

    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer()
        return Response({"serializer": serializer, "objects": queryset})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("category_list")
        queryset = Category.objects.all()
        return Response({"serializer": serializer, "objects": queryset})


class CategoryDetailView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/category_detail.html"

    def get(self, request, pk):
        obj = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(obj)
        return Response({"serializer": serializer, "obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(obj, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "obj": obj})
        serializer.save()
        return redirect("category_list")


# ---------SubCategoryViews---------
class SubCategoryListView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/subcategory_list.html"

    def get(self, request):
        queryset = SubCategory.objects.all()
        serializer = SubCategorySerializer()
        return Response({"serializer": serializer, "objects": queryset})

    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("subcategory_list")
        queryset = SubCategory.objects.all()
        return Response({"serializer": serializer, "objects": queryset})


class SubCategoryCreateView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/subcategory_create.html"

    def get(self, request):
        serializer = SubCategorySerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("subcategory_list")
        return Response({"serializer": serializer})


class SubCategoryDeleteView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/subcategory_delete.html"

    def get(self, request, pk):
        obj = get_object_or_404(SubCategory, pk=pk)
        serializer = SubCategorySerializer(obj)
        return Response({"serializer": serializer, "obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(SubCategory, pk=pk)
        obj.delete()
        return redirect("subcategory_list")


class SubCategoryDetailView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/subcategory_detail.html"

    def get(self, request, pk):
        obj = get_object_or_404(SubCategory, pk=pk)
        serializer = SubCategorySerializer(obj)
        return Response({"serializer": serializer, "obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(SubCategory, pk=pk)
        serializer = SubCategorySerializer(obj, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "obj": obj})
        serializer.save()
        return redirect("subcategory_list")


# ---------TypeViews---------
class TypeCreateView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/type_create.html"

    def get(self, request):
        serializer = TypeSerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("type_list")
        return Response({"serializer": serializer})


class TypeDeleteView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/type_delete.html"

    def get(self, request, pk):
        obj = get_object_or_404(Type, pk=pk)
        serializer = TypeSerializer(obj)
        return Response({"serializer": serializer, "obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(Type, pk=pk)
        obj.delete()
        return redirect("type_list")


class TypeListView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/type_list.html"

    def get(self, request):
        queryset = Type.objects.all()
        serializer = TypeSerializer()
        return Response({"serializer": serializer, "objects": queryset})

    def post(self, request):
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("type_list")
        queryset = Type.objects.all()
        return Response({"serializer": serializer, "objects": queryset})


class TypeDetailView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/type_detail.html"

    def get(self, request, pk):
        obj = get_object_or_404(Type, pk=pk)
        serializer = TypeSerializer(obj)
        return Response({"serializer": serializer, "obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(Type, pk=pk)
        serializer = TypeSerializer(obj, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "obj": obj})
        serializer.save()
        return redirect("type_list")


# ---------StatusViews---------
class StatusListView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/status_list.html"

    def get(self, request):
        queryset = Status.objects.all()
        serializer = StatusSerializer()
        return Response({"serializer": serializer, "objects": queryset})

    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("status_list")
        queryset = Status.objects.all()
        return Response({"serializer": serializer, "objects": queryset})


class StatusDetailView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/status_detail.html"

    def get(self, request, pk):
        obj = get_object_or_404(Status, pk=pk)
        serializer = StatusSerializer(obj)
        return Response({"serializer": serializer, "obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(Status, pk=pk)
        serializer = StatusSerializer(obj, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "obj": obj})
        serializer.save()
        return redirect("status_list")


class StatusCreateView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/status_create.html"

    def get(self, request):
        serializer = StatusSerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("status_list")
        return Response({"serializer": serializer})


class StatusDeleteView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "dds/status_delete.html"

    def get(self, request, pk):
        obj = get_object_or_404(Status, pk=pk)
        serializer = StatusSerializer(obj)
        return Response({"serializer": serializer, "obj": obj})

    def post(self, request, pk):
        obj = get_object_or_404(Status, pk=pk)
        obj.delete()
        return redirect("status_list")
