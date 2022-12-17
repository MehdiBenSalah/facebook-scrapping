import unittest
from app.scraper import scrape_facebook_page

class TestScraper(unittest.TestCase):

    def setUp(self):
        self.URL1 = 'www.facebook.com/insat.rnu.tn' ## old structure
        self.URL2 = 'www.facebook.com/facebook' ## new structure
        self.max_post_to_extract = 10

    def tearDown(self):
        pass

    def test_old_structure(self):
        self.assertRegex(self.URL1, '^(?:https?:\/\/)?(?:www\.)?(facebook|fb)\.(com|me)\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)')

        data = scrape_facebook_page(self.URL1, self.max_post_to_extract,10, 0)

        self.assertEqual(data['_id'],"insat.rnu.tn")
        self.assertIn(self.URL1,data['url'])
        self.assertEqual(data['page title'],'INSAT')
        self.assertEqual(data['About'],"Établissement public d’enseignement supérieur")
        self.assertIsInstance(data['followers'],int)
        self.assertIsInstance(data['likes'],int)
        self.assertEqual(data['Category'],"College & university")
        self.assertEqual(data['Contact info'],[
            '676 INSAT Centre Urbain Nord BP، Tunis Cedex 1080',
            "71 703 829",
            'contact@insat.u-carthage.tn'
        ])
        self.assertEqual(data['Websites and social links'],'http://www.insat.rnu.tn/')
        self.assertEqual(data['Basic info'],'Not yet rated (2 Reviews)')
        self.assertEqual(len(data['posts']), self.max_post_to_extract)
        for i in range(self.max_post_to_extract):
            self.assertIsInstance(data['posts'][i]['number of likes'],int)
            self.assertIsInstance(data['posts'][i]['number of comments'],int)
            self.assertIsInstance(data['posts'][i]['number of shares'],int)
        
    def test_new_structure(self):
        self.assertRegex(self.URL2, '^(?:https?:\/\/)?(?:www\.)?(facebook|fb)\.(com|me)\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)')
        data = scrape_facebook_page(self.URL2, self.max_post_to_extract,10, 0)
        self.assertEqual(data['_id'],"facebook")
        self.assertIn(self.URL2,data['url'])
        self.assertEqual(data['page title'],'Facebook')
        self.assertEqual(data['About'],"The Facebook app Page celebrates how our friends inspire us, support us, and help us discover the world when we connect.")
        self.assertIsInstance(data['followers'],int)
        self.assertIsInstance(data['likes'],int)
        self.assertIsInstance(data['checks'],int)
        self.assertEqual(data['Category'],"Internet Company")
        self.assertNotIn('See more', data['Additional information'])
        self.assertEqual(data['Contact info'],'http://www.facebook.com/facebook')
        self.assertEqual(len(data['posts']), self.max_post_to_extract)
        for i in range(self.max_post_to_extract):
            self.assertIsInstance(data['posts'][i]['number of likes'],int)
            self.assertIsInstance(data['posts'][i]['number of comments'],int)
            self.assertIsInstance(data['posts'][i]['number of shares'],int)
        
        



if __name__ == '__main__':
    unittest.main()