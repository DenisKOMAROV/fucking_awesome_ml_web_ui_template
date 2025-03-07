import { useState } from "react";
import axios from "axios";
import Dropdown from "./components/Dropdown";
import Slider from "./components/Slider";
import FileUpload from "./components/FileUpload";
import TextBox from "./components/TextBox";
import Button from "./components/Button";

const API_BASE_URL = "http://localhost:8000"; // Backend URL

function App() {
  const categories = ["Webinar", "Digest Analitycs", "Digest Product", "Ads", "Offline Event", "Other", "Fucking_Category"];
  const [selectedCategory, setSelectedCategory] = useState(categories[0]);
  const [responseRate, setResponseRate] = useState(69);
  const [newsletterContent, setNewsletterContent] = useState("");
  const [fileId, setFileId] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filesGenerated, setFilesGenerated] = useState(false);
  const [zipFilename, setZipFilename] = useState(null);  // ✅ Added missing useState

  // Upload UID file to backend
  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append("uid_file", file);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload_uid_file`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFileId(response.data.file_id);
      alert("File uploaded successfully!");
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload file.");
    }
  };

  // Fetch stats from backend
  const handleSelectUsers = async () => {
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/select_users`, {
        category: selectedCategory,
        open_rate: responseRate,
        newsletter_content: newsletterContent,
        file_id: fileId,
      });

      setStats(response.data.stats);
      setZipFilename(response.data.zip_filename);  // ✅ Store zip filename for download
      setFilesGenerated(true);
    } catch (error) {
      console.error("Error selecting users:", error);
      alert("Failed to select users.");
    } finally {
      setLoading(false);
    }
  };

  // Download user groups ZIP file
  const handleDownloadGroups = async () => {
    if (!filesGenerated || !zipFilename) return;

    try {
      const response = await axios.get(`${API_BASE_URL}/download_user_groups`, { responseType: "blob" });

      // Use backend-provided filename
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", zipFilename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Error downloading user groups:", error);
      alert("Failed to download user groups.");
    }
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
          <p className="text-green-500">Select File (CSV, JSON, XLS)</p>
          <FileUpload onFileSelect={handleFileUpload} />
        </div>
      </div>

      {/* Display Stats (After Selecting Users) */}
      {stats && (
        <div className="w-full text-center border border-green-500 p-4 mt-6">
          <h2 className="text-xl">❯ Stats Summary</h2>
          <p>Total Users: {stats.total_users}</p>
          <p>Expected Open Rate: {stats.expected_open_rate}%</p>
          <p>Mail Group: {stats.mail_group}</p>
          <p>WhatsApp Group: {stats.whatsapp_group}</p>
          <p>Ignored Group: {stats.ignored_group}</p>
        </div>
      )}

      <div className="mt-6 space-x-4 flex">
        <Button text={loading ? "Loading..." : "Select Users"} onClick={handleSelectUsers} />
        <button
          onClick={handleDownloadGroups}
          disabled={!filesGenerated || !zipFilename}
          className={`px-6 py-2 text-lg border ${filesGenerated ? "bg-black text-green-500 border-green-500 hover:bg-green-500 hover:text-black transition" : "border-gray-500 text-gray-500 cursor-not-allowed"}`}
        >
          ❯ Download User Groups
        </button>
      </div>
    </div>
  );
}

export default App;
