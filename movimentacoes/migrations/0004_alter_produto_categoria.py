# Generated by Django 4.0.2 on 2022-04-23 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movimentacoes', '0003_alter_produto_quantidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.CharField(choices=[('ACOUGUE', 'Açougue'), ('BEBIDAS', 'Bebidas'), ('CEREAIS', 'Cereais'), ('COZINHA', 'Cozinha'), ('HORTIFRUTI', 'Hortifruti'), ('LACTICINIOS', 'Lacticínios'), ('LIMPEZA', 'Limpeza'), ('TEMPEROS', 'Temperos'), ('UTENSILIOS', 'Utensílios')], max_length=50),
        ),
    ]
