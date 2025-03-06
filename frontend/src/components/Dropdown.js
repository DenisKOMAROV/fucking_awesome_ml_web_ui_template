import { useState } from "react";

const Dropdown = ({ options, onSelect }) => {
  const [selected, setSelected] = useState(options[0]);
  const [isOpen, setIsOpen] = useState(false);

  const handleSelect = (option) => {
    setSelected(option);
    onSelect(option);
    setIsOpen(false);
  };

  return (
    <div className="relative inline-block w-full">
      <div
        className="bg-black text-green-500 border border-green-500 px-4 py-2 cursor-pointer hover:bg-green-500 hover:text-black transition"
        onClick={() => setIsOpen(!isOpen)}
      >
        ❯ {selected}
      </div>
      {isOpen && (
        <div className="absolute left-0 w-full bg-black border border-green-500 mt-1">
          {options.map((option, index) => (
            <div
              key={index}
              className="px-4 py-2 hover:bg-green-500 hover:text-black cursor-pointer transition"
              onClick={() => handleSelect(option)}
            >
              ❯ {option}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dropdown;
