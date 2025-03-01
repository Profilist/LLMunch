from flask import Blueprint, request, jsonify
from services.agent import YoutubeService
import asyncio

api_bp = Blueprint('api', __name__)
youtube_service = YoutubeService()

@api_bp.route('/play-video', methods=['POST'])
async def play_video():
    data = request.get_json()
    video_type = data.get('video_type')
    
    if not video_type:
        return jsonify({
            "error": "No video type provided"
        }), 400
    
    try:
        result = await youtube_service.play_video(video_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# Cleanup when the application shuts down
@api_bp.teardown_app_request
async def cleanup(exception=None):
    await youtube_service.close_browser() 