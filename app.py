#importing libraries
from flask import Flask
from flask import request
from flask import app, render_template
import requests
import mammoth
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'upload/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def homepage():
    lang = request.args.get('lang', 'en')
    if lang == 'en':
        return render_template("index_en.html", lang=lang)
    if lang == 'fr':
        return render_template("code_fr.html", lang=lang)

@app.route('/html_convert', methods=['GET', 'POST'])
def html_convert():

    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        file = open(app.config['UPLOAD_FOLDER'] + filename,"rb")

    custom_styles = """ i => cite
                        p[style-name='ordered'] => ol
                        p[style-name='details'] => details:fresh
                        p[style-name='btn-cta'] => button.btn-call-to-action
                        p[style-name='btn-primary'] => button.btn-primary
                        p[style-name='btn-secondary'] => button.btn-default
                        p[style-name='btn-danger'] => button.btn-danger
                        p[style-name='alert-danger'] => section.alert-danger > h2
                        p[style-name='alert-warning'] => section.alert-warning > h2
                        p[style-name='alert-info'] => section.alert-info > h2
                        p[style-name='alert-success'] => section.alert-success > h2
                        p[style-name='label-default'] => span.label-default
                        p[style-name='label-primary'] => span.label-primary
                        p[style-name='label-success'] => span.label-success
                        p[style-name='label-info'] => span.label-info
                        p[style-name='label-warning'] => span.label-warning
                        p[style-name='label-danger'] => span.label-danger
                        p[style-name='alert-text'] => alert > p
                        p[style-name='subway-group-h1'] => nav.gc-subway > h1
                        p[style-name='subway-section-h1'] => nav > h1.gc-thickline
                        p[style-name='subway-nav'] => li.hidden-xs:fresh
                        p[style-name='subway-nav-active'] => li.active
                        p[style-name='summary'] => summary"""


    with file as docx_file:
        result = mammoth.convert_to_html(docx_file, style_map = custom_styles)
        text = result.value
        with open('transitory/doc.html', 'w', encoding= 'unicode_escape') as html_file:
            html_file.write(text)


    #parse the html created from the word doc
    with open("transitory/doc.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    #parse the stable beginning of a Canada.ca page (header, menu)
    with open("templates/start.html") as fp:
        soup1 = BeautifulSoup(fp, 'html.parser')


    #parse the stable end of a Canada.ca page (pre-footer and footer)
    with open("templates/end.html") as fp:
        soup2 = BeautifulSoup(fp, 'html.parser')

    #prettify the html from word doc
    with open("transitory/doc_output.html", "w") as file:
        file.write(str((soup.prettify())))

    #combine the header, main and footer sections into a prettified html page
    with open("templates/page.html", "w") as file:
        file.write(str((soup1.prettify())+(soup.prettify())+(soup2.prettify())))



    #clean up the generated html page into filedata
    with open("templates/page.html", "r") as file:
        filedata = file.read()
        filedata = filedata.replace('</meta>\n </head>\n', '</head>\n')
        filedata = filedata.replace('<nav>\n   <ul id="wb-tphp">\n    <div class="par iparys_inherited">\n     <div class="global-header">\n', '<div class="par iparys_inherited">\n     <div class="global-header">\n')
        filedata = filedata.replace('<main class="container" property="mainContentOfPage" resource="#wb-main" typeof="WebPageElement">\n    </main>\n   </ul>\n  </nav>\n </body>\n</html><h1>', '<main class="container" property="mainContentOfPage" resource="#wb-main" typeof="WebPageElement">\n    <h1>')
        filedata = filedata.replace('</script>\n  </link>\n </head>\n', '</script>\n </head>\n')
        filedata = filedata.replace('<link href="https://www.canada.ca/etc/designs/canada/wet-boew/assets/wmms-blk.svg" property="logo"/>\n           </meta>\n          </meta>\n', '<link href="https://www.canada.ca/etc/designs/canada/wet-boew/assets/wmms-blk.svg" property="logo"/>\n')
        filedata = filedata.replace('<div class="par iparys_inherited">\n</div>\n<div class="par iparys_inherited">\n', '</main>\n<div class="par iparys_inherited">\n</div>\n<div class="par iparys_inherited">\n')
        filedata = filedata.replace('\n </a>\n ', '</a> ')
        filedata = filedata.replace('<h3>\n On this page\n</h3>', '<h2 class="h3">\n On this page\n</h2>')
        filedata = filedata.replace('<summary>\n', '<details>\n<summary>\n')
        filedata = filedata.replace('<details>\n end\n</details>\n', '</details>\n')
        filedata = filedata.replace('class="btn-call-to-action', 'class="btn btn-call-to-action')
        filedata = filedata.replace('class="btn-primary', 'class="btn btn-primary')
        filedata = filedata.replace('class="btn-default', 'class="btn btn-default')
        filedata = filedata.replace('class="btn-danger', 'class="btn btn-danger')
        filedata = filedata.replace('class="alert-danger', 'class="alert alert-danger')
        filedata = filedata.replace('class="alert-warning', 'class="alert alert-warning')
        filedata = filedata.replace('class="alert-info', 'class="alert alert-info')
        filedata = filedata.replace('class="alert-success', 'class="alert alert-success')
        filedata = filedata.replace('</section>\n<alert>\n', '')
        filedata = filedata.replace('</alert>', '</section>')
        filedata = filedata.replace('<table>', '<table class="provisional gc-table table" id="myTable1">')
        filedata = filedata.replace('class="label-default', 'class="label label-default')
        filedata = filedata.replace('class="label-primary', 'class="label label-primary')
        filedata = filedata.replace('class="label-success', 'class="label label-success')
        filedata = filedata.replace('class="label-info', 'class="label label-info')
        filedata = filedata.replace('class="label-warning', 'class="label label-warning')
        filedata = filedata.replace('class="label-danger', 'class="label label-danger')
        filedata = filedata.replace('class="gc-subway', 'class="provisional gc-subway')
        filedata = filedata.replace('<h1 class="gc-thickline">', '<h1 property="name" id="wb-cont" class="gc-thickline">')
        filedata = filedata.replace('</main>\n   </ul>\n  </nav>\n </body>\n</html><nav class="provisional gc-subway">\n <h1>\n', '<nav class="provisional gc-subway">\n <h1 id="gc-document-nav">\n')
        filedata = filedata.replace('<nav>\n <h1 property="name"', '</ul>\n </nav>\n <h1 property="name"')
        filedata = filedata.replace('<li class="active">\n <a href=', '<li><a class="active" aria-current="page" href=')
        filedata = filedata.replace('</nav>\n<li class="hidden-xs">\n', '<ul>\n<li class="hidden-xs">\n')
        filedata = filedata.replace('class="hidden-xs"', 'class="hidden-xs hidden-sm"')
        filedata = filedata.replace('<h2>\n <a id=', '<h2 id=')
        filedata = filedata.replace('<h3>\n <a id=', '<h3 id=')
        filedata = filedata.replace('<h4>\n <a id=', '<h4 id=')
        filedata = filedata.replace('"></a', '">')
        filedata = filedata.replace('\n </strong>', '\n</strong>')
        filedata = filedata.replace('\\xa0', '&nbsp;')
        filedata = filedata.replace('\\u2019', '&rsquo;')
        filedata = filedata.replace('\\u202f', '&nbsp;')
        filedata = filedata.replace('\\u201c', '&ldquo;')
        filedata = filedata.replace('\\u201d', '&rdquo;')
        filedata = filedata.replace('\\u2013', '&ndash;')
        filedata = filedata.replace('\\xc0', '&Agrave;')
        filedata = filedata.replace('\\xc2', '&Acirc;')
        filedata = filedata.replace('\\xc2', '&Acirc;')
        filedata = filedata.replace('\\xc7', '&Ccedil;')
        filedata = filedata.replace('\\xc8', '&Egrave;')
        filedata = filedata.replace('\\xc9', '&Eacute;')
        filedata = filedata.replace('\\xdb', '&Ucirc;')
        filedata = filedata.replace('\\xd4', '&Ocirc;')
        filedata = filedata.replace('\\xd6', '&Ouml;')
        filedata = filedata.replace('\\xd9', '&Ugrave;')
        filedata = filedata.replace('\\xe0', '&agrave;')
        filedata = filedata.replace('\\xe1', '&aacute;')
        filedata = filedata.replace('\\xe2', '&acirc;')
        filedata = filedata.replace('\\xe4', '&auml;')
        filedata = filedata.replace('\\xe6', '&aelig;')
        filedata = filedata.replace('\\xe7', '&ccedil;')
        filedata = filedata.replace('\\xe8', '&egrave;')
        filedata = filedata.replace('\\xe9', '&eacute;')
        filedata = filedata.replace('\\xea', '&ecirc;')
        filedata = filedata.replace('\\xf9', '&ugrave;')
        filedata = filedata.replace('\\xf4', '&ocirc;')
        filedata = filedata.replace('\\xf6', '&ouml;')
        filedata = filedata.replace('>>', '>')

    #write the cleaned up filedata to the html page
    with open('templates/page.html', 'w') as file:
      file.write(filedata)

    with open("templates/page.html") as fp:
         page_soup= BeautifulSoup(fp, 'html.parser')


    html_page = page_soup.prettify()

    lang = request.args.get('lang', 'en')

    if lang == 'en':
        return render_template("code_en.html", lang=lang, html_page=html_page)

    if lang == 'fr':
        return render_template("code_fr.html", lang=lang)

if __name__ == '__main__':
    app.run()
