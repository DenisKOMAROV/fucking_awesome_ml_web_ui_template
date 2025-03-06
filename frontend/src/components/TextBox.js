import { useState } from "react";

const TextBox = ({ onContentChange }) => {
  const [content, setContent] = useState("");

  const handleChange = (event) => {
    const newContent = event.target.value;
    setContent(newContent);
    onContentChange(newContent);
  };

  return (
    <div className="flex flex-col items-center space-y-10 w-full px-10">
      <textarea
        className="w-full h-40 p-2 bg-black border border-green-500 text-green-500 rounded outline-none focus:ring-2 focus:ring-green-500"
        value={content}
        onChange={handleChange}
        placeholder="❯ Enter newsletter content here..."
      />
    </div>
  );
};

export default TextBox;
