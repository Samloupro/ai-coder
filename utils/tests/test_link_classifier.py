import unittest
from utils.analyzers.link_classifier import classify_links

class TestLinkClassifier(unittest.TestCase):
    def test_classify_links(self):
        urls = [
            "https://example.com/",
            "https://example.com/pages/about",
            "https://example.com/page/contact",
            "https://example.com/policies/privacy",
            "https://example.com/policy/terms",
            "https://example.com/blogs/news",
            "https://example.com/blog/latest",
            "https://example.com/collections/shoes", 
            "https://example.com/collection/summer",
            "https://example.com/products/shirt",
            "https://example.com/product/123",
            "https://example.com/cart",
            "https://example.com/account/login",
            "https://example.com/search?q=test",
            "https://example.com/pages/contact?lang=fr",
            "https://example.com/account/login#info",
            "https://sub.example.com/",
            "https://example.com/unknown/path"
        ]
        
        expected = {
            "Home": ["https://example.com/"],
            "Pages": [
                "https://example.com/pages/about",
                "https://example.com/page/contact",
                "https://example.com/pages/contact?lang=fr"
            ],
            "Policies": [
                "https://example.com/policies/privacy",
                "https://example.com/policy/terms"
            ],
            "Blogs": [
                "https://example.com/blogs/news",
                "https://example.com/blog/latest"
            ],
            "Collections": [
                "https://example.com/collections/shoes",
                "https://example.com/collection/summer"
            ],
            "Products": [
                "https://example.com/products/shirt",
                "https://example.com/product/123"
            ],
            "Others": [
                "https://example.com/cart",
                "https://example.com/account/login",
                "https://example.com/search?q=test",
                "https://example.com/account/login#info",
                "https://sub.example.com/",
                "https://example.com/unknown/path"
            ]
        }
        
        result = classify_links(urls)
        self.assertEqual(result, expected)

    def test_root_domain_validation(self):
        urls = [
            "https://example.com/",
            "https://example.com/pages/",
            "https://sub.example.com/",
            "https://example.org/",
            "https://www.example.com/"
        ]
        
        expected = {
            "Home": ["https://example.com/"],
            "Pages": ["https://example.com/pages/"],
            "Policies": [],
            "Blogs": [],
            "Collections": [],
            "Products": [],
            "Others": [
                "https://sub.example.com/",
                "https://example.org/",
                "https://www.example.com/"
            ]
        }
        
        result = classify_links(urls, "example.com")
        self.assertEqual(result, expected)

    def test_edge_cases(self):
        # Test avec des URLs vides ou invalides
        self.assertEqual(classify_links([], "example.com"), {
            "Home": [],
            "Pages": [],
            "Policies": [],
            "Blogs": [],
            "Collections": [],
            "Products": [],
            "Others": []
        })
        
        # Test avec des URLs sans schéma
        urls = [
            "example.com/",
            "www.example.com/pages",
            "/pages/about"
        ]
        expected = {
            "Home": [],
            "Pages": [],
            "Policies": [],
            "Blogs": [],
            "Collections": [],
            "Products": [],
            "Others": [
                "example.com/",
                "www.example.com/pages",
                "/pages/about"
            ]
        }
        self.assertEqual(classify_links(urls, "example.com"), expected)

if __name__ == '__main__':
    unittest.main()
