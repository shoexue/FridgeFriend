import React from 'react'
import '../styling/login.css'
import Smile from '../../assets/smile.png'
import { useNavigate } from 'react-router-dom'
import TempoLogin from "./TempoLogin"
import { useAuth0 } from '@auth0/auth0-react';

const Login = () => {
  const { loginWithRedirect, isAuthenticated } = useAuth0();
  const navigate = useNavigate();

  // Submit handler for the login form
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Call loginWithRedirect and specify the redirect URL after successful login
    loginWithRedirect({
      redirectUri: "http://127.0.0.1:5000/"  // Flask app URL where the user should be redirected
    });
  };

  return (
    !isAuthenticated && (
      <div className="bg-white h-screen w-screen text-black login-div flex items-center justify-center flex-col relative">
        <div className='bg-l-blue p-10 rounded-lg w-1/4 flex flex-row justify-center items-center'>
          <div className='mr-2'>
            <h1 className="text-yellow font-mooli font-bold w-1/4">Fridge Friend</h1>
          </div>
          <div>
            <img src={Smile} alt="Smiling face" />
          </div>
        </div>
        <div className='bg-l-blue p-10 rounded-lg w-1/4'>
          {/* Use onSubmit handler */}
          <form onSubmit={handleSubmit}>
            <TempoLogin />

            <div className="flex items-center flex-col justify-center">
              <button
                type="submit"
                className="font-mooli bg-yellow hover:bg-d-yellow text-l-blue font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full mb-2"
              >
                Login
              </button>
              <div className='flex flex-row justify-between w-full'>
                <p className='text-yellow'>Don't have an account? </p>
              </div>
            </div>
          </form>
        </div>
      </div>
    )
  );
};

export default Login;
