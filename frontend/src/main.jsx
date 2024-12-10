import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { BrowserRouter } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/ReactToastify.min.css";
console.log("here -2")
createRoot(document.getElementById('root')).render(
  <>
    <ToastContainer />
      <App />
  </>,
)
