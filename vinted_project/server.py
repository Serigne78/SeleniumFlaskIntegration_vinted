from flask import Flask, render_template, request ,redirect, url_for

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time



app =Flask(__name__)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.vinted.fr/catalog?search_text=jordan%204&search_id=11993295535&size_ids[]=792&order=newest_first")


def pictures_recup():
      liste =[]
      
      pictures = driver.find_elements(By.CLASS_NAME, value='web_ui__Image__content')
      for pic in pictures:
            if len(pic.get_attribute("src")) == 129:
                  liste.append((pic.get_attribute("src")))
      return liste


def price_recup():
      liste =[]
      element_prix = driver.find_elements(By.CLASS_NAME, value='title-content')
      for pic in element_prix:
            liste.append(pic.text)
      return liste


def profile_photo():
      liste =[]
      profile = driver.find_elements(By.CLASS_NAME, value='web_ui__Image__content')
      for pic in profile:
            if len(pic.get_attribute("src")) ==127:
                  liste.append(pic.get_attribute("src"))
      return liste





miniature = pictures_recup()
prix = price_recup()
photo = profile_photo()





@app.route('/index.html')
def home():
      return render_template("index.html", MINIATURE= miniature, PRIX=prix, PHOTO=photo, zip=zip)




# Route pour la page de contact, accessible via GET et POST
@app.route('/contact.html', methods=["GET", "POST"])
def contact():
    if request.method == "POST":  # Si la requête est de type POST (formulaire soumis)
        try:
            # Récupération des données du formulaire
            name = request.form["prenom"]
            email = request.form["mail"]
            telephone = request.form["telephone"]
            message = request.form["message"]

            # Redirection vers la page de réception avec les données du formulaire
            return redirect(url_for('receive', name=name, email=email, telephone=telephone, message=message))
        except KeyError as e:
            # Gestion de l'erreur si certains champs du formulaire sont manquants
            return "Erreur : Certains champs du formulaire sont manquants.", 400
    else:  # Si la requête est de type GET (accès direct à la page de contact)
        # Affichage du formulaire de contact
        return render_template("contact.html")

# Route pour la page de réception, accessible via GET et POST
@app.route("/receive.html", methods=["GET", "POST"])
def receive():
    if request.method == "GET":  # Si la requête est de type GET (accès direct à la page de réception)
        # Récupération des données transmises dans la chaîne de requête
        name = request.args.get("prenom")
        email = request.args.get("mail")
        telephone = request.args.get("telephone")
        message = request.args.get("message")
    elif request.method == "POST":  # Si la requête est de type POST (formulaire soumis)
        # Récupération des données du formulaire
        name = request.form["prenom"]
        email = request.form["mail"]
        telephone = request.form["telephone"]
        message = request.form["message"]

    # Affichage des données sur la page de réception
    return render_template("receive.html", name=name, email=email, telephone=telephone, message=message)

if __name__ == "__main__":
    # Lancement de l'application Flask en mode debug sur le port 8080
    app.run(debug=True, port=8080)