import { useState } from "react";
import Dropdown from "./components/Dropdown";
import Slider from "./components/Slider";
import FileUpload from "./components/FileUpload";
import TextBox from "./components/TextBox";
import Button from "./components/Button";

function App() {
  const categories = ["Webinar", "Newsletter", "Event"];
  const [selectedCategory, setSelectedCategory] = useState(categories[0]);
  const [responseRate, setResponseRate] = useState(50);
  const [selectedFile, setSelectedFile] = useState(null);
  const [newsletterContent, setNewsletterContent] = useState("");

  const handleSelectUsers = () => {
    alert(`Selecting users for ${selectedCategory} with ${responseRate}% response rate.`);
    // Here we will later call the FastAPI backend
  };

  const handleGetUserGroups = () => {
    alert("Downloading user groups...");
    // This will trigger a download from FastAPI later
  };

  return (
    <div className="h-screen bg-black text-green-500 flex flex-col items-center justify-center space-y-4 p-4">
      <h1 className="text-2xl">❯ Select a Category</h1>
      <Dropdown options={categories} onSelect={setSelectedCategory} />
      <p className="text-lg">Selected: {selectedCategory}</p>

      <h2 className="text-2xl mt-4">❯ Set Response Rate</h2>
      <Slider onChange={setResponseRate} />
      <p className="text-lg">Expected Response Rate: {responseRate}%</p>

      <h2 className="text-2xl mt-4">❯ Upload UID File</h2>
      <FileUpload onFileSelect={setSelectedFile} />
      {selectedFile && <p className="text-lg">Selected File: {selectedFile.name}</p>}

      <h2 className="text-2xl mt-4">❯ Enter Newsletter Content</h2>
      <TextBox onContentChange={setNewsletterContent} />
      {newsletterContent && (
        <p className="text-sm text-gray-400 mt-2">Saved content preview: {newsletterContent.substring(0, 50)}...</p>
      )}

      <div className="mt-6 space-x-4 flex">
        <Button text="Select Users" onClick={handleSelectUsers} />
        <Button text="Get User Groups" onClick={handleGetUserGroups} />
      </div>
    </div>
  );
}

export default App;
