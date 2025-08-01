import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from postify.utils import html_reader

def test_html_reader():
    file = html_reader("tracking_template.html")
    assert file
    
file = html_reader("tracking_template.html")

print(file)