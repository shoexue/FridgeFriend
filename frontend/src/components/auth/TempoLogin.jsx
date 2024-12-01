import React from "react";

import PasswordInput from "./PasswordInput";
import EmailInput from "./EmailInput";

function Home() {
  return (
    // <div className="w-screen h-screen bg-white flex items-center justify-center p-4">
    <div>
    <div class="mb-4">
        <EmailInput />
            
     </div>
    <div class="mb-6">

        <PasswordInput />
        </div>
     </div>
  );
}

export default Home;
