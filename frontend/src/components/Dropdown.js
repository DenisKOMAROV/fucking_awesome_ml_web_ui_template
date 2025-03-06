import { useState } from "react";

const Dropdown = ({ options, onSelect }) => {
  const [selected, setSelected] = useState(options[0]); // Default to first option

  const handleSelect = (event) => {
    setSelected(event.target.value);
    onSelect(event.target.value);
  };

  return (
    <div className="border border-green-500 p-2 rounded text-green-500 bg-black">
      <select
        className="bg-black text-green-500 outline-none"
        value={selected}
        onChange={handleSelect}
      >
        {options.map((option, index) => (
          <option key={index} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
};

export default Dropdown;
