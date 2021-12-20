import mammoth
from BeautifulSoup import BeautifulSoup
f = open("test_code.docx", 'rb')
b = open('page.html', 'wb')
document = mammoth.convert_to_html(f)
b.write(document.value.encode('utf8'))
f.close()
b.close()

with open("page.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

with open("output1.html", "w") as file:
    file.write(str((soup.prettify())))
