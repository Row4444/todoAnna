# Generated by Django 3.1.1 on 2020-10-01 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0003_auto_20200930_1907"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="taskinfo",
            options={},
        ),
        migrations.RenameField(
            model_name="taskinfo",
            old_name="dead_line",
            new_name="deadline",
        ),
    ]
