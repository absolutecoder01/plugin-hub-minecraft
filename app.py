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
def edit_plugin(plugin_id):
    if request.method == "GET":
        found_plugin = None
        for plugin in plugins:
            found_plugin = plugin
            if plugin.id == plugin_id:
                return render_template("edit_plugin.html", plugin=found_plugin)
                break

    elif request.method == "POST":
        new_plugin_name = request.form.get("plugin_name")
        new_plugin_description = request.form.get("plugin_description")
        for plugin in plugins:
            if plugin.id == plugin_id:
                plugin.editPlugin(new_plugin_name, new_plugin_description)
                return redirect("/")
                break

    return render_template("edit_plugin.html", plugin=plugin)


@app.route("/delete/<int:plugin_id>", methods=["GET"])
def delete_plugin(plugin_id):
    if request.method == "GET":
        for plugin in plugins:
            if plugin.id == plugin_id:
                plugins.remove(plugin)
                return redirect("/")
                break


# Should be enabled when fixing bugs
if __name__ == "__main__":
    app.debug = True
    app.run()
