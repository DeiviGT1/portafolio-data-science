-- Create the table for the app_data dataset

CREATE TABLE public.app_data (
    App TEXT,
    Category VARCHAR(50),
    Rating NUMERIC(3, 1),
    Reviews INTEGER,
    Size VARCHAR(10),
    Installs VARCHAR(20),
    Type TEXT,
    Price NUMERIC,
    Content_Rating VARCHAR(20),
    Genres VARCHAR(100),
    Last_Updated DATE,
    Current_Ver VARCHAR(50),
    Android_Ver VARCHAR(20)
);

-- Import the data from the CSV file
COPY googleplaystore (App, Category, Rating, Reviews, Size, Installs, Type, Price, "Content Rating", Genres, "Last Updated", "Current Ver", "Android Ver")
FROM '/Users/david/Desktop/analisis/portafolio-ds/usa-data/data/csv/V2/googleplaystore.csv'
WITH (FORMAT csv, HEADER true);