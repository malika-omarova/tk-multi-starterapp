import sgtk
import os
import maya.cmds as cmds
import tempfile
import shutil
import traceback


# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.preview_geometry import Ui_Preview_Geometry

# standard toolkit logger
logger = sgtk.platform.get_logger(__name__)


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    app_instance.engine.show_dialog("Prveiew Geometry", app_instance, AppDialog)

class AppDialog(QtGui.QWidget):
    """
    Plugin to preview FBX files in the Unreal Engine
    """

    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)

        # now load in the UI that was created in the UI designer
        self.ui = Ui_Preview_Geometry()
        self.ui.setupUi(self)

        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()

        # logging happens via a standard toolkit logger
        logger.info("Launching Preview Geometry Application...")

        # creates temporary directory variable to use later
        self.temp_dir_path = self.create_temp_dir()
        # variable to store the file name of Maya mesh
        self.imported_file_name = ""
        # destination path in Unreal, can be changed based on artists' preferences 
        self.destination_path = "/Game/"

        # set up basic UI
        self.ui.update_btn.pressed.connect(self.update_mesh)
        self.ui.finalize_btn.pressed.connect(self.finaliaze_mesh)

    def create_temp_dir(self):
        """
        Creates temporary directory to store fbx file in
        :returns str:

        """
        temp_dir = tempfile.mkdtemp()
        print(temp_dir)
        return temp_dir

    def update_mesh(self):
        """
        Exports selected Maya mesh in FBX format to a temporary directory
        The mesh is then imported to Unreal Engine's /Game/ folder 
        Maya re-exports mesh and Unreal Engine reimports it every time
        Update button is pressed

        """
        # extract export name from Maya's file
        temp_dir = self.temp_dir_path

        filepath = cmds.file(q=True, sn=True)

        file_name_extension = os.path.basename(filepath)
        file_name_extension = file_name_extension.split(".")

        file_just_name = file_name_extension[0]
        file_name = file_just_name + "_temp.fbx"
        self.imported_file_name = file_just_name + "_temp"

        fbx_file_path = os.path.join(temp_dir, file_name)

        # get name of a selected object
        selected_object = cmds.ls(selection=True)[0]

        # check if objects are selected
        if selected_object:
            try:
                # export selected object to the specified file path
                cmds.file(fbx_file_path, force=True, options="v=0", type='FBX export', pr=True, es=True)
            except Exception as e:
                print("Export failed")
        
        file_path = os.path.normpath(fbx_file_path).replace(os.sep, "//")

        # code below is based on tk-remote-server
        # get the remote app
        remote = sgtk.platform.current_engine().apps['tk-remote-server']
        
        # find a port for a running engine instance by name
        target_port = remote.get_node_from_server("tk-unreal")

        # provide the payload
        # supply a dict with the key "exec" and a list of commands to run

        # import mesh to unreal
        commands = ["import unreal", 
        "task = unreal.AssetImportTask()",
        "task.filename =" + "'" + file_path + "'",
        "task.destination_path =" "'" + self.destination_path + "'",
        "task.destination_name =" "'" + file_just_name+ "'" + "'_temp'" ,
        "task.replace_existing = True",
        "task.automated = True",
        "asset_tools = unreal.AssetToolsHelpers.get_asset_tools()",
        "asset_tools.import_asset_tasks([task])"]

        payload = {"exec": commands}

        # send the payload to the target with return
        res = remote.send_message_to_server(target_port, payload, ret=True)

        # print return payload
        print(res)

        if res['success']:
            # print the return data from command
            print(res['results'][1])
        else:
            # raise an exception from the exception on the remote server
            raise Exception(res['error'])

    def finaliaze_mesh(self):
        """
        Deletes imported mesh's Static Mesh Actor, Static Mesh 
        and the material in Unreal Engine. Deletes temporary directory
        with the mesh and closes app's UI

        """
        asset_path = self.destination_path + self.imported_file_name

        # code below is based on tk-remote-server
        # get the remote app
        remote = sgtk.platform.current_engine().apps['tk-remote-server']

        # find a port for a running engine instance by name
        target_port = remote.get_node_from_server("tk-unreal")

        # provide the payload
        # supply a dict with the key "exec" and a list of commands to run

        #delete actor, static mesh and the material in unreal
        commands = ["import unreal", 
        "unrealSystem=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)",
        "actorsList = unrealSystem.get_all_level_actors()\n",
        "for actor in actorsList:\n"
        "    actorLabel = actor.get_actor_label()\n"
        "    actorPos = actor.get_actor_location()\n"
        "    if (actorLabel == " + "'" + self.imported_file_name + "'" + "):\n"
        "        unrealSystem.destroy_actor(actor)\n", 
        "paths = []",
        "editor_lib = unreal.EditorAssetLibrary()",
        "staticmesh_path = " + "'" + asset_path + "'",
        "asset = editor_lib.load_asset(staticmesh_path)",
        "paths.append(staticmesh_path)",
        "for material_index in range(0, asset.get_num_sections(0)):\n"
        "   material_path = asset.get_material(material_index).get_path_name()\n"
        "   paths.append(material_path)" + "\n" + "for i in paths:" + "    editor_lib.delete_asset(i)",
        "print(paths)"
        ]

        for i in commands:
            try:
                # perform exec of statements that define variables
                whitelist = ["import", "="]
                if any(substring in i for substring in whitelist):
                    exec(i, globals())
                    res = None
                else:
                    res = eval(i, globals())
        
            except (Exception,):
                # break the loop here, if we are running multiple lines of code,
                # all lines should pass successfully
                traceback.format_exc()
                break


        payload = {"exec": commands}

        # send the payload to the target with return
        res = remote.send_message_to_server(target_port, payload, ret=True)

        # print return payload
        print(res)

        if res['success']:
            # print the return data from command
            print(res['results'][1])
        else:
            # raise an exception from the exception on the remote server
            raise Exception(res['error'])

        # get temporary directory path and delete it
        temp_dir = self.temp_dir_path
        shutil.rmtree(temp_dir)
        
        # close UI if Finalize button is pressed
        self.close()