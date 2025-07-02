# Sci-Hub MCP Server

[![smithery badge](https://smithery.ai/badge/@JackKuo666/sci-hub-mcp-server)](https://smithery.ai/server/@JackKuo666/sci-hub-mcp-server)

🔍 Enable AI assistants to search, access, and analyze academic papers through Sci-Hub using a simple MCP interface.

The Sci-Hub MCP Server provides a bridge between AI assistants and Sci-Hub's repository of academic literature through the Model Context Protocol (MCP). It allows AI models to search for scientific articles by DOI, title, or keywords, access their metadata, and download PDFs in a programmatic way.

## ✨ Core Features

- 🔎 Paper Search by DOI: Find papers using their Digital Object Identifier ✅
- 🔍 Paper Search by Title: Locate papers using their full or partial title ✅
- 🔑 Paper Search by Keyword: Discover papers related to specific research areas ✅
- 📊 Metadata Access: Retrieve detailed metadata for specific papers ✅
- 📄 PDF Download: Download full-text PDF content when available ✅
- 🤖 AI Paper Summarization: Generate comprehensive summaries using Google Gemini AI ✅
- ✅ Citation Validation: Validate citations with contextual analysis ✅

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- FastMCP library
- Google Gemini API key (for summarization features)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/JackKuo666/Sci-Hub-MCP-Server.git
   cd Sci-Hub-MCP-Server
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Google Gemini API key (required for summarization features):
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key-here"
   ```

## 📊 Usage

Start the MCP server:

```bash
python sci_hub_server.py
```

## Usage with Claude Desktop

Add this configuration to your `claude_desktop_config.json`:

(Mac OS)

```json
{
  "mcpServers": {
    "scihub": {
      "command": "python",
      "args": ["-m", "sci_hub_server.py"]
      }
  }
}
```

(Windows version):

```json
{
  "mcpServers": {
    "scihub": {
      "command": "C:\\Users\\YOUR\\PATH\\miniconda3\\envs\\mcp_server\\python.exe",
      "args": [
        "D:\\code\\YOUR\\PATH\\Sci-Hub-MCP-Server\\sci_hub_server.py"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## 🛠 MCP Tools

The Sci-Hub MCP Server provides the following tools:

1. `search_scihub_by_doi`: Search for a paper on Sci-Hub using its DOI (Digital Object Identifier).
2. `search_scihub_by_title`: Search for a paper on Sci-Hub using its title.
3. `search_scihub_by_keyword`: Search for papers on Sci-Hub using a keyword.
4. `download_scihub_pdf`: Download a paper PDF from Sci-Hub.
5. `get_paper_metadata`: Get metadata information for a paper using its DOI.
6. `summarize_pdf_papers`: Generate AI-powered summaries of PDF papers using Google Gemini AI.

### Searching Papers by DOI

You can ask the AI assistant to search for papers using DOI:
```
Can you search Sci-Hub for the paper with DOI 10.1038/nature09492?
```

### Searching Papers by Title

You can search for papers using their title:
```
Can you find the paper titled "Choosing Assessment Instruments for Posttraumatic Stress Disorder Screening and Outcome Research" on Sci-Hub?
```

### Searching Papers by Keyword

You can search for papers related to specific keywords:
```
Can you search Sci-Hub for recent papers about artificial intelligence in medicine?
```

### Downloading Papers

Once you have found a paper, you can download it:
```
Can you download the PDF for this paper to my_paper.pdf?
```

### Getting Paper Metadata

You can request metadata for a paper using its DOI:
```
Can you show me the metadata for the paper with DOI 10.1038/nature09492?
```

### Summarizing Papers with AI

You can generate comprehensive summaries of papers using Google Gemini AI:
```
Can you summarize this paper PDF for me?
```

With citation validation context:
```
Can you summarize this paper and validate if my citation is appropriate? I cited it as: "Recent studies have shown that machine learning can improve medical diagnosis accuracy (Smith et al., 2023)."
```

## 📁 Project Structure

- `sci_hub_server.py`: The main MCP server implementation using FastMCP
- `sci_hub_search.py`: Contains the logic for searching Sci-Hub and retrieving paper information

## 🔧 Dependencies

- Python 3.10+
- FastMCP
- requests
- bs4
- scihub
- google-generativeai (for AI summarization)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This tool is for research purposes only. Please respect copyright laws and use this tool responsibly. The authors do not endorse or encourage any copyright infringement.
