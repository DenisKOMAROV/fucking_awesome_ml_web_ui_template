import { useState } from "react";

const Slider = ({ min = 0, max = 100, onChange }) => {
  const [value, setValue] = useState(69); // Default to 69%

  const handleChange = (event) => {
    const newValue = event.target.value;
    setValue(newValue);
    onChange(newValue);
  };

  return (
    <div className="flex flex-col items-center space-y-5">
      <label className="text-green-500">Response Rate: {value}%</label>
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={handleChange}
        className="w-64 accent-green-500"
      />
    </div>
  );
};

export default Slider;
