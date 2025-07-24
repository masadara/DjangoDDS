from django.utils import timezone
from rest_framework import serializers

from .models import CashFlowRecord, Category, Status, SubCategory, Type


class CashFlowRecordSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CashFlowRecord.

    Обрабатывает преобразование данных модели в формат JSON и обратно,
    а также реализует валидацию связей между полями:
    - Проверяет, что категория соответствует выбранному типу.
    - Проверяет, что подкатегория соответствует выбранной категории.
    - Проверяет корректность суммы (неотрицательная).
    - Проверяет дату создания (не больше текущей).
    """

    status = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(), label="Статус"
    )
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), label="Тип")
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), label="Категория"
    )
    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), label="Подкатегория"
    )

    class Meta:
        model = CashFlowRecord
        fields = [
            "id",
            "created_at",
            "status",
            "type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]

    def validate(self, data):
        status = data.get("status", getattr(self.instance, "status", None))
        type_ = data.get("type", getattr(self.instance, "type", None))
        category = data.get("category", getattr(self.instance, "category", None))
        subcategory = data.get(
            "subcategory", getattr(self.instance, "subcategory", None)
        )
        amount = data.get("amount", getattr(self.instance, "amount", None))
        created_at = data.get("created_at", getattr(self.instance, "created_at", None))

        # Проверяем, что необходимые поля есть
        if category is None or type_ is None:
            raise serializers.ValidationError(
                "Поля category и type обязательны для проверки."
            )

        if category.type != type_:
            raise serializers.ValidationError(
                {"category": "Категория должна принадлежать выбранному типу."}
            )

        if subcategory is None or subcategory.category != category:
            raise serializers.ValidationError(
                {"subcategory": "Подкатегория должна принадлежать выбранной категории."}
            )

        if amount is None:
            raise serializers.ValidationError({"amount": "Сумма операции обязательна."})
        if amount < 0:
            raise serializers.ValidationError(
                {"amount": "Сумма не может быть отрицательной."}
            )

        if created_at is None:
            raise serializers.ValidationError(
                {"created_at": "Дата создания обязательна."}
            )
        if created_at > timezone.now().date():
            raise serializers.ValidationError(
                {"created_at": "Дата не может быть больше текущей."}
            )

        return data


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    """

    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SubCategory.
    """

    class Meta:
        model = SubCategory
        fields = "__all__"


class TypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Type.
    """

    class Meta:
        model = Type
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Status.
    """

    class Meta:
        model = Status
        fields = "__all__"
