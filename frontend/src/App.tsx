import { useAuth } from './contexts/AuthContext';
import { LoginPage } from './pages/LoginPage';
import { PracticePage } from './pages/PracticePage';

export default function App() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <PracticePage /> : <LoginPage />;
}
