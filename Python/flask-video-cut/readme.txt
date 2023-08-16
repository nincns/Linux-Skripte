Of course, here's the `README.md` content presented as a code block:

```markdown
# Flask Video Cutter

Flask Video Cutter is a sophisticated video control and editing web application built on top of Flask. It allows users to control video playback, skip through videos, mark sections for cutting, and manage a collection of video files.

![Application Screenshot](https://github.com/nincns/Linux-Skripte/blob/main/Python/flask-video-cut/screenshots/Screenshot%202023-08-16%20at%2020.21.10.png)

## Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Features

- **Intuitive Video Playback Control:** Play, pause, and navigate with ease.
- **Cutting Mechanism:** Define start and end cut points for video sections.
- **Video Management System:** Easily add, select, or remove videos from the library.
- **Responsive Design:** Built with Bootstrap for a seamless experience across devices.

## System Requirements

- [Python](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- Web browser compatible with ES6 (e.g., Chrome, Firefox)
- [jQuery](https://jquery.com/download/)
- [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/download/)

## Installation & Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/nincns/Linux-Skripte.git
   cd Linux-Skripte/Python/flask-video-cut
   ```

2. **Set Up a Virtual Environment (Recommended)**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Required Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   If a `requirements.txt` isn't provided, at least ensure Flask is installed:

   ```bash
   pip install Flask
   ```

4. **Start the Flask Application:**

   ```bash
   flask run
   ```

   Access the application via `http://0.0.0.0:5000/`.

## Usage

1. **Control Video Playback:** Utilize the provided buttons to control the video's playback.
2. **Segmentation:** Select the "Open Cut Mark" to mark the beginning of a segment and "Close Cut Mark" to define its endpoint.
3. **Video Library:** Use the "Manage Videos" option to include new videos, delete existing ones, or select a video to play.

## Contributing

Contributions are always welcome! Please read the [CONTRIBUTING.md](path_to_contributing.md) *(if you have one)* for guidelines on how to proceed. Create issues for any new feature or bug fixes you'd like to see. For major changes, ensure to open an issue first to discuss the intended change.

## Acknowledgements

Thank those who contributed to the project or inspired its creation.

## License

[MIT License](https://choosealicense.com/licenses/mit/)
```

You can copy the above code block and place it in your repository's `README.md` file. Adjust any placeholders or sections as necessary for your project's specifics.
