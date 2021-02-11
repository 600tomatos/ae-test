from cache_loader import logger, image_attributes
from cache_loader.celery import app, PRIMARY_CACHE_DB, BUFFER_CACHE_DB
from cache_loader.api_client import get_image_details_by_id, get_images_by_page
from redis import Redis


@app.task()
def reload_cache():
    logger.info('Cache reloading Task started')
    with Redis(host='redis', db=BUFFER_CACHE_DB) as buffer_cache:
        images_feed_response = get_images_by_page().json()
        current_page = images_feed_response.get('page')
        page_count = images_feed_response.get('pageCount')

        _process_images_feed(images_feed_response.get('pictures'), buffer_cache)

        if images_feed_response.get('hasMore'):
            for page in range(current_page + 1, page_count + 1):
                _process_images_feed(get_images_by_page(page).json().get('pictures'), buffer_cache)

        buffer_cache.swapdb(PRIMARY_CACHE_DB, BUFFER_CACHE_DB)
        buffer_cache.flushdb()
    logger.info('Cache reloading task finished')


def _process_images_feed(feed, cache):
    image_ids = [image.get('id') for image in feed]
    images_details_list = [get_image_details_by_id(image_id).json() for image_id in image_ids]

    for image_details in images_details_list:
        _fill_cache_with_data(image_details, cache)


def _fill_cache_with_data(image_details, cache):
    image_data_to_store = f'{image_details.get("id")} {image_details.get("cropped_picture")}'
    for attribute in image_attributes.SINGLE_ITEM_ATTRIBUTES:
        if attribute_value := image_details.get(attribute):
            if attribute in image_attributes.URL_ATTRIBUTES:
                attribute_value = attribute_value.split('/')[-1]
                cache.sadd(f'file_name:{attribute_value}', image_data_to_store)
            else:
                cache.sadd(f'{attribute}:{attribute_value}', image_data_to_store)
    for attribute in image_attributes.MULTI_ITEM_ATTRIBUTES:
        if attribute_values := image_details.get(attribute):
            for attribute_value in attribute_values.strip().split(' '):
                cache.sadd(f'{attribute}:{attribute_value}', image_data_to_store)


# launch task manually in order not to wait beat 'init timeout'. Can be removed (but there will be init timeout 5 mins)
reload_cache.delay()

