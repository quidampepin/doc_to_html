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
        return render_template("index_fr.html", lang=lang)

@app.route('/instructions', methods=['GET', 'POST'])
def instructions():
    lang = request.args.get('lang', 'en')
    if lang == 'en':
        return render_template("instructions_en.html", lang=lang)
    if lang == 'fr':
        return render_template("instructions_fr.html", lang=lang)


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
                        p[style-name='btn-cta'] => a.btn-call-to-action
                        p[style-name='btn-primary'] => a.btn-primary
                        p[style-name='btn-secondary'] => a.btn-default
                        p[style-name='btn-danger'] => a.btn-danger
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
                        p[style-name='summary'] => summary
                        p[style-name='multi-page-start'] => ul.toc
                        p[style-name='multi-page-end'] => div
                        p[style-name='multi-page-item'] => li.multi:fresh
                        p[style-name='next'] => nav.next
                        p[style-name='previous'] => nav.previous
                        p[style-name='H1-ILP'] => div.provisional > h1
                        p[style-name='image-ILP'] => img.ilp
                        p[style-name='most_requested'] => section.most_requested > h2
                        p[style-name='mr_link'] => li.most_requested:fresh
                        p[style-name='doormat'] => div.col-md-4 > h3:fresh
                        p[style-name='ilp-feature'] => section.gc-feature > h2
                        p[style-name='end-doormats'] => div.row > div.col
                        p[style-name='ilp-feature-link'] => h3.h5
                        p[style-name='ilp-social-media-h2'] => section.follow-us > h2
                        p[style-name='ilp-facebook'] => li.facebook:fresh
                        p[style-name='ilp-twitter'] => li.twitter:fresh
                        p[style-name='ilp-youtube'] => li.youtube:fresh
                        p[style-name='ilp-insta'] => li.instagram:fresh
                        p[style-name='ilp-linkedin'] => li.linkedin:fresh
                        p[style-name='ilp-contributors'] => section.gc-contributors > h2
                        p[style-name='multi-page-active'] => li.multiactive"""

    lang = request.args.get('lang', 'en')



    with file as docx_file:
        result = mammoth.convert_to_html(docx_file, style_map = custom_styles)
        text = result.value
        with open('transitory/doc.html', 'w', encoding= 'unicode_escape') as html_file:
            html_file.write(text)


    #parse the html created from the word doc
    with open("transitory/doc.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')



        if lang == 'en':

            #parse the stable beginning of a Canada.ca page (header, menu)
            with open("templates/start_en.html") as fp:
                soup1 = BeautifulSoup(fp, 'html.parser')


            #parse the stable end of a Canada.ca page (pre-footer and footer)
            with open("templates/end_en.html") as fp:
                soup2 = BeautifulSoup(fp, 'html.parser')

            #combine the header, main and footer sections into a prettified html page
            with open("templates/page.html", "w") as file:
                file.write(str(soup1)+str(soup)+str(soup2))



        if lang == 'fr':

        #parse the stable beginning of a Canada.ca page (header, menu)
            with open("templates/start_fr.html") as fp:
                soup1 = BeautifulSoup(fp, 'html.parser')


            #parse the stable end of a Canada.ca page (pre-footer and footer)
            with open("templates/end_fr.html") as fp:
                soup2 = BeautifulSoup(fp, 'html.parser')

            #combine the header, main and footer sections into a prettified html page
            with open("templates/page.html", "w") as file:
                file.write(str(soup1)+str(soup)+str(soup2))


#clean up the generated html page into filedata

    with open("templates/page.html", "r") as file:
        filedata = file.read()
        filedata = filedata.replace('</main></body></html><h1>', '<h1>')
        filedata = filedata.replace('<h3>On this page</h3>', '<h2 class="h3">On this page</h2>')
        filedata = filedata.replace('<h3>Sur cette page</h3>', '<h2 class="h3">Sur cette page</h2>')
        filedata = filedata.replace('<summary>', '<details><summary>')
        filedata = filedata.replace('<details>end</details>', '</details>')
        filedata = filedata.replace('class="alert-danger', 'class="alert alert-danger')
        filedata = filedata.replace('class="alert-warning', 'class="alert alert-warning')
        filedata = filedata.replace('class="alert-info', 'class="alert alert-info')
        filedata = filedata.replace('class="alert-success', 'class="alert alert-success')
        filedata = filedata.replace('</section><alert>', '')
        filedata = filedata.replace('</alert>', '</section>')
        filedata = filedata.replace('<table>', '<table class="provisional gc-table table" id="myTable1">')
        filedata = filedata.replace('<a class="btn-call-to-action"><a ', '<a class="btn btn-call-to-action" ')
        filedata = filedata.replace('<a class="btn-primary"><a ', '<a class="btn btn-primary" ')
        filedata = filedata.replace('<a class="btn-default"><a ', '<a class="btn btn-default" ')
        filedata = filedata.replace('<a class="btn-danger"><a ', '<a class="btn btn-danger" ')
        filedata = filedata.replace('class="label-default', 'class="label label-default')
        filedata = filedata.replace('class="label-primary', 'class="label label-primary')
        filedata = filedata.replace('class="label-success', 'class="label label-success')
        filedata = filedata.replace('class="label-info', 'class="label label-info')
        filedata = filedata.replace('class="label-warning', 'class="label label-warning')
        filedata = filedata.replace('class="label-danger', 'class="label label-danger')
        filedata = filedata.replace('class="gc-subway', 'class="provisional gc-subway')
        filedata = filedata.replace('<h1 class="gc-thickline">', '<h1 property="name" id="wb-cont" class="gc-thickline">')
        filedata = filedata.replace('<nav class="provisional gc-subway"><h1>', '<nav class="provisional gc-subway"><h1 id="gc-document-nav">')
        filedata = filedata.replace('</main></body></html><nav class="provisional gc-subway">', ' <nav class="provisional gc-subway">')
        filedata = filedata.replace('<nav><h1 property="name"', '</ul></nav><h1 property="name"')
        filedata = filedata.replace('</nav><li class="active">', '<ul><li class="active">')
        filedata = filedata.replace('<li class="active"><a href=', '<li><a class="active" aria-current="page" href=')
        filedata = filedata.replace('</nav><li class="hidden-xs">', '<ul><li class="hidden-xs">')
        filedata = filedata.replace('<ul class="toc">', '<div class="mrgn-tp-md mrgn-bttm-lg brdr-bttm"><div class="row"><ul class="toc lst-spcd">')
        filedata = filedata.replace('class="hidden-xs"', 'class="hidden-xs hidden-sm"')
        filedata = filedata.replace('<li class="multi"><a', '<li class="col-md-4"><a class="list-group-item" ')
        filedata = filedata.replace('<li class="multiactive">', '<li class="col-md-4"><a class="list-group-item active" ')
        filedata = filedata.replace('start</ul>', '')
        filedata = filedata.replace('<div>end</div>', '</ul>')
        filedata = filedata.replace('<nav class="next">', '<nav class="mrgn-bttm-lg mrgn-tp-lg"><h3 class="wb-inv">Document navigation</h3><ul class="pager"><li class="next">')
        filedata = filedata.replace('<nav class="previous">', '<nav class="mrgn-bttm-lg mrgn-tp-lg"><h3 class="wb-inv">Document navigation</h3><ul class="pager"><li class="previous">')
        filedata = filedata.replace('</a></nav>">', '</li></ul></nav>')
        filedata = filedata.replace('<main class="container" property="mainContentOfPage" resource="#wb-main" typeof="WebPageElement">\n</main></body></html><div class="provisional"><h1>', '<main property="mainContentOfPage" resource="#wb-main" typeof="WebPageElement"><div class="container"><div class="row"><div class="col-md-6"><h1 property="name" id="wb-cont">')
        filedata = filedata.replace('<img class="ilp"/>', '</div><div class="col-md-6 mrgn-tp-sm hidden-sm hidden-xs provisional gc-topic-bg"><div data-bgimg>')
        filedata = filedata.replace('</h1></div>', '</h1>')
        filedata = filedata.replace('<section class="most_requested">', '</div></div></div></div><section class="well well-sm provisional gc-most-requested"><div class="container"><div class="row"><div class="col-md-2">')
        filedata = filedata.replace('</h2></section><li class="most_requested">', '</h2></div><div class="col-md-10"><ul class="colcount-md-2"><li>')
        filedata = filedata.replace('<li class="most_requested">', '<li>')
        filedata = filedata.replace('<p><strong>Services and information</strong></p>', '</ul></div></div></div></section><div class="container"><section class="gc-srvinfo"><h2 class="wb-inv">Services and information</h2><div class="row wb-eqht-grd">')
        filedata = filedata.replace('</h3></div><p>', '</h3><p>')
        filedata = filedata.replace('</p><div class="col-md-4">', '</p></div><div class="col-md-4">')
        filedata = filedata.replace('<div class="row"><div class="col">(end of doormats)</div></div>', '</div></div></section>')
        filedata = filedata.replace('<section class="gc-feature"><h2>Features</h2></section><p><img', '<div class="row mrgn-tp-xl"><div class="col-md-8"><section class="gc-feature"><h2 class="wb-inv">Features</h2><div class="row"><div class="col-md-6"><img')
        filedata = filedata.replace('<h3 class="h5"><a', '</div><div class="col-md-6"><h3 class="h5"><a class="stretched-link"')
        filedata = filedata.replace('<section class="follow-us"><h2>On social media</h2></section>', '</div></div></section></div><div class="col-md-4"><section class="provisional gc-followus"><h2>On social media</h2><ul>')
        filedata = filedata.replace('<li class="facebook"><a', '<li><a class="facebook wb-lbx "')
        filedata = filedata.replace('<li class="twitter"><a', '<li><a class="twitter "')
        filedata = filedata.replace('<li class="youtube"><a', '<li><a class="youtube "')
        filedata = filedata.replace('<li class="instagram"><a', '<li><a class="instagram "')
        filedata = filedata.replace('<li class="linkedin"><a', '<li><a class="linkedin "')
        filedata = filedata.replace('<section class="gc-contributors"><h2>From:</h2></section>', '<section class="provisional gc-contributors"><h2>From:</h2>')
        filedata = filedata.replace('</li><section class="provisional gc-contributors">', '</ul></section></div></div><section class="provisional gc-contributors">')
        filedata = filedata.replace('<h2><a id=', '<h2 id=')
        filedata = filedata.replace('<h3><a id=', '<h3 id=')
        filedata = filedata.replace('<h4><a id=', '<h4 id=')
        filedata = filedata.replace('"></a', '">')
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
        filedata2 = filedata.split('<!--CONTENT STARTS HERE-->')
        filedata2 = filedata2[1]
        filedata3 = filedata2.split('<!-- CONTENT ENDS HERE -->')
        filedata3 = filedata3[0]

        #write the cleaned up filedata to the html page
        with open('templates/page.html', 'w') as file:
          file.write(filedata)

        with open('templates/page_aem.html', 'w') as file:
          file.write(filedata3)

        with open("templates/page.html") as fp:
             page_soup= BeautifulSoup(fp, 'html.parser')

        with open("templates/page_aem.html") as fp:
             pageaem_soup= BeautifulSoup(fp, 'html.parser')


        html_page = page_soup
        aem_page = pageaem_soup


    if lang == 'en':

        return render_template("code_en.html", lang=lang, html_page=html_page, aem_page=aem_page)

    if lang == 'fr':

        return render_template("code_fr.html", lang=lang, html_page=html_page, aem_page=aem_page)


if __name__ == '__main__':
    app.run()
