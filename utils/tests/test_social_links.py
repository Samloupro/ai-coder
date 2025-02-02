import unittest
from utils.social_links import extract_social_links

class TestSocialLinks(unittest.TestCase):
    def test_extract_social_links(self):
        # Test avec différents formats d'URLs de réseaux sociaux
        test_links = [
            # Facebook
            "https://www.facebook.com/profile",
            "https://facebook.com/profile",
            "https://fb.com/profile",
            
            # Instagram
            "https://www.instagram.com/profile",
            "https://instagram.com/profile",
            
            # Twitter
            "https://twitter.com/profile",
            "https://www.twitter.com/profile",
            "https://x.com/profile",
            
            # TikTok
            "https://www.tiktok.com/@username",
            "https://tiktok.com/username",
            
            # LinkedIn
            "https://www.linkedin.com/in/profile",
            "https://linkedin.com/company/company-name",
            
            # YouTube
            "https://www.youtube.com/channel/UCxxxxxxxx",
            "https://youtube.com/user/username",
            "https://youtube.com/@username",
            "https://youtu.be/username",
            
            # Pinterest
            "https://www.pinterest.com/username",
            "https://pinterest.fr/username",
            
            # GitHub
            "https://github.com/username",
            "https://www.github.com/username",
            
            # Snapchat
            "https://snapchat.com/add/username",
            "https://www.snapchat.com/@username",
            
            # Liens non sociaux pour tester le filtrage
            "https://example.com",
            "https://test.com/facebook",
            "https://notsocial.com"
        ]

        result = extract_social_links(test_links)

        # Vérifier que chaque réseau social a été trouvé
        self.assertIsNotNone(result["facebook"])
        self.assertIsNotNone(result["instagram"])
        self.assertIsNotNone(result["twitter"])
        self.assertIsNotNone(result["tiktok"])
        self.assertIsNotNone(result["linkedin"])
        self.assertIsNotNone(result["youtube"])
        self.assertIsNotNone(result["pinterest"])
        self.assertIsNotNone(result["github"])
        self.assertIsNotNone(result["snapchat"])

        # Vérifier les formats spécifiques
        self.assertTrue(result["facebook"].startswith("https://"))
        self.assertTrue("facebook.com" in result["facebook"] or "fb.com" in result["facebook"])
        
        self.assertTrue("instagram.com" in result["instagram"])
        
        self.assertTrue("twitter.com" in result["twitter"] or "x.com" in result["twitter"])
        
        self.assertTrue("tiktok.com" in result["tiktok"])
        
        self.assertTrue("linkedin.com" in result["linkedin"])
        
        self.assertTrue("youtube.com" in result["youtube"] or "youtu.be" in result["youtube"])
        
        self.assertTrue("pinterest." in result["pinterest"])
        
        self.assertTrue("github.com" in result["github"])
        
        self.assertTrue("snapchat.com" in result["snapchat"])

    def test_empty_links(self):
        # Test avec une liste vide
        result = extract_social_links([])
        for platform in result.values():
            self.assertIsNone(platform)

    def test_no_social_links(self):
        # Test avec des liens qui ne sont pas des réseaux sociaux
        test_links = [
            "https://example.com",
            "https://test.com",
            "https://notsocial.com"
        ]
        result = extract_social_links(test_links)
        for platform in result.values():
            self.assertIsNone(platform)

if __name__ == '__main__':
    unittest.main()