import React from "react";



const EmailInput = ({ value = "", onChange = () => {} }) => {
  return (
    <div>
    <label for="email" class="block text-lg font-bold mb-2 font-mooli text-yellow">Email:</label>

        <input
        type="email"
        placeholder="Email"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full"
        />
    </div>
  );
};

export default EmailInput;
