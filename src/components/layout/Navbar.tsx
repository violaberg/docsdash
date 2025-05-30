import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import { logout } from '../../store/authSlice';
import { toggleTheme } from '../../store/themeSlice';
import { RootState } from '../../store';

const Navbar = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);
  const { isDark } = useSelector((state: RootState) => state.theme);

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <nav className="bg-primary dark:bg-primary-dark shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/dashboard" className="text-white text-xl font-bold">
              DocsDash
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <button
              onClick={() => dispatch(toggleTheme())}
              className="text-white hover:text-accent-light"
            >
              {isDark ? '🌞' : '🌙'}
            </button>
            
            <span className="text-white">
              {user?.first_name} {user?.last_name}
            </span>
            
            <button
              onClick={handleLogout}
              className="text-white hover:text-accent-light"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;