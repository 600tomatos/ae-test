# Simple search API with cache


### Prerequisites

To run app on your local machine, make sure the you have installed the following software:
* [Docker](https://docs.docker.com/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)

### Usage

Start app

`cd <project_dir>`

`docker-compose up`

The API is available on port 8000. 

You should wait a little bit (depends on inet speed and PC performance) until the cache fills up (you'll see the log message).

You can use Postman, `curl` in your terminal or any other HTTP client to test `search` endpoint
Example:
`curl localhost:8000/search/Canon`

### Description
##### Technologies:
- Flask: API
- Celery (beat mode): periodic tasks
- Redis: cache storage and broker for celery-beat.

##### Search Response

The API returns list of image objects. Fields are: 
- 'id' and 'cropped_picture': in any case;
- 'tags', 'file_name', 'author', 'camera': if there is a match. 

### Known issues
- If the "schedule" time of the "reload_cache" task is less than the execution time of this task, the tasks will accumulate in the execution stack

### Disclaimer

This app describes only the simple process of caching data from external API and searching data using this cache.
Some cases wasn't handled such as:
- merging several matching tags for one image in API response (if such matching occurred);
- controlling performance in case of large amount of data (hundreds of millions records) in cache
- sensitive data encryption/hiding
- running services as root
etc

In addition:
- only basic API error handling are implemented (by means of logs)
