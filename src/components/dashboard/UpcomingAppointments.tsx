import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../api/axios';
import { Appointment } from '../../types';

const UpcomingAppointments = () => {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      const response = await api.get('/appointments/');
      setAppointments(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching appointments:', error);
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">Upcoming Appointments</h2>
        <button
          onClick={() => navigate('/appointments/new')}
          className="btn-secondary"
        >
          New Appointment
        </button>
      </div>

      {loading ? (
        <div className="text-center py-8">Loading...</div>
      ) : (
        <div className="space-y-4">
          {appointments.map((appointment) => (
            <div
              key={appointment.id}
              className="p-4 border rounded-lg dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer"
              onClick={() => navigate(`/appointments/${appointment.id}`)}
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-semibold">
                    {appointment.patient.first_name} {appointment.patient.last_name}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    {new Date(appointment.date_time).toLocaleString()}
                  </p>
                </div>
                {appointment.follow_up_needed && (
                  <span className="px-2 py-1 text-xs bg-accent text-white rounded-full">
                    Follow-up
                  </span>
                )}
              </div>
              <p className="text-sm mt-2 text-gray-600 dark:text-gray-300">
                {appointment.reason}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default UpcomingAppointments;