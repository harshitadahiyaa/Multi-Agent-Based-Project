# 🛍️ Smart Product Price Comparison Assistant using Multi-Agent AI

An AI-powered product comparison system that searches products across multiple e-commerce platforms, compares prices, ratings, and specifications, and recommends the best product using a Multi-Agent Architecture built with LangGraph.

---

# 📌 Table of Contents

- Project Overview
- Features
- System Architecture
- Technology Stack
- Project Structure
- System Requirements
- Installation & Setup
- Usage Instructions
- Multi-Agent Workflow
- APIs Used
- Future Enhancements
- License

---

# 📖 Project Overview

Shopping online often requires users to browse multiple websites before finding the best deal. This project automates that process using a Multi-Agent AI architecture.

The application searches products from multiple shopping platforms, compares their prices, ratings, specifications, and availability, then provides an intelligent recommendation with an easy-to-understand summary.

The application is developed using Python, LangGraph, Streamlit, Groq LLM, SerpAPI, Firecrawl, and Playwright.

---

# ✨ Features

- Multi-Agent AI Architecture
- Product Search across multiple stores
- Amazon Product Search using SerpAPI
- Flipkart Product Search using Playwright
- Additional Store Search using Firecrawl
- Intelligent Product Comparison
- AI-based Product Recommendation
- Natural Language Recommendation using Groq LLM
- Interactive Streamlit Dashboard
- Duplicate Product Removal
- Product Ranking
- Price Comparison
- Rating Comparison
- Best Value Product Detection

---

# 🏗️ System Architecture

```
                User
                  │
                  ▼
          Streamlit Frontend
                  │
                  ▼
          LangGraph Workflow
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
 Search Agent  Comparison  Recommendation
                    │
                    ▼
            Response Agent
                    │
                    ▼
             Final Recommendation
```

---

# 💻 Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| AI Framework | LangGraph |
| LLM | Groq |
| Frontend | Streamlit |
| Product Search | SerpAPI |
| Web Scraping | Playwright |
| Web Crawling | Firecrawl |
| Data Validation | Pydantic |
| Configuration | python-dotenv |

---

# 📂 Project Structure

```
Multi-Agent-Based-Project/

│── Agents/
│   ├── graph_state.py
│   ├── workflow.py
│   ├── search_agent.py
│   ├── comparison_agent.py
│   ├── recommendation_agent.py
│   └── response_agent.py
│
│── Services/
│   ├── amazon_service.py
│   ├── flipkart_service.py
│   ├── firecrawl_service.py
│   └── groq_service.py
│
│── frontend/
│
│── models/
│   └── product.py
│
│── utils/
│
│── cache/
│
│── tests/
│
│── app.py
│── requirements.txt
│── README.md
│── .env.example
```

---

# ⚙️ System Requirements

| Requirement | Specification |
|------------|---------------|
| Python Version | Python 3.10+ (Recommended: Python 3.11) |
| Operating System | Windows 10/11, Ubuntu 22.04+, macOS 12+, Google Colab (Testing Only) |
| GPU | Not Required (Runs on CPU) |
| RAM | Minimum 8 GB |
| Internet | Required |
| Disk Space | Approximately 500 MB |

---

# 🔑 Required API Keys

Create a `.env` file and add the following:

```env
GROQ_API_KEY=your_groq_api_key
SERPAPI_KEY=your_serpapi_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

> **Important:** Never commit your actual API keys to GitHub. Keep the `.env` file private.

---

# 🚀 Installation & Setup

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Multi-Agent-Based-Project
```

---

## Step 2: Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
SERPAPI_KEY=your_serpapi_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

---

## Step 5: Install Playwright Browser

```bash
playwright install
```

---

## Step 6: Run the Application

```bash
streamlit run app.py
```

Open your browser:

```
http://localhost:8501
```

---

# 📖 Usage Instructions

### Step 1

Launch the application.

```bash
streamlit run app.py
```

---

### Step 2

Open the application in your web browser.

```
http://localhost:8501
```

---

### Step 3

Enter the product you want to compare.

Example:

```
iPhone 16 Pro 256GB
```

or

```
Best gaming laptop under ₹1,00,000
```

---

### Step 4

The **Search Agent** retrieves product information from supported shopping platforms using:

- SerpAPI
- Playwright
- Firecrawl

---

### Step 5

The **Comparison Agent** compares:

- Prices
- Ratings
- Specifications
- Sellers
- Availability

---

### Step 6

The **Recommendation Agent** evaluates all products using a scoring mechanism based on:

- Price
- Rating
- Reviews
- Value Score
- Budget Compatibility

---

### Step 7

The **Response Agent** uses Groq LLM to generate:

- Product Comparison Summary
- Best Product Recommendation
- Buying Suggestions
- Key Highlights

---

### Step 8

The user reviews the comparison and visits the recommended retailer website to verify the latest price and complete the purchase.

---

# 🤖 Multi-Agent Workflow

## 🔍 Search Agent

- Searches Amazon using SerpAPI
- Searches Flipkart using Playwright
- Searches other stores using Firecrawl
- Removes duplicate products

---

## 📊 Comparison Agent

- Compares products
- Finds cheapest product
- Finds highest-rated product
- Calculates value score
- Groups products by brand and source

---

## 🎯 Recommendation Agent

Ranks products based on:

- Budget
- Price
- Rating
- Reviews
- Value Score

---

## 💬 Response Agent

Uses Groq LLM to generate:

- Product Summary
- Buying Recommendation
- Comparison Explanation

---

# 🔌 APIs Used

| API | Purpose |
|------|---------|
| Groq API | AI-powered recommendation generation |
| SerpAPI | Amazon Product Search |
| Firecrawl API | Product Search from other websites |
| Playwright | Flipkart Web Scraping |

---

# 🚀 Future Enhancements

- More e-commerce platforms
- User login system
- Wishlist functionality
- Price history tracking
- Email price alerts
- Product sentiment analysis
- Voice-based product search
- Personalized recommendations

---

# 👥 Team Responsibilities

| Member | Responsibility |
|---------|----------------|
| Member 1 | LangGraph Workflow & Agent Orchestration |
| Member 2 | Amazon Integration (SerpAPI) |
| Member 3 | Flipkart (Playwright) & Firecrawl Integration |
| Member 4 | Comparison Agent & Recommendation Agent |
| Member 5 | Streamlit UI, Testing, Deployment & Documentation |

---

# 📜 License

This project is developed for educational purposes as part of a college project.

Feel free to use and modify it for learning purposes.
