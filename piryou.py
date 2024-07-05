from flask import Flask, Response, request
import json
import os
import requests
import subprocess

file_path =  os.path.dirname(__file__)
valid_id = {}
metadata = "/results.json"
if os.path.exists(file_path + metadata):
    with open(file_path + metadata, "r") as file:
        try:
            valid_id = json.load(file)
        except json.JSONDecodeError as e:
            with open(file_path + metadata, "w") as file:
                json.dump({}, file)
else:
    with open(file_path + metadata, "w") as file:
        json.dump({}, file)


def gtandt(v):
    v = v
    global valid_id
    global file_path
    global metadata
    video_url = f"{v}"
    if valid_id.get(f"{v}"):
        return valid_id[v]
    try:
        result = subprocess.run(
            ["yt-dlp", "--get-title", "--get-thumbnail", video_url],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            output_lines = result.stdout.strip().split("\n")
            title = output_lines[0] if len(output_lines) > 0 else ""
            if v not in valid_id and title != "":
                valid_id[v] = title
                with open(file_path + metadata, "w") as file:
                    json.dump(valid_id, file)

            return valid_id[v]
        else:
            return "FF"
    except:
        return "FF"


app = Flask(__name__)


@app.route("/def.css")
def css():
    return """

body {
    font-family: Arial, sans-serif;
    background-color: #1a1a1a;
    color: #ccc;
    margin: 20px;
}

h1 {
    color: #fff;
}

video {
    width: 100%;
    max-width: 800px;
    display: block;
    margin: 20px auto;
    background-color: #333;
    border-radius: 5px;
}

hr {
    border-color: #666;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    display: inline-block;
    width: 400px;
    margin: 10px;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    overflow: hidden; 
    text-align: center;
}

img {
    width: 100px;
    height: auto;
    border-radius: 5px;
    float: left;
    margin-right: 10px;
}

p {
    margin: 0;
    color: #333;
    font-weight: bold;
    text-decoration: none; 
}
    """


@app.route("/thumbnail")
def thumbnail():
    global file_path
    vid = request.args.get("v", "").encode().hex().upper()
    if not os.path.exists(file_path + f"/{vid}.JPG"):

        video_url = f"{vid}"
        try:
            result = subprocess.run(
                ["yt-dlp", "--get-thumbnail", bytes.fromhex(video_url).decode()],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                thumbnail_url = result.stdout.strip()

                response = requests.get(thumbnail_url)

                if response.status_code == 200:
                    with open(file_path + f"/{vid}.JPG", "wb") as f:
                        f.write(response.content)
                    return Response(response.content, mimetype="image/jpeg")
                else:
                    return "FF"
            else:
                return "FF"
        except Exception as e:
            return "FF"
    else:
        with open(file_path + f"/{vid}.JPG", "rb") as f:
            return Response(f.read(), mimetype="image/jpeg")


@app.route("/video")
def video():
    global file_path
    vid = request.args.get("v", "").encode().hex().upper()
    if os.path.exists(file_path + f"/{vid}.MP4"):
        with open(file_path + f"/{vid}.MP4", "rb") as f:
            video_data = f.read()
        return Response(video_data, mimetype="video/mp4")
    youtube_url = f"{vid}"
    command = [
        "yt-dlp",
        bytes.fromhex(youtube_url).decode(),
        "-o",
        "-",
        "--sub-lang",
        "en",
        "-f",
        "best",
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        return "FF"
    with open(file_path + f"/{vid}.MP4", "wb") as f:
        f.write(stdout)
    return Response(stdout, mimetype="video/mp4")


@app.route("/watch")
def watch():
    vid = request.args.get("v", "")
    info = gtandt(vid)
    result = f"""
    <html>
    <head>
    <title>{info}</title>
    <link rel="stylesheet" href="/def.css">
    </head>
    <body>
    <a href="/"><h1>home</h1></a>
    <hr>
    <h1>{info}</h1>
    <hr>
    <video src="/video?v={vid}" controls></video>
    <hr>
    </body>
    </html>
    """
    return result


@app.route("/")
def index():
    global valid_id
    html_content = """
    <html>
    <head>
        <title>portable</title>
        <link rel="stylesheet" href="/def.css">
    </head>
    <body>
        <h1>portable videos</h1>
        <hr>
<form action="/watch" method="get">
<input type="text" name="v" required>
<input type="submit" value="search">
</form>
        <hr>
        <ul>
    """
    for video in valid_id:
        html_content += f"""
            <li>
            <a href="/watch?v={video}">
                <img src="/thumbnail?v={video}">
                <p>{valid_id[video]}</p>
            </a>
            </li>  
        """
    html_content += """
        </ul>
    </body>
    </html>
    """
    return html_content


app.run()
