![Banner](https://github.com/nammmx/nammmx.github.io/blob/main/pictures/environmental-scraper.jpg)
# Environmental News Scraper and Summarizer

This project automates the extraction, summarization, and categorization of environmental news articles from "The Guardian", generating associated images and storing all related data in a PostgreSQL database. It is designed to provide researchers, journalists, and enthusiasts with an automated, comprehensive daily overview of environmental news.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Detailed Workflow](#detailed-workflow)
- [Deployment](#deployment)
- [Acknowledgments](#acknowledgments)

## Features

- **Automated Scraping**: Fetches daily environmental news from "The Guardian".
- **Text Summarization**: Summarizes the articles using Transformer models.
- **Topic Detection**: Utilizes OpenAI's language models to classify articles into predefined topics.
- **Image Generation**: Generates images relevant to the articles using Stability AI.
- **Cloud Image Storage**: Manages image uploads and storage via Cloudinary.

## Technology Stack

- **Python**: Main programming language.
- **Requests & BeautifulSoup**: For scraping web content.
- **SQLAlchemy**: For interacting with the PostgreSQL database.
- **Transformers**: For applying natural language processing tasks.
- **Pillow**: For handling image processing tasks.
- **Stability SDK & Cloudinary**: For generating and uploading images.
- **OpenAI**: For generating text completions and classifications.
- **Streamlit**: For Front-end.

## Detailed Workflow

1. **Environment Setup**  
   - **Input**: None directly.
   - **Output**: Environment variables for Hugging Face models are set, and necessary libraries (requests, BeautifulSoup, SQLAlchemy, AI tools, etc.) are imported.

2. **Logging Setup**  
   - **Input**: None.
   - **Output**: Basic logging configuration is established to track function calls and errors.

3. **Database Session: `create_session()`**
   - **Input**: Database credentials (`user`, `password`, `host`, `port`, `db`).
   - **Output**: Creates a PostgreSQL database session using SQLAlchemy, returning a session object for further use in interacting with the database.

4. **AI Tools Setup: `setup_ai_tools()`**
   - **Input**: None directly (uses model paths and API keys from environment/credentials).
   - **Output**: Initializes a BART summarizer (using the `bart-large-cnn` model) and a Stability AI client for image generation. Returns the summarizer and Stability AI client.

5. **Cloudinary Configuration: `configure_cloudinary()`**
   - **Input**: Cloudinary credentials (`cloud_name`, `api_key`, `api_secret`).
   - **Output**: Configures Cloudinary for uploading images. No explicit output, but Cloudinary is now ready for use.

6. **Article Processing: `process_articles()`**
   - **Input**: Database session, summarizer from `setup_ai_tools()`.
   - **Output**:
     - Scrapes articles from The Guardian environment section.
     - Checks for already-existing articles by querying the database for recent links.
     - Calls `fetch_and_summarize_article()` for each new article, processing up to 10 new articles.
     - Inserts new articles into the database using `insert_article()`.

7. **Fetch and Summarize Articles: `fetch_and_summarize_article()`**
   - **Input**: Article URL (`href`), summarizer from `setup_ai_tools()`.
   - **Output**:
     - Scrapes the article content from the provided URL.
     - Truncates the content to 1024 tokens using Hugging Face's BART tokenizer.
     - Generates a summary of the truncated content with the BART model.
     - Calls `chatgpt_topic()` to determine the two most fitting topics.
     - Returns the truncated article content, generated summary, and two topics.

8. **Topic Assignment: `chatgpt_topic()`**
   - **Input**: Truncated article content.
   - **Output**: Sends the article content to OpenAI GPT with a predefined list of topics. GPT returns two topics in the format `topic1-topic2`, where `topic1` is the best-fitting topic and `topic2` is the second-best.

9. **Insert Article into Database: `insert_article()`**
   - **Input**: Database session, article title, URL (`href`), content, summary, and topics (`topic1`, `topic2`).
   - **Output**: Inserts the article, summary, and topics into the `news` table in PostgreSQL. If the article link already exists, it skips the insertion (`ON CONFLICT DO NOTHING`).

10. **Upload Image to Cloudinary: `upload_image()`**
    - **Input**: Image data (in bytes) and a `public_id` (derived from the article title).
    - **Output**: Uploads the image to Cloudinary using the provided image data and public ID. Returns the URL of the uploaded image or `None` if an error occurs.

11. **Generate Image with Stability AI: `generate_image()`**
    - **Input**: Stability AI client, article title, and summary.
    - **Output**:
      - Generates an image from a prompt that includes the title and summary using Stability AI’s Stable Diffusion model.
      - Converts the generated image to JPEG format in memory.
      - Returns the image data as a byte string and calls `upload_image()` to upload the image to Cloudinary, returning the image URL.

12. **Generate and Upload Images: `generate_and_upload_images()`**
    - **Input**: Database session, Stability AI client.
    - **Output**:
      - Queries the `news` table to fetch articles without images.
      - For each article, calls `generate_image()` to create an image, uploads it using `upload_image()`, and updates the article’s database entry with the image URL. 
## Deployment
- Create Docker-AWS image with scrape function and Transformer model (https://www.youtube.com/watch?v=nZU9_2bTNTM)
- Deploy Docker image to AWS ECR (https://www.youtube.com/watch?v=nZU9_2bTNTM)
- Create Lambda function using Docker image from ECR (https://www.youtube.com/watch?v=nZU9_2bTNTM)
  - Set up VPC with internet access for lambda function (https://www.youtube.com/watch?v=Z3dMhPxbuG0&t=136s)
- Set schedule to run daily: (3 separate lambda functions and schedules)
  - Everyday at 09:45 and 21:45 a NAT Gateway is created (lower cost compared to keeping NAT Gateway active 24/7)
  - Everyday at 10:00 and 22:00 the scrape function is executed
  - Everyday at 10:20 and 22:20 the NAT Gateway is deleted

## Acknowledgments

- **The Guardian**: For providing an accessible platform with extensive environmental reporting.
- **OpenAI**: For making advanced AI tools accessible to developers.
- **Cloudinary**: For offering a robust solution for image management and storage.
- **Stability AI**: For their state-of-the-art image generation technology.
- **Hugging Face**: For their work in democratizing natural language processing tools.

