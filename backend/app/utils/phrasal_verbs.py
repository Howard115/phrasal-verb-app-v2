import csv
from pathlib import Path
from typing import List
from app.models import PhrasalVerbEntry

def load_phrasal_verbs() -> List[PhrasalVerbEntry]:
    """
    Load phrasal verbs from the CSV file.
    Returns a list of PhrasalVerb objects.
    """
    csv_path = Path("./phrasal-verbs.csv")
    
    if not csv_path.exists():
        return []
        
    phrasal_verbs = []
    
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            phrasal_verbs.append(PhrasalVerbEntry(
                phrasal_verb=row["Phrasal Verb"],
                meaning=row["Meaning"],
                example=row["Example"]
            ))
    
    return phrasal_verbs 