import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useStore } from './store/store';
import { auth } from './utils/api';
import Scene from './components/ThreeBackground/Scene';
import Login from './pages/Login';
import Register from './pages/Register';
import Chat from './pages/Chat';

function App() {
  const { setUser, isAuthenticated } = useStore();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await auth.getCurrentUser();
      setUser(response.data.data.user);
    } catch (error) {
      // Not authenticated
      setUser(null);
    }
  };

  return (
    <BrowserRouter>
      <Scene />
      <Routes>
        <Route
          path="/"
          element={
            isAuthenticated ? <Navigate to="/chat" replace /> : <Navigate to="/login" replace />
          }
        />
        <Route
          path="/login"
          element={isAuthenticated ? <Navigate to="/chat" replace /> : <Login />}
        />
        <Route
          path="/register"
          element={isAuthenticated ? <Navigate to="/chat" replace /> : <Register />}
        />
        <Route
          path="/chat"
          element={isAuthenticated ? <Chat /> : <Navigate to="/login" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
