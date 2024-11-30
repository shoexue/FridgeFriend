import { useState } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './app.css'
import Login from './components/auth/Login';
import Signup from './components/auth/Signup';
import Home from './components/homepage/Home';

function App() {
  const [count, setCount] = useState(0)

  return (	
	<BrowserRouter>
		<Routes>
			<Route path="/login" element={<Login />}/>
			<Route path="/signup" element={<Signup />}/>
			<Route path = "/" element={<Home />}/>
		</Routes>
	</BrowserRouter>
  )
}

export default App
