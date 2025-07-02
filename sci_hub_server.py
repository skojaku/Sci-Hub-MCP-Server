from typing import Any, List, Dict, Optional, Union
import asyncio
import logging
import os
import google.generativeai as genai
from mcp.server.fastmcp import FastMCP
from sci_hub_search import search_paper_by_doi, search_paper_by_title, search_papers_by_keyword, download_paper

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Gemini API
gemini_api_key = os.getenv('GEMINI_API_KEY')
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    logging.info("Gemini API configured successfully")
else:
    logging.warning("GEMINI_API_KEY environment variable not set. Summarization features will not work.")

# Initialize FastMCP server
mcp = FastMCP("scihub")

@mcp.tool()
async def search_scihub_by_doi(doi: str) -> Dict[str, Any]:
    logging.info(f"Searching for paper with DOI: {doi}")
    """
    Search for a paper on Sci-Hub using its DOI (Digital Object Identifier).

    Args:
        doi (str): The Digital Object Identifier of the paper, a unique alphanumeric string 
             that identifies academic, professional, and scientific content 
             (e.g., "10.1038/nature09492").

    Returns:
        Dict[str, Any]: Dictionary containing paper information including:
            - title: The title of the paper
            - author: The author(s) of the paper
            - year: Publication year
            - pdf_url: URL to download the PDF if available
            - status: Success or error status
            - error: Error message if search failed
    """
    try:
        result = await asyncio.to_thread(search_paper_by_doi, doi)
        return result
    except Exception as e:
        return {"error": f"An error occurred while searching by DOI: {str(e)}"}

@mcp.tool()
async def search_scihub_by_title(title: str) -> Dict[str, Any]:
    logging.info(f"Searching for paper with title: {title}")
    """
    Search for a paper on Sci-Hub using its title.

    Args:
        title (str): The full or partial title of the academic paper to search for.
               More specific and complete titles will yield more accurate results.

    Returns:
        Dict[str, Any]: Dictionary containing paper information including:
            - title: The title of the paper
            - author: The author(s) of the paper
            - year: Publication year
            - pdf_url: URL to download the PDF if available
            - status: Success or error status
            - error: Error message if search failed
    """
    try:
        result = await asyncio.to_thread(search_paper_by_title, title)
        return result
    except Exception as e:
        return {"error": f"An error occurred while searching by title: {str(e)}"}

@mcp.tool()
async def search_scihub_by_keyword(keyword: str, num_results: int = 10) -> List[Dict[str, Any]]:
    logging.info(f"Searching for papers with keyword: {keyword}, number of results: {num_results}")
    """
    Search for papers on Sci-Hub using a keyword.

    Args:
        keyword (str): The keyword or search term to use for finding relevant papers.
                 Can be a subject, concept, or any term related to the research area.
        num_results (int, optional): Maximum number of search results to return. 
                      Defaults to 10. Higher values may increase search time.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing information about a paper:
            - title: The title of the paper
            - author: The author(s) of the paper
            - year: Publication year
            - doi: Digital Object Identifier if available
            - pdf_url: URL to download the PDF if available
            - status: Success or error status
            - error: Error message if search failed
    """
    try:
        results = await asyncio.to_thread(search_papers_by_keyword, keyword, num_results)
        return results
    except Exception as e:
        return [{"error": f"An error occurred while searching by keyword: {str(e)}"}]

@mcp.tool()
async def download_scihub_pdf(pdf_url: str, output_path: str) -> str:
    logging.info(f"Attempting to download PDF from {pdf_url} to {output_path}")
    """
    Download a paper PDF from Sci-Hub.

    Args:
        pdf_url (str): The URL of the PDF to download. This should be a direct link to the PDF file,
                 typically obtained from a previous search result's 'pdf_url' field.
        output_path (str): The file path where the downloaded PDF should be saved.
                     Should include the filename with .pdf extension.

    Returns:
        str: A message indicating the download result:
             - Success message with the output path if download was successful
             - Failure message if download failed
             - Error message with exception details if an error occurred
    """
    try:
        success = await asyncio.to_thread(download_paper, pdf_url, output_path)
        if success:
            return f"PDF successfully downloaded to {output_path}"
        else:
            return f"Failed to download PDF to {output_path}"
    except Exception as e:
        return f"An error occurred while downloading PDF: {str(e)}"

@mcp.tool()
async def get_paper_metadata(doi: str) -> Dict[str, Any]:
    logging.info(f"Getting metadata for paper with DOI: {doi}")
    """
    Get metadata information for a paper using its DOI.

    Args:
        doi (str): The Digital Object Identifier of the paper, a unique alphanumeric string
             that identifies the academic paper (e.g., "10.1038/nature09492").

    Returns:
        Dict[str, Any]: Dictionary containing paper metadata including:
            - doi: The DOI of the paper
            - title: The title of the paper
            - author: The author(s) of the paper
            - year: Publication year
            - pdf_url: URL to download the PDF if available
            - status: Success or error status
            - error: Error message if retrieval failed
    """
    try:
        # First search for the paper by DOI
        paper_info = await asyncio.to_thread(search_paper_by_doi, doi)
        
        if paper_info.get('status') == 'success':
            # Extract and return metadata
            return {
                'doi': doi,
                'title': paper_info.get('title', ''),
                'author': paper_info.get('author', ''),
                'year': paper_info.get('year', ''),
                'pdf_url': paper_info.get('pdf_url', ''),
                'status': 'success'
            }
        else:
            return {"error": f"Could not find metadata for paper with DOI {doi}"}
    except Exception as e:
        return {"error": f"An error occurred while getting metadata: {str(e)}"}

@mcp.tool()
async def summarize_pdf_papers(pdf_url: str, context: Optional[str] = None) -> Dict[str, Any]:
    logging.info(f"Summarizing PDF from URL: {pdf_url}")
    """
    Summarize PDF papers using Google Gemini AI with optional context for citation validation.

    Args:
        pdf_url (str): The URL of the PDF to summarize. This should be a direct link to the PDF file,
                 typically obtained from a previous search result's 'pdf_url' field.
        context (str, optional): Additional context for the summarization, such as the sentence/paragraph
                    where the paper was cited. This helps validate if the citation is appropriate.

    Returns:
        Dict[str, Any]: Dictionary containing:
            - summary: The AI-generated summary of the paper
            - citation_validation: Analysis of whether the citation is appropriate (if context provided)
            - status: Success or error status
            - error: Error message if summarization failed
    """
    try:
        # Check if Gemini API is configured
        if not gemini_api_key:
            return {"error": "GEMINI_API_KEY environment variable not set. Please configure your Gemini API key."}
        
        # Download the PDF to a temporary location
        import tempfile
        import requests
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_path = temp_file.name
            
        # Download the PDF
        response = requests.get(pdf_url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logging.info(f"PDF downloaded to temporary file: {temp_path}")
        
        # Upload the PDF to Gemini
        uploaded_file = genai.upload_file(temp_path)
        logging.info(f"PDF uploaded to Gemini: {uploaded_file.name}")
        
        # Create the model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Create the prompt based on whether context is provided
        if context:
            prompt = f"""Please analyze this PDF paper and provide:

1. A comprehensive summary of the paper including:
   - Main research question/objective
   - Methodology used
   - Key findings and results
   - Conclusions and implications

2. Citation validation: Given the following context where this paper was cited:
   "{context}"
   
   Please evaluate:
   - Is this citation appropriate and accurate?
   - Does the context correctly represent the paper's findings?
   - Are there any misrepresentations or misunderstandings?
   - Suggestions for improving the citation if needed

Please provide a clear, structured response."""
        else:
            prompt = """Please provide a comprehensive summary of this PDF paper including:

1. Main research question/objective
2. Methodology used
3. Key findings and results
4. Conclusions and implications
5. Significance and potential impact

Please provide a clear, structured response."""
        
        # Generate the summary
        response = await asyncio.to_thread(model.generate_content, [uploaded_file, prompt])
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        # Delete the uploaded file from Gemini
        genai.delete_file(uploaded_file.name)
        
        result = {
            "summary": response.text,
            "status": "success"
        }
        
        if context:
            result["citation_validation"] = True
            result["context_provided"] = context
        
        return result
        
    except Exception as e:
        # Clean up temporary file if it exists
        try:
            if 'temp_path' in locals():
                os.unlink(temp_path)
        except:
            pass
        
        return {"error": f"An error occurred while summarizing PDF: {str(e)}", "status": "error"}

if __name__ == "__main__":
    logging.info("Starting Sci-Hub MCP Server")
    # Initialize and run the server
    mcp.run(transport='stdio')
