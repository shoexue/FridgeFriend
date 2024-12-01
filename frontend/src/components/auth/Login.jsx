import React from 'react'
import '../styling/login.css'
import Smile from '../../assets/smile.png'
import { useNavigate } from 'react-router-dom'
import TempoLogin from "./TempoLogin"

const handleSubmit = async (e) => {
	e.preventDefault();
	try {

			window.location.href = "http://127.0.0.1:5000/";

	} catch (error) {
		setErrorMessage(error);
	}
};


const Login = () => {
	const navigate = useNavigate();
	// const { loginWithRedirect } = useAuth0();


  return (
	<div className="bg-white h-screen w-screen text-black login-div flex items-center justify-center flex-col relative">
		<div className='bg-l-blue p-10 rounded-lg w-1/4 flex flex-row justify-center items-center'>
			<div className='mr-2'>
				<h1 className="text-yellow font-mooli font-bold w-1/4">Fridge Friend</h1>
			</div>
			<div>
				<img src={Smile}/>
			</div>
		</div>
		<div className='bg-l-blue p-10 rounded-lg w-1/4'>
        <form onSubmit={handleSubmit}>
				<TempoLogin/>
			
				<div class="flex items-center flex-col justify-center">
					<button 
						type="submit" class="font-mooli bg-yellow hover:bg-d-yellow text-l-blue font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full mb-2"
					>
						Login
					</button>
					<div className='flex flexrow justify-between w-full'>
						<p className='text-yellow'>Don't have an account? </p>
						<a className='text-yellow cursor-pointer hover:text-d-yellow' onClick={() => {navigate('/signup')}}>Sign up</a>
					</div>
				</div>
			</form>
		</div>
	</div>
  )
}

export default Login