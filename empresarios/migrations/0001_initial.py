# Generated by Django 5.0.7 on 2024-08-06 00:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Empresas",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=50)),
                ("cnpj", models.CharField(max_length=30)),
                ("site", models.URLField()),
                (
                    "tempo_existencia",
                    models.CharField(
                        choices=[
                            ("-6", "Menos de 6 meses"),
                            ("+6", "Mais de 6 meses"),
                            ("+1", "Mais de 1 ano"),
                            ("+5", "Mais de 5 anos"),
                        ],
                        default="-6",
                        max_length=2,
                    ),
                ),
                ("descricao", models.TextField()),
                ("data_final_captacao", models.DateField()),
                ("percentual_equity", models.IntegerField()),
                (
                    "estagio",
                    models.CharField(
                        choices=[
                            ("I", "Tenho apenas uma idea"),
                            ("MVP", "Possuo um MVP"),
                            ("MVPP", "Possuo um MVP com clientes pagantes"),
                            ("E", "Empresa pronta para escalar"),
                        ],
                        default="I",
                        max_length=4,
                    ),
                ),
                (
                    "area",
                    models.CharField(
                        choices=[
                            ("ED", "Ed-tech"),
                            ("FT", "Fintech"),
                            ("AT", "Agrotech"),
                        ],
                        max_length=3,
                    ),
                ),
                ("publico_alvo", models.CharField(max_length=3)),
                ("valor", models.DecimalField(decimal_places=2, max_digits=9)),
                ("pitch", models.FileField(upload_to="pitchs")),
                ("logo", models.FileField(upload_to="logo")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
