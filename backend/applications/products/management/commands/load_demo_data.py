from django.core.management.base import BaseCommand
from django.utils.text import slugify
from applications.products.models import Category, Brand, Material, Product


class Command(BaseCommand):
    help = 'Carga datos de demostración para la tienda'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando carga de datos de demostración...')

        # Crear categorías
        categories_data = [
            {'name': 'Sofás', 'description': 'Sofás y sillones confortables'},
            {'name': 'Mesas', 'description': 'Mesas para sala y comedor'},
            {'name': 'Sillas', 'description': 'Sillas y taburetes'},
            {'name': 'Camas', 'description': 'Camas y colchones'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True,
                }
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Categoría creada: {cat.name}')
                )
            else:
                self.stdout.write(f'  Categoría ya existe: {cat.name}')

        # Crear marcas
        brands_data = ['IKEA', 'Möbel', 'HomeStyle', 'Design Pro']
        brands = {}
        for brand_name in brands_data:
            brand, created = Brand.objects.get_or_create(
                slug=slugify(brand_name),
                defaults={'name': brand_name, 'is_active': True}
            )
            brands[brand_name] = brand
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Marca creada: {brand.name}')
                )

        # Crear materiales
        materials_data = ['Madera', 'Cuero', 'Tela', 'Acero', 'Metal', 'Cristal']
        materials = {}
        for mat_name in materials_data:
            mat, created = Material.objects.get_or_create(
                name=mat_name,
                defaults={'description': f'{mat_name} de alta calidad'}
            )
            materials[mat_name] = mat
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Material creado: {mat.name}')
                )

        # Crear productos
        products_data = [
            {
                'name': 'Sofá Clásico Gris',
                'sku': 'SOFA-CLASSIC-GRAY',
                'category': 'Sofás',
                'brand': 'IKEA',
                'price': 599.99,
                'description': 'Sofá cómodo con diseño clásico',
                'materials': ['Tela', 'Madera'],
            },
            {
                'name': 'Sofá Moderno Negro',
                'sku': 'SOFA-MODERN-BLACK',
                'category': 'Sofás',
                'brand': 'Design Pro',
                'price': 899.99,
                'description': 'Sofá contemporáneo con líneas limpias',
                'materials': ['Cuero', 'Metal'],
            },
            {
                'name': 'Mesa Comedor Madera',
                'sku': 'TABLE-DINING-WOOD',
                'category': 'Mesas',
                'brand': 'Möbel',
                'price': 449.99,
                'description': 'Mesa de comedor en madera maciza',
                'materials': ['Madera'],
            },
            {
                'name': 'Mesa Centro Cristal',
                'sku': 'TABLE-CENTER-GLASS',
                'category': 'Mesas',
                'brand': 'HomeStyle',
                'price': 299.99,
                'description': 'Mesa de centro con base de acero',
                'materials': ['Acero', 'Cristal'],
            },
            {
                'name': 'Silla Comedor',
                'sku': 'CHAIR-DINING-WOOD',
                'category': 'Sillas',
                'brand': 'IKEA',
                'price': 149.99,
                'description': 'Silla cómoda para comedor',
                'materials': ['Madera', 'Tela'],
            },
            {
                'name': 'Cama Matrimonio',
                'sku': 'BED-QUEEN-WOOD',
                'category': 'Camas',
                'brand': 'Design Pro',
                'price': 1299.99,
                'description': 'Cama tamaño matrimonio con cabecera',
                'materials': ['Madera', 'Metal'],
            },
        ]

        for prod_data in products_data:
            slug = slugify(prod_data['name'])
            prod, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'sku': prod_data['sku'],
                    'name': prod_data['name'],
                    'category': categories[prod_data['category']],
                    'brand': brands[prod_data['brand']],
                    'price': prod_data['price'],
                    'description': prod_data['description'],
                    'stock': 50,
                    'is_active': True,
                }
            )
            if created:
                # Agregar materiales
                for mat_name in prod_data['materials']:
                    prod.materials.add(materials[mat_name])
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Producto creado: {prod.name}')
                )
            else:
                self.stdout.write(f'  Producto ya existe: {prod.name}')

        self.stdout.write(
            self.style.SUCCESS('✓ Datos de demostración cargados exitosamente')
        )
