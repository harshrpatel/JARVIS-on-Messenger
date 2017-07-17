import requests
import requests_cache

from templates.button import *
import tmdbsimple as tmdb
import config


def datetoyear(date):
    return date.split('-')[0]


def process(input, entities):
    output = {}
    try:
        movie = entities['movie'][0]['value']
        tmdb.API_KEY = config.TMDB_API_KEY
        search = tmdb.Search()
        qs = search.movie(query=movie)

        # for movieset in search.results:
        #     print movieset['title']
        #     break
        #     print(movieset['title'], movieset['id'], movieset['release_date'], movieset['popularity'])

        with requests_cache.enabled('movie_cache', backend='sqlite', expire_after=86400):
            tmdb.API_KEY = config.TMDB_API_KEY
            search = tmdb.Search()
            qs = search.movie(query=movie)
            first_movie = qs['results'][0]
            # print first_movie['title']
            recommended_movies = qs['results'][1:16]
            rmovies = []
            for m in recommended_movies:
                rmovies.append("{0}/{1}".format(m['title'], datetoyear(m['release_date'])))
            import pprint
            pprint.pprint(rmovies)
        output['input'] = input
        # print "here", first_movie['title'], datetoyear(first_movie['release_date']), first_movie['popularity'], first_movie['overview']
        # template = TextTemplate("Helo")
        template = TextTemplate('Title: ' + first_movie['title'] + '\nYear: ' + datetoyear(first_movie['release_date'])
                                + '\nRating: ' + str(first_movie['popularity']) + ' / 10' + '\nPlot: ' +
                                first_movie['overview'])
        text = template.get_text()
        template = ButtonTemplate(text)
        # template.add_web_url('IMDb Link', 'http://www.imdb.com/title/' + data['imdbID'] + '/')
        output['output'] = template.get_message()
        output['success'] = True

    except:
        error_message = 'I couldn\'t find that movie.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - batman movie'
        error_message += '\n  - iron man 2 movie plot'
        error_message += '\n  - What is the rating of happyness movie?'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output
