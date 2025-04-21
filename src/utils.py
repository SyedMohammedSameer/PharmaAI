import json
import os

def save_conversation(user_input, context, llm_response, save_dir="./conversations"):
    """Save conversation for later review or analysis."""
    os.makedirs(save_dir, exist_ok=True)
    
    # Create a unique filename based on timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.json"
    
    conversation_data = {
        "timestamp": str(datetime.datetime.now()),
        "user_input": user_input,
        "context_summary": context[:200] + "..." if len(context) > 200 else context,
        "llm_response": llm_response
    }
    
    with open(os.path.join(save_dir, filename), 'w') as f:
        json.dump(conversation_data, f, indent=2)

def format_medicine_info(medicine):
    """Format medicine information for display."""
    return f"""
## {medicine['name']} ({medicine['generic_name']})

**Manufacturer:** {medicine['manufacturer']}
**Dosage:** {medicine['dosage']}
**Indications:** {medicine['indications']}

**Contraindications:** {medicine['contraindications']}
**Side Effects:** {medicine['side_effects']}
**Mechanism of Action:** {medicine['mechanism_of_action']}
**Drug Interactions:** {medicine['drug_interactions']}
"""

def prepare_sample_medicines_json():
    """Create a sample medicines.json file for testing if it doesn't exist."""
    if not os.path.exists("./data"):
        os.makedirs("./data")
    
    if not os.path.exists("./data/medicines.json"):
        sample_data = [
            {
                "medicine_id": 1,
                "name": "Tylenol",
                "generic_name": "Acetaminophen",
                "manufacturer": "Johnson & Johnson",
                "dosage": "500-1000 mg orally every 4-6 hours as needed (max ~3000 mg per day for adults)",
                "indications": "Mild to moderate pain, fever reduction",
                "contraindications": "Severe hepatic impairment or active liver disease; hypersensitivity to acetaminophen",
                "side_effects": "Generally well tolerated; possible nausea, rash; hepatotoxicity in overdose",
                "mechanism_of_action": "Inhibits prostaglandin synthesis in the central nervous system, leading to analgesic and antipyretic effects (with minimal anti-inflammatory action)",
                "drug_interactions": "Excessive alcohol use increases risk of liver damage; concurrent use with other acetaminophen-containing products can lead to overdose"
            },
            {
                "medicine_id": 2,
                "name": "Advil",
                "generic_name": "Ibuprofen",
                "manufacturer": "Pfizer",
                "dosage": "400-800 mg orally every 6-8 hours as needed (for pain/fever); max 3200 mg/day",
                "indications": "Mild to moderate pain, fever, and inflammatory conditions (such as arthritis, muscle aches)",
                "contraindications": "Active gastrointestinal bleeding or ulcer, severe renal impairment; history of NSAID-induced asthma or urticaria",
                "side_effects": "Upset stomach, nausea, heartburn; risk of GI ulceration or bleeding, elevated blood pressure, kidney dysfunction",
                "mechanism_of_action": "Reversibly inhibits COX-1 and COX-2 enzymes, reducing prostaglandin synthesis which results in analgesic, anti-inflammatory, and antipyretic effects",
                "drug_interactions": "Concurrent use with warfarin or other blood thinners increases bleeding risk; may reduce antihypertensive efficacy; concomitant use with other NSAIDs or corticosteroids heightens GI injury risk"
            }
        ]
        
        with open("./data/medicines.json", 'w') as f:
            json.dump(sample_data, f, indent=2)