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

    filedata = filedata.replace('</meta>\n </head>\n', '</head>\n')
    filedata = filedata.replace('<nav>\n   <ul id="wb-tphp">\n    <div class="par iparys_inherited">\n     <div class="global-header">\n', '<div class="par iparys_inherited">\n     <div class="global-header">\n')
    filedata = filedata.replace('<main class="container" property="mainContentOfPage" resource="#wb-main" typeof="WebPageElement">\n    </main>\n   </ul>\n  </nav>\n </body>\n</html><h1>', '<main class="container" property="mainContentOfPage" resource="#wb-main" typeof="WebPageElement">\n    <h1>')
    filedata = filedata.replace('</script>\n  </link>\n </head>\n', '</script>\n </head>\n')
    filedata = filedata.replace('<link href="https://www.canada.ca/etc/designs/canada/wet-boew/assets/wmms-blk.svg" property="logo"/>\n           </meta>\n          </meta>\n', '<link href="https://www.canada.ca/etc/designs/canada/wet-boew/assets/wmms-blk.svg" property="logo"/>\n')
    filedata = filedata.replace('<div class="par iparys_inherited">\n</div>\n<div class="par iparys_inherited">\n', '</main>\n<div class="par iparys_inherited">\n</div>\n<div class="par iparys_inherited">\n')
    filedata = filedata.replace('\n </a>\n ', '</a>')
    filedata = filedata.replace('<h3>\n On this page\n</h3>', '<h2 class="h3">\n On this page\n</h2>')
    filedata = filedata.replace('&lt;', '<')
    filedata = filedata.replace('&gt;', '>')
    filedata = filedata.replace('<p>\n <details>\n</p>\n', '<details>\n')
    filedata = filedata.replace('<p>\n <summary>', '<summary>')
    filedata = filedata.replace('</summary>\n</p>', '</summary>\n')
    filedata = filedata.replace('<p>\n </details>\n</p>\n', '</details>\n')



# Write the file out again
with open('page.html', 'w') as file:
  file.write(filedata)
