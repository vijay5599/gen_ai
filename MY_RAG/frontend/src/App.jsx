import React from "react";
import { Routes, Route } from "react-router-dom";
import UploadPage from "./components/UploadPDF";
import ChatPage from "./components/QueryRAG";

export default function App() {
	return (
		<Routes>
			<Route path="/" element={<UploadPage />} />
			<Route path="/chat" element={<ChatPage />} />
		</Routes>
	);
}
