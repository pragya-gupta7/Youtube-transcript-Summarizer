import re

def extract_video_id(youtube_url):
    try:
        # Extract the video ID from the YouTube URL
        video_id = None

        # Try to match common YouTube URL formats
        match = re.match(r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=|embed\/|v\/|)([^#\&\?]+)", youtube_url)

        if match:
            video_id = match.group(1)

        return video_id
    except Exception as e:
        return None


from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)

# Load the T5 model and tokenizer
model_name = "t5-small"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

@app.route('/api/summarize', methods=['GET'])
def summarize_from_url():
    try:
        # Extract the YouTube URL from query params
        youtube_url = request.args.get('youtube_url')

        if not youtube_url:
            return jsonify({'error': 'Please provide a valid YouTube URL as a query parameter.'}), 400

        # Extract the video ID from the YouTube URL
        video_id = extract_video_id(youtube_url)

        if not video_id:
            return jsonify({'error': 'Invalid YouTube URL. Please provide a valid YouTube video URL.'}), 400

        # Fetch the transcript for the YouTube video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Concatenate the text of all transcript segments into a single string
        full_transcript = ' '.join([segment['text'] for segment in transcript])
        print(full_transcript)

        # Define the T5-specific prefix for summarization
        prefix = "summarize: "

        # Combine the prefix and transcript for summarization
        input_text = prefix + full_transcript

        # Tokenize and generate the summary
        input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=len(full_transcript), truncation=True)
        summary_ids = model.generate(input_ids, max_length=len(full_transcript)//4, min_length=40, length_penalty=1.0, num_beams=4, early_stopping=False)
        summarized_transcript = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summarized_transcript

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)