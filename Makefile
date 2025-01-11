export FLASK_APP=app.py
export FLASK_DEBUG=1

run:
	npx raml2html doc.raml > templates/doc.html
	flask run --port=5000
