from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(error_messages={'unique': 'Există deja o categorie cu acest nume.'}, max_length=60, unique=True)),
                ('descriere', models.TextField(blank=True, null=True)),
                ('culoare', models.CharField(default='#E6EBD9', error_messages={'max_length': 'Culoarea poate avea cel mult 7 caractere.'}, help_text='Culoare în format hexazecimal, de exemplu #E6EBD9.', max_length=7)),
                ('sigla', models.CharField(blank=True, help_text='Calea unei imagini din static sau numele unei pictograme.', max_length=200, null=True)),
                ('ordine_afisare', models.PositiveIntegerField(blank=True, default=0)),
            ],
            options={
                'verbose_name': 'categorie',
                'verbose_name_plural': 'categorii',
                'ordering': ['ordine_afisare', 'nume'],
            },
        ),
        migrations.CreateModel(
            name='Furnizor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(error_messages={'unique': 'Există deja un furnizor cu acest nume.'}, max_length=100, unique=True)),
                ('telefon', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, error_messages={'invalid': 'Introdu o adresă de email validă pentru furnizor.'}, max_length=254, null=True)),
            ],
            options={
                'verbose_name': 'furnizor',
                'verbose_name_plural': 'furnizori',
                'ordering': ['nume'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(error_messages={'unique': 'Există deja un ingredient cu acest nume.'}, max_length=80, unique=True)),
                ('alergen', models.BooleanField(default=False)),
                ('denumiri_alternative', models.JSONField(blank=True, default=list, help_text='Listă de denumiri în format JSON, de exemplu ["lapte de vacă", "lapte integral"]. Pentru nicio denumire, folosește [].')),
                ('furnizor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ingrediente', to='brunch.furnizor')),
            ],
            options={
                'verbose_name': 'ingredient',
                'verbose_name_plural': 'ingrediente',
                'ordering': ['nume'],
            },
        ),
        migrations.CreateModel(
            name='Sediu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=80)),
                ('adresa', models.CharField(max_length=250)),
                ('telefon', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'sediu',
                'verbose_name_plural': 'sedii',
                'ordering': ['nume'],
            },
        ),
        migrations.CreateModel(
            name='Preparat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(error_messages={'unique': 'Există deja un preparat cu acest nume.'}, max_length=100, unique=True)),
                ('descriere', models.TextField(blank=True, null=True)),
                ('pret', models.DecimalField(decimal_places=2, help_text='Prețul unei porții, în lei. Trebuie să fie mai mare decât zero.', max_digits=7)),
                ('gramaj', models.PositiveIntegerField(help_text='Cantitatea unei porții: grame pentru mâncare, mililitri pentru băuturi.')),
                ('calorii', models.PositiveIntegerField(help_text='Numărul de kilocalorii pentru întreaga porție.')),
                ('vegetarian', models.BooleanField(default=False)),
                ('disponibil', models.BooleanField(default=True)),
                ('tip', models.CharField(choices=[('sarat', 'Sărat'), ('dulce', 'Dulce'), ('bautura', 'Băutură')], default='sarat', max_length=10)),
                ('data_lansare', models.DateField(blank=True, null=True)),
                ('data_adaugare', models.DateTimeField(default=django.utils.timezone.now)),
                ('imagine', models.ImageField(blank=True, null=True, upload_to='preparate/')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='preparate', to='brunch.categorie')),
                ('ingrediente', models.ManyToManyField(related_name='preparate', to='brunch.ingredient')),
            ],
            options={
                'verbose_name': 'preparat',
                'verbose_name_plural': 'preparate',
                'ordering': ['nume'],
            },
        ),
        migrations.CreateModel(
            name='LotPreparat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numar_lot', models.PositiveIntegerField(help_text='Numărul lotului în cadrul preparatului ales.')),
                ('data_preparare', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_expirare', models.DateTimeField(help_text='Trebuie să fie după data și ora preparării.')),
                ('cantitate', models.PositiveIntegerField(help_text='Numărul de porții pregătite în acest lot.')),
                ('preparat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loturi', to='brunch.preparat')),
                ('sediu', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loturi', to='brunch.sediu')),
            ],
            options={
                'verbose_name': 'lot de preparat',
                'verbose_name_plural': 'loturi de preparate',
                'ordering': ['-data_preparare'],
            },
        ),
        migrations.AddConstraint(
            model_name='categorie',
            constraint=models.CheckConstraint(check=models.Q(('ordine_afisare__gte', 0)), name='categorie_ordine_pozitiva'),
        ),
        migrations.AddConstraint(
            model_name='categorie',
            constraint=models.CheckConstraint(check=models.Q(('culoare__regex', '^#[0-9A-Fa-f]{6}$')), name='categorie_culoare_hex'),
        ),
        migrations.AddIndex(
            model_name='preparat',
            index=models.Index(fields=['pret'], name='preparat_pret_idx'),
        ),
        migrations.AddIndex(
            model_name='preparat',
            index=models.Index(fields=['gramaj'], name='preparat_gramaj_idx'),
        ),
        migrations.AddIndex(
            model_name='preparat',
            index=models.Index(fields=['calorii'], name='preparat_calorii_idx'),
        ),
        migrations.AddIndex(
            model_name='preparat',
            index=models.Index(fields=['data_lansare'], name='preparat_lansare_idx'),
        ),
        migrations.AddConstraint(
            model_name='preparat',
            constraint=models.CheckConstraint(check=models.Q(('pret__gt', 0)), name='preparat_pret_pozitiv'),
        ),
        migrations.AddConstraint(
            model_name='preparat',
            constraint=models.CheckConstraint(check=models.Q(('gramaj__gt', 0)), name='preparat_gramaj_pozitiv'),
        ),
        migrations.AddConstraint(
            model_name='preparat',
            constraint=models.CheckConstraint(check=models.Q(('calorii__gte', 0)), name='preparat_calorii_pozitive'),
        ),
        migrations.AddConstraint(
            model_name='preparat',
            constraint=models.CheckConstraint(check=models.Q(('tip__in', ['sarat', 'dulce', 'bautura'])), name='preparat_tip_valid'),
        ),
        migrations.AddConstraint(
            model_name='lotpreparat',
            constraint=models.UniqueConstraint(fields=('preparat', 'numar_lot'), name='lot_preparat_numar_unic'),
        ),
        migrations.AddConstraint(
            model_name='lotpreparat',
            constraint=models.CheckConstraint(check=models.Q(('numar_lot__gt', 0)), name='lot_numar_pozitiv'),
        ),
        migrations.AddConstraint(
            model_name='lotpreparat',
            constraint=models.CheckConstraint(check=models.Q(('cantitate__gt', 0)), name='lot_cantitate_pozitiva'),
        ),
        migrations.AddConstraint(
            model_name='lotpreparat',
            constraint=models.CheckConstraint(check=models.Q(('data_expirare__gt', models.F('data_preparare'))), name='lot_expirare_dupa_preparare'),
        ),
    ]
