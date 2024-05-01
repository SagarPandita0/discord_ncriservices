# Discord Data Viewer

This project is a full-stack application that facilitates the exportation of Discord chat histories, allows for the searching of these chats by various criteria, and provides a user-friendly graphical user interface (GUI) for data interaction.

## Features

- **Export Discord Chats**: Export chats from the past 7 days of a specific Discord channel.
- **Search by Keyword**: Search through exported chats using a keyword.
- **Filter by Date**: Find chats within a specified date range.
- **User-Friendly GUI**: Easily interact with the data and backend services through a GUI.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher
- PostgreSQL
- A Discord account with access to the channel you wish to export data from.

## Installation

Follow these steps to install the Discord Data Viewer:

1. Clone the repository:
git clone [https://github.com/your-username/discord-data-viewer.git](https://github.com/SagarPandita0/discord_ncriservices.git)

    `cd discord_ncriservices`


3. Install the necessary Python packages: 

    `pip install -r requirements.txt`

3. Set up the required environment variables by creating a `.env` file with your Discord credentials and database URL:

    `DATABASE_URL=postgresql://user:password@localhost/discordData`

    `DISCORD_TOKEN=your_discord_token_here`

    `CHANNEL_ID=your_channel_id_here`



## Initialization

Run the `init_db.py` script to initialize your database:


## Running the Application

To launch the application, follow these steps:

1. Start the FastAPI server:

    `python -m app.main`


2. To access the GUI, open the `index.html` file in your browser or use a local server.


## Usage

Utilize the application as follows:

- To **export chats** from Discord, navigate to the `/export-discord-chats` endpoint and provide a channel ID.
- To **search by keyword**, access the `/search` endpoint and enter your search term.
- To **filter by date range**, use the `/search_by_date` endpoint with the desired start and end dates.
- To **filter by author name**, use the `/search_by_author`

## API Endpoints

The following endpoints are available:

- `GET /export-discord-chats/?channel_id={channel_id}`
- `GET /search?search_term={search_term}`
- `GET /search_by_date?start_date={start_date}&end_date={end_date}`
- `GET /search_by_author?author_name={name}`

