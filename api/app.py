from flask import Flask, jsonify
from redis import Redis
from cache_loader.celery import PRIMARY_CACHE_DB

app = Flask(__name__)


@app.route('/search/<string:search_term>', methods=['GET'])
def search_images(search_term):
    with Redis(host='redis', db=PRIMARY_CACHE_DB) as cache:
        matching_attributes = cache.keys(f'*:*{search_term}*')
        image_ids = []
        matching_images_collection = []
        for matching_attribute in matching_attributes:
            # matching_attribute example: "author:Nervous Respond"
            attribute_name, attribute_value = matching_attribute.decode("utf-8").split(':')
            for images_by_attribute_value in cache.smembers(matching_attribute):
                # images_by_attribute_value example: "89881d4094f33673796a http://interview...pictures/cropped/53.jpg""
                image_id, url = images_by_attribute_value.decode("utf-8") .split(' ')[:2]
                if image_id not in image_ids:
                    image_ids.append(image_id)
                    matching_images_collection.append({
                        'id': image_id,
                        'cropped_picture': url,
                        attribute_name: attribute_value
                    })
                else:
                    for matching_image in matching_images_collection:
                        if matching_image.get('id') == image_id:
                            matching_image.update({attribute_name: attribute_value})

        return jsonify(images=matching_images_collection)
