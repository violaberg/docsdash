export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

export interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  preferred_name: string;
  date_of_birth: string;
  medical_record_number: string;
  phone_primary: string;
  phone_emergency: string;
  email: string;
  address: string;
  mailing_address: string;
  emergency_contact_name: string;
  emergency_contact_relationship: string;
  emergency_contact_phone: string;
  insurance_provider: string;
  insurance_id: string;
  blood_type: string;
  allergies: string;
  chronic_conditions: string;
  current_medications: string;
  height: number;
  weight: number;
  created_at: string;
  updated_at: string;
  created_by: number;
}

export interface Appointment {
  id: number;
  patient: Patient;
  doctor: User;
  date_time: string;
  reason: string;
  notes: string;
  medications_prescribed: string;
  follow_up_needed: boolean;
  follow_up_date: string | null;
  vital_signs: {
    blood_pressure?: string;
    pulse?: number;
    temperature?: number;
    oxygen_saturation?: number;
  };
  created_at: string;
  updated_at: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export interface ThemeState {
  isDark: boolean;
}