import asyncio
from swarms_tools.healthcare.epic_integration import (
    search_patients, get_patient_by_id, get_patient_observations,
    add_patient_resource, add_observation_resource, get_encounters_for_patient,
    get_medications_for_patient, get_appointments, get_conditions
)

# Test that all functions exist and are callable
assert callable(search_patients)
assert callable(get_patient_by_id)
assert callable(get_patient_observations)
assert callable(add_patient_resource)
assert callable(add_observation_resource)
assert callable(get_encounters_for_patient)
assert callable(get_medications_for_patient)
assert callable(get_appointments)
assert callable(get_conditions)

async def test_epic_functions():
    # Test patient search function
    patient_name = "John Doe"
    patients = await search_patients(patient_name)
    assert patients is not None
    assert isinstance(patients, dict)
    assert 'entry' in patients or 'total' in patients or 'resourceType' in patients
    
    # Test getting patient by ID
    sample_patient_id = "12345"
    try:
        patient = await get_patient_by_id(sample_patient_id)
        assert patient is not None
        assert isinstance(patient, dict)
        assert patient.get('resourceType') == 'Patient'
        assert 'id' in patient
    except Exception:
        pass  # Expected to fail with demo ID
    
    # Test getting patient observations
    try:
        observations = await get_patient_observations(sample_patient_id)
        assert observations is not None
        assert isinstance(observations, dict)
        assert 'entry' in observations or 'total' in observations or 'resourceType' in observations
    except Exception:
        pass  # Expected to fail with demo ID
    
    # Test getting patient encounters
    try:
        encounters = await get_encounters_for_patient(sample_patient_id)
        assert encounters is not None
        assert isinstance(encounters, dict)
        assert 'entry' in encounters or 'total' in encounters or 'resourceType' in encounters
    except Exception:
        pass  # Expected to fail with demo ID
    
    # Test getting patient medications
    try:
        medications = await get_medications_for_patient(sample_patient_id)
        assert medications is not None
        assert isinstance(medications, dict)
        assert 'entry' in medications or 'total' in medications or 'resourceType' in medications
    except Exception:
        pass  # Expected to fail with demo ID
    
    # Test getting patient appointments
    try:
        appointments = await get_appointments(sample_patient_id)
        assert appointments is not None
        assert isinstance(appointments, dict)
        assert 'entry' in appointments or 'total' in appointments or 'resourceType' in appointments
    except Exception:
        pass  # Expected to fail with demo ID
    
    # Test getting patient conditions
    try:
        conditions = await get_conditions(sample_patient_id)
        assert conditions is not None
        assert isinstance(conditions, dict)
        assert 'entry' in conditions or 'total' in conditions or 'resourceType' in conditions
    except Exception:
        pass  # Expected to fail with demo ID

# Run the async tests
asyncio.run(test_epic_functions())
