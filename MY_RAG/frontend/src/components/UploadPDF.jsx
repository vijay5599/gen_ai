import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [company, setCompany] = useState("");
  const [year, setYear] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !company || !year) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("company", company);
    formData.append("year", year);

    try {
      const res = await fetch("http://localhost:8000/ingest_pdf/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.status === "success") {
        navigate("/chat"); // go to chatbot after successful upload
      } else {
        alert("Upload failed!");
      }
    } catch (err) {
      alert("Error uploading file!");
      console.error(err);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-20 p-4 bg-white rounded shadow">
      <h1 className="text-2xl font-bold mb-4">Upload Financial Report</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="border p-2 rounded"
        />
        <input
          type="text"
          placeholder="Company Name"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="text"
          placeholder="Year"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          className="border p-2 rounded"
        />
        <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Upload & Start Chat
        </button>
      </form>
    </div>
  );
}
