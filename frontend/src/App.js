import { Routes, Route } from "react-router-dom";

import Index from "./Pages/Index";
import Login from "./Pages/Login";
import Painting from "./Pages/Painting";
import Register from "./Pages/Register";
import Evaluation from "./Pages/Evaluation";

import "./Styles/App.css";

function App() {
  return (
    <Routes>
      <Route index element={<Index />} />
      <Route path="/login" element={<Login />}></Route>
      <Route path="/register" element={<Register />}></Route>
      <Route path="/painting/:id" element={<Painting />} />
      <Route path="/evaluation" element={<Evaluation />} />
    </Routes>
  );
}

export default App;
