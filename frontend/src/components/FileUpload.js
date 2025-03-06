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
      <label className="text-green-500">❯ Upload UID List (CSV, TXT, XLS)</label>
      <input
        type="file"
        accept=".csv,.txt,.xls,.xlsx"
        onChange={handleFileChange}
        className="hidden"
        id="file-upload"
      />
      <label
        htmlFor="file-upload"
        className="cursor-pointer bg-black text-green-500 border border-green-500 px-4 py-2 rounded hover:bg-green-500 hover:text-black transition"
      >
        Select File
      </label>
      <p className="text-sm">{fileName}</p>
    </div>
  );
};

export default FileUpload;
