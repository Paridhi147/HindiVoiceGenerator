from flask import Flask, render_template, request, send_file
import edge_tts
import os
import uuid
import asyncio

app = Flask(__name__)

# Create audio folder if it doesn't exist
AUDIO_FOLDER = "static/audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Different speech styles
VOICE_MAP = {
    "female": "hi-IN-SwaraNeural",
    "male": "hi-IN-MadhurNeural",
    "podcast": "en-US-AndrewMultilingualNeural",
    "assistant": "en-US-EmmaMultilingualNeural"
}


# Generate speech
async def generate_voice(text, filepath, voice):

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate="-5%",
        volume="+10%"
    )

    await communicate.save(filepath)


@app.route("/", methods=["GET", "POST"])
def home():

    audio_file = None

    if request.method == "POST":

        text = request.form["message"]
        voice_choice = request.form["voice"]

        voice = VOICE_MAP.get(
            voice_choice,
            "hi-IN-SwaraNeural"
        )

        filename = f"{uuid.uuid4()}.mp3"

        filepath = os.path.join(
            AUDIO_FOLDER,
            filename
        )

        asyncio.run(
            generate_voice(
                text,
                filepath,
                voice
            )
        )

        audio_file = filename

    return render_template(
        "index.html",
        audio_file=audio_file
    )


@app.route("/download/<filename>")
def download(filename):

    filepath = os.path.join(
        AUDIO_FOLDER,
        filename
    )

    return send_file(
        filepath,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)