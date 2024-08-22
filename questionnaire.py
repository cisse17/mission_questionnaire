
import json
import sys

class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def FromJsonData(data):
        choix = [i[0] for i in data["choix"]]
        bonne_reponse = [i[0] for i in data["choix"] if i[1] == True]
        if len(bonne_reponse) != 1:
            return None
        q = Question(data["titre"], choix, bonne_reponse[0])
        return q

    def poser_question(self, numero_question, nbre_questions):
        print(f"QUESTION N° {numero_question} / {nbre_questions}")
        print(" " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1] == self.bonne_reponse:
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
    
class Questionnaire:
    def __init__(self, questions, titre, categorie, difficulte):
        self.questions = questions
        self.titre = titre
        self.categorie = categorie
        self.difficulte = difficulte
    
    def from_json_data(data):
        questionnaire_data = data["questions"]
        # questionnaire_data = questions[0]
        questions = [ Question.FromJsonData(i) for i in questionnaire_data]

        return Questionnaire(questions, data["titre"], data["categorie"], data["difficulte"])

    def recuperer_file_json(filename):
        try:
            # Chargement du fichier json
            file = open(filename)
            json_data = file.read()
            file.close()
            data = json.loads(json_data)
        except:
            print(f'ERREUR : exception lors de l\'ouverture du fichier  "{filename}" assurez-vous d\'avoir charger un fichier json valide.')
            return None

        return Questionnaire.from_json_data(data)
    
    def lancer(self):
        print("***************************")
        print("Questionnaire : ", self.titre)
        print("Categorie : ", self.categorie)
        print("Difficulte : ", self.difficulte)
        print("Nombre de questions : ", len(self.questions))
        print("***************************")
        score = 0

        for q in range(len(self.questions)):
            question = self.questions[q]
            if question.poser_question(q+1, len(self.questions)):
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


#Questionnaire.from_json_data(data).lancer()

# LANCEMENT DU FICHIER JSON EN LIGNE DE COMMANDE (argv)
  
if len(sys.argv) < 2:
    print("ERREUR : vous devez preciser le nom du fichier json à charger ou à lancer")
    exit(0)

json_file_name = sys.argv[1]
quetionnaire = Questionnaire.recuperer_file_json(json_file_name)
if quetionnaire:
    quetionnaire.lancer()

    









    


