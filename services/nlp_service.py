import spacy


nlp = spacy.load("en_core_web_sm")


def extract_entities(text):

    doc = nlp(text)

    entities = {

        "money": [],
        "dates": [],
        "organizations": []
    }

    for ent in doc.ents:

        if ent.label_ == "MONEY":
            entities["money"].append(ent.text)

        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)

        elif ent.label_ == "ORG":
            entities["organizations"].append(ent.text)

    return entities