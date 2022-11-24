Note: this repo will not ne updated. Official repo is now at https://github.com/alpha-canada-ca/doc_to_html, and the tool itself can be accessed at https://doc-to-html.tbs.alpha.canada.ca/

# From Word doc to full Canada.ca html
This is an experiment to try to turn Word documents into the full HTML code for Canada.ca pages.

## Use the template
Use the template.dotx file in this repo and connect it to your word doc. Disclosure: it's messy right now and needs a cleanup.

## Use the styles in Word
Use the styles in Word (Heading 1, Heading 2, bullet, btn-primary, etc.) for them to be turned into the right HTML tags and classes. Some styles are a bit complicated to use at the moment. You can look at the various test_code files in the repo for examples.

### Expand collapse
To use the expand collapse:
- apply the "summary" style to the visible part of the expand collapse.
- use whatever style for what's hidden
- after the hidden part, add the word "end" (no caps, not bold, nothing), and apply the "details" style. This will tell the script when to close the details HTML tag.

### Alerts
Alerts need a heading. Apply the right alert style to the heading (alert-info, alert-warning, alert-danger, etc.), and apply "alert-text" to the text within the alert.

## Running the web app

### Without VSCode and DevContainers
- you need Python 3 and a few packages to run the script, to install the packages run `pip3 install -r requirements.txt`
- run  the script with the command `python3 app.py`


### With VSCode and DevContainers

If you are using VSCode and have docker engine running on your machine you can use the **Remote - Containers** plugin to create a standardized development enviroment for this project. 

To install dependencies run `make install` from within the dev container.  
To run the app run `make run` from within the devcontainer.

### Once Running

- go to http://127.0.0.1:5000/ in a web browser
- select a docx document
- this will create a page that will show the whole code in expand-collapse and the fully prototyped page

## Using the HTML in a prototype
- if in AEM, only paste the middle part (after the H1, before the footer)
- if in GitHub, paste the whole HTML in a file - it will create an entire Canada.ca page
