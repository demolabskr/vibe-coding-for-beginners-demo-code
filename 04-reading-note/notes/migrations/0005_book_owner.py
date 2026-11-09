# 책에 주인 칸을 더한다. 이미 있는 책은 첫 관리자 계정의 책으로 정한다.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def give_books_to_admin(apps, schema_editor):
    Book = apps.get_model("notes", "Book")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    if not Book.objects.filter(owner__isnull=True).exists():
        return
    admin = User.objects.filter(is_superuser=True).order_by("id").first()
    if admin is None:
        raise RuntimeError("주인을 정할 관리자 계정이 없습니다. createsuperuser로 관리자 계정을 먼저 만드세요.")
    Book.objects.filter(owner__isnull=True).update(owner=admin)


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0004_book_cover"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="books",
                to=settings.AUTH_USER_MODEL,
                verbose_name="주인",
            ),
        ),
        migrations.RunPython(give_books_to_admin, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="book",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="books",
                to=settings.AUTH_USER_MODEL,
                verbose_name="주인",
            ),
        ),
    ]
