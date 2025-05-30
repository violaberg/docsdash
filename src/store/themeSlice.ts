import { createSlice } from '@reduxjs/toolkit';
import { ThemeState } from '../types';

const initialState: ThemeState = {
  isDark: window.matchMedia('(prefers-color-scheme: dark)').matches
};

const themeSlice = createSlice({
  name: 'theme',
  initialState,
  reducers: {
    toggleTheme: (state) => {
      state.isDark = !state.isDark;
    }
  }
});

export const { toggleTheme } = themeSlice.actions;
export default themeSlice.reducer;