# One a Day

*Photoblogging like it's 1996*

This quick and dirty static site for hosting [this "one picture a day" project](https://jpreardon.com/oad/). I know, far from original.

No databases, no javascript, no frameworks. Just some very, very basic code.

I used Chat GPT as a starting point for the python code. I'll leave it to the reader to judge whether what it created is better or worse than what I would have done with my normal, trial & error workflow.

## Usage

1. Create a publicly accessible location on a web server and copy the contents of this repository to it.
2. Change the name of data-example.json in the images directory to data.json.
3. Add images (side expects a thumbnail for the index page and a full size image) to the images directory. The file name of the full size image will be used for the HTML page name.
4. Run the generator, it requires three arguments: the public URL of the site, the full (local) path to the directory where the HTML files are located, and "True" if all files are to be re-written, "False" if not. Usually "False" is the right call here.