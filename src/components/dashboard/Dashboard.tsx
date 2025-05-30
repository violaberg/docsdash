import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import PatientList from './PatientList';
import QuickStats from './QuickStats';
import UpcomingAppointments from './UpcomingAppointments';

const Dashboard = () => {
  const { user } = useSelector((state: RootState) => state.auth);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-primary dark:text-white">
          Welcome, Dr. {user?.last_name}
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Here's your overview for today
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <QuickStats />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <PatientList />
        </div>
        <div>
          <UpcomingAppointments />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;