from flask import Flask, redirect, render_template, request

from plugin import Plugin

app = Flask(__name__)


plugins = [
    Plugin("Plugin1", "Description of plugin1"),
    Plugin("Plugin2", "Description of plugin2"),
    Plugin("Plugin3", "Description of plugin3"),
    Plugin("Plugin4", "Description of plugin4"),
]


@app.route("/")
def home():
    return render_template("home.html", plugins=plugins)


@app.route("/add_plugin", methods=["GET", "POST"])
def add_plugin():
    if request.method == "POST":
        plugin_name = request.form.get("plugin_name")
        plugin_description = request.form.get("plugin_description")
        plugins.append(Plugin(plugin_name, plugin_description))
        return redirect("/")
    elif request.method == "GET":
        return render_template("add_plugin.html", plugins=plugins)


@app.route("/edit_plugin/<int:plugin_id>", methods=["GET", "POST"])
def edit_plugin():
    if request.method == "POST":
        new_plugin_name = request.form.get("new_plugin_name")
        new_plugin_description = request.form.get("new_plugin_description")
        # TODO: Editing plugin data within code, find a way to identify which plugin it is and set new data using plugin.editPlugn(newName, newDescription), in Plugin class already desclared an id.

    return render_template("edit_plugin.html", plugin=plugin)


# Should be enabled when fixing bugs
if __name__ == "__main__":
    app.debug = True
    app.run()
