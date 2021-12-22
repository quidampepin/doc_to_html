import mammoth
from bs4 import BeautifulSoup


custom_styles = """ i => cite
                    p[style-name='ordered'] => ol
                    p[style-name='details'] => details
                    p[style-name='btn-cta'] => button.btn-call-to-action
                    p[style-name='btn-primary'] => button.btn-primary
                    p[style-name='btn-secondary'] => button.btn-default
                    p[style-name='alert-danger'] => section.alert-danger > h2
                    p[style-name='alert-warning'] => section.alert-warning > h2
                    p[style-name='alert-text'] => alert > p
                    p[style-name='summary'] => summary"""


#convert word doc to an html file

with open("test_code.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file, style_map = custom_styles)
    text = result.value
    with open('doc.html', 'w') as html_file:
        html_file.write(text)


#parse the html created from the word doc
with open("doc.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

#parse the stable beginning of a Canada.ca page (header, menu)
with open("start.html") as fp:
    soup1 = BeautifulSoup(fp, 'html.parser')


#parse the stable end of a Canada.ca page (pre-footer and footer)
with open("end.html") as fp:
    soup2 = BeautifulSoup(fp, 'html.parser')

#prettify the html from word doc
with open("doc_output.html", "w") as file:
    file.write(str((soup.prettify())))

#combine the header, main and footer sections into a prettified html page
with open("page.html", "w") as file:
    file.write(str((soup1.prettify())+(soup.prettify())+(soup2.prettify())))



#clean up the generated html page into filedata
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
    filedata = filedata.replace('</summary>\n<details>\n', '</summary>\n<p>\n')
    filedata = filedata.replace('\n</details>', '\n</p>\n</details>')
    filedata = filedata.replace('\n<summary>', '\n<details>\n<summary>')
    filedata = filedata.replace('class="btn-call-to-action', 'class="btn btn-call-to-action')
    filedata = filedata.replace('class="btn-primary', 'class="btn btn-primary')
    filedata = filedata.replace('class="btn-default', 'class="btn btn-default')
    filedata = filedata.replace('class="alert-danger', 'class="alert alert-danger')
    filedata = filedata.replace('class="alert-warning', 'class="alert alert-warning')
    filedata = filedata.replace('</section>\n<alert>\n', '')
    filedata = filedata.replace('</alert>', '</section>')


#write the cleaned up filedata to the html page
with open('page.html', 'w') as file:
  file.write(filedata)


 #the generated HTML cam be copied in a gc-proto GitHub repo and create a full Canada.ca page
