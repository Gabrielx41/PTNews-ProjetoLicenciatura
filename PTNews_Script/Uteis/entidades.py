import spacy
from .uteis import exist


def get_entidades(texto):
    loc = []
    per = []
    org = []
    misc = []
    try:
        nlp = spacy.load('pt_core_news_sm')
        doc = nlp(texto)
    except:
        return {"PER": [], "LOC": [], "ORG": [], "MISC": []}
    
    for ent in doc.ents:
        match (ent.label_):
            case "PER": 
                if (not ent.text in per):
                    per.append(ent.text)
                
            case "LOC":
                if (not ent.text in loc):
                    loc.append(ent.text)
                
            case "ORG":
                if (not ent.text in org):
                    org.append(ent.text)
                
            case "MISC":
                if (not ent.text in misc):
                    misc.append(ent.text)
                
    return {"PER": exist(per, per), 
            "LOC": exist(loc, loc), 
            "ORG": exist(org, org), 
            "MISC": exist(misc, misc)
            }