import asyncio
from swarms_tools.healthcare.epic_integration import search_patients, get_patient_by_id, get_patient_observations

async def main():
    # Search for patients
    patient_name = "John Doe"
    try:
        patients = await search_patients(patient_name)
        print(f"Search results for '{patient_name}': {len(patients.get('entry', []))} patients found")
        if patients.get('entry'):
            for patient in patients['entry'][:2]:  # Show first 2 patients
                resource = patient.get('resource', {})
                print(f"  - Patient ID: {resource.get('id', 'N/A')}")
                names = resource.get('name', [])
                if names:
                    name = names[0]
                    given = ' '.join(name.get('given', []))
                    family = name.get('family', '')
                    print(f"    Name: {given} {family}")
    except Exception as e:
        print(f"Could not search for patients: {e}")
    
    # Get patient by ID
    sample_patient_id = "12345"
    try:
        patient = await get_patient_by_id(sample_patient_id)
        print(f"\nPatient details retrieved successfully")
        print(f"  Patient ID: {patient.get('id', 'N/A')}")
        print(f"  Resource Type: {patient.get('resourceType', 'N/A')}")
        names = patient.get('name', [])
        if names:
            name = names[0]
            given = ' '.join(name.get('given', []))
            family = name.get('family', '')
            print(f"  Name: {given} {family}")
    except Exception as e:
        print(f"Could not fetch patient {sample_patient_id}: {e}")
    
    # Get patient observations
    try:
        observations = await get_patient_observations(sample_patient_id)
        print(f"\nFound {len(observations.get('entry', []))} observations for patient")
        if observations.get('entry'):
            for obs in observations['entry'][:2]:  # Show first 2 observations
                resource = obs.get('resource', {})
                print(f"  - Observation ID: {resource.get('id', 'N/A')}")
                print(f"    Status: {resource.get('status', 'N/A')}")
                code = resource.get('code', {})
                if code:
                    codings = code.get('coding', [])
                    if codings:
                        print(f"    Code: {codings[0].get('display', 'N/A')}")
    except Exception as e:
        print(f"Could not fetch observations: {e}")

asyncio.run(main())
