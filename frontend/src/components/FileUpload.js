import { useState } from "react";

const FileUpload = ({ onFileSelect }) => {
  const [fileName, setFileName] = useState("No file selected");

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name);
      onFileSelect(file);
    }
  };

  return (
    <div className="flex flex-col items-center space-y-2">
      <label
        htmlFor="file-upload"
        className="cursor-pointer bg-black text-green-500 border border-green-500 px-4 py-2 hover:bg-green-500 hover:text-black transition"
      >
        Select File
      </label>
      <input
        type="file"
        accept=".csv,.json,.xls,.xlsx"
        id="file-upload"
        className="hidden"
        onChange={handleFileChange}
      />
      <p className="text-sm text-gray-400">{fileName}</p>
    </div>
  );
};

export default FileUpload;
