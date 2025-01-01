Python Personal Assistant
This project is inspired by Jarvis from the Iron Man movies, designed to simulate a versatile, AI-powered personal assistant. It leverages state-of-the-art models and tools to provide a seamless, command-line-based interaction experience.

The assistant integrates Ollama, Hugging Face Inference Models, and Whisper Speech Recognition for offline functionality while utilizing Google Speech Recognition for enhanced online capabilities. The assistant can perform tasks like answering queries, opening software, generating images from prompts, and more.

This repository offers a command-line interface (CLI) version of the assistant, providing an excellent foundation for more advanced integrations or graphical user interface (GUI) enhancements in the future.

Features
AI-powered Q&A: Utilizes Ollama and Hugging Face models for accurate and context-aware responses.
Speech Recognition:
Offline: Uses OpenAI's Whisper model for robust speech-to-text conversion.
Online: Integrates Google Speech Recognition for dynamic and accurate transcription when connected to the internet.
Application Control: Open and control software on your device via voice or text commands.
Image Generation: Generate stunning visuals from text prompts using advanced generative AI models.
Flexible Operation: Supports both offline and online modes for uninterrupted use.
Extensible Design: Built with modularity, allowing developers to easily add or enhance functionalities.
Prerequisites
General Requirements
Python 3.8 or above installed on your system.
All required Python libraries installed (see Dependencies).
Ollama setup and configured on your device for AI interactions.
A valid Hugging Face API key for online question-answering functionality.
Add gemini 2 flash exp model for online reasoning because of the models capability.







