"""
Seed database with realistic Uttarakhand/Himachal Pradesh risk zones
and sample incidents for demonstration purposes.
All geographic coordinates are real locations in the Indian Himalayas.
"""
from datetime import datetime, timezone, timedelta
import random
from database import models
from services.priority_service import compute_priority_score
from services.verification_service import compute_verification_confidence, determine_verification_status

# Uttarakhand / HP risk zones — real geographic coordinates
ZONES_DATA = [
    {
        "name": "Chamoli — Badrinath Highway",
        "district": "Chamoli",
        "latitude": 30.744, "longitude": 79.493,
        "radius_km": 8,
        "rainfall_mm": 145, "rainfall_intensity": 9.8,
        "cumulative_rainfall": 320, "soil_moisture": 0.82,
        "slope_degrees": 48, "elevation_m": 1900,
        "vegetation_index": 0.28, "geology_risk": 0.72, "drainage_score": 0.25,
        "population_at_risk": 1200, "roads_at_risk": 3,
        "hospitals_nearby": 1, "schools_nearby": 2,
    },
    {
        "name": "Uttarkashi — Gangotri Road",
        "district": "Uttarkashi",
        "latitude": 30.729, "longitude": 78.436,
        "radius_km": 6,
        "rainfall_mm": 98, "rainfall_intensity": 6.2,
        "cumulative_rainfall": 210, "soil_moisture": 0.65,
        "slope_degrees": 38, "elevation_m": 1450,
        "vegetation_index": 0.45, "geology_risk": 0.55, "drainage_score": 0.40,
        "population_at_risk": 800, "roads_at_risk": 2,
        "hospitals_nearby": 0, "schools_nearby": 1,
    },
    {
        "name": "Pithoragarh — Dharchula Corridor",
        "district": "Pithoragarh",
        "latitude": 29.582, "longitude": 80.218,
        "radius_km": 10,
        "rainfall_mm": 78, "rainfall_intensity": 4.5,
        "cumulative_rainfall": 165, "soil_moisture": 0.50,
        "slope_degrees": 32, "elevation_m": 1200,
        "vegetation_index": 0.55, "geology_risk": 0.42, "drainage_score": 0.55,
        "population_at_risk": 2500, "roads_at_risk": 4,
        "hospitals_nearby": 1, "schools_nearby": 3,
    },
    {
        "name": "Rudraprayag — Kedarnath Zone",
        "district": "Rudraprayag",
        "latitude": 30.285, "longitude": 79.007,
        "radius_km": 12,
        "rainfall_mm": 185, "rainfall_intensity": 13.2,
        "cumulative_rainfall": 420, "soil_moisture": 0.91,
        "slope_degrees": 55, "elevation_m": 2400,
        "vegetation_index": 0.20, "geology_risk": 0.85, "drainage_score": 0.18,
        "population_at_risk": 650, "roads_at_risk": 2,
        "hospitals_nearby": 0, "schools_nearby": 0,
    },
    {
        "name": "Tehri — New Tehri Urban Zone",
        "district": "Tehri Garhwal",
        "latitude": 30.378, "longitude": 78.480,
        "radius_km": 5,
        "rainfall_mm": 45, "rainfall_intensity": 2.8,
        "cumulative_rainfall": 95, "soil_moisture": 0.38,
        "slope_degrees": 22, "elevation_m": 770,
        "vegetation_index": 0.62, "geology_risk": 0.30, "drainage_score": 0.68,
        "population_at_risk": 15000, "roads_at_risk": 5,
        "hospitals_nearby": 2, "schools_nearby": 8,
    },
    {
        "name": "Nainital — Bhowali Road",
        "district": "Nainital",
        "latitude": 29.392, "longitude": 79.463,
        "radius_km": 4,
        "rainfall_mm": 65, "rainfall_intensity": 3.9,
        "cumulative_rainfall": 140, "soil_moisture": 0.48,
        "slope_degrees": 28, "elevation_m": 1350,
        "vegetation_index": 0.70, "geology_risk": 0.35, "drainage_score": 0.60,
        "population_at_risk": 5000, "roads_at_risk": 3,
        "hospitals_nearby": 1, "schools_nearby": 4,
    },
    {
        "name": "Joshimath — Auli Slope",
        "district": "Chamoli",
        "latitude": 30.556, "longitude": 79.564,
        "radius_km": 7,
        "rainfall_mm": 110, "rainfall_intensity": 7.5,
        "cumulative_rainfall": 260, "soil_moisture": 0.75,
        "slope_degrees": 44, "elevation_m": 1890,
        "vegetation_index": 0.32, "geology_risk": 0.78, "drainage_score": 0.28,
        "population_at_risk": 4500, "roads_at_risk": 2,
        "hospitals_nearby": 1, "schools_nearby": 2,
    },
    {
        "name": "Dharamshala — McLeod Ganj",
        "district": "Kangra",
        "latitude": 32.219, "longitude": 76.319,
        "radius_km": 5,
        "rainfall_mm": 55, "rainfall_intensity": 3.2,
        "cumulative_rainfall": 120, "soil_moisture": 0.44,
        "slope_degrees": 30, "elevation_m": 1450,
        "vegetation_index": 0.68, "geology_risk": 0.38, "drainage_score": 0.55,
        "population_at_risk": 12000, "roads_at_risk": 4,
        "hospitals_nearby": 2, "schools_nearby": 5,
    },
]

INCIDENT_DATA = [
    {
        "incident_id": "INC-2024-0001",
        "title": "Major Landslide — Badrinath Highway KM-142",
        "incident_type": "landslide",
        "severity": "critical",
        "latitude": 30.748, "longitude": 79.496,
        "location_description": "Badrinath Highway KM 142, near Pipalkoti",
        "district": "Chamoli",
        "status": "verified",
        "verification_confidence": 94,
        "road_blocked": True,
        "road_name": "NH-58 Badrinath Highway",
        "people_affected": 320,
        "houses_damaged": 4,
        "description": "Large debris flow blocking both lanes. Estimated 2000m3 material.",
        "hours_ago": 3,
    },
    {
        "incident_id": "INC-2024-0002",
        "title": "Rockfall — Kedarnath Pilgrim Route",
        "incident_type": "rockfall",
        "severity": "severe",
        "latitude": 30.288, "longitude": 79.012,
        "location_description": "Kedarnath trekking route, 3km before temple",
        "district": "Rudraprayag",
        "status": "corroborated",
        "verification_confidence": 71,
        "road_blocked": False,
        "people_affected": 150,
        "description": "Multiple boulders fallen on pilgrim path. Trail partially blocked.",
        "hours_ago": 1.5,
    },
    {
        "incident_id": "INC-2024-0003",
        "title": "Ground Cracks — Joshimath Housing",
        "incident_type": "ground_cracks",
        "severity": "moderate",
        "latitude": 30.559, "longitude": 79.566,
        "location_description": "Ward No. 4, Joshimath town",
        "district": "Chamoli",
        "status": "under_review",
        "verification_confidence": 45,
        "road_blocked": False,
        "people_affected": 80,
        "houses_damaged": 12,
        "description": "Progressive ground cracking reported in multiple structures.",
        "hours_ago": 6,
    },
    {
        "incident_id": "INC-2024-0004",
        "title": "Mudslide — Uttarkashi District Road",
        "incident_type": "mudslide",
        "severity": "severe",
        "latitude": 30.733, "longitude": 78.440,
        "location_description": "Uttarkashi-Bhatwari Road KM 28",
        "district": "Uttarkashi",
        "status": "reported",
        "verification_confidence": 28,
        "road_blocked": True,
        "people_affected": 45,
        "description": "Mud and debris flow reported by locals. Road access cut off.",
        "hours_ago": 0.5,
    },
    {
        "incident_id": "INC-2024-0005",
        "title": "Soil Movement — Nainital Hillside",
        "incident_type": "soil_movement",
        "severity": "minor",
        "latitude": 29.395, "longitude": 79.460,
        "location_description": "Mallital, Nainital — Hillside near Ballia Nala",
        "district": "Nainital",
        "status": "reported",
        "verification_confidence": 20,
        "road_blocked": False,
        "people_affected": 15,
        "description": "Slow soil movement detected. No immediate danger but monitoring required.",
        "hours_ago": 8,
    },
]


def seed_database(db):
    """Insert seed zones and incidents into the database."""
    from services.prediction_service import prediction_service

    # Try to load model for predictions
    model_loaded = False
    try:
        prediction_service.ensure_loaded()
        model_loaded = True
    except Exception:
        pass

    # Create risk zones with predictions
    zone_objects = []
    for z in ZONES_DATA:
        inputs = {
            "rainfall_mm": z["rainfall_mm"],
            "rainfall_intensity": z["rainfall_intensity"],
            "cumulative_rainfall": z["cumulative_rainfall"],
            "soil_moisture": z["soil_moisture"],
            "slope_degrees": z["slope_degrees"],
            "elevation_m": z["elevation_m"],
            "vegetation_index": z["vegetation_index"],
            "geology_risk": z["geology_risk"],
            "drainage_score": z["drainage_score"],
        }

        if model_loaded:
            pred = prediction_service.predict(inputs)
            risk_score = pred["risk_score"]
            risk_level = pred["risk_level"]
            confidence = pred["confidence"]
            feature_imp = {c["feature"]: c["importance_pct"] for c in pred["feature_contributions"]}
            explanation = pred["explanation"]
        else:
            risk_score = 50.0
            risk_level = "MODERATE"
            confidence = 70.0
            feature_imp = {}
            explanation = "Model not available — using default values."

        zone = models.RiskZone(
            name=z["name"],
            district=z["district"],
            latitude=z["latitude"],
            longitude=z["longitude"],
            radius_km=z["radius_km"],
            risk_score=risk_score,
            risk_level=risk_level,
            prediction_confidence=confidence,
            last_predicted_at=datetime.now(timezone.utc),
            feature_importance=feature_imp,
            risk_explanation=explanation,
            population_at_risk=z["population_at_risk"],
            roads_at_risk=z["roads_at_risk"],
            hospitals_nearby=z["hospitals_nearby"],
            schools_nearby=z["schools_nearby"],
            **inputs,
        )
        db.add(zone)
        zone_objects.append(zone)

        # Add to prediction history
        hist = models.PredictionHistory(
            zone_name=z["name"],
            risk_score=risk_score,
            risk_level=risk_level,
            confidence=confidence,
            feature_importance=feature_imp,
            predicted_at=datetime.now(timezone.utc),
            **inputs,
        )
        db.add(hist)

    db.flush()

    # Create incidents
    now = datetime.now(timezone.utc)
    for inc_data in INCIDENT_DATA:
        hours_ago = inc_data.pop("hours_ago", 2)
        incident_time = now - timedelta(hours=hours_ago)

        inc = models.Incident(
            incident_id=inc_data["incident_id"],
            title=inc_data["title"],
            incident_type=inc_data["incident_type"],
            severity=inc_data["severity"],
            latitude=inc_data["latitude"],
            longitude=inc_data["longitude"],
            location_description=inc_data.get("location_description", ""),
            district=inc_data.get("district", ""),
            status=inc_data["status"],
            verification_confidence=inc_data["verification_confidence"],
            road_blocked=inc_data.get("road_blocked", False),
            road_name=inc_data.get("road_name", ""),
            people_affected=inc_data.get("people_affected", 0),
            houses_damaged=inc_data.get("houses_damaged", 0),
            description=inc_data.get("description", ""),
            incident_time=incident_time,
            predicted_risk_score=random.uniform(55, 95),
        )

        # Compute priority
        priority = compute_priority_score(
            severity=inc.severity,
            verification_confidence=inc.verification_confidence,
            risk_score=inc.predicted_risk_score,
            people_affected=inc.people_affected,
            road_blocked=inc.road_blocked,
            hospitals_nearby=0,
            schools_nearby=0,
            response_status="pending",
            hours_since_incident=hours_ago,
        )
        inc.priority_score = priority["priority_score"]
        inc.priority_level = priority["priority_level"].lower()

        db.add(inc)
        db.flush()

        # Add initial audit log
        audit = models.AuditLog(
            incident_id=inc.id,
            action="incident_created",
            previous_status=None,
            new_status=inc.status,
            performed_by="system",
            comment="Incident created from seed data.",
            timestamp=incident_time,
        )
        db.add(audit)

        # Add sample reports for each incident
        for r_idx in range(2 if inc.verification_confidence > 50 else 1):
            rtype = "field_officer" if r_idx == 0 and inc.verification_confidence > 70 else "citizen"
            report = models.Report(
                incident_id=inc.id,
                reporter_type=rtype,
                latitude=inc.latitude + random.uniform(-0.01, 0.01),
                longitude=inc.longitude + random.uniform(-0.01, 0.01),
                location_description=inc.location_description,
                incident_type=inc.incident_type,
                severity=inc.severity,
                description=inc.description,
                road_blocked=inc.road_blocked,
                status="reviewed",
                reported_at=incident_time + timedelta(minutes=random.randint(5, 30)),
            )
            db.add(report)

    # Add sample alerts
    alerts_data = [
        {
            "alert_type": "prediction",
            "level": "emergency",
            "title": "⚠️ CRITICAL Risk — Rudraprayag Kedarnath Zone",
            "message": "Predicted landslide risk score: 89/100 (CRITICAL). Intense rainfall + steep slopes.",
            "location": "Rudraprayag — Kedarnath Zone",
            "latitude": 30.285, "longitude": 79.007,
            "is_active": True, "acknowledged": False,
        },
        {
            "alert_type": "incident",
            "level": "emergency",
            "title": "🚨 Verified Landslide — Badrinath Highway",
            "message": "INC-2024-0001: Verified critical landslide. NH-58 blocked. Dispatch required.",
            "location": "Chamoli — Badrinath Highway KM 142",
            "latitude": 30.748, "longitude": 79.496,
            "is_active": True, "acknowledged": False,
        },
        {
            "alert_type": "prediction",
            "level": "warning",
            "title": "🔶 High Risk — Chamoli Badrinath Zone",
            "message": "Predicted risk score: 78/100. Rainfall 145mm/day with saturated soil conditions.",
            "location": "Chamoli — Badrinath Highway",
            "latitude": 30.744, "longitude": 79.493,
            "is_active": True, "acknowledged": False,
        },
    ]
    for a in alerts_data:
        db.add(models.Alert(**a))

    db.commit()
    print(f"  [OK] Seeded {len(ZONES_DATA)} zones, {len(INCIDENT_DATA)} incidents, {len(alerts_data)} alerts")
