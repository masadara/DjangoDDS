from django.db import models
from django.utils import timezone


class Status(models.Model):
    """
    Модель представления статуса операции в денежном потоке.
    """

    name = models.CharField(
        max_length=50, unique=True, verbose_name="Название статуса операции"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Type(models.Model):
    """
    Модель представления типа операции в денежном потоке.
    """

    name = models.CharField(
        max_length=50, unique=True, verbose_name="Название типа операции"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"


class Category(models.Model):
    """
    Модель представления категории операции в денежном потоке.
    """

    name = models.CharField(max_length=50, verbose_name="Название категории операции")
    type = models.ForeignKey(
        Type,
        related_name="categories",
        on_delete=models.CASCADE,
        verbose_name="Тип операции",
    )

    class Meta:
        unique_together = ("name", "type")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name} ({self.type.name})"


class SubCategory(models.Model):
    """
    Модель представления подкатегории операции в денежном потоке.
    """

    name = models.CharField(
        max_length=50, verbose_name="Название подкатегории операции"
    )
    category = models.ForeignKey(
        Category,
        related_name="subcategories",
        on_delete=models.CASCADE,
        verbose_name="Категория операции",
    )

    class Meta:
        unique_together = ("name", "category")
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class CashFlowRecord(models.Model):
    """
    Основная модель для записи движения денежных средств.
    """

    created_at = models.DateField(
        default=timezone.now, verbose_name="Дата создания операции"
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name="Статус операции"
    )
    type = models.ForeignKey(
        Type, on_delete=models.PROTECT, verbose_name="Тип операции"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Категория операции"
    )
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.PROTECT, verbose_name="Подкатегория операции"
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Сумма операции"
    )
    comment = models.TextField(
        blank=True, null=True, verbose_name="Комментарий к операции"
    )

    is_deleted = models.BooleanField(default=False, verbose_name="Удалена")

    def save(self, *args, **kwargs):
        # Логика проверки: категория должна принадлежать типу, подкатегория - категории
        if self.category.type != self.type:
            raise ValueError("Категория должна относиться к выбранному типу")
        if self.subcategory.category != self.category:
            raise ValueError("Подкатегория должна относиться к выбранной категории")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.created_at} | {self.status} | {self.type} | {self.category} | {self.subcategory} | {self.amount}"

    class Meta:
        verbose_name = "Движение денежных средств"
        verbose_name_plural = "Движения денежных средств"
        ordering = ["-created_at"]
