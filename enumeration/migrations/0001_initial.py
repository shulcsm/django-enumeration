# Generated by Django 2.2 on 2019-04-08 06:38

from django.db import migrations, models
import django.db.models.deletion
import enumeration.const
import enumfields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=0)),
                ('period', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('format', models.CharField(max_length=255)),
                ('reset_period', enumfields.fields.EnumField(default='never', enum=enumeration.const.ResetPeriod, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Gap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('counter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gaps', to='enumeration.Counter')),
            ],
        ),
        migrations.AddField(
            model_name='counter',
            name='sequence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='counters', to='enumeration.Sequence'),
        ),
        migrations.AddConstraint(
            model_name='counter',
            constraint=models.UniqueConstraint(condition=models.Q(period__isnull=True), fields=('sequence',), name='unique_counter_for_no_period'),
        ),
        migrations.AlterUniqueTogether(
            name='counter',
            unique_together={('sequence', 'period')},
        ),
    ]
