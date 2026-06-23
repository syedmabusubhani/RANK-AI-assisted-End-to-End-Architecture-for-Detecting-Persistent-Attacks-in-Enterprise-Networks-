from mitreattack.stix20 import MitreAttackData

# Load the Enterprise ATT&CK framework
mitre_attack_data = MitreAttackData("enterprise-attack.json")
tactics = mitre_attack_data.get_techniques(remove_revoked_deprecated=True)
techniques = []
for tactic in tactics:
    techniques.append(tactic["external_references"][0]['external_id'])

def get_tactic_score(technique_id):
    """
    Calculates a score for each tactic based on the presence of a given technique.
    A tactic receives a score of 1 if the technique is associated with it, otherwise 0.
    """
    technique = mitre_attack_data.get_object_by_attack_id(technique_id, "attack-pattern")
    if technique:
        tactic_refs = technique.get("kill_chain_phases", [])
        tactic_scores = {}
        for tactic_ref in tactic_refs:
            tactic_name = tactic_ref["phase_name"]
            tactic_scores[tactic_name] = 1
        
        # Add tactics with a score of 0 if the technique is not associated with them
        all_tactics = mitre_attack_data.get_tactics()
        for tactic in all_tactics:
            if tactic["name"] not in tactic_scores:
                tactic_scores[tactic["name"]] = 0
                
        return tactic_scores
    else:
        return None
for i in range(len(techniques)):
    # Example usage: Get tactic scores for technique T1059.001 (PowerShell) 
    technique_id = techniques[i]
    tactic_scores = get_tactic_score(technique_id)
    if tactic_scores:
        total = 0
        for tactic, score in tactic_scores.items():
            total += score
        if total > 1:
            total = total / len(tactic_scores.items())
            print(str(total)+" "+technique_id)
    else:
        print(f"Technique {technique_id} not found.")
