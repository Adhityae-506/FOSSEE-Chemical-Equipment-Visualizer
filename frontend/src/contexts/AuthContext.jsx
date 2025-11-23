import React, { createContext, useState, useEffect } from "react";
import {
  getToken as _getToken,
  setToken as _setToken,
  clearToken as _clearToken,
  login as apiLogin,
} from "../api/api";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(_getToken());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setToken(_getToken());
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    const res = await apiLogin(username, password);
    _setToken(res.token);
    setToken(res.token);
    setLoading(false);
  };

  const logout = () => {
    _clearToken();
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}
