#!/usr/bin/python3

"""
Review controler file
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def httpGetReviewsByPlaceID(place_id):
    """
    GET /api/v1/places/<place_id>/reviews
    Get all the reviews from a place, based on its ID
    If the ID do not match with any places, error 404 is
        raised
    Return: All reviews through json object
    """
    placeInstance = storage.get(Place, place_id)
    if placeInstance is None:
        abort(404)
    allReviews = []
    for reviews in placeInstance.reviews:
        allReviews.append(reviews.to_dict())
    return jsonify(allReviews), 200


@app_views.route('/reviews/<string:reviews_id>',
                 methods=['GET'],
                 strict_slashes=False)
def httpGetReviewsByID(reviews_id):
    """
    GET /api/v1/reviews/<reviews_id>
    Get a review based on given ID
    If the ID do not match with any reviews, error 404 is
        raised
    Return: The matched reviews through json object
    """
    reviewInstance = storage.get(Review, reviews_id)
    if reviewInstance is not None:
        return jsonify(reviewInstance.to_dict()), 200
    abort(404)


@app_views.route('/reviews/<string:review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def httpDeleteReviewByID(review_id):
    """
    DELETE /api/v1/reviews/<review_id>
    Delete a review based on given ID
    If the ID do not match with any review, error 404 is
        raised
    Return: A empty json object
    """
    reviewInstance = storage.get(Review, review_id)
    if reviewInstance is not None:
        storage.delete(reviewInstance)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def httpAddNewReview(place_id):
    """
    POST /api/v1/places/<place_id>/reviews
    Post a new review to the database, user_id text
        required
    Return: Return the new created review through json object
    """
    if storage.get(Place, place_id) is None:
        abort(404)
    dataFromRequest = request.get_json()
    if not dataFromRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in dataFromRequest:
        return jsonify({'error': 'Missing user_id'}), 400
    if storage.get(User, dataFromRequest['user_id']) is None:
        abort(404)
    if 'text' not in dataFromRequest:
        return jsonify({'error': 'Missing text'}), 400
    dataFromRequest['place_id'] = place_id
    newReview = Review(**dataFromRequest)
    newReview.save()
    return jsonify(newReview.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def httpModifyReviewByID(review_id):
    """
    PUT /api/v1/reviews/<review_id>
    Update a review based on given ID
    If the ID do not match with any review, error 404 is
        raised
    Return: The review through a json object
    """
    reviewInstance = storage.get(Review, review_id)
    if reviewInstance is None:
        abort(404)
    dataFromRequest = request.get_json()
    if not dataFromRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in dataFromRequest.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(reviewInstance, key, value)
    reviewInstance.save()
    return jsonify(reviewInstance.to_dict()), 200
