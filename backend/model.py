import os
from PyPDF2 import PdfReader
import tiktoken
from openai import OpenAI
import json
from typing import List, Dict
import logging
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()    

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TenKAnalyzer:
    def __init__(self, api_key: str):
        """Initialize the analyzer with DeepSeek API credentials."""
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        # Initialize tokenizer for counting tokens
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")  # Using GPT-4 tokenizer as approximation
        self.max_tokens = 8000  # Set conservative token limit for context window

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise

    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess the extracted text."""
        # Remove multiple newlines
        text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
        # Remove multiple spaces
        text = ' '.join(text.split())
        return text

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks that fit within the model's context window."""
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        sentences = text.split('. ')
        
        for sentence in sentences:
            sentence_tokens = len(self.tokenizer.encode(sentence + '. '))
            
            if current_tokens + sentence_tokens > self.max_tokens:
                chunks.append(current_chunk)
                current_chunk = sentence + '. '
                current_tokens = sentence_tokens
            else:
                current_chunk += sentence + '. '
                current_tokens += sentence_tokens
        
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks

    def analyze_chunk(self, chunk: str) -> Dict:
        """Analyze a chunk of text using DeepSeek-V3."""
        try:
            system_prompt = """You are a concise financial analyst expert. Analyze the following 10-K filing excerpt and provide the MOST critical insights in pure JSON format (do not wrap in markdown code blocks). Use this exact structure:
{
    "key_financial_metrics": [],
    "risks_and_challenges": [],
    "strategic_initiatives": [],
    "significant_changes": []
}

Be extremely selective and concise. Each array should contain only 3-5 of the MOST important points as strings. Focus on high-level, material insights that would be most relevant to investors. Each point should be a single sentence. Do not include any markdown formatting or code blocks in your response."""

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": chunk}
                ],
                stream=False
            )
            
            # Debug logging
            raw_content = response.choices[0].message.content
            logger.debug(f"Raw API response content: {raw_content}")
            
            # Clean up the response if it's wrapped in markdown code blocks
            cleaned_content = raw_content
            if cleaned_content.startswith('```json'):
                cleaned_content = cleaned_content.replace('```json', '', 1)
            if cleaned_content.endswith('```'):
                cleaned_content = cleaned_content.rsplit('```', 1)[0]
            cleaned_content = cleaned_content.strip()
            
            try:
                parsed_response = json.loads(cleaned_content)
                # Ensure we have all required keys with at least empty arrays
                return {
                    "key_financial_metrics": parsed_response.get("key_financial_metrics", []),
                    "risks_and_challenges": parsed_response.get("risks_and_challenges", []),
                    "strategic_initiatives": parsed_response.get("strategic_initiatives", []),
                    "significant_changes": parsed_response.get("significant_changes", [])
                }
            except json.JSONDecodeError as je:
                logger.error(f"Failed to parse JSON response: {cleaned_content}")
                # Return empty structure
                return {
                    "key_financial_metrics": [],
                    "risks_and_challenges": [],
                    "strategic_initiatives": [],
                    "significant_changes": [],
                    "raw_response": raw_content
                }
                
        except Exception as e:
            logger.error(f"Error in API call: {str(e)}")
            return {
                "key_financial_metrics": [],
                "risks_and_challenges": [],
                "strategic_initiatives": [],
                "significant_changes": [],
                "error": str(e)
            }

    def consolidate_analyses(self, analyses: List[Dict]) -> Dict:
        """Consolidate analyses from multiple chunks into a single comprehensive report."""
        consolidated = {
            "key_financial_metrics": [],
            "risks_and_challenges": [],
            "strategic_initiatives": [],
            "significant_changes": []
        }
        
        # Collect all unique insights
        for analysis in analyses:
            for key in consolidated.keys():
                if key in analysis:
                    consolidated[key].extend(analysis[key])
        
        # Remove duplicates while preserving order
        for key in consolidated.keys():
            # Remove duplicates
            consolidated[key] = list(dict.fromkeys(consolidated[key]))
            
            # Sort by length (to prioritize more concise points) and take top 10
            consolidated[key] = sorted(consolidated[key], key=len)[:10]
            
            # Ensure we don't have more than 5 points per category
            if len(consolidated[key]) > 10:
                consolidated[key] = consolidated[key][:7]
        
        return consolidated

    def analyze_10k(self, pdf_path: str) -> Dict:
        """Main function to analyze a 10-K filing."""
        logger.info(f"Starting analysis of {pdf_path}")
        
        # Extract and preprocess text
        text = self.extract_text_from_pdf(pdf_path)
        text = self.preprocess_text(text)
        
        # Split into chunks
        chunks = self.chunk_text(text)
        logger.info(f"Split document into {len(chunks)} chunks")
        
        # Analyze each chunk
        analyses = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Analyzing chunk {i+1}/{len(chunks)}")
            analysis = self.analyze_chunk(chunk)
            analyses.append(analysis)
        
        # Consolidate analyses
        final_analysis = self.consolidate_analyses(analyses)
        
        return final_analysis

def main():
    # Example usage
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("Please set DEEPSEEK_API_KEY environment variable")
    
    analyzer = TenKAnalyzer(api_key)
    
    # Example analysis
    pdf_path = "/Users/dhrubhagatsingh/Desktop/10kproject/backend/coinbase.pdf"
    analysis = analyzer.analyze_10k(pdf_path)
    
    # Save results
    with open("10k_analysis.json", "w") as f:
        json.dump(analysis, f, indent=4)

if __name__ == "__main__":
    main()