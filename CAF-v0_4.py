bl_info = {  
 "name": "CAF - Collect All Files",  
 "author": "Samy Tichadou (tonton), RUben Begalov@gmail.com",  
 "version": (0, 3),  
 "blender": (2, 80, 0),  
 "location": "Import-Export > Collect All Files",  
 "description": "Add a Menu in the Info/File header to Collect your external files, copy them in a dedicated folder near the .blend, and relink the datablocks",  
 "warning": "Some Type of proprietary files can cause errors. Doesn't work with an unsaved .blend, it is strongly recommanded to Save As before using. Still experimental.",
 "wiki_url": "https://github.com/samytichadou/CAF-collect-all-file-addon",  
 "tracker_url": "https://github.com/samytichadou/CAF-collect-all-file-addon/issues/new",  
 "category": "Import-Export"}  

import bpy
import os
import shutil
import datetime

today = datetime.date.today()
dt = datetime.datetime.today()

###################################################

# Op1 Tous les fichiers #

###################################################
def get_path(context):
    path = bpy.context.blend_data.filepath
    return os.path.dirname(path)

def is_image(obj):
    return obj.type == 'IMAGE'

def getimages(context):
    # Make all paths absolute
    bpy.ops.file.make_paths_absolute()

    # Get the path of the blend file
    blend_path = get_path(context)

    # Define the path to the resources directory
    resources_folder = os.path.join(blend_path, "blends_ressources")

    # Define the type of datablocks to collect
    images = bpy.data.images

    # Create the resources directory if it doesn't exist
    os.makedirs(resources_folder, exist_ok=True)

    # Create a file to log the operation
    file = open(os.path.join(resources_folder, "report.txt"), "w")
    file.write("Collect Files Operation Report\n\n\n")
    file.write("Operation starts : " + str(datetime.datetime.now()) + "\n\n")

    # Collect and link images
    for obj in images:
        if is_image(obj):
            folder = os.path.join(resources_folder, "Images")
            new_path = os.path.join(folder, os.path.basename(obj.filepath))

            if obj.filepath == new_path:
                file.write("    The image " + obj.name + " is already linked.\n")
                print(obj.name + " - IMAGE ALREADY LINKED")

            elif os.path.exists(new_path):
                obj.filepath = new_path
                file.write("    The image " + obj.name + " is linked to " + os.path.basename(obj.filepath) + "\n")
                print(obj.name + " - IMAGE LINKED")

            else:
                file.write("    Copying image " + obj.name + " to " + os.path.basename(obj.filepath) + ".\n")
                shutil.copy2(os.path.abspath(obj.filepath), folder)
                obj.filepath = new_path
                print(obj.name + " - IMAGE COPIED")

    # Close the log file
    file.write("\n\n\n\n\nOperation ends : " + str(datetime.datetime.now()) + "\n\n")
    file.close()

    print("\nFiles Copied and Relinked\nCheck associated _Ressources folder for files and report\n")
    print("---Warning---")
    print("Path of the Copied Files are Absolute")
def getthemall (context):

    ### rendre tous les chemins absolus ###
    bpy.ops.file.make_paths_absolute()

    ### définir chemin et nom du fichier blend ###
    blendossier=bpy.path.abspath("//")
    Oblendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    Oblendnom=os.path.splitext(Oblendnom2)[0]

    blendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    blendnom=os.path.splitext(blendnom2)[0]

    ### définir chemin folder ressources ###
    ressourcesfolder=blendossier + "/" + "blends_ressources"

    ### définir types de datablocks à récupérer ###
    image = bpy.data.images
    clip = bpy.data.movieclips
    lib = bpy.data.libraries
    font = bpy.data.fonts

    ### créer compte rendu ###
    os.makedirs(ressourcesfolder, exist_ok=True)
    file = open(ressourcesfolder + "//" + blendnom + "_allfiles_" + "_" + str(today) + "_report.txt", "w")
    file.write("Collect Files Operation Report\n\n\n")
    file.write("Operation starts : " + str(dt) + "\n\n")

    ### Strips ###

    file.write("\nSequencer Strips :\n\n")

    for scene in bpy.data.scenes: 
        
        if scene.sequence_editor is not None:
            
            strip = scene.sequence_editor.sequences_all
            
            if strip is not None:
                
                           
                for obj in strip:
                    
                    if obj.type == 'MOVIE' :
                        
                        folder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)
                        sfolder = folder + "/" +  "Video Strips"
                        newpath=sfolder + "/" + bpy.path.basename(obj.filepath)
                        
                        if os.path.exists(newpath) == True :
                            
                            if obj.filepath == newpath:
                                file.write("    VIDEO STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                                print(bpy.path.basename(obj.filepath) + " already copied/linked - VIDEO STRIP IGNORED")
                                
                            else :
                                obj.filepath=newpath
                                file.write("    VIDEO STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                print(bpy.path.basename(obj.filepath) + " - VIDEO STRIP LINKED")

                        else:
                            os.makedirs(ressourcesfolder, exist_ok=True)
                            os.makedirs(sfolder, exist_ok=True)
                            print(bpy.path.basename(obj.filepath) + " - VIDEO STRIP COPYING...")
                            shutil.copy2(bpy.path.abspath(obj.filepath), newpath) 
                            obj.filepath=newpath
                            file.write("    VIDEO STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                            print(bpy.path.basename(obj.filepath) + " - VIDEO STRIP COPIED")

                    ### Problème avec image fixe à régler ###    
                    elif obj.type == 'IMAGE':

                        folder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)
                        sfolder = folder + "/" + "Images Strips" + "/"
                        ISfolder = folder + "/" + "Image Sequence Strips"
                        Inewpath=sfolder + obj.elements[0].filename
                        ISnewpath=ISfolder + "/" + os.path.splitext(obj.elements[0].filename)[0] + "/"
                        
                        if obj.frame_duration == 1 :

                            if obj.directory == sfolder :
                                
                                file.write("    IMAGE STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                                print(obj.elements[0].filename + " already copied/linked - IMAGE STRIP IGNORED")

                            else:
                                if os.path.exists(Inewpath) == True :
                                
                                    obj.directory=sfolder
                                    file.write("    IMAGE STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " - IMAGE STRIP LINKED")

                                else :
                                    os.makedirs(ressourcesfolder, exist_ok=True)
                                    os.makedirs(sfolder, exist_ok=True)
                                    print(obj.elements[0].filename + " - IMAGE STRIP COPYING...")
                                    shutil.copy2(bpy.path.abspath(obj.directory) + "/" + obj.name, Inewpath)
                                    obj.directory=sfolder
                                    file.write("    IMAGE STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " - IMAGE STRIP COPIED")

                        else :
                            if obj.directory == ISnewpath :
                                
                                file.write("    IMAGE SEQUENCE STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                                print(obj.elements[0].filename + " sequence already copied/linked - IMAGE SEQUENCE STRIP IGNORED")
                            
                            else:
                                if os.path.exists(ISnewpath) == True :
                                
                                    obj.directory=ISnewpath
                                    file.write("    IMAGE SEQUENCE STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " sequence - IMAGE SEQUENCE STRIP LINKED")
                                
                                else :
                                    os.makedirs(ressourcesfolder, exist_ok=True)
                                    os.makedirs(ISfolder, exist_ok=True)
                                    print(obj.elements[0].filename + " sequence - IMAGE SEQUENCE STRIP COPYING")
                                    shutil.copytree(bpy.path.abspath(obj.directory), ISnewpath)
                                    obj.directory=ISnewpath
                                    file.write("    IMAGE SEQUENCE STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " sequaence - IMAGE SEQUENCE STRIP COPIED")

                    elif obj.type == 'SOUND':
                        
                        vfolder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)
                        vsfolder = vfolder + "/" +  "Video Strips"
                        vnewpath=vsfolder + "/" + bpy.path.basename(obj.sound.filepath)
                        
                        folder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)    
                        sfolder = folder + "/" +  "Sounds Strips"
                        newpath=sfolder + "/" + bpy.path.basename(obj.sound.filepath)
                        
                        if os.path.isfile(vnewpath) == True :
                            
                            if obj.sound.filepath==vnewpath :
                                file.write("    SOUND STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.sound.filepath) + "\n")
                                print(bpy.path.basename(obj.sound.filepath) + " already copied/linked - SOUND IGNORED")
                                
                            else :
                                obj.sound.filepath=vnewpath
                                file.write("    SOUND STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.sound.filepath) + "\n")
                                print(bpy.path.basename(obj.sound.filepath) + " - SOUND LINKED")
                                
                        else :
                            if os.path.isfile(newpath) == True :
                                
                                if obj.sound.filepath==newpath :
                                    file.write("    SOUND STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.sound.filepath) + "\n")
                                    print(bpy.path.basename(obj.sound.filepath) + " already copied/linked - SOUND IGNORED")
                                
                                else:
                                    
                                    obj.sound.filepath=newpath
                                    file.write("    SOUND STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.sound.filepath) + "\n")
                                    print(bpy.path.basename(obj.sound.filepath) + " - SOUND LINKED")
                                    
                            else:
                                os.makedirs(ressourcesfolder, exist_ok=True)
                                os.makedirs(sfolder, exist_ok=True)   
                                print(bpy.path.basename(obj.sound.filepath) + " - SOUND COPYING...")                 
                                shutil.copy2(bpy.path.abspath(obj.sound.filepath), newpath) 
                                obj.sound.filepath=newpath
                                file.write("    SOUND STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.sound.filepath) + "\n")
                                print(bpy.path.basename(obj.sound.filepath) + " - SOUND COPIED")

    ### Images ###

    file.write("\nImages :\n\n")

    for obj in image:
        
        if obj is not None:
            
            ### folder à créer en fonction du type ###
            folder=ressourcesfolder + "/" + "Images"        
            newpath=folder + "/" + bpy.path.basename(obj.filepath)
            
            if obj.filepath == '' :
                
                print("WARNING " + obj.name + " is not an external file - IMAGE IGNORED")
                file.write("    IMAGE IGNORED : " + obj.name + " is not an external file\n")
                
            else :
                if obj.filepath == newpath:
                    
                    file.write("    IMAGE IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " already copied/linked - IMAGE IGNORED")
                    
                elif os.path.exists(newpath) == True :
                    
                    obj.filepath=newpath
                    file.write("    IMAGE LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " - IMAGE LINKED")

                else:
                    os.makedirs(ressourcesfolder, exist_ok=True)
                    os.makedirs(folder, exist_ok=True)
                    print(bpy.path.basename(obj.filepath) + " - IMAGE COPYING...")
                    shutil.copy2(bpy.path.abspath(obj.filepath), folder + "/" + bpy.path.basename(obj.filepath)) 
                    ### relink fichier ###

                    obj.filepath=newpath
                    file.write("    IMAGE COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " - IMAGE COPIED")


    ### Movie Clips ###

    file.write("\nMovie Clips :\n\n")

    for obj in clip:
        
        if obj is not None:

            ### folder à créer en fonction du type ###
            folder=ressourcesfolder + "/" + "Movie Clips"        
            newpath=folder + "/" + bpy.path.basename(obj.filepath)
            Snewpath=folder + "/" + os.path.splitext(bpy.path.basename(obj.filepath))[0] + "/"
            Sfpath=Snewpath + bpy.path.basename(obj.filepath)
            
            ab=bpy.path.abspath(obj.filepath)
            path = os.path.normpath(ab)
            parts = path.split(os.sep)

            parentpath = os.sep.join(parts[:-1])
            
            
            if obj.filepath == newpath:
                
                file.write("    MOVIE CLIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                print(bpy.path.basename(obj.filepath) + " already copied/linked - VIDEO IGNORED")
                
            elif obj.filepath == Sfpath :
                
                file.write("    IMAGE SEQUENCE IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                print(bpy.path.basename(obj.filepath) + " sequence already copied/linked - IMAGE SEQUENCE IGNORED")

            else:
                if obj.source == 'SEQUENCE' :
                    if os.path.exists(Snewpath) == True :
                        obj.filepath=Sfpath
                        file.write("    IMAGE SEQUENCE LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                        print(bpy.path.basename(obj.filepath) + " sequence - IMAGE SEQUENCE LINKED")

                    else :
                        os.makedirs(ressourcesfolder, exist_ok=True)
                        os.makedirs(folder, exist_ok=True)
                        print(bpy.path.basename(obj.filepath) + " sequence - IMAGE SEQUENCE COPYING...")
                        shutil.copytree(parentpath, Snewpath)
                        obj.filepath=Sfpath
                        file.write("    IMAGE SEQUENCE COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                        print(bpy.path.basename(obj.filepath) + " sequence - IMAGE SEQUENCE COPIED")

                else :
                    os.makedirs(ressourcesfolder, exist_ok=True)
                    os.makedirs(folder, exist_ok=True)
                    print(bpy.path.basename(obj.filepath) + " - VIDEO COPYING...")
                    shutil.copy2(bpy.path.abspath(obj.filepath), folder + "/" + bpy.path.basename(obj.filepath)) 
                    ### relink fichier ###

                    obj.filepath=newpath
                    file.write("    MOVIE CLIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " - VIDEO COPIED")


    ### Libraries ###

    file.write("\nBlend Libraries :\n\n")

    for obj in lib:
        
        if obj is not None:
            
            ### folder à créer en fonction du type ###
            folder=ressourcesfolder + "/" + "Blend Libraries"
            newpath=folder + "/" + bpy.path.basename(obj.filepath)
            
            if obj.filepath == newpath:
                file.write("    BLEND LIBRARY IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                print(bpy.path.basename(obj.filepath) + " already copied/linked - LIBRARY IGNORED")
                
            elif os.path.exists(newpath) == True : 
                
                obj.filepath=newpath
                file.write("    BLEND LIBRARY LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                print(bpy.path.basename(obj.filepath) + " - LIBRARY LINKED")
                
            else:
                
                os.makedirs(ressourcesfolder, exist_ok=True)
                os.makedirs(folder, exist_ok=True)
                print(bpy.path.basename(obj.filepath) + " - LIBRARY COPYING...")
                shutil.copy2(bpy.path.abspath(obj.filepath), folder + "/" + bpy.path.basename(obj.filepath)) 
                ### relink fichier ###

                obj.filepath=newpath
                file.write("    BLEND LIBRARY COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                print(bpy.path.basename(obj.filepath) + " - LIBRARY COPIED")
                
                
    ### Fonts ###

    file.write("\nFonts :\n\n")

    for obj in font:
        if obj is not None:
            ### folder à créer en fonction du type ###
            folder=ressourcesfolder + "/" + "Fonts"        
            newpath=folder + "/" + bpy.path.basename(obj.filepath)
            
            if obj.filepath == '' :
                
                print("WARNING " + obj.name + " is not an external file - FONT IGNORED")
                file.write("    FONT IGNORED : " + obj.name + " is not an external file\n")
                
            elif obj.filepath == '<builtin>' :
                
                print("WARNING " + obj.name + " is not an external file - FONT IGNORED")
                file.write("    FONT IGNORED : " + obj.name + " is not an external file\n")
                
            else :
            
                if obj.filepath == newpath:
                    
                    file.write("    FONT IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " already copied/linked - FONT IGNORED")
                    
                elif os.path.exists(newpath) == True :
                    
                    obj.filepath=newpath
                    file.write("    FONT LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " - FONT LINKED")

                else:
                    os.makedirs(ressourcesfolder, exist_ok=True)
                    os.makedirs(folder, exist_ok=True)
                    print(bpy.path.basename(obj.filepath) + " - FONT COPYING...")
                    shutil.copy2(bpy.path.abspath(obj.filepath), folder + "/" + bpy.path.basename(obj.filepath)) 
                    ### relink fichier ###

                    obj.filepath=newpath
                    file.write("    FONT COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " - FONT COPIED")

    file.write("\n\n\n\n\nOperation ends : " + str(dt))
    file.close()

    print()
    print("Files Copied and Relinked")
    print("Check associated _Ressources folder for files and report")
    print()
    print("---Warning---")
    print("Path of the Copied Files are Absolute")


class GetThemAll(bpy.types.Operator):
    """Collect and Link in a ressource folder all External Files\nWARNING : Blender will freeze, check out the python console. All pahts are absolute."""
    bl_idname = "get.them_all"
    bl_label = "Collect All External Files"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        getthemall(context)
        return {'FINISHED'}


###################################################
# Op2 Images #
###################################################

def getimages (context):

    ### rendre tous les chemins absolus ###
    bpy.ops.file.make_paths_absolute()

    ### définir chemin et nom du fichier blend ###
    blendossier=bpy.path.abspath("//")
    Oblendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    Oblendnom=os.path.splitext(Oblendnom2)[0]

    blendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    blendnom=os.path.splitext(blendnom2)[0]


    ### définir chemin folder ressources ###
    ressourcesfolder=blendossier + "/" + "blends_ressources"

    ### définir types de datablocks à récupérer ###
    image = bpy.data.images
    
    ### créer compte rendu ###
    os.makedirs(ressourcesfolder, exist_ok=True)
    file = open(ressourcesfolder + "//" + blendnom + "_images_" + "_" + str(today) + "_report.txt", "w")
    file.write("Collect Files Operation Report\n\n\n")
    file.write("Operation starts : " + str(dt) + "\n\n")


    ### Images ###

    file.write("\nImages :\n\n")

    for obj in image:
        if obj is not None:

            ### folder à créer en fonction du type ###
            folder=ressourcesfolder + "/" + "Images"        
            newpath=folder + "/" + bpy.path.basename(obj.filepath)
            
            if obj.filepath == '' :
                
                print("WARNING " + obj.name + " is not an external file - IMAGE IGNORED")
                file.write("    IMAGE IGNORED : " + obj.name + " is not an external file\n")
                
            else :
                if obj.filepath == newpath:
                    file.write("    IMAGE IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " already copied/linked - IMAGE IGNORED")
                    
                elif os.path.exists(newpath) == True :
                    obj.filepath=newpath
                    file.write("    IMAGE LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " - IMAGE LINKED")
                                
                else:
                    os.makedirs(ressourcesfolder, exist_ok=True)
                    os.makedirs(folder, exist_ok=True)
                    print(bpy.path.basename(obj.filepath) + " - IMAGE COPYING...")
                    shutil.copy2(bpy.path.abspath(obj.filepath), folder + "/" + bpy.path.basename(obj.filepath)) 
                    ### relink fichier ###

                    obj.filepath=newpath
                    file.write("    IMAGE COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " - IMAGE COPIED")

    file.write("\n\n\n\n\nOperation ends : " + str(dt))
    file.close()

    print()
    print("Files Copied and Relinked")
    print("Check associated _Ressources folder for files and report")
    print()
    print("---Warning---")
    print("Path of the Copied Files are Absolute")


class GetImages(bpy.types.Operator):
    """Collect and Link in a ressource folder all Images\nWARNING : Blender will freeze, check out the python console. All pahts are absolute."""
    bl_idname = "get.images"
    bl_label = "Collect Images Only"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        getimages(context)
        return {'FINISHED'}


###################
# Op3 Movie Clips #
###################

def getclips (context):

    ### rendre tous les chemins absolus ###
    bpy.ops.file.make_paths_absolute()

    ### définir chemin et nom du fichier blend ###
    blendossier=bpy.path.abspath("//")
    Oblendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    Oblendnom=os.path.splitext(Oblendnom2)[0]

    blendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    blendnom=os.path.splitext(blendnom2)[0]

    ### définir chemin folder ressources ###
    ressourcesfolder=blendossier + "/" + "blends_ressources"

    ### définir types de datablocks à récupérer ###
    clip = bpy.data.movieclips
    
    ### créer compte rendu ###
    os.makedirs(ressourcesfolder, exist_ok=True)
    file = open(ressourcesfolder + "//" + blendnom + "_movieclips_" + "_" + str(today) + "_report.txt", "w")
    file.write("Collect Files Operation Report\n\n\n")
    file.write("Operation starts : " + str(dt) + "\n\n")


    ### Movie Clips ###

    file.write("\nMovie Clips :\n\n")

    for obj in clip:
        if obj is not None:

            ### folder à créer en fonction du type ###
            folder=ressourcesfolder + "/" + "Movie Clips"        
            newpath=folder + "/" + bpy.path.basename(obj.filepath)
            Snewpath=folder + "/" + os.path.splitext(bpy.path.basename(obj.filepath))[0] + "/"
            Sfpath=Snewpath + bpy.path.basename(obj.filepath)
            
            ab=bpy.path.abspath(obj.filepath)
            path = os.path.normpath(ab)
            parts = path.split(os.sep)

            parentpath = os.sep.join(parts[:-1])
            
            if obj.filepath == newpath:
                
                file.write("    MOVIE CLIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                print(bpy.path.basename(obj.filepath) + " already copied/linked - VIDEO IGNORED")
                
            elif obj.filepath == Sfpath :
                
                file.write("    IMAGE SEQUENCE IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                print(bpy.path.basename(obj.filepath) + " sequence already copied/linked - IMAGE SEQUENCE IGNORED")
                
            else:
                if obj.source == 'SEQUENCE' :
                    if os.path.exists(Snewpath) == True :
                        obj.filepath=Sfpath
                        file.write("    IMAGE SEQUENCE LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                        print(bpy.path.basename(obj.filepath) + " sequence - IMAGE SEQUENCE LINKED")

                    else :
                        os.makedirs(ressourcesfolder, exist_ok=True)
                        os.makedirs(folder, exist_ok=True)
                        print(bpy.path.basename(obj.filepath) + " sequence - IMAGE SEQUENCE COPYING...")
                        shutil.copytree(parentpath, Snewpath)
                        obj.filepath=Sfpath
                        file.write("    IMAGE SEQUENCE COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                        print(bpy.path.basename(obj.filepath) + " sequence - IMAGE SEQUENCE COPIED")

                else :
                    os.makedirs(ressourcesfolder, exist_ok=True)
                    os.makedirs(folder, exist_ok=True)
                    print(bpy.path.basename(obj.filepath) + " - VIDEO COPYING...")
                    shutil.copy2(bpy.path.abspath(obj.filepath), folder + "/" + bpy.path.basename(obj.filepath)) 
                    ### relink fichier ###

                    obj.filepath=newpath
                    file.write("    MOVIE CLIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " - VIDEO COPIED")

    file.write("\n\n\n\n\nOperation ends : " + str(dt))
    file.close()

    print()
    print("Files Copied and Relinked")
    print("Check associated _Ressources folder for files and report")
    print()
    print("---Warning---")
    print("Path of the Copied Files are Absolute")


class GetClips(bpy.types.Operator):
    """Collect and Link in a ressource folder all Movie Clips\nWARNING : Blender will freeze, check out the python. All pahts are absolute."""
    bl_idname = "get.clips"
    bl_label = "Collect Movie Clips Only"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        getclips(context)
        return {'FINISHED'}


#################
# Op4 Libraries #
#################
#
def getlibraries (context):

    ### rendre tous les chemins absolus ###
    bpy.ops.file.make_paths_absolute()

    ### définir chemin et nom du fichier blend ###
    blendossier=bpy.path.abspath("//")
    Oblendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    Oblendnom=os.path.splitext(Oblendnom2)[0]

    blendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    blendnom=os.path.splitext(blendnom2)[0]

    ### définir chemin folder ressources ###
    ressourcesfolder=blendossier + "/" + "blends_ressources"

    ### définir types de datablocks à récupérer ###
    lib = bpy.data.libraries

    ### créer compte rendu ###
    os.makedirs(ressourcesfolder, exist_ok=True)
    file = open(ressourcesfolder + "//" + blendnom + "_blendlibraries_" + "_" + str(today) + "_report.txt", "w")
    file.write("Collect Files Operation Report\n\n\n")
    file.write("Operation starts : " + str(dt) + "\n\n")


    ### Libraries ###

    file.write("\nBlend Libraries :\n\n")

    for obj in lib:
        
        if obj is not None:
            
            ### folder à créer en fonction du type ###
            folder=ressourcesfolder + "/" + "Blend Libraries"
            newpath=folder + "/" + bpy.path.basename(obj.filepath)
            
            if obj.filepath == newpath:
                file.write("    BLEND LIBRARY IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                print(bpy.path.basename(obj.filepath) + " already copied/linked - LIBRARY IGNORED")
                
            elif os.path.exists(newpath) == True : 
                obj.filepath=newpath
                file.write("    BLEND LIBRARY LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                print(bpy.path.basename(obj.filepath) + " - LIBRARY LINKED")
                
            else:
                os.makedirs(ressourcesfolder, exist_ok=True)
                os.makedirs(folder, exist_ok=True)
                print(bpy.path.basename(obj.filepath) + " - LIBRARY COPYING...")
                shutil.copy2(bpy.path.abspath(obj.filepath), folder + "/" + bpy.path.basename(obj.filepath)) 
                ### relink fichier ###

                obj.filepath=newpath
                file.write("    BLEND LIBRARY COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                print(bpy.path.basename(obj.filepath) + " - LIBRARY COPIED")
                
                
    file.write("\n\n\n\n\nOperation ends : " + str(dt))
    file.close()

    print()
    print("Files Copied and Relinked")
    print("Check associated _Ressources folder for files and report")
    print()
    print("---Warning---")
    print("Path of the Copied Files are Absolute")


class GetLibraries(bpy.types.Operator):
    """Collect and Link in a ressource folder all Blend Libraries\nWARNING : Blender will freeze, check out the python. All pahts are absolute."""
    bl_idname = "get.libraries"
    bl_label = "Collect Blend Libraries Only"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        getlibraries(context)
        return {'FINISHED'}


##################
# Op5 All Strips #
##################

def getallstrips (context):

    ### rendre tous les chemins absolus ###
    bpy.ops.file.make_paths_absolute()

    ### définir chemin et nom du fichier blend ###
    blendossier=bpy.path.abspath("//")
    Oblendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    Oblendnom=os.path.splitext(Oblendnom2)[0]

    blendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    blendnom=os.path.splitext(blendnom2)[0]

    ### définir chemin folder ressources ###
    ressourcesfolder=blendossier + "/" + "blends_ressources"

    ### créer compte rendu ###
    os.makedirs(ressourcesfolder, exist_ok=True)
    file = open(ressourcesfolder + "//" + blendnom + "_strips_" + "_" + str(today) + "_report.txt", "w")
    file.write("Collect Files Operation Report\n\n\n")
    file.write("Operation starts : " + str(dt) + "\n\n")

    ### Strips ###

    file.write("\nSequencer Strips :\n\n")

    for scene in bpy.data.scenes: 
        if scene.sequence_editor is not None:
            strip = scene.sequence_editor.sequences_all
            
            if strip is not None:
                for obj in strip:
                    if obj.type == 'MOVIE' :
                        folder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)
                        sfolder = folder + "/" +  "Video Strips"
                        newpath=sfolder + "/" + bpy.path.basename(obj.filepath)
                        
                        if os.path.exists(newpath) == True :
                            
                            if obj.filepath == newpath:
                                file.write("    VIDEO STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                                print(bpy.path.basename(obj.filepath) + " already copied/linked - VIDEO STRIP IGNORED")

                            else :
                                obj.filepath=newpath
                                file.write("    VIDEO STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                print(bpy.path.basename(obj.filepath) + " - VIDEO STRIP LINKED")

                        else:
                            os.makedirs(ressourcesfolder, exist_ok=True)
                            os.makedirs(sfolder, exist_ok=True)
                            print(bpy.path.basename(obj.filepath) + " - VIDEO STRIP COPYING...")
                            shutil.copy2(bpy.path.abspath(obj.filepath), newpath) 
                            obj.filepath=newpath
                            file.write("    VIDEO STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                            print(bpy.path.basename(obj.filepath) + " - VIDEO STRIP COPIED")

                    ### Problème avec image fixe à régler ###    
                    elif obj.type == 'IMAGE':

                        folder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)
                        sfolder = folder + "/" + "Images Strips" + "/"
                        ISfolder = folder + "/" + "Image Sequence Strips"
                        Inewpath=sfolder + obj.elements[0].filename
                        ISnewpath=ISfolder + "/" + os.path.splitext(obj.elements[0].filename)[0] + "/"
                        
                        if obj.frame_duration == 1 :

                            if obj.directory == sfolder :
                                
                                file.write("    IMAGE STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                                print(obj.elements[0].filename + " already copied/linked - IMAGE STRIP IGNORED")

                            else:
                                if os.path.exists(Inewpath) == True :
                                
                                    obj.directory=sfolder
                                    file.write("    IMAGE STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " - IMAGE STRIP LINKED")

                                else :
                                    os.makedirs(ressourcesfolder, exist_ok=True)
                                    os.makedirs(sfolder, exist_ok=True)
                                    print(obj.elements[0].filename + " - IMAGE STRIP COPYING...")
                                    shutil.copy2(bpy.path.abspath(obj.directory) + "/" + obj.name, Inewpath)
                                    obj.directory=sfolder
                                    file.write("    IMAGE STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " - IMAGE STRIP COPIED")

                        else :
                            if obj.directory == ISnewpath :
                                
                                file.write("    IMAGE SEQUENCE STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                                print(obj.elements[0].filename + " sequence already copied/linked - IMAGE SEQUENCE STRIP IGNORED")

                            else:
                                if os.path.exists(ISnewpath) == True :
                                
                                    obj.directory=ISnewpath
                                    file.write("    IMAGE SEQUENCE STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " sequence - IMAGE SEQUENCE STRIP LINKED")

                                else :
                                    os.makedirs(ressourcesfolder, exist_ok=True)
                                    os.makedirs(ISfolder, exist_ok=True)
                                    print(obj.elements[0].filename + " sequence - IMAGE SEQUENCE STRIP COPYING")
                                    shutil.copytree(bpy.path.abspath(obj.directory), ISnewpath)
                                    obj.directory=ISnewpath
                                    file.write("    IMAGE SEQUENCE STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " sequence - IMAGE SEQUENCE STRIP COPIED")

                    elif obj.type == 'SOUND':
                        vfolder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)
                        vsfolder = vfolder + "/" +  "Video Strips"
                        vnewpath=vsfolder + "/" + bpy.path.basename(obj.sound.filepath)
                        
                        folder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)    
                        sfolder = folder + "/" +  "Sounds Strips"
                        newpath=sfolder + "/" + bpy.path.basename(obj.sound.filepath)
                        
                        if os.path.isfile(vnewpath) == True :
                            if obj.sound.filepath==vnewpath :
                                file.write("    SOUND STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.sound.filepath) + "\n")
                                print(bpy.path.basename(obj.sound.filepath) + " already copied/linked - SOUND IGNORED")

                            else :
                                obj.sound.filepath=vnewpath
                                file.write("    SOUND STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.sound.filepath) + "\n")
                                print(bpy.path.basename(obj.sound.filepath) + " - SOUND LINKED")

                        else :
                            if os.path.isfile(newpath) == True :
                                
                                if obj.sound.filepath==newpath :
                                    file.write("    SOUND STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.sound.filepath) + "\n")
                                    print(bpy.path.basename(obj.sound.filepath) + " already copied/linked - SOUND IGNORED")

                                else:
                                    obj.sound.filepath=newpath
                                    file.write("    SOUND STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.sound.filepath) + "\n")
                                    print(bpy.path.basename(obj.sound.filepath) + " - SOUND LINKED")

                            else:
                                os.makedirs(ressourcesfolder, exist_ok=True)
                                os.makedirs(sfolder, exist_ok=True)   
                                print(bpy.path.basename(obj.sound.filepath) + " - SOUND COPYING...")                 
                                shutil.copy2(bpy.path.abspath(obj.sound.filepath), newpath) 
                                obj.sound.filepath=newpath
                                file.write("    SOUND STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.sound.filepath) + "\n")
                                print(bpy.path.basename(obj.sound.filepath) + " - SOUND COPIED")    

    file.write("\n\n\n\n\nOperation ends : " + str(dt))
    file.close()

    print()
    print("Files Copied and Relinked")
    print("Check associated _Ressources folder for files and report")
    print()
    print("---Warning---")
    print("Path of the Copied Files are Absolute")


class GetAllStrips(bpy.types.Operator):
    """Collect and Link in a ressource folder all Sequencer Strips\nWARNING : Blender will freeze, check out the python console. All pahts are absolute."""
    bl_idname = "get.all_strips"
    bl_label = "Collect Video Sequencer Strips Only"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        getallstrips(context)
        return {'FINISHED'}


############################
# Op6 Current Scene Strips #
############################

def getcurrentscenestrips (context):

    ### rendre tous les chemins absolus ###
    bpy.ops.file.make_paths_absolute()

    ### définir chemin et nom du fichier blend ###
    blendossier=bpy.path.abspath("//")
    Oblendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    Oblendnom=os.path.splitext(Oblendnom2)[0]

    blendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    blendnom=os.path.splitext(blendnom2)[0]

    ### définir chemin folder ressources ###
    ressourcesfolder=blendossier + "/" + "blends_ressources"
    
    scene = bpy.context.scene
    scname = scene.name
    strip = bpy.data.scenes[scname].sequence_editor.sequences_all

    ### créer compte rendu ###
    os.makedirs(ressourcesfolder, exist_ok=True)
    file = open(ressourcesfolder + "//" + blendnom + "_" + scname + "_strips_" + "_" + str(today) + "_report.txt", "w")
    file.write("Collect Files Operation Report\n\n\n")
    file.write("Operation starts : " + str(dt) + "\n\n")

    ### Strips ###

    file.write("\nSequencer Strips :\n\n")

    for obj in strip: 
        
        if scene.sequence_editor is not None:
            
            if strip is not None:

                for obj in strip:
                    
                    if obj.type == 'MOVIE' :
                        
                        folder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)
                        sfolder = folder + "/" +  "Video Strips"
                        newpath=sfolder + "/" + bpy.path.basename(obj.filepath)
                        
                        if os.path.exists(newpath) == True :
                            
                            if obj.filepath == newpath:
                                file.write("    VIDEO STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                                print(bpy.path.basename(obj.filepath) + " already copied/linked - VIDEO STRIP IGNORED")

                            else :
                                
                                obj.filepath=newpath
                                file.write("    VIDEO STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                print(bpy.path.basename(obj.filepath) + " - VIDEO STRIP LINKED")

                        else:
                            os.makedirs(ressourcesfolder, exist_ok=True)
                            os.makedirs(sfolder, exist_ok=True)
                            print(bpy.path.basename(obj.filepath) + " - VIDEO STRIP COPYING...")
                            shutil.copy2(bpy.path.abspath(obj.filepath), newpath) 
                            obj.filepath=newpath
                            file.write("    VIDEO STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                            print(bpy.path.basename(obj.filepath) + " - VIDEO STRIP COPIED")

                    ### Problème avec image fixe à régler ###    
                    elif obj.type == 'IMAGE':
                        folder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)
                        sfolder = folder + "/" + "Images Strips" + "/"
                        ISfolder = folder + "/" + "Image Sequence Strips"
                        Inewpath=sfolder + obj.elements[0].filename
                        ISnewpath=ISfolder + "/" + os.path.splitext(obj.elements[0].filename)[0] + "/"
                        
                        if obj.frame_duration == 1 :

                            if obj.directory == sfolder :

                                file.write("    IMAGE STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                                print(obj.elements[0].filename + " already copied/linked - IMAGE STRIP IGNORED")

                            else:
                                if os.path.exists(Inewpath) == True :
                                
                                    obj.directory=sfolder
                                    file.write("    IMAGE STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " - IMAGE STRIP LINKED")

                                else :
                                    os.makedirs(ressourcesfolder, exist_ok=True)
                                    os.makedirs(sfolder, exist_ok=True)
                                    print(obj.elements[0].filename + " - IMAGE STRIP COPYING...")
                                    shutil.copy2(bpy.path.abspath(obj.directory) + "/" + obj.name, Inewpath)
                                    obj.directory=sfolder
                                    file.write("    IMAGE STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " - IMAGE STRIP COPIED")

                        else :
                            if obj.directory == ISnewpath :
                                
                                file.write("    IMAGE SEQUENCE STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                                print(obj.elements[0].filename + " sequence already copied/linked - IMAGE SEQUENCE STRIP IGNORED")
                            
                            else:
                                if os.path.exists(ISnewpath) == True :
                                
                                    obj.directory=ISnewpath
                                    file.write("    IMAGE SEQUENCE STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " sequence - IMAGE SEQUENCE STRIP LINKED")
                                
                                else :
                        
                                    os.makedirs(ressourcesfolder, exist_ok=True)
                                    os.makedirs(ISfolder, exist_ok=True)
                                    print(obj.elements[0].filename + " sequence - IMAGE SEQUENCE STRIP COPYING")
                                    shutil.copytree(bpy.path.abspath(obj.directory), ISnewpath)
                                    obj.directory=ISnewpath
                                    file.write("    IMAGE SEQUENCE STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                                    print(obj.elements[0].filename + " sequence - IMAGE SEQUENCE STRIP COPIED")

                    elif obj.type == 'SOUND':
                        vfolder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)
                        vsfolder = vfolder + "/" +  "Video Strips"
                        vnewpath=vsfolder + "/" + bpy.path.basename(obj.sound.filepath)
                        
                        folder=ressourcesfolder + "/" + "Video Sequencer" + "/" + str(scene.name)    
                        sfolder = folder + "/" +  "Sounds Strips"
                        newpath=sfolder + "/" + bpy.path.basename(obj.sound.filepath)

                        if os.path.isfile(vnewpath) == True :

                            if obj.sound.filepath==vnewpath :
                                file.write("    SOUND STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.sound.filepath) + "\n")
                                print(bpy.path.basename(obj.sound.filepath) + " already copied/linked - SOUND IGNORED")

                            else :
                                obj.sound.filepath=vnewpath
                                file.write("    SOUND STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.sound.filepath) + "\n")
                                print(bpy.path.basename(obj.sound.filepath) + " - SOUND LINKED")

                        else :
                            if os.path.isfile(newpath) == True :
                                
                                if obj.sound.filepath==newpath :
                                    file.write("    SOUND STRIP IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.sound.filepath) + "\n")
                                    print(bpy.path.basename(obj.sound.filepath) + " already copied/linked - SOUND IGNORED")

                                else:
                                    obj.sound.filepath=newpath
                                    file.write("    SOUND STRIP LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.sound.filepath) + "\n")
                                    print(bpy.path.basename(obj.sound.filepath) + " - SOUND LINKED")

                            else:
                                os.makedirs(ressourcesfolder, exist_ok=True)
                                os.makedirs(sfolder, exist_ok=True)   
                                print(bpy.path.basename(obj.sound.filepath) + " - SOUND COPYING...")                 
                                shutil.copy2(bpy.path.abspath(obj.sound.filepath), newpath) 
                                obj.sound.filepath=newpath
                                file.write("    SOUND STRIP COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.sound.filepath) + "\n")
                                print(bpy.path.basename(obj.sound.filepath) + " - SOUND COPIED")    
                        

    file.write("\n\n\n\n\nOperation ends : " + str(dt))
    file.close()

    print()
    print("Files Copied and Relinked")
    print("Check associated _Ressources folder for files and report")
    print()
    print("---Warning---")
    print("Path of the Copied Files are Absolute")


class GetCurrentSceneStrips(bpy.types.Operator):
    """Collect and Link in a ressource folder all Sequencer Strips from the Current Scene\nWARNING : Blender will freeze, check out the python console. All pahts are absolute."""
    bl_idname = "get.current_scene_strips"
    bl_label = "Collect Video Sequencer Strips from Current Scene Only"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        getcurrentscenestrips(context)
        return {'FINISHED'}


#############
# Op7 Fonts #
#############

def getfonts (context):

    ### rendre tous les chemins absolus ###
    bpy.ops.file.make_paths_absolute()

    ### définir chemin et nom du fichier blend ###
    blendossier=bpy.path.abspath("//")
    Oblendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    Oblendnom=os.path.splitext(Oblendnom2)[0]

    blendnom2=bpy.path.abspath(bpy.path.basename(bpy.context.blend_data.filepath))
    blendnom=os.path.splitext(blendnom2)[0]


    ### définir chemin folder ressources ###
    ressourcesfolder=blendossier + "/" + "blends_ressources"

    ### définir types de datablocks à récupérer ###
    font = bpy.data.fonts
    
    ### créer compte rendu ###
    os.makedirs(ressourcesfolder, exist_ok=True)
    file = open(ressourcesfolder + "//" + blendnom + "_fonts_" + "_" + str(today) + "_report.txt", "w")
    file.write("Collect Files Operation Report\n\n\n")
    file.write("Operation starts : " + str(dt) + "\n\n")


    ### Fonts ###

    file.write("\nFonts :\n\n")

    for obj in font:

        if obj is not None:

            ### folder à créer en fonction du type ###
            folder=ressourcesfolder + "/" + "Fonts"        
            newpath=folder + "/" + bpy.path.basename(obj.filepath)
            
            if obj.filepath == '' :

                print("WARNING " + obj.name + " is not an external file - FONT IGNORED")
                file.write("    FONT IGNORED : " + obj.name + " is not an external file\n")
                
            elif obj.filepath == '<builtin>' :
                
                print("WARNING " + obj.name + " is not an external file - FONT IGNORED")
                file.write("    FONT IGNORED : " + obj.name + " is not an external file\n")

            else :            
                if obj.filepath == newpath:
                    file.write("    FONT IGNORED : " + obj.name + " already copied and linked to "+ bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " already copied/linked - FONT IGNORED")

                elif os.path.exists(newpath) == True :
                    obj.filepath=newpath
                    file.write("    FONT LINKED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " - FONT LINKED")

                else:
                    os.makedirs(ressourcesfolder, exist_ok=True)
                    os.makedirs(folder, exist_ok=True)
                    print(bpy.path.basename(obj.filepath) + " - FONT COPYING...")
                    shutil.copy2(bpy.path.abspath(obj.filepath), folder + "/" + bpy.path.basename(obj.filepath)) 
                    ### relink fichier ###

                    obj.filepath=newpath
                    file.write("    FONT COPIED : " + obj.name + " linked to " + bpy.path.basename(obj.filepath) + "\n")
                    print(bpy.path.basename(obj.filepath) + " - FONT COPIED")

    file.write("\n\n\n\n\nOperation ends : " + str(dt))
    file.close()

    print()
    print("Files Copied and Relinked")
    print("Check associated _Ressources folder for files and report")
    print()
    print("---Warning---")
    print("Path of the Copied Files are Absolute")


class GetFonts(bpy.types.Operator):
    """Collect and Link in a ressource folder all Fonts\nWARNING : Blender will freeze, check out the python console. All pahts are absolute."""
    bl_idname = "get.fonts"
    bl_label = "Collect Fonts Only"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        getfonts(context)
        return {'FINISHED'}


########
# Menu #
########

class CollectExternalFiles(bpy.types.Menu):
    bl_label = "Collect External Files"

    def draw(self, context):
        layout = self.layout

        layout.operator("get.them_all" , text = "All External Files" , icon='FILE_TICK')
        layout.operator("get.images" , text = "Images Only" , icon='IMAGE_DATA')
        layout.operator("get.clips" , text = "Movie Clips Only" , icon='FILE_MOVIE')
        layout.operator("get.libraries" , text = "Blend Libraries Only" , icon='FILE_BLEND')
        layout.operator("get.all_strips" , text = "Sequencer Strips Only" , icon='SEQUENCE')
        layout.operator("get.current_scene_strips" , text = "Sequencer Strips from Current Scene Only" , icon='SEQ_SEQUENCER')
        layout.operator("get.fonts" , text = "Fonts Only" , icon='FILE_FONT')
        
        
def menu_draw(self, context):
    layout = self.layout
    layout.separator()
    layout.menu("CollectExternalFiles" , icon='GHOST_ENABLED')

classes = (
    GetThemAll,
    GetImages,
    GetClips,
    GetLibraries,
    GetAllStrips,
    GetCurrentSceneStrips,
    GetFonts,
    CollectExternalFiles,
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_external_data.append(menu_draw)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_external_data.remove(menu_draw)

if __name__ == "__main__":
    register()
