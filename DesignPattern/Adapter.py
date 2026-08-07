from abc import ABC, abstractmethod

# The unified interface your app actually works with
class HealthDataSource(ABC):
    @abstractmethod
    def get_vitals(self, patient_id) -> dict:
        pass

# --- External system #1: Apple HealthKit-style API (nested JSON) ---
class AppleHealthKitAPI:
    def fetch_metrics(self, user_id):
        return {"user": user_id, "metrics": [{"type": "heart_rate", "value": 72},
                                              {"type": "steps", "value": 8450}]}

class AppleHealthAdapter(HealthDataSource):
    def __init__(self, api: AppleHealthKitAPI):
        self._api = api
    def get_vitals(self, patient_id) -> dict:
        raw = self._api.fetch_metrics(patient_id)
        return {m["type"]: m["value"] for m in raw["metrics"]}  # translate to flat dict

# --- External system #2: Lab report platform (XML-ish response) ---
class LabReportPlatformAPI:
    def get_lab_xml(self, patient_code):
        return f"<lab><patient id='{patient_code}'><glucose>95</glucose><cholesterol>180</cholesterol></lab></lab>"

class LabReportAdapter(HealthDataSource):
    def __init__(self, api: LabReportPlatformAPI):
        self._api = api
    def get_vitals(self, patient_id) -> dict:
        xml = self._api.get_lab_xml(patient_id)
        # Simplified parsing for illustration
        glucose = xml.split("<glucose>")[1].split("</glucose>")[0]
        cholesterol = xml.split("<cholesterol>")[1].split("</cholesterol>")[0]
        return {"glucose": int(glucose), "cholesterol": int(cholesterol)}

# --- External system #3: Patient-entered manual form ---
class ManualEntryAdapter(HealthDataSource):
    def get_vitals(self, patient_id) -> dict:
        # Comes straight from a form submission, already close to our shape
        return {"weight_kg": 70, "blood_pressure": "120/80"}

# Application code — doesn't care which source it's talking to
def build_patient_profile(patient_id, sources: list[HealthDataSource]):
    profile = {}
    for source in sources:
        profile.update(source.get_vitals(patient_id))
    return profile

sources = [
    AppleHealthAdapter(AppleHealthKitAPI()),
    LabReportAdapter(LabReportPlatformAPI()),
    ManualEntryAdapter()
]
print(build_patient_profile("P-2001", sources))