import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';

const QuickStats = () => {
  return (
    <>
      <div className="card bg-white dark:bg-primary-dark">
        <h3 className="text-lg font-semibold mb-2">Today's Appointments</h3>
        <p className="text-3xl font-bold text-primary">8</p>
      </div>
      
      <div className="card bg-white dark:bg-primary-dark">
        <h3 className="text-lg font-semibold mb-2">Pending Follow-ups</h3>
        <p className="text-3xl font-bold text-accent">3</p>
      </div>
      
      <div className="card bg-white dark:bg-primary-dark">
        <h3 className="text-lg font-semibold mb-2">New Patients</h3>
        <p className="text-3xl font-bold text-secondary">2</p>
      </div>
    </>
  );
};

export default QuickStats;