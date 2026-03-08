import os
import shutil
import unicodedata

from flask import Flask, redirect, render_template, request
from sqlalchemy import select
from werkzeug.utils import secure_filename

from plugin import Plugin, db

UPLOAD_FOLDER = "static/uploads/plugins"
ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "jar",
    "java",
    "txt",
    "zip",
    "rar",
    "webp",
}
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
db.init_app(app)


def list_plugins():
    statement = select(Plugin).order_by(Plugin.name)
    row = db.session.execute(statement).scalars().all()
    return row


def load_plugin(plugin_id):
    return db.session.get(Plugin, plugin_id)


def remove_plugin(plugin_id):
    Plugin.query.filter_by(id=plugin_id).delete()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_name(name):
    name = unicodedata.normalize("NFKD", name)
    name = name.replace(" ", "-")
    cleaned_name = ""
    for char in name:
        if char.isalnum() or char == "-":
            cleaned_name += char
        else:
            continue
    cleaned_name = cleaned_name.lower()
    return cleaned_name


@app.route("/")
def home():
    return render_template("home.html", plugins=list_plugins())


@app.route("/add_plugin", methods=["GET", "POST"])
def add_plugin():
    if request.method == "POST":
        if "plugin_file" not in request.files:
            return redirect(request.url)

        plugin_name = request.form.get("plugin_name")
        plugin_description = request.form.get("plugin_description")
        plugin_file = request.files.get("plugin_file")
        plugin_image = request.files.get("plugin_image")
        saved_filename_plugin_file = ""
        saved_filename_plugin_image = ""
        if plugin_file and allowed_file(plugin_file.filename):
            filename = secure_filename(plugin_file.filename)
            saved_filename_plugin_file = filename
        if plugin_image and allowed_file(plugin_image.filename):
            filename = secure_filename(plugin_image.filename)
            saved_filename_plugin_image = filename
        new_plugin = Plugin(
            name=plugin_name,
            description=plugin_description,
            file_filename=saved_filename_plugin_file,
            image_filename=saved_filename_plugin_image,
        )
        db.session.add(new_plugin)
        db.session.commit()
        # Creating plugin folder using ID from database
        upload_path = str(new_plugin.id) + "-" + allowed_name(new_plugin.name)
        if not os.path.exists(os.path.join(UPLOAD_FOLDER, upload_path)):
            os.makedirs(os.path.join(UPLOAD_FOLDER, upload_path))
        if plugin_file:
            plugin_file.save(
                os.path.join(UPLOAD_FOLDER, upload_path, saved_filename_plugin_file)
            )

        if plugin_image:
            plugin_image.save(
                os.path.join(UPLOAD_FOLDER, upload_path, saved_filename_plugin_image),
            )
        full_path_file = os.path.join(
            UPLOAD_FOLDER, upload_path, saved_filename_plugin_file
        )
        full_path_image = os.path.join(
            UPLOAD_FOLDER, upload_path, saved_filename_plugin_image
        )
        new_plugin.file_filename = full_path_file
        new_plugin.image_filename = full_path_image
        db.session.commit()
        return redirect("/")
    elif request.method == "GET":
        return render_template("add_plugin.html")


@app.route("/edit_plugin/<int:plugin_id>", methods=["GET", "POST"])
def edit_plugin(plugin_id):
    plugin = load_plugin(plugin_id)
    if request.method == "GET":
        if plugin is None:
            print("Nie znaleziono takiego pluginu!")
            return render_template("home.html", plugins=list_plugins())
        if plugin.id == plugin_id:
            return render_template("edit_plugin.html", plugin=plugin)

    elif request.method == "POST":
        if plugin:
            new_plugin_name = request.form.get("plugin_name")
            new_plugin_description = request.form.get("plugin_description")
            new_plugin_file = request.files.get("plugin_file")
            new_plugin_image = request.files.get("plugin_image")
            old_path_file = plugin.file_filename
            old_path_image = plugin.image_filename
            if new_plugin_name:
                plugin.name = new_plugin_name
            if new_plugin_description:
                plugin.description = new_plugin_description
            if new_plugin_file and allowed_file(new_plugin_file.filename):
                filename = secure_filename(new_plugin_file.filename)
                if plugin.file_filename:
                    folder = os.path.dirname(plugin.file_filename)
                else:
                    upload_path = str(plugin.id) + "-" + allowed_name(plugin.name)
                    folder = os.path.join(UPLOAD_FOLDER, upload_path)
                os.makedirs(folder, exist_ok=True)
                new_plugin_file.save(os.path.join(folder, filename))
                if old_path_file and os.path.exists(old_path_file):
                    os.remove(old_path_file)
                full_path = os.path.join(folder, filename)
                plugin.file_filename = full_path

            if new_plugin_image and allowed_file(new_plugin_image.filename):
                filename = secure_filename(new_plugin_image.filename)
                if plugin.image_filename:
                    folder = os.path.dirname(plugin.image_filename)
                else:
                    upload_path = str(plugin.id) + "-" + allowed_name(plugin.name)
                    folder = os.path.join(UPLOAD_FOLDER, upload_path)

                os.makedirs(folder, exist_ok=True)
                new_plugin_image.save(os.path.join(folder, filename))

                if old_path_image and os.path.exists(old_path_image):
                    os.remove(old_path_image)

                full_path = os.path.join(folder, filename)
                plugin.image_filename = full_path
            db.session.commit()
            return redirect("/")
        else:
            # inform user about it, for later
            pass

    return render_template("edit_plugin.html", plugin=plugin)


@app.route("/delete/<int:plugin_id>", methods=["POST"])
def delete_plugin(plugin_id):
    plugin = load_plugin(plugin_id)
    if plugin:
        file_path_to_remove = plugin.file_filename
        image_path_to_remove = plugin.image_filename
        if file_path_to_remove:
            if os.path.exists(file_path_to_remove):
                try:
                    shutil.rmtree(os.path.dirname(file_path_to_remove))
                    image_path_to_remove = None
                except OSError as e:
                    print(f"Nie udało się usunąć folderu: {e}")

        if image_path_to_remove:
            if os.path.exists(image_path_to_remove):
                try:
                    shutil.rmtree(os.path.dirname(image_path_to_remove))
                except OSError as e:
                    print(f"Nie udało się usunąć folderu: {e}")
        remove_plugin(plugin_id)
        db.session.commit()
        return redirect("/")
    else:
        print("Nie znaleziono takiego pluginu!")
        return render_template("home.html", plugins=list_plugins())


# Should be enabled when fixing bugs
if __name__ == "__main__":
    app.debug = True
    with app.app_context():
        db.create_all()
    app.run()
