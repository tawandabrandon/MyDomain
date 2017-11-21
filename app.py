from flask import Flask, flash, redirect, render_template, request, session, abort
import whois
app = Flask(__name__)
homePage = True
class domain(object):
	updated = ""
	name = ""
	dnssec = ""
	city = ""
	expires = ""
	zipcode = ""
	domain_name = ""
	country = ""
	whois_server = ""
	state = ""
	registrar = ""
	referral_url = ""
	address = ""
	ns = list()
	org = ""
	created = ""
	emails = list()
	status = list()
	
def parse(domain, info):
	domain.name = info.name
	domain.dnssec = str(info.dnssec)
	domain.updated = str(str(info.updated_date[0].year)+'/' + str(info.updated_date[0].month)+'/' + str(info.updated_date[0].day))
	domain.city = str(info.city)
	domain.expires = str(str(info.expiration_date[0].year)+'/' + str(info.expiration_date[0].month)+'/' + str(info.expiration_date[0].day))
	domain.zipcode = str(info.zipcode)
	domain.domain_name = str(info.domain_name[1])
	domain.country = str(info.country)
	domain.whois_server = str(info.whois_server)
	domain.state = str(info.state)
	domain.registrar = str(info.registrar)
	domain.referral_url = str(info.referral_url)
	domain.address = str(info.address)
	for x in info.name_servers:
		if not (str(x).lower() in domain.ns):
			domain.ns.append(str(x).lower())

	domain.org = str(info.org)
	domain.created = str(str(info.creation_date[0].year)+'/' + str(info.creation_date[0].month)+'/' + str(info.creation_date[0].day))
	for x in info.emails:
		domain.emails.append(str(x))
	for x in info.status:
			domain.status.append(str(x))
	return domain


def domainHandler(domainName):
	info = whois.whois(domainName)

	return info


@app.route("/")
def index():
	homePage = True;
	return render_template('home.html', homePage = homePage)

@app.route('/', methods=["POST"])
def myDomainer():
	domainName = request.form['entry']
	answer = domainHandler(domainName)
	info = parse(domain,answer)
	homePage = False
	return render_template('wadii.html', info=info, homePage = homePage)

@app.route("/wadii/<string:name>/")
def wadii(name):
	return render_template('wadii.html', name=name)

if __name__ == '__main__':
	app.run()