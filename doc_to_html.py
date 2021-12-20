import mammoth
from bs4 import BeautifulSoup
f = open("test_code.docx", 'rb')
b = open('page.html', 'wb')
document = mammoth.convert_to_html(f)
b.write(document.value.encode('utf8'))
f.close()
b.close()

with open("page.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

with open("start.html") as fp:
    soup1 = BeautifulSoup(fp, 'html.parser')


with open("end.html") as fp:
    soup2 = BeautifulSoup(fp, 'html.parser')

with open("output1.html", "w") as file:
    file.write(str((soup.prettify())))


with open("output2.html", "w") as file:
    file.write(str((soup1.prettify())+(soup.prettify())+(soup2.prettify())))



with open("output2.html", "r") as file:
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('<main class="container" property="mainContentOfPage" resource="#wb-main" typeof="WebPageElement">\n  </main>\n </body>\n</html>', '<main class="container" property="mainContentOfPage" resource="#wb-main" typeof="WebPageElement">\n')

# Write the file out again
with open('output2.html', 'w') as file:
  file.write(filedata)
