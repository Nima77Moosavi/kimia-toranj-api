from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Collection, Attribute, AttributeValue, Product, ProductImage, ProductVariant


class CollectionTests(APITestCase):
    def setUp(self):
        # Create a collection and an attribute to attach to it
        self.collection = Collection.objects.create(
            title="Summer Collection", description="Cool stuff for summer", image="path/to/image.jpg"
        )
        self.attribute = Attribute.objects.create(title="Color")
        self.collection.attributes.add(self.attribute)

        # Create a product linked to this collection for testing the custom action
        self.product = Product.objects.create(
            title="Cool Shirt", description="A very cool shirt", collection=self.collection
        )

    def test_list_collections(self):
        url = reverse("collection-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect at least one collection in the response
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_products_for_collection(self):
        # Assumes the custom action is registered as "products"
        url = reverse("collection-products", kwargs={"pk": self.collection.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response should include the product we added in setUp
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.product.title)


class ProductTests(APITestCase):
    def setUp(self):
        # Create a collection required for products
        self.collection = Collection.objects.create(
            title="Winter Collection", description="Cozy things for winter", image="path/to/image.jpg"
        )
        # Data for creating a product; note that we must supply the collection's ID
        self.product_data = {
            "title": "Snow Jacket",
            "description": "Keeps you warm",
            "collection": self.collection.id
        }

    def test_create_product(self):
        url = reverse("product-list")
        # We are not sending any images for this request
        response = self.client.post(url, self.product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.product_data["title"])

    def test_create_product_with_images(self):
        url = reverse("product-list")
        # Create a temporary image file using SimpleUploadedFile
        image_content = b"dummy image content"
        image_file = SimpleUploadedFile(
            "jacket.jpg", image_content, content_type="image/jpeg")
        data = self.product_data.copy()
        # When sending files, use "multipart" as format. Ensure the field name "images" corresponds to your view logic.
        data["images"] = [image_file]

        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that images are attached in the response (assuming your serializer returns a list under "images")
        self.assertTrue("images" in response.data)
        self.assertGreaterEqual(len(response.data["images"]), 1)


class ProductImageTests(APITestCase):
    def setUp(self):
        # Create a collection and a product to attach images to.
        self.collection = Collection.objects.create(
            title="Electronics", description="Gadgets", image="path/to/electronics.jpg"
        )
        self.product = Product.objects.create(
            title="Smartphone", description="A smart phone", collection=self.collection
        )

    def test_upload_product_images(self):
        url = reverse("product-image-list")
        # Create a dummy image
        image_content = b"dummy image bytes"
        image_file = SimpleUploadedFile(
            "phone.jpg", image_content, content_type="image/jpeg")
        data = {
            "product": self.product.id,
            "images": [image_file]
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Expect at least one image in the response
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn("phone", response.data[0]["image"])


class AttributeTests(APITestCase):
    def setUp(self):
        # Create an attribute
        self.attribute = Attribute.objects.create(title="Size")

    def test_list_attributes(self):
        url = reverse("attribute-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_add_value_to_attribute(self):
        # Use the custom action `add_value` to add an AttributeValue to an attribute
        url = reverse("attribute-add-value", kwargs={"pk": self.attribute.id})
        payload = {"value": "Large"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["value"], "Large")


class ProductVariantTests(APITestCase):
    def setUp(self):
        # Create a collection, product, attribute, attribute value, and then a variant.
        self.collection = Collection.objects.create(
            title="Footwear", description="Shoes", image="path/to/footwear.jpg"
        )
        self.product = Product.objects.create(
            title="Running Shoes", description="Comfortable running shoes", collection=self.collection
        )
        self.attribute = Attribute.objects.create(title="Color")
        self.attribute_value = AttributeValue.objects.create(
            attribute=self.attribute, value="Blue")
        # Create a product variant and add the attribute value
        self.variant = ProductVariant.objects.create(
            product=self.product, price=100, stock=10
        )
        self.variant.attributes.add(self.attribute_value)

    def test_list_product_variants(self):
        url = reverse("productvariant-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
