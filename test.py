import unittest
from io import BytesIO
from main import app, os, UPLOAD_FOLDER

class FileHandleTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def tearDown(self):
        pass

    def test_home_page(self):
        print("\nTesting home page...\n")
        result = self.app.get('/')
        try:
            self.assertEqual(result.status_code, 200)
            print("Testing if upload option exists...")
            self.assertTrue(b'<input type="file" name="file" />' in result.data)
            print("passed")
            print("Testing if download option exists...")
            self.assertTrue(b'<input type="submit" value="start download" />' in result.data)
            print("passed")
            print("Testing if delete option exists...")
            self.assertTrue(b'<input type="submit" value="DELETE" />' in result.data)
            print("passed")
            print("Testing if there is an option to view all the uploaded files...")
            self.assertTrue(b'<button onclick="window.location.href=\'/display\'">Click to see all the files</button>' in result.data)
            print("passed")
        except Exception as e:
            print(e)

    def inDirectory(self, filename):
        files = os.listdir(UPLOAD_FOLDER)
        for file in files:
            if filename == file:
                return True
        return False
    
    def test_upload(self):
        print("\nTesting file upload...\n")
        with app.test_client() as client:
            data = {}
            print("trying to upload a test file 'test_file.txt'")
            data['file'] = (BytesIO(b'This is a test.'), "test_file.txt")
            result = client.post('/upload', content_type='multipart/form-data', data=data, follow_redirects=True)
        print("Testing if the page redirects and message is displayed...")
        self.assertTrue(b'test_file.txt is uploaded successfully' in result.data)
        print("passed")
        print("Testing if 'test_file.txt' is in the directory...")
        self.assertTrue(self.inDirectory("test_file.txt"))
        print("passed")

    def test_delete(self):
        print("\nTesting file delete...\n")
        print("trying to delete file 'test_file.txt'")
        with app.test_client() as client:
            result = client.post('/delete', data={'filename':'test_file.txt'}, follow_redirects=True)

        print("Testing if the page redirects and message is displayed...")
        self.assertTrue(b'test_file.txt is removed' in result.data)
        print("passed")
        print("Testing if 'test_file.txt' is not in the directory...")
        self.assertTrue(not self.inDirectory("test_file.txt"))
        print("passed")
        print("trying to delete an unexisted file")
        result = client.post('/delete', data={'filename':'does_not_exist.txt'}, follow_redirects=True)
        print("Testing if the page redirects and message is displayed...")
        self.assertTrue(b'Error: can not find the file' in result.data)
        print("passed")

    def test_download(self):
        print("\nTesting file download...\n")
        print("trying to download a file that doesn't exist")
        result = self.app.post('/download', data={'filename':'does_not_exist.txt'}, follow_redirects=True)
        print("Testing if the page redirects and message is displayed...")
        self.assertTrue(b'Error: can not find the file' in result.data)
        print("passsed")

if __name__ == "__main__":
    unittest.main()
