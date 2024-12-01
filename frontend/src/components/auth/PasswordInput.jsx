import React from "react";



const PasswordInput = ({
  value = "",
  onChange = () => {},
}) => {
  return (
  <div>
  <label for="password" class="block text-lg font-bold mb-2 font-mooli text-yellow">Password:</label>

    <input
      type="password"
      placeholder="Password"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full"
    />
  </div>
  );
};

export default PasswordInput;
