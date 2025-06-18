
# My Movies 

This app aims at collecting all your favorite movies (or all that you want really) and display this collection into a beautiful HTML frontend.

## Installation

To install this app, simply clone the repository and install the dependencies in requirements.txt using `pip`

```bash
   pip install -r requirements.txt
```

## Usage

To use this app, run the following command `python my_movies.py`
> The app now supports multi-users with individual collection and website for each user, you'll first be prompted to select a user (you may Add, Delete, or Update a user)

Once the user selected, you'll be presented with a CLI menu including 12 options:
> 0. Exit >>> leave the program
> 1. List Movies >>> Get a list of all the movies added to the collection with year of release and average rating
> 2. Add Movie >>> Prompts you to enter a title and will fetch the corresponding data via OMDb database (https://www.omdbapi.com/)
> 3. Delete Movie >>> Prompts you to enter the title of the movie you want to remove from your collection
> 4. Update Movie >>> Prompts you to enter a personal note on any given movie from the collection
> 5. List Stats >>> Will provide some KPIs about all the movies in your collection (e.g., best-rated movie...)
> 6. Random Movie >>> Will select a random movie from the collection
> 7. Search Movie >>> Provides a search engine of your collection (allows minor typos via edit distance)
> 8. Movies Sorted by Rating >>> Get a list of all movies sorted by descending average rating 
> 9. Movies Sorted by Year >>> Get a list of all movies sorted by ascending or descending year (your choice)
> 10. Filter Movies >>> Provides basic filter movies for narrow search of specific movies
> 11. Generate Website >>> Will build the HTML user interface
> 12. Create Ratings Histogram >>> Will build and store a ratings histogram of all movies from the collection

## Project Status

As of _18-JUN-2025_, project is: _in progress_

## Room for Improvement

> - A list of movies could be provided to the user instead of "guessing" which are available
> - More data could be provided in the final HTML page
> - A GUI could be introduced next

## Acknowledgements

A special thanks to the entire team at Masterschool for providing the guidance in building this app.

## Contributing

I welcome any contributions! If you'd like to contribute to this project, please reach out to [email@edgroell.com](mailto:email@edgroell.com)