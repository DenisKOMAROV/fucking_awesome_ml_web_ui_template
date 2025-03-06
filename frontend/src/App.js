import { useState } from "react";
import Dropdown from "./components/Dropdown";
import Slider from "./components/Slider";
import FileUpload from "./components/FileUpload";
import TextBox from "./components/TextBox";
import Button from "./components/Button";

function App() {
  const categories = ["Webinar", "Digest Analitycs", "Digest Product", "Ads", "Offline Event", "Other",];
  const [selectedCategory, setSelectedCategory] = useState(categories[0]);
  const [responseRate, setResponseRate] = useState(69);
  const [filesGenerated, setFilesGenerated] = useState(false);
  const [newsletterContent, setNewsletterContent] = useState("");


  const handleSelectUsers = () => {
    alert(`Selecting users for ${selectedCategory} with ${responseRate}% response rate.`);
    setFilesGenerated(true);
  };

  const handleDownloadGroups = () => {
    if (!filesGenerated) return;
    alert("Downloading user groups...");
  };

  return (
    <div className="h-screen bg-black text-green-500 flex flex-col items-center justify-start space-y-10 p-10">
      <h1 className="text-3xl font-bold">❯ Welcome to the fucking awesome model service!</h1>
      <h2 className="text-2xl mt-2">❯ Newsletter Content</h2>
        <TextBox onContentChange={setNewsletterContent} />
      
      <div className="flex w-full justify-between px-10">        
        <div className="w-1/3 space-y-4">
          <h2 className="text-2xl">❯ Select a Category</h2>
          <Dropdown options={categories} onSelect={setSelectedCategory} />
        </div>

        <div className="w-1/3 flex flex-col items-center space-y-4">
          <h2 className="text-2xl">❯ Response Rate</h2>
          <Slider onChange={setResponseRate} />
        </div>

        <div className="w-1/3 text-center space-y-4">
          <h2 className="text-2xl">❯ Upload UID File</h2>
          <p className="text-green-500">Select File (CSV, TXT, XLS)</p>
          <FileUpload onFileSelect={(file) => console.log("Uploaded file:", file)} />
        </div>
      </div>


      <div className="mt-6 space-x-4 flex">
        <Button text="Select Users" onClick={handleSelectUsers} />
        <button
          onClick={handleDownloadGroups}
          disabled={!filesGenerated}
          className={`px-6 py-2 text-lg border ${filesGenerated ? "bg-black text-green-500 border-green-500 hover:bg-green-500 hover:text-black transition" : "border-gray-500 text-gray-500 cursor-not-allowed"}`}
        >
          ❯ Download User Groups
        </button>
      </div>
    </div>
  );
}

export default App;