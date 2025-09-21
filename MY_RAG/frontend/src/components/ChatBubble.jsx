import React from "react";

export default function ChatBubble({ text, isUser }) {
	return (
		<div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
			<div
				className={`p-3 rounded-lg max-w-xs ${
					isUser ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-900"
				}`}
			>
				{text}
			</div>
		</div>
	);
}
