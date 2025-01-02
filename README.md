# 10K Analyzer

A web application that analyzes SEC 10-K financial reports using AI. Upload your 10-K PDF documents and get instant insights and analysis.

## Project Structure

- `frontend/` - Next.js web application
- `backend/` - FastAPI server with AI analysis capabilities

## Features

- 📄 PDF document upload and processing
- 🤖 AI-powered analysis of 10-K reports
- 💻 Modern, responsive web interface
- 🚀 RESTful API backend

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the backend directory
   - Add your DeepSeek API key:
     ```
     DEEPSEEK_API_KEY=your_api_key_here
     ```

5. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   - Create a `.env.local` file in the frontend directory
   - Configure your environment variables as needed

4. Run the development server:
   ```bash
   npm run dev
   ```

## Deployment

- Frontend is deployed on Vercel
- Backend is deployed on Render

## API Endpoints

- `POST /analyze` - Upload and analyze a 10-K PDF document

## Tech Stack

- **Frontend:**
  - Next.js
  - TypeScript
  - React
  - TailwindCSS

- **Backend:**
  - FastAPI
  - Python
  - DeepSeek AI

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 