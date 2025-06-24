# MentorAgents 🤖💡

**Your personal mentors, anytime. Anywhere.**

MentorAgents is an AI-powered platform where users interact with agents modeled after legendary real-world experts—like Elon Musk for startups, Naval Ravikant for wealth, or Lex Fridman for AI. Ask questions, get tailored guidance, and learn from the best minds — anytime, anywhere.


## 🚀 Features

- **Legendary Mentor AI Agents**: Chat with AI versions of famous entrepreneurs, investors, and thought leaders
- **Intelligent Memory System**: Both short-term and long-term memory capabilities using MongoDB
- **RAG-Powered Knowledge**: Vector database containing comprehensive mentor profiles, life experiences, and wisdom
- **Gamified Learning Experience**: Interactive React-based frontend with engaging user experience
- **Real-time Conversations**: Fast and responsive chat interface powered by FastAPI
- **Personalized Insights**: Get tailored advice based on your specific questions and context

## 🛠 Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **LangGraph** - Advanced AI agent orchestration with memory management
- **LangChain** - LLM integration and RAG implementation
- **MongoDB** - Document database for persistent memory and state management
- **Vector Database** - Semantic search for mentor knowledge retrieval
- **Groq** - Fast LLM inference
- **Sentence Transformers** - Text embeddings for RAG

### Frontend
- **React** - Modern frontend framework
- **Interactive UI** - Gamified chat experience

### AI & ML
- **RAG (Retrieval Augmented Generation)** - Knowledge-enhanced responses
- **Text Embeddings** - Semantic search capabilities
- **Memory Management** - Context preservation across conversations

## 🏗 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Web     │    │   FastAPI        │    │   MongoDB       │
│   Frontend      │◄──►│   Backend        │◄──►│   Database      │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   LangGraph      │
                       │   AI Agents      │
                       │                  │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Vector DB      │
                       │   (RAG System)   │
                       │                  │
                       └──────────────────┘
```

### Key Components

1. **AI Agent Layer**: LangGraph manages intelligent conversations with mentor personalities
2. **Memory Management**: 
   - Short-term memory for conversation context
   - Long-term memory for user preferences and history
3. **Knowledge Retrieval**: RAG system pulls relevant mentor insights from vector database
4. **API Layer**: FastAPI provides high-performance backend services
5. **Data Persistence**: MongoDB stores conversation history and agent states

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 16+
- MongoDB instance
- Groq API key

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mentoragents.git
   cd mentoragents/backend
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv install

   # Or using pip
   pip install -e .
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

   Required environment variables:
   ```
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   MONGO_URI=your_mongodb_connection_string
   COMET_API_KEY=your_comet_api_key (optional)
   ```

4. **Start the backend server**
   ```bash
   python -m mentoragents.main
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The web app will be available at `http://localhost:3000`

## 📖 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🤖 Available Mentors

- **Naval Ravikant** - Entrepreneur, Angel Investor, Philosophy
- **Elon Musk** - Innovation, Technology, Space Exploration
- **Warren Buffett** - Investing, Business Strategy, Long-term Thinking
- **And many more...** (Expanding mentor library)

## 💬 How It Works

1. **Choose Your Mentor**: Select from available mentor personalities
2. **Ask Your Question**: Type your question or describe your challenge
3. **Get Personalized Advice**: The AI agent retrieves relevant knowledge and provides mentor-style guidance
4. **Continue the Conversation**: Build on previous discussions with persistent memory

## 🧠 Memory System

- **Short-term Memory**: Maintains conversation context within sessions
- **Long-term Memory**: Remembers user preferences, past topics, and learning progress
- **Knowledge Base**: Continuously updated mentor profiles and experiences

## 🔧 Configuration

Key configuration options in `backend/src/mentoragents/core/config.py`:

- **RAG Settings**: Embedding model, chunk size, retrieval parameters
- **Memory Settings**: Message limits, summary triggers
- **Database Settings**: MongoDB collections and connection settings
- **API Settings**: CORS, server configuration

## 🛣 Roadmap

- [ ] Expand mentor library with more personalities
- [ ] Add voice chat capabilities
- [ ] Implement mentor-specific knowledge domains
- [ ] Mobile app development
- [ ] Advanced analytics and insights
- [ ] Multi-language support

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- LangChain and LangGraph communities for AI agent frameworks
- The mentors whose wisdom inspired this project
- Open source contributors making AI accessible

## 📞 Support

- **Documentation**: [docs.mentoragents.ai](https://docs.mentoragents.ai)
- **Issues**: [GitHub Issues](https://github.com/yourusername/mentoragents/issues)
- **Discord**: [Join our community](https://discord.gg/mentoragents)

---

**Ready to learn from the best? Start your mentorship journey today!** 🚀

