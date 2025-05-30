import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../api/axios';
import { Patient, Appointment } from '../../types';

const PatientDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchPatientData();
  }, [id]);

  const fetchPatientData = async () => {
    try {
      const [patientResponse, appointmentsResponse] = await Promise.all([
        api.get(`/patients/${id}/`),
        api.get(`/appointments/?patient=${id}`)
      ]);
      setPatient(patientResponse.data);
      setAppointments(appointmentsResponse.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching patient data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  if (!patient) {
    return <div className="text-center py-8">Patient not found</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-primary dark:text-white">
          {patient.first_name} {patient.last_name}
        </h1>
        <div className="space-x-4">
          <button
            onClick={() => navigate(`/patients/${id}/edit`)}
            className="btn-secondary"
          >
            Edit Patient
          </button>
          <button
            onClick={() => navigate('/appointments/new')}
            className="btn-primary"
          >
            New Appointment
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="card mb-6">
            <div className="flex space-x-4 mb-6">
              <button
                className={`px-4 py-2 rounded-lg ${
                  activeTab === 'overview'
                    ? 'bg-primary text-white'
                    : 'text-gray-600 dark:text-gray-300'
                }`}
                onClick={() => setActiveTab('overview')}
              >
                Overview
              </button>
              <button
                className={`px-4 py-2 rounded-lg ${
                  activeTab === 'medical'
                    ? 'bg-primary text-white'
                    : 'text-gray-600 dark:text-gray-300'
                }`}
                onClick={() => setActiveTab('medical')}
              >
                Medical History
              </button>
              <button
                className={`px-4 py-2 rounded-lg ${
                  activeTab === 'appointments'
                    ? 'bg-primary text-white'
                    : 'text-gray-600 dark:text-gray-300'
                }`}
                onClick={() => setActiveTab('appointments')}
              >
                Appointments
              </button>
            </div>

            {activeTab === 'overview' && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h3 className="font-semibold">Date of Birth</h3>
                    <p>{patient.date_of_birth}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold">Medical Record Number</h3>
                    <p>{patient.medical_record_number}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold">Primary Phone</h3>
                    <p>{patient.phone_primary}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold">Email</h3>
                    <p>{patient.email}</p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'medical' && (
              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold mb-2">Current Medications</h3>
                  <p className="whitespace-pre-line">{patient.current_medications}</p>
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Allergies</h3>
                  <p className="whitespace-pre-line">{patient.allergies}</p>
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Chronic Conditions</h3>
                  <p className="whitespace-pre-line">{patient.chronic_conditions}</p>
                </div>
              </div>
            )}

            {activeTab === 'appointments' && (
              <div className="space-y-4">
                {appointments.map((appointment) => (
                  <div
                    key={appointment.id}
                    className="p-4 border rounded-lg dark:border-gray-700"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-semibold">
                          {new Date(appointment.date_time).toLocaleString()}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-300">
                          {appointment.reason}
                        </p>
                      </div>
                      {appointment.follow_up_needed && (
                        <span className="px-2 py-1 text-xs bg-accent text-white rounded-full">
                          Follow-up
                        </span>
                      )}
                    </div>
                    {appointment.notes && (
                      <p className="mt-2 text-sm">{appointment.notes}</p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div>
          <div className="card mb-6">
            <h2 className="text-xl font-bold mb-4">Critical Information</h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold">Blood Type</h3>
                <p>{patient.blood_type}</p>
              </div>
              <div>
                <h3 className="font-semibold">Height</h3>
                <p>{patient.height} cm</p>
              </div>
              <div>
                <h3 className="font-semibold">Weight</h3>
                <p>{patient.weight} kg</p>
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-bold mb-4">Emergency Contact</h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold">Name</h3>
                <p>{patient.emergency_contact_name}</p>
              </div>
              <div>
                <h3 className="font-semibold">Relationship</h3>
                <p>{patient.emergency_contact_relationship}</p>
              </div>
              <div>
                <h3 className="font-semibold">Phone</h3>
                <p>{patient.emergency_contact_phone}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDetails;