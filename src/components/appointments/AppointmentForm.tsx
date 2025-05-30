import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useSelector } from 'react-redux';
import api from '../../api/axios';
import { Patient, Appointment } from '../../types';
import { RootState } from '../../store';

const AppointmentForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  const [loading, setLoading] = useState(id ? true : false);
  const [error, setError] = useState('');
  const [patients, setPatients] = useState<Patient[]>([]);
  const [appointment, setAppointment] = useState<Partial<Appointment>>({
    patient: null,
    date_time: '',
    reason: '',
    notes: '',
    medications_prescribed: '',
    follow_up_needed: false,
    follow_up_date: null,
    vital_signs: {
      blood_pressure: '',
      pulse: '',
      temperature: '',
      oxygen_saturation: ''
    }
  });

  useEffect(() => {
    fetchPatients();
    if (id) {
      fetchAppointment();
    }
  }, [id]);

  const fetchPatients = async () => {
    try {
      const response = await api.get('/patients/');
      setPatients(response.data);
    } catch (error) {
      setError('Error fetching patients');
    }
  };

  const fetchAppointment = async () => {
    try {
      const response = await api.get(`/appointments/${id}/`);
      setAppointment(response.data);
      setLoading(false);
    } catch (error) {
      setError('Error fetching appointment data');
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (id) {
        await api.put(`/appointments/${id}/`, appointment);
      } else {
        await api.post('/appointments/', appointment);
      }
      navigate('/dashboard');
    } catch (error) {
      setError('Error saving appointment data');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    if (name.startsWith('vital_signs.')) {
      const vitalSign = name.split('.')[1];
      setAppointment(prev => ({
        ...prev,
        vital_signs: {
          ...prev.vital_signs,
          [vitalSign]: value
        }
      }));
    } else {
      setAppointment(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
      }));
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-primary dark:text-white">
          {id ? 'Edit Appointment' : 'New Appointment'}
        </h1>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="card">
            <h2 className="text-xl font-bold mb-4">Appointment Details</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Patient</label>
                <select
                  name="patient"
                  value={appointment.patient?.id || ''}
                  onChange={handleChange}
                  className="input-field"
                  required
                >
                  <option value="">Select Patient</option>
                  {patients.map(patient => (
                    <option key={patient.id} value={patient.id}>
                      {patient.first_name} {patient.last_name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Date & Time</label>
                <input
                  type="datetime-local"
                  name="date_time"
                  value={appointment.date_time}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
            </div>
            <div className="mt-4">
              <label className="block text-sm font-medium mb-1">Reason</label>
              <textarea
                name="reason"
                value={appointment.reason}
                onChange={handleChange}
                className="input-field"
                rows={3}
                required
              />
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-bold mb-4">Vital Signs</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Blood Pressure</label>
                <input
                  type="text"
                  name="vital_signs.blood_pressure"
                  value={appointment.vital_signs?.blood_pressure}
                  onChange={handleChange}
                  placeholder="120/80"
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Pulse (bpm)</label>
                <input
                  type="number"
                  name="vital_signs.pulse"
                  value={appointment.vital_signs?.pulse}
                  onChange={handleChange}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Temperature (°C)</label>
                <input
                  type="number"
                  name="vital_signs.temperature"
                  value={appointment.vital_signs?.temperature}
                  onChange={handleChange}
                  step="0.1"
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Oxygen Saturation (%)</label>
                <input
                  type="number"
                  name="vital_signs.oxygen_saturation"
                  value={appointment.vital_signs?.oxygen_saturation}
                  onChange={handleChange}
                  className="input-field"
                />
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-bold mb-4">Notes & Follow-up</h2>
            <div>
              <label className="block text-sm font-medium mb-1">Notes</label>
              <textarea
                name="notes"
                value={appointment.notes}
                onChange={handleChange}
                className="input-field"
                rows={3}
              />
            </div>
            <div className="mt-4">
              <label className="block text-sm font-medium mb-1">Medications Prescribed</label>
              <textarea
                name="medications_prescribed"
                value={appointment.medications_prescribed}
                onChange={handleChange}
                className="input-field"
                rows={3}
              />
            </div>
            <div className="mt-4 flex items-center">
              <input
                type="checkbox"
                name="follow_up_needed"
                checked={appointment.follow_up_needed}
                onChange={handleChange}
                className="mr-2"
              />
              <label className="text-sm font-medium">Follow-up Required</label>
            </div>
            {appointment.follow_up_needed && (
              <div className="mt-4">
                <label className="block text-sm font-medium mb-1">Follow-up Date</label>
                <input
                  type="date"
                  name="follow_up_date"
                  value={appointment.follow_up_date || ''}
                  onChange={handleChange}
                  className="input-field"
                />
              </div>
            )}
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
              Save Appointment
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AppointmentForm;