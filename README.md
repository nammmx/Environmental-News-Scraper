![Banner](https://github.com/nammmx/nammmx.github.io/blob/main/pictures/environmental-scraper.jpg)
# Environmental News Scraper and Summarizer

This project automates the extraction, summarization, and categorization of environmental news articles from "The Guardian", generating associated images and storing all related data in a PostgreSQL database. It is designed to provide researchers, journalists, and enthusiasts with an automated, comprehensive daily overview of environmental news.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Detailed Function Documentation](#detailed-function-documentation)
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

## Detailed Function Documentation

### Database Connection

#### `create_session(user, password, host, port, db)`
Initializes a connection to the PostgreSQL database using SQLAlchemy. This function creates an `engine` and a session maker that returns a session object to interact with the database, enabling transaction management.

- **Parameters**:
  - `user`: Username for the database.
  - `password`: Password for the database access.
  - `host`: Database server host URL.
  - `port`: Port on which the database server is listening.
  - `db`: Name of the database to connect to.

### Cloudinary Configuration

#### `configure_cloudinary()`
Configures the Cloudinary service with the required credentials for API access, setting up the environment for future image uploads. This configuration is necessary for the `upload_image` function to operate correctly.

### AI Tools Initialization

#### `setup_ai_tools()`
Sets up the AI models used for text summarization and image generation. This function initializes a summarization pipeline using models from Hugging Face's Transformers library and configures the Stability AI client for generating images based on textual descriptions.

- **Returns**:
  - A tuple containing the initialized summarizer and Stability AI client objects.

### Article Processing

#### `process_articles(session, summarizer)`
Orchestrates the end-to-end process of fetching, summarizing, and storing articles. It scrapes the website, checks for new articles, processes each new article for summarization and topic detection, and finally stores them in the database.

- **Detailed Steps**:
  - Fetches the HTML content of the page.
  - Parses the HTML to find articles.
  - Checks existing entries in the database to avoid duplicates.
  - For each new article, extracts content, generates a summary, and detects topics.

### Image Handling

#### `generate_and_upload_images(session, stability_api)`
Generates images based on article summaries and uploads them to Cloudinary. This function loops through all articles that do not yet have an associated image, generates an image using Stability AI, and uploads the image using the configured Cloudinary client.

- **Process Flow**:
  - Retrieve articles needing images from the database.
  - For each article, generate an image based on its title and summary.
  - Convert the image to JPEG format.
  - Upload the image and update the article record with the image URL.
 
## Deployment
- Create Docker-AWS image with scrape function and Transformer model
- Deploy Docker image to AWS ECR
- Create Lambda function using Docker image from ECR
  - Set up VPC with internet access for lambda function
- Set schedule to run Lambda function daily

## Acknowledgments

- **The Guardian**: For providing an accessible platform with extensive environmental reporting.
- **OpenAI**: For making advanced AI tools accessible to developers.
- **Cloudinary**: For offering a robust solution for image management and storage.
- **Stability AI**: For their state-of-the-art image generation technology.
- **Hugging Face**: For their work in democratizing natural language processing tools.

