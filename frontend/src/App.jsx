import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Login from "./auth/Login";
import Signup from "./auth/signup/Signup";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
  );
}

export default App;
