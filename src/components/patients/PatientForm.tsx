import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../api/axios';
import { Patient } from '../../types';

const PatientForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(id ? true : false);
  const [error, setError] = useState('');
  const [patient, setPatient] = useState<Partial<Patient>>({
    first_name: '',
    last_name: '',
    preferred_name: '',
    date_of_birth: '',
    medical_record_number: '',
    phone_primary: '',
    phone_emergency: '',
    email: '',
    address: '',
    mailing_address: '',
    emergency_contact_name: '',
    emergency_contact_relationship: '',
    emergency_contact_phone: '',
    insurance_provider: '',
    insurance_id: '',
    blood_type: 'A+',
    allergies: '',
    chronic_conditions: '',
    current_medications: '',
    height: 0,
    weight: 0,
  });

  useEffect(() => {
    if (id) {
      fetchPatient();
    }
  }, [id]);

  const fetchPatient = async () => {
    try {
      const response = await api.get(`/patients/${id}/`);
      setPatient(response.data);
      setLoading(false);
    } catch (error) {
      setError('Error fetching patient data');
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (id) {
        await api.put(`/patients/${id}/`, patient);
      } else {
        await api.post('/patients/', patient);
      }
      navigate('/dashboard');
    } catch (error) {
      setError('Error saving patient data');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setPatient(prev => ({
      ...prev,
      [name]: value
    }));
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-primary dark:text-white">
          {id ? 'Edit Patient' : 'New Patient'}
        </h1>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="card">
            <h2 className="text-xl font-bold mb-4">Personal Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">First Name</label>
                <input
                  type="text"
                  name="first_name"
                  value={patient.first_name}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Last Name</label>
                <input
                  type="text"
                  name="last_name"
                  value={patient.last_name}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Preferred Name</label>
                <input
                  type="text"
                  name="preferred_name"
                  value={patient.preferred_name}
                  onChange={handleChange}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Date of Birth</label>
                <input
                  type="date"
                  name="date_of_birth"
                  value={patient.date_of_birth}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-bold mb-4">Contact Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Primary Phone</label>
                <input
                  type="tel"
                  name="phone_primary"
                  value={patient.phone_primary}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Emergency Phone</label>
                <input
                  type="tel"
                  name="phone_emergency"
                  value={patient.phone_emergency}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <input
                  type="email"
                  name="email"
                  value={patient.email}
                  onChange={handleChange}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Medical Record Number</label>
                <input
                  type="text"
                  name="medical_record_number"
                  value={patient.medical_record_number}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-bold mb-4">Medical Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Blood Type</label>
                <select
                  name="blood_type"
                  value={patient.blood_type}
                  onChange={handleChange}
                  className="input-field"
                  required
                >
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Height (cm)</label>
                <input
                  type="number"
                  name="height"
                  value={patient.height}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Weight (kg)</label>
                <input
                  type="number"
                  name="weight"
                  value={patient.weight}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
            </div>
            <div className="mt-4">
              <label className="block text-sm font-medium mb-1">Allergies</label>
              <textarea
                name="allergies"
                value={patient.allergies}
                onChange={handleChange}
                className="input-field"
                rows={3}
              />
            </div>
            <div className="mt-4">
              <label className="block text-sm font-medium mb-1">Chronic Conditions</label>
              <textarea
                name="chronic_conditions"
                value={patient.chronic_conditions}
                onChange={handleChange}
                className="input-field"
                rows={3}
              />
            </div>
            <div className="mt-4">
              <label className="block text-sm font-medium mb-1">Current Medications</label>
              <textarea
                name="current_medications"
                value={patient.current_medications}
                onChange={handleChange}
                className="input-field"
                rows={3}
              />
            </div>
          </div>

          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="btn-secondary"
            >
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              Save Patient
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PatientForm;