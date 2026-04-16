def preprocess_input(data):
    """
    Transforms JSON input into standard format required by the model.
    Categorical mappings:
    weather_condition: Clear=0, Rain=1, Storm=2
    equipment_health: Good=0, Moderate=1, Poor=2
    maintenance_delay: No=0, Yes=1
    """
    
    weather_map = {'Clear': 0, 'Rain': 1, 'Storm': 2}
    health_map = {'Good': 0, 'Moderate': 1, 'Poor': 2}
    
    # Process Maintenance Delay: 'Yes'/'No' string or True/False
    md_raw = data.get('maintenance_delay', 'No')
    if isinstance(md_raw, str):
        md = 1 if md_raw.lower() == 'yes' else 0
    else:
        md = 1 if md_raw else 0
        
    weather_cond = weather_map.get(data.get('weather_condition', 'Clear'), 0)
    health = health_map.get(data.get('equipment_health', 'Good'), 0)
    
    features = [
        float(data.get('load_percentage', 50.0)),
        float(data.get('temperature', 25.0)),
        weather_cond,
        health,
        md
    ]
    return features

def evaluate_risk(probability):
    """
    Returns risk level strings based on percentage
    Low (0-40%), Medium (41-70%), High (71-100%)
    """
    if probability <= 40:
        return 'LOW'
    elif probability <= 70:
        return 'MEDIUM'
    else:
        return 'HIGH'

def generate_recommendations(data, risk_level):
    """
    Generates dynamic recommendations based on input context
    """
    recs = []
    zone = data.get('zone_name', 'your zone')
    
    if risk_level == 'HIGH':
        recs.append(f"URGENT: Reduce load immediately in {zone}.")
        recs.append("Activate backup power supply.")
    elif risk_level == 'MEDIUM':
        recs.append(f"Monitor load levels closely in {zone}.")
        
    if data.get('equipment_health') == 'Poor':
        recs.append("Schedule preventive maintenance immediately.")
    
    if data.get('weather_condition') == 'Storm':
        recs.append("Prepare emergency response teams for extreme weather.")
        
    if not recs:
        recs.append("Operations normal. Continue routine monitoring.")
        
    return recs
