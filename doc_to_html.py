import mammoth
from bs4 import BeautifulSoup
f = open("test_code.docx", 'rb')
b = open('doc.html', 'wb')
document = mammoth.convert_to_html(f)
b.write(document.value.encode('utf8'))
f.close()
b.close()

with open("doc.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

with open("start.html") as fp:
    soup1 = BeautifulSoup(fp, 'html.parser')


with open("end.html") as fp:
    soup2 = BeautifulSoup(fp, 'html.parser')

with open("doc_output.html", "w") as file:
    file.write(str((soup.prettify())))


with open("page.html", "w") as file:
    file.write(str((soup1.prettify())+(soup.prettify())+(soup2.prettify())))



with open("page.html", "r") as file:
    filedata = file.read()
    filedata = filedata.replace('<main class="container" property="mainContentOfPage" resource="#wb-main" typeof="WebPageElement">\n  </main>\n </body>\n</html>', '<main class="container" property="mainContentOfPage" resource="#wb-main" typeof="WebPageElement">\n')
    filedata = filedata.replace('</script>\n  </link>\n </head>\n', '</script>\n </head>\n')
    filedata = filedata.replace('<link href="https://www.canada.ca/etc/designs/canada/wet-boew/assets/wmms-blk.svg" property="logo"/>\n         </meta>\n        </meta>\n       </div>\n', '<link href="https://www.canada.ca/etc/designs/canada/wet-boew/assets/wmms-blk.svg" property="logo"/>\n         </div>\n')
    filedata = filedata.replace('<div class="par iparys_inherited">\n</div>\n<div class="par iparys_inherited">\n', '</main>\n<div class="par iparys_inherited">\n</div>\n<div class="par iparys_inherited">\n')




# Write the file out again
with open('page.html', 'w') as file:
  file.write(filedata)
