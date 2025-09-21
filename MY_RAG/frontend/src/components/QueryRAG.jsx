import React, { useState, useEffect, useRef } from "react";
import ChatBubble from "./ChatBubble";

export default function ChatPage() {
	const [messages, setMessages] = useState([
		{
			text: "Hello! Ask me about the uploaded financial report.",
			isUser: false,
		},
	]);
	const [input, setInput] = useState("");
	const messagesEndRef = useRef(null);

	const scrollToBottom = () => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
	};

	useEffect(scrollToBottom, [messages]);

	const handleSend = async () => {
		if (!input.trim()) return;

		const userMessage = { text: input, isUser: true };
		setMessages((prev) => [...prev, userMessage]);
		setInput("");

		try {
			const res = await fetch(
				`http://localhost:8000/query/?question=${encodeURIComponent(input)}`
			);
			const data = await res.json();
			setMessages((prev) => [
				...prev,
				{ text: data.answer || "No answer found.", isUser: false },
			]);
		} catch (err) {
			setMessages((prev) => [
				...prev,
				{ text: "Error connecting to backend.", isUser: false },
			]);
		}
	};

	return (
		<div className="flex flex-col h-screen max-w-2xl mx-auto p-4">
			<h1 className="text-2xl font-bold mb-4">Financial Report Assistant</h1>
			<div className="flex-1 overflow-y-auto mb-4">
				{messages.map((msg, idx) => (
					<ChatBubble key={idx} text={msg.text} isUser={msg.isUser} />
				))}
				<div ref={messagesEndRef} />
			</div>
			<div className="flex gap-2">
				<input
					type="text"
					className="flex-1 p-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
					value={input}
					onChange={(e) => setInput(e.target.value)}
					onKeyDown={(e) => e.key === "Enter" && handleSend()}
					placeholder="Type your question..."
				/>
				<button
					className="bg-blue-500 text-white px-4 rounded hover:bg-blue-600"
					onClick={handleSend}
				>
					Send
				</button>
			</div>
		</div>
	);
}
