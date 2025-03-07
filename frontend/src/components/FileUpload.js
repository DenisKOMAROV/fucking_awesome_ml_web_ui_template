import { useState } from "react";

const FileUpload = ({ onFileSelect, fileUploading }) => {
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
        className={`cursor-pointer px-4 py-2 border transition ${
          fileUploading
            ? "border-gray-500 text-gray-500 cursor-not-allowed"
            : "bg-black text-green-500 border border-green-500 hover:bg-green-500 hover:text-black"
        }`}
      >
        {fileUploading ? "❯ Loading..." : "❯ Select File"}
      </label>
      <input
        type="file"
        accept=".csv,.json,.xls,.xlsx"
        id="file-upload"
        className="hidden"
        onChange={handleFileChange}
        disabled={fileUploading} // Prevent selecting a new file while uploading
      />
      <p className="text-sm text-gray-400">{fileUploading ? "Uploading..." : fileName}</p>
    </div>
  );
};

export default FileUpload;
